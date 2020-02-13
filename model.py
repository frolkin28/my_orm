class Meta(type):
	def __new__(cls, name, parents, props):
		print(props)
		return type.__new__(cls, name, parents, props)


class Model(metaclass=Meta):
	pass


class Field:
	def __get__(self, obj, object):
		pass

	def __set__(self, obj, value):
		pass