jk_simpleobjpersistency
========

Introduction
------------

This python module provides a simple persistency for data objects.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-simpleobjpersistency)
* [pypi.python.org](https://pypi.python.org/pypi/jk_simpleobjpersistency)

How to use this module
----------------------

### Import package

To import the package `jk_simpleobjpersistency` use the following code:

```python
import jk_simpleobjpersistency
```

### Implement a class usable for persistency

If you want to persist an object you have to consider a few minor aspects for your implementation:

* Your constructor must be parameterless.
* You require to implement a regular object method deserializing *from* a dictionary: `deserialize(self, dataObj:dict)`
* You require to implement a regular object method serializing *to* a dictionary: `serialize(self) -> dict`
* You must not use any of these member identifiers: `setChanged`, `store`, `storeIfChanged`, `isModified`, `destroy`, `isNew`, `isPersistent` as well as `_x_isModified`. `_x_persisteer`, `_x_identifier`, `_x_isAutoStore`.

That's it.

A quite minimum implementation of a serializing class might then look like this:

```python
class MyUserObj(object):

	def __init__(self):
		self.userName = None
		self.password = None
		self.eMail = None
		self.yearOfBirth = None

	def deserialize(self, jData:dict):
		self.userName = jData.get("userName")
		self.password = jData.get("password")
		self.eMail = jData.get("eMail")
		self.yearOfBirth = jData.get("yearOfBirth")

	def serialize(self):
		return {
			"userName": self.userName,
			"password": self.password,
			"eMail": self.eMail,
			"yearOfBirth": self.yearOfBirth,
		}
```

This is just an example but it demonstrates the basic concept. Here: The object variables will hold the object's data, and the methods `deserialize()` and `serialize()` will be used by the framework to implement persistency.

For persistency to work the class and the objects will be patched by the persistency framework. Additional methods are added: `setChanged`, `store`, `storeIfChanged`, `isModified`, `destroy`, `isNew`, `isPersistent` as well as `_x_isModified`. `_x_persisteer`, `_x_identifier`, `_x_isAutoStore`. This is the reason why you must not use the specific identifiers listed above. (If you do they will get overridden by the framework and your implementation will likely break.)

### Instantiate and initialize the persistency layer

In order to work with this persistency layer you need a) to instantiate a persistency data manager first and b) register all classes that should be persistent before then c) working with instances of these classes.

The most recommended way for isntantiation is something like this:

```python
pm = jk_simpleobjpersistency.PersistencyManager("/my/data/dir/path")
```

The path argument is the root directory where data is stored (if not specified otherwise during registration of a class).

After that you must register all classes that the persistency layer should deal with. This is done invoking `registerClass()` for each class persistency should be active for.

A class registration requires the following arguments:

| Argument name	| Argument typ										| Required or optional	| Description				|
|---------------|---------------------------------------------------|-----------------------|---------------------------|
| `clazz`		| A class type										| required				| The class itself			|
| `defaults`	| `dict` or an instance of the serialization type	| optional				| Either the serialized data or an prototypical instance of the class type (that get serialized by invoking `serialize()`	|
| `dirPath`		| `str`												| optional				| The directory to store the data. (By default the class name is used.)	|
| `autoStore`	| `bool`											| optional				| If `true` modified objects get stored automatically on delete if they have been changed. (Default: `false`)	|

Example:

```python
ppdm = jk_simpleobjpersistency.PersistencyManager("testdata")
ppdm.registerClass(
	clazz=MyUserObj,
	defaults={
		"eMail": "example@example.com"
	},
	dirPath="testdata/users",
	autoStore=True)
```

As you can see in this example we use a dictionary for the defaults. The content of the dictionary must match expectations of the class implementation.

### Creating instances

An instance of an object can be created like this:

```python
obj = pp.createObject(MyUserObj, "myUser")
```

That's it. `obj` now contains a fresh instance of `MyUserObj`.

But let's have a look at the arguments:

| Argument name	| Argument typ										| Required or optional	| Description				|
|---------------|---------------------------------------------------|-----------------------|---------------------------|
| `clazz`		| A class type										| required				| The class itself			|
| `identifier`	| `str`												| optional				| If specified an instance is created that furtheron will be uniquely identified by this string. If no identifier is specified, a new one is generated.	|

Please note that the object will not have been stored yet. If you throw it away without storing - and `autoStore` is not `True` - then data you might have put into the object will be lost.

### Modifying instances

You have two options:

* Either using the modified-flag that is provided by every instance or
* store every modified object explicitely.

Example:

```python
obj = pp.createObject(MyUserObj, "myUser")
obj.userName = "something"
obj.password = "somepwd123"
obj.store()
```

Or:

```python
obj = pp.createObject(MyUserObj, "myUser")
obj.userName = "something"
obj.password = "somepwd123"
obj.setModified()
```

And later on invoke ```obj.storeIfModified()```. (This storing is performed automatically if `autoStore` is set to `True` during registration of a class.

**CAUTION!** Be aware that at the end of your program all objects should be stored already. Python defines no order in how objects get disposed: It might well be that
build in functions like `open()` used for writing a file might be disposed already at the time a modified object tries to store itself. It's remains your reponsibility
as programmer to take care that all objects have been properly saved when your program terminates. (Compare: https://stackoverflow.com/questions/23422188/why-am-i-getting-nameerror-global-name-open-is-not-defined-in-del) Have a look at `storeAllModified(clazz)` which might
help you in this case.

### Destroying an instance

Instances can be destroyed by invoking `destroy()` on the persistent object itself. Please be aware that this action is **immediate**: If data is persistently stored on disk this
data is removed instantly.

Example:

```python
obj = pp.getObject(MyUserObj, "myUser")
obj.destroy()
```

### A note about caching

All objects created or retrieved from backgroud storage are cached. That means that these objects **consume memory**. If this is a problem you can invoke any of these methods at any time:

| Method					| Description								|
|---------------------------|-------------------------------------------|
| `clearEntireCache()`		| That will remove all cached intances.		|
| `clearClassCache(clazz)`	| Clear the cache for a specific class.		|

Contact Information
-------------------

This is Open Source code. That not only gives you the possibility of freely using this code it also
allows you to contribute. Feel free to contact the author(s) of this software listed below, either
for comments, collaboration requests, suggestions for improvement or reporting bugs:

* Jürgen Knauth: pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



