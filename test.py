from model import Model
from fields import IntField, VarcharField, FloatField


class MyModel(Model):
	__tablename__ = 'test'
	a = IntField(unique=True)
	b = VarcharField(num_char=255)
	c = FloatField()


if __name__ == '__main__':
	# create table
	MyModel.create_table()
	# isnert
	m1 = MyModel(a=1000, b='Test', c=3.14)
	m2 = MyModel(a=12, b='c', c=3.14)
	m3 = MyModel(a=5, b='c', c=3.14)
	m1.insert()
	m2.insert()
	m3.insert()
	# select all
	for i in MyModel.all():
		print(i.pk)
	# update
	m = MyModel.get(1)
	m.b = 'test'
	m.save()
	# delete
	m = MyModel.get(3)
	MyModel.delete(m)
