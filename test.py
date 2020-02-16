from model import Model
from fields import IntField, CharField, FloatField

class MyModel(Model):
	__tablename__ = 'test'
	a = IntField()
	b = CharField()
	c = FloatField()


if __name__ == '__main__':
	for i in MyModel.all():
		print(i.b)
