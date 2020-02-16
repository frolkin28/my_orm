import sys
import sqlite3
from fields import IntField, CharField, FloatField, Field, TextField


class Meta(type):
	def __new__(cls, name, parents, props):
		my_types = {}
		for field_name, field in props.items():
			if type(field) in [IntField, CharField, FloatField]:
				field._name = field_name # for each Field object add _name

				if isinstance(field, IntField):
					my_types['_'+field_name] = 'integer'
				elif isinstance(field, FloatField):
					my_types['_'+field_name] = 'float'
				elif isinstance(field, CharField):
					my_types['_'+field_name] = 'varchar(255)'
				elif isinstance(field, TextField):
					my_types['_'+field_name] = 'text'
		props['types'] = my_types
		return type.__new__(cls, name, parents, props)


class Model(metaclass=Meta):
	def __init__(self, *args, **kwargs):
		self.__dict__['types'] = {}
		for key, value in kwargs.items():
			self.__dict__['_'+key] = value
		self.conn = sqlite3.connect('database.db')
		self.cur = self.conn.cursor()

	def create_table(self):
		str_types = ', '.join(['{} {}'.format(i[1:], j) for i, j in self.__class__.types.items()])
		query = 'create table if not exists {} ({})'.format(self.__class__.__tablename__, str_types)
		self.cur.execute(query)
		self.conn.commit()

	def insert(self):
		tablename = self.__class__.__tablename__
		self.cur.execute(f'insert into {tablename} values (?, ?, ?)', tuple(value for key, value in m.__dict__.items() if key.startswith('_')))
		self.conn.commit()

	def save(self):
		self.cur.execute('')

	def get(self, **kwargs):
		self.cur.execute('select * from {}'.format(self.__class__.__tablename__))
		self.conn.commit()
		return self.cur.fetchall()

	def drop_table(self):
		self.cur.execute('drop table if exists {}'.format(self.__class__.__tablename__))
		self.conn.commit()
		self.conn.close()


class MyModel(Model):
	__tablename__ = 'test'
	a = IntField()
	b = CharField()
	c = FloatField()


if __name__ == '__main__':
	m = MyModel(a=1, b='aaa', c=3.14)
	m.a = 10
	print(m.get())
