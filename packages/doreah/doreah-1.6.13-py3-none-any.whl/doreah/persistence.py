import pickle
import os
import math
import zlib
import random
import yaml
import shutil

from ._internal import DEFAULT, defaultarguments, gopen, DoreahConfig


# folder	folder to store log files
config = DoreahConfig("persistence",
	folder="storage"
)


@defaultarguments(config,folder="folder")
def save(data,name,folder=DEFAULT):
	"""Saves the supplied data structure to disk.

	:param data: Object to be serialized and saved to disk
	:param string name: File name to be used
	:param string folder: Custom folder to save the file in"""

	filename = os.path.join(folder,name)

	try:
		with gopen(filename,"wb") as fl:
			stream = pickle.dumps(data)
			fl.write(stream)
	except:
		pass

@defaultarguments(config,folder="folder")
def load(name,folder=DEFAULT):
	"""Loads a data structure from disk.

	:param string name: File name to be read
	:param string folder: Custom folder where the file is stored
	:return: Data object"""

	filename = os.path.join(folder,name)

	try:
		with gopen(filename,"rb") as fl:
			ob = pickle.loads(fl.read())
	except: ob = None

	return ob

@defaultarguments(config,folder="folder")
def delete(name,folder=DEFAULT):
	"""Deletes a serialized data structure from disk.

	:param string name: File name
	:param string folder: Custom folder where the file is stored"""

	filename = os.path.join(folder,name)
	try:
		os.remove(filename)
	except:
		pass

@defaultarguments(config,folder="folder")
def size(name,folder=DEFAULT):
	"""Returns the size of a serialized object.

	:param string name: File name
	:param string folder: Custom folder where the file is stored"""

	filename = os.path.join(folder,name)
	return os.path.getsize(filename)


# need a deterministic hash function
def _hash(val):
	if isinstance(val,int):
		return val
	elif isinstance(val,str):
		return zlib.adler32(bytes(val,encoding='UTF-8'))
	elif isinstance(val,dict):
		return _hash(tuple((k,val[k]) for k in sorted(val)))
	elif isinstance(val,tuple) or isinstance(val,list):
		x = 10
		i = 1
		for element in val:
			x = ((x * _hash(element)) ** i)
			i += 1
		return x

	try:
		return zlib.adler32(val)
	except: pass
	try:
		return zlib.adler32(bytes(val))
	except: pass



class DiskDict:
	"""Dictionary-like object that stores its authorative information completely on disk.

	:param integer maxmemory: Soft memory limit (in bytes), not meant for precision
	:param integer maxstorage: Soft disk space limit (in bytes), not meant for precision
	:param string name: Directory name used for storage
	:param string folder: Parent directory"""

	@defaultarguments(config,folder="folder")
	def __init__(self,maxmemory=math.inf,maxstorage=1024*1024*1024*4,name="diskdict",folder=DEFAULT):

		self.maxmemory = maxmemory
		self.maxstorage = maxstorage

		self.name = name
		self.folder = os.path.join(folder,name)


		self.cache = {}
		self.cache_unhashable = {}


	def __contains__(self,key):
		try:
			self.get(key)
			return True
		except:
			return False
	def __getitem__(self,key):
		return self.get(key)
	def __setitem__(self,key,value):
		return self.add(key,value)
	def __delitem__(self,key):
		pass

	def __str__(self):
		return "{" + ",".join([str(key) + ":" + str(self.cache[key]) for key in self.cache] + ["etc."]) + "}"

	def get(self,key):
		"""Get the value of a key.

		:param key: Key to be retrieved
		:return: Value of the requested key
		:raises KeyError: No valid entry for the key found."""

		hashvalue = str(_hash(key))
		try:
			return self.cache[key]
		except: pass
		try:
			return self.cache_unhashable[hashvalue]
		except: pass

		if os.path.exists(os.path.join(self.folder,hashvalue)):
			possibilities = os.listdir(os.path.join(self.folder,hashvalue))
			for p in possibilities:
				result = load(os.path.join(self.name,hashvalue,p),folder=self.folder)
				if result[0] == key:
					val = result[1]
					try:
						self.cache[key] = val
					except TypeError:
						self.cache_unhashable[hashvalue] = val
					return val

		raise KeyError()



	def add(self,key,value):
		"""Add an entry.

		:param key: Key to be added
		:param value: Value of this entry"""

		hashvalue = str(_hash(key))

		# cache
		try:
			self.cache[key] = value
		except TypeError:
			self.cache_unhashable[hashvalue] = value

		name = str(random.uniform(1000000000,9999999999)).replace(".","")
		save((key,value),os.path.join(self.name,hashvalue,name),folder=self.folder)



class YAMLDict(dict):

	def __init__(self,filename,d={},update_every_nth_change=10):
		self.filename = filename
		self.freq = update_every_nth_change
		super().__init__(d)
		if os.path.exists(self.filename):
			with open(self.filename) as df:
				self.update(yaml.safe_load(df))

		self.savetodisk()

	def __setitem__(self,key,value):
		super().__setitem__(key,value)
		if random.choice(range(0,self.freq)) == 0:
			self.savetodisk()

	def savetodisk(self):
		with open(self.filename + ".tmp","w") as df:
			yaml.dump(self.tonormaldict(),df)
		shutil.move(self.filename + ".tmp",self.filename)

	def tonormaldict(self):
		return {k:self[k] for k in self}
