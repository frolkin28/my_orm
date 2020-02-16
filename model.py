import sqlite3
from fields import IntField, CharField, FloatField, Field, TextField, PrimaryKey


class Query:
	def __init__(self, tablename):
		self.conn = sqlite3.connect('database.db')
		self.cur = self.conn.cursor()
		self.tablename = tablename


class Meta(type):
	def __new__(cls, name, parents, props):
		my_types = {}
		for field_name, field in props.items():
			if type(field) in [IntField, CharField, FloatField, PrimaryKey]:
				field._name = field_name  # for each Field object add _name

				if isinstance(field, IntField):
					my_types['_' + field_name] = 'integer'
				elif isinstance(field, FloatField):
					my_types['_' + field_name] = 'float'
				elif isinstance(field, CharField):
					my_types['_' + field_name] = 'varchar(255)'
				elif isinstance(field, TextField):
					my_types['_' + field_name] = 'text'

		my_types['_pk'] = 'integer primary key'
		props['types'] = my_types

		if '__tablename__' in props.keys():
			props['query'] = Query(props['__tablename__'])

		return type.__new__(cls, name, parents, props)


class Model(metaclass=Meta):

	def __init__(self, *args, **kwargs):
		for key, value in kwargs.items():
			self.__dict__['_' + key] = value

	@classmethod
	def create_table(cls):
		str_types = ', '.join(['{} {}'.format(i[1:], j) for i, j in cls.types.items()])
		query = 'create table if not exists {} ({})'.format(cls.query.tablename, str_types)
		cls.query.cur.execute(query)
		cls.query.conn.commit()

	def insert(self):
		tablename = self.__class__.__tablename__
		fields = ', '.join(key[1:] for key in self.__dict__.keys() if key.startswith('_'))
		query = f'insert into {tablename}({fields})'
		self.__class__.query.cur.execute(query + ' values (?, ?, ?)',
							  tuple(value for key, value in self.__dict__.items() if key.startswith('_')))
		self.__class__.query.conn.commit()

	def save(self):
		tablename = self.__class__.query.tablename
		query_fields = list((key[1:], value) for key, value in self.__dict__.items() if key.startswith('_') and key != '_pk')
		str_fields = []
		for key, value in query_fields:
			if isinstance(value, str):
				str_fields.append("{}='{}'".format(key, value))
			else:
				str_fields.append("{}={}".format(key, value))
		str_query = ', '.join(str_fields)
		self.query.cur.execute('update {} set {} where pk={}'.format(tablename, str_query, self._pk))
		self.query.conn.commit()

	@classmethod
	def get(cls, pk):
		fields = tuple(key[1:] for key in cls.types.keys())
		str_fields = ','.join(fields)
		cls.query.cur.execute('select {} from {} where pk={}'.format(str_fields, cls.__tablename__, pk))
		cls.query.conn.commit()
		result = dict(zip(fields, cls.query.cur.fetchone()))
		obj = cls(**result)
		return obj

	@classmethod
	def all(cls):
		fields = tuple(key[1:] for key in cls.types.keys())
		str_fields = ','.join(fields)
		cls.query.cur.execute('select {} from {}'.format(str_fields, cls.__tablename__))
		cls.query.conn.commit()
		result = []
		for entry in cls.query.cur.fetchall():
			obj_dict = dict(zip(fields, entry))
			obj = cls(**obj_dict)
			result.append(obj)
		return result

	@classmethod
	def drop_table(cls):
		cls.query.cur.execute('drop table if exists {}'.format(cls.__tablename__))
		cls.query.conn.commit()
		cls.query.conn.close()
