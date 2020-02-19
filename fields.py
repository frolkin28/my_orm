class Field:
	def __get__(self, obj, object):
		return obj.__dict__['_' + self._name]

	def __set__(self, obj, value):
		obj.__dict__['_' + self._name] = value


class IntField(Field):

	def __init__(self, primary_key=False, unique=False, default=None):
		self.params = 'integer '
		if primary_key:
			self.params += 'primary key'
		if unique:
			self.params += 'unique'
		if default:
			self.params += 'default {}'.format(default)

	def __set__(self, obj, value):
		if isinstance(value, int):
			super().__set__(obj, value)
		else:
			raise ValueError


class VarcharField(Field):

	def __init__(self, num_char=None):
		if not num_char:
			raise ValueError('Number of characters arent defined')
		self.params = 'varchar({})'.format(num_char)

	def __set__(self, obj, value):
		if isinstance(value, str) and len(value) < 255:
			super().__set__(obj, value)
		else:
			raise ValueError


class FloatField(Field):

	def __init__(self,  unique=False, default=None):
		self.params = 'float'
		if unique:
			self.params += 'unique'
		if default:
			self.params += 'default {}'.format(default)

	def __set__(self, obj, value):
		if isinstance(value, float):
			super().__set__(obj, value)
		else:
			raise ValueError


class TextField(Field):

	def __init__(self):
		self.params = 'text'

	def __set__(self, obj, value):
		if isinstance(value, str):
			super().__set__(obj, value)
		else:
			raise ValueError

class BooleanField(Field):
	def __init__(self):
		self.params = 'boolean'

	def __set__(self, obj, value):
		if isinstance(value, float):
			super().__set__(obj, value)
		else:
			raise ValueError
