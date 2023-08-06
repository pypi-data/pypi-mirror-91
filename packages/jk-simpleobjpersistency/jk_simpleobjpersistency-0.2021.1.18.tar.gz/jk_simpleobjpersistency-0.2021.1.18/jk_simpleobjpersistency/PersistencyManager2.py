

import os
import copy
import json
import typing

import jk_json
import jk_utils
import jk_typing

from ._ClassRecord import _ClassRecord







def _store(self):
	if self._x_persisteer is None:
		raise Exception("Object is destroyed!")
	self._x_persisteer.storeObject(self)
	self._x_isModified = False
#

def _storeIfModified(self):
	if self._x_persisteer is None:
		raise Exception("Object is destroyed!")
	if self._x_isModified:
		self._x_persisteer.storeObject(self)
		self._x_isModified = False
#

def _setModified(self):
	self._x_isModified = True
#

def _isNew(self):
	if self._x_persisteer is None:
		return False
	return not self._x_persisteer._objectExistsPersistently(self.__class__, self._x_identifier)
#

def _isPersistent(self):
	if self._x_persisteer is None:
		return False
	return self._x_persisteer._objectExistsPersistently(self.__class__, self._x_identifier)
#

def _isModified(self):
	if self._x_persisteer is None:
		return False
	return self._x_isModified
#

def _destroy(self):
	if self._x_persisteer is not None:
		self._x_persisteer.destroyObject(self)
		self._x_isModified = False
		self._x_persisteer = None
#

def _del(self):
	if self._x_isAutoStore and self._x_isModified and (self._x_persisteer is not None):
		self._x_persisteer.storeObject(self)
#






class PersistencyManager2(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	@jk_typing.checkFunctionSignature()
	def __init__(self, baseDirPath:str):
		if baseDirPath is not None:
			assert isinstance(baseDirPath, str)
			baseDirPath = os.path.abspath(baseDirPath)
			if not os.path.isdir(baseDirPath):
				os.makedirs(baseDirPath)

		self.__baseDirPath = os.path.abspath(baseDirPath)
		self.__classRecords = {}
		self.__objCache = {}
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	def __allIdentifiers2(self, clazzName:str):
		cr = self.__classRecords[clazzName]
		for fileEntryName in os.listdir(cr.dirPath):
			if fileEntryName.endswith(".json"):
				yield fileEntryName[:-5]
	#

	def _objectExistsPersistently(self, clazz:type, identifier):
		cr = self.__classRecords[clazz.__name__]
		filePath = os.path.join(cr.dirPath, identifier + ".json")
		return os.path.exists(filePath)
	#

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def registerClass(self, clazz:type, defaults = None, dirPath:str = None, autoStore:bool = False, ctx = None):
		assert clazz is not None

		assert isinstance(clazz, type)
		if defaults is None:
			defaults = {}
		else:
			if not isinstance(defaults, dict):
				defaults = defaults.serialize(ctx)
		if dirPath:
			assert isinstance(dirPath, str)

		if not dirPath:
			if not self.__baseDirPath:
				raise Exception("No base dir path and no explicit dir path specified!")
			dirPath = os.path.join(self.__baseDirPath, clazz.__name__)
		else:
			if not os.path.isabs(dirPath):
				dirPath = os.path.join(self.__baseDirPath, dirPath)

		if not os.path.isdir(dirPath):
			os.makedirs(dirPath)

		cr = _ClassRecord(clazz, dirPath, defaults, ctx)
		self.__classRecords[clazz.__name__] = cr

		clazz.isNew = _isNew
		clazz.isPersistent = _isPersistent
		clazz.setModified = _setModified
		clazz.store = _store
		clazz.storeIfModified = _storeIfModified
		clazz.isModified = _isModified
		clazz.destroy = _destroy
		clazz._x_isAutoStore = autoStore
		clazz.__del__ = _del

		self.__objCache[clazz.__name__] = {}
	#

	#
	# Get a list of all objects of the specified class.
	#
	# @return		list		Returns a list of instances.
	#
	def getAllObjectsAsList(self, clazz:type) -> list:
		assert clazz is not None

		return [
			self.getObject(clazz, identifier) for identifier in self.allIdentifiers(clazz)
		]
	#

	#
	# Get a list of all objects of the specified class.
	#
	# @return		dict		Returns a dictionary mapping identifiers to instances.
	#
	def getAllObjectsAsMap(self, clazz:type) -> dict:
		assert clazz is not None

		return {
			identifier: self.getObject(clazz, identifier) for identifier in self.allIdentifiers(clazz)
		}
	#

	def countObjects(self, clazz:type = None):
		if clazz is None:
			n = 0
			for clazz in self.__classRecords:
				n += len(self.__allIdentifiers2(clazz))
			return n
		else:
			n = 0
			for x in self.allIdentifiers(clazz):
				n += 1
			return n
	#

	def loadAllObjects(self, clazz:type = None):
		if clazz is None:
			for clazz in self.__classRecords:
				for identifier in self.__allIdentifiers2(clazz):
					self.getObject(clazz, identifier)
		else:
			for identifier in self.allIdentifiers(clazz):
				self.getObject(clazz, identifier)
	#

	def allIdentifiers(self, clazz:type):
		assert clazz is not None

		cr = self.__classRecords[clazz.__name__]
		for fileEntryName in os.listdir(cr.dirPath):
			if fileEntryName.endswith(".json"):
				yield fileEntryName[:-5]
	#

	def objectExists(self, clazz:type, identifier):
		assert clazz is not None

		if identifier in self.__objCache[clazz.__name__]:
			return True
		else:
			cr = self.__classRecords[clazz.__name__]
			filePath = os.path.join(cr.dirPath, identifier + ".json")
			return os.path.exists(filePath)
	#

	#
	# Creates a new object instance and adds it to this persistency management infrastructure.
	#
	# @param		type clazz				The type of the object to create.
	# @param		identifier str			If present specifies the identifier that later on can be used to retrieve this object again.
	# @return		object					Returns the object.
	#
	def createObject(self, clazz:type, identifier:str = None, deserializationData:dict = None):
		assert clazz is not None

		cr = self.__classRecords[clazz.__name__]

		if identifier is not None:
			assert isinstance(identifier, str)
			if self.objectExists(clazz, identifier):
				raise Exception("An object of type " + repr(clazz) + " identified by " + repr(identifier) + " already exists!")
		else:
			identifier = cr.findFreeIdentifier()

		obj = cr.clazz()
		if deserializationData is not None:
			obj.deserialize(cr.ctx, deserializationData)
		else:
			obj.deserialize(cr.ctx, copy.deepcopy(cr.defaults))

		obj._x_identifier = identifier
		obj._x_persisteer = self
		obj._x_isModified = clazz._x_isAutoStore
		obj._x_timeStamp = -1

		self.__objCache[clazz.__name__][identifier] = obj

		return obj
	#

	#
	# Add an already existing object to the persistency management infrastructure.
	#
	# @param		object obj				The object to add. (The object's class must be registered.)
	# @param		identifier str			If present specifies the identifier that later on can be used to retrieve this object again.
	# @return		object					Returns the object.
	#
	def addExternalObject(self, obj, identifier:str = None):
		clazz = obj.__class__
		cr = self.__classRecords[clazz.__name__]

		if identifier is not None:
			assert isinstance(identifier, str)
			if self.objectExists(clazz, identifier):
				raise Exception("An object of type " + repr(clazz) + " identified by " + repr(identifier) + " already exists!")
		else:
			identifier = cr.findFreeIdentifier()

		obj._x_identifier = identifier
		obj._x_persisteer = self
		obj._x_isModified = True
		obj._x_timeStamp = -1
		obj.store()

		self.__objCache[clazz.__name__][identifier] = obj

		return obj
	#

	def getObject(self, clazz:type, identifier:str):
		assert clazz is not None

		obj = self.__objCache[clazz.__name__].get(identifier)
		if obj is None:
			cr = self.__classRecords[clazz.__name__]

			filePath = os.path.join(cr.dirPath, identifier + ".json")
			if not os.path.exists(filePath):
				return None

			jData = jk_json.loadFromFile(filePath)
			obj = cr.clazz()
			obj.deserialize(cr.ctx, jData)

			obj._x_identifier = identifier
			obj._x_persisteer = self
			obj._x_isModified = False
			obj._x_timeStamp = int(os.path.getmtime(filePath))

		return obj
	#

	def getObjectE(self, clazz:type, identifier:str):
		assert clazz is not None

		cr = self.__classRecords[clazz.__name__]
		filePath = os.path.join(cr.dirPath, identifier + ".json")

		obj = self.__objCache[clazz.__name__].get(identifier)
		if obj is not None:
			t = int(os.path.getmtime(filePath))

		if (obj is None) or (obj._x_timeStamp != t):
			if not os.path.exists(filePath):
				raise Exception("Object of type " + repr(clazz) + " identified by " + repr(identifier) + " does not exists!")

			jData = jk_json.loadFromFile(filePath)
			obj = cr.clazz()
			obj.deserialize(cr.ctx, jData)

			obj._x_identifier = identifier
			obj._x_persisteer = self
			obj._x_isModified = False
			obj._x_timeStamp = t

		return obj
	#

	def storeObject(self, obj):
		clazz = obj.__class__

		self.__objCache[clazz.__name__][obj._x_identifier] = obj

		identifier = obj._x_identifier
		assert identifier is not None
		cr = self.__classRecords[clazz.__name__]
		filePath = os.path.join(cr.dirPath, identifier + ".json")
		jData = obj.serialize(cr.ctx)
		with jk_utils.file_rw.openWriteText(filePath) as f:
			f.write(json.dumps(jData, indent="\t"))

		obj._x_timeStamp = int(os.path.getmtime(filePath))
		obj._x_isModified = False
	#

	def destroyObject(self, obj):
		clazz = obj.__class__

		identifier = obj._x_identifier
		assert identifier is not None
		cr = self.__classRecords[clazz.__name__]
		filePath = os.path.join(cr.dirPath, identifier + ".json")
		if os.path.exists(filePath):
			os.unlink(filePath)
		obj._x_persisteer = None

		dataMap = self.__objCache[clazz.__name__]
		if obj._x_identifier in dataMap:
			del dataMap[obj._x_identifier]

		obj._x_persisteer = None
	#

	def destroyObjectByID(self, clazz:type, identifier:str):
		assert clazz is not None

		cr = self.__classRecords[clazz.__name__]
		dataMap = self.__objCache[clazz.__name__]

		if identifier in dataMap:
			obj = dataMap[identifier]
			del dataMap[identifier]
			obj._x_persisteer = None

		filePath = os.path.join(cr.dirPath, identifier + ".json")
		if os.path.exists(filePath):
			os.unlink(filePath)
	#

	def destroyAllObjects(self, clazz:type):
		assert clazz is not None

		for obj in self.__objCache[clazz.__name__]:
			obj._x_identifier = None
		self.__objCache[clazz.__name__].clear()

		cr = self.__classRecords[clazz.__name__]
		for fileEntryName in os.listdir(cr.dirPath):
			if fileEntryName.endswith(".json"):
				filePath = os.path.join(cr.dirPath, fileEntryName)
				os.unlink(filePath)
	#

	def storeAllModified(self, clazz:type):
		assert clazz is not None

		for obj in self.__objCache[clazz.__name__]:
			obj.storeIfModified()
	#

	def clearEntireCache(self):
		for v in self.__objCache.values():
			v.clear()
	#

	def clearClassCache(self, clazz:type):
		assert clazz is not None

		self.__objCache[clazz.__name__].clear()
	#

#








