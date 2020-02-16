class Field:
	def __get__(self, obj, object):
		return obj.__dict__['_' + self._name]

	def __set__(self, obj, value):
		obj.__dict__['_' + self._name] = value


class IntField(Field):
	type = 'integer'

	def __set__(self, obj, value):
		if isinstance(value, int):
			super().__set__(obj, value)
		else:
			raise ValueError


class CharField(Field):
	type = 'varchar'

	def __set__(self, obj, value):
		if isinstance(value, str) and len(value) < 255:
			super().__set__(obj, value)
		else:
			raise ValueError


class FloatField(Field):
	type = 'float'

	def __set__(self, obj, value):
		if isinstance(value, float):
			super().__set__(obj, value)
		else:
			raise ValueError


class TextField(Field):
	type = 'Text'

	def __set__(self, obj, value):
		if isinstance(value, str):
			super().__set__(obj, value)
		else:
			raise ValueError


class PrimaryKey(Field):
	def __set__(self, obj, value):
		raise ValueError
