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

class policy(object):


	def __init__(self,name):

		global policies_list,defs
	
		self.policy_1_list=[]
		self.policy_2_list=[]
		self.policy_3_list=[]

		self.id=name

		policies_list.append(self)
		defs.append(self)
	
class policy_type_1:
		
	def __init__(self,pol):
			
		self.allow=[]
		self.access=[]
		self.outer_instance=pol
		self.outer_instance.policy_1_list.append(self)

class policy_type_2:
		
	def __init__(self,pol):
	
		self.actor_field={}
		
		self.outer_instance=pol
		self.outer_instance.policy_2_list.append(self)
			
class policy_type_3:

		
	def __init__(self,pol):

		self.condition={}
		self.group=""
						
		self.outer_instance=pol			
		self.outer_instance.policy_3_list.append(self)

