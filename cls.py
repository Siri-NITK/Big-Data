import sys

defs=[]
resources_list=[]
actors_list=[]
policies_list=[]

class resource(object):

	fields=[]

	def __init__(self,id):

		global resources_list,defs

		self.id=id

		resources_list.append(self)
		defs.append(self)

class actor(object):

	fields=[]

	def __init__(self,id):

		global actors_list,defs

		self.id=id

		actors_list.append(self)
		defs.append(self)


