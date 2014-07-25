class TopNList(object):
	def __init__(self,n,reverse=False,value_func=lambda x:x):
		if n<=0:
			raise Exception("n must be a postive integer")
		self.n=n
		self.value_func=value_func
		self.compare_func=(lambda x,y:x>y) if reverse else (lambda x,y:x<y)
		self._data=[]

	def append(self,value):
		if not self._data:
			self._data.append(value)
		else:
			for index,v in enumerate(reversed(self._data)):
				if self.compare_func(self.value_func(value),self.value_func(v)):
					self._data.insert(len(self._data)-index,value)
					if len(self._data)>self.n:
						self._data.pop()
					break
				if index==len(self._data)-1:
					self._data.insert(0,value)
					if len(self._data)>self.n:
						self._data.pop()
					break
			

	def __len__(self):
		return len(self._data)

	def __iter__(self):
		self.index=0
		return self

	def __getitem__(self,index):
		return self._data[index]

	def next(self):
		if self.index == len(self):
			raise StopIteration
		res=self._data[self.index]
		self.index = self.index + 1
		return res
