from sets import Set

import pdb
import re
import sys
import os.path
from sys import argv
from cls import *

class lexer(object):

	line_count=0
	file_ptr=16
	keywords=set(["resource","policy","actor","exists","all","access","allow","in"])

	def __init__(self):
		self.f = open("res.txt", 'r')
		self.start()

	############################## LEXICAL ANALYSER ########################################

	def eat_whitespace(self):
		char =self.f.read(1)
		if(char==" "):
			
			while(self.f.read(1)==" "):
				print ""
			self.f.seek(-1,1)
			self.eat_whitespace()
		elif(char=="\n"):
			#print "skip line"
			self.line_count+=1
			self.eat_whitespace()

		elif(char==""):
			print"parsed successfully"
		else:
			self.f.seek(-1,1)

	def lex(self):

		self.eat_whitespace()

		char =self.f.read(1)

		if (char==""):
			  return "EOF",char

		if (char.isalpha()):
			s=""
			while(char.isalnum()):
	    			s = "".join((s, char))
	    			char=self.f.read(1)

			self.f.seek(-1,1)
			if s in self.keywords:
				return s,"keyword"
			return "identifier",s

		if(char==";"):
			return "semi",char
		if(char=="("):
			return "simpleopen",char
		if(char==")"):
			return "simpleclose",char
		if(char=="{"):
			return "curlyopen",char
		if(char=="}"):
			return "curlyclose",char
		if(char==","):
			return "comma",char
		if(char=="."):
			return "dot",char
		if(char==":"):
			return "colon",char
		if(char=="-"):
			char=self.f.read(1)
			print char
			if(char==">"):
				return "arrow",char
			else:
				pass
		if(char=="*"):
			return "asterisk",char
		if(char=="!"):
			return "exclamation",char
		if(char=="="):
			return "equals",char

	############################# START PARSER #############################################

	def start(self):
		tok=self.lex()[0]
		
		if(tok!="resource" and tok!="actor"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)

		if(tok=="resource"):
			self.f.seek(-len("resource"),1)
			self.resource_def()
		else:
			self.actor_def()

		print "Parsed successfully :D"


	############################## ID/RESOURCE/ACTOR LIST ##################################

	def id_list(self,lst):


		tok,val=self.lex()

		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)
		lst.append(val)


		tok=self.lex()[0]

		if(tok!="simpleclose" and tok!="comma" and tok!="curlyclose" and tok!="access"):
			print "Error-idlist"
			sys.exit(0)
		if(tok=="comma"):
			self.id_list(lst)
		if(tok=="simpleclose" or tok=="curlyclose"):
			self.f.seek(-1,1)

		if(tok=="access"):
			self.f.seek(-len("access"),1)

		return lst

	def resource_id(self,rlst):

		lst=[]

		tok,val=self.lex()
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		#print "In resource ID going into rlst %s"%val
		r=resource(val)


		tok=self.lex()[0]
		if(tok!="dot" ):
			print "Error-no dot"
			sys.exit(0)

		tok,val=self.lex()
		if(tok!="simpleopen" and tok!="identifier" and tok!="asterisk"):
			print "Error-define resources properly"
			sys.exit(0)

		if(tok=="simpleopen"):

			r.fields=self.id_list(lst)
			print "*******************id list"
			print r.fields
			rlst.append(r)

			tok=self.lex()[0]
			if(tok!="simpleclose"):
				print "Error-closebrace"
				sys.exit(0)

			tok=self.lex()[0]
			if(tok!="semi" and tok!="comma"):
				print "Error-add ; OR ,"
				sys.exit(0)

			if(tok=="comma"):
				self.resource_id(rlst)

		if(tok=="identifier"):
			r.fields=val
			print "*******************id list"
			print r.fields
			rlst.append(r)

			tok=self.lex()[0]
			if(tok!="comma" and tok!="semi"):
				print "Error no , or ;"
				sys.exit(0)
			if(tok=="comma"):
				self.resource_id(rlst)

		if(tok=="asterisk"):
			tok=self.lex()[0]
			if(tok!="comma" and tok!="semi"):
				print "Error no , or ;"
				sys.exit(0)
			if(tok=="comma"):
				self.resource_id(rlst)

		return rlst

	def actor_list(self):
		tok=self.lex()[0]
		if(tok!="identifier"):
			print "Error-iden"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="colon"):
			print "Error-colon"
			sys.exit(0)

		use_rlst=[]
		use_rlst=self.resource_id(use_rlst)
		#print "===================actorlist"
		#print use_rlst

		curr_fileptr=self.f.tell()
		tok=self.lex()[0]
		if(tok=="identifier"):
			self.f.seek(curr_fileptr)
			self.actor_list()
		self.f.seek(curr_fileptr)

		return use_rlst
	################################# ACTOR DEFINITION #####################################

	def actor_def(self):
		tok=self.lex()[0]

		lst=[]

		if(tok!="actor"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)

		tok,val=self.lex()
		if(tok!="identifier"):
			print "Error-iden"
			sys.exit(0)

        	a=actor(val)

		tok=self.lex()[0]
		if(tok!="curlyopen" and tok!="equals"):
				print "Error-keep curly open brace or equals"
				sys.exit(0)

		if(tok=="curlyopen"):
			a.fields=self.actor_list()
			print a.fields

			tok=self.lex()[0]
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)
		else:
			tok=self.lex()[0]

			if(tok!="curlyopen"):
				print "ERROR- no curly open :( "
				sys.exit(0)
			a.fields=self.id_list(lst)

			tok=self.lex()[0]
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)

			tok=self.lex()[0]
			if(tok!="semi"):
				print "Error-no semi %d"%self.line_count
				sys.exit(0)

		tok=self.lex()[0]
		if(tok=="resource"):
			self.f.seek(-len("resource"),1)
			self.resource_def()

		elif(tok=="actor"):
			self.f.seek(-len("actor"),1)
			self.actor_def()
		elif(tok=="policy"):
			self.f.seek(-len("resource"),1)
			self.policy_def()
		else:
			self.f.seek(-1,1)
	############################## RESOURCE DEFINITION #####################################

	def resource_def(self):

		lst=[]

		tok=self.lex()[0]
		if(tok!="resource"):
			print "Start line %d with resource." %self.line_count
			sys.exit(0)

		tok,val=self.lex()
		
		if(tok!="identifier"):
			print "Error-iden"
			sys.exit(0)

		r=resource(val)

		tok=self.lex()[0]
		if(tok=="equals"):
			tok=self.lex()[0]
			if(tok!="curlyopen"):
				print "Error-keep curly open brace"
				sys.exit(0)

			r.fields=self.id_list(lst)

			print "*******list/**************"
			print r.fields

			tok=self.lex()[0]
			if(tok!="curlyclose"):
				print "Error-keep curly close brace"
				sys.exit(0)

		elif(tok=="simpleopen"):

			r.fields=self.id_list(lst)

			print "*******list/**************"
			print r.fields

			tok=self.lex()[0]
			if(tok!="simpleclose"):
				print "Error-closebrace"
				sys.exit(0)

		else:
			print "put either equals or simple brace"
			sys.exit(0)

		tok=self.lex()[0]

		if(tok!="semi"):
			print "Error-no semi %d"%self.line_count
			sys.exit(0)

		tok=self.lex()[0]
		if(tok=="resource"):
			self.f.seek(-len("resource"),1)
			self.resource_def()

		elif(tok=="actor"):
			self.f.seek(-len("actor"),1)
			self.actor_def()
		elif(tok=="policy"):
			self.f.seek(-len("resource"),1)
			self.policy_def()
		else:
			self.f.seek(-1,1)


	############################## POLICY DEFINITION #######################################

	def policy_def(self):
		print "In policy definition"
		tok=self.lex()[0]
		if(tok!="policy"):
			print "Start line %d with policy." %self.line_count
			sys.exit(0)

		tok,name=self.lex()
		print "The policy is %s"%name

		if(tok!="identifier"):
			print "Error-iden"
			sys.exit(0)

		p=policy(name)

		print p.policy_1_list		
		tok=self.lex()[0]
		if(tok!="colon"):
			print "Error- no Colon"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok=="allow"):
			self.policy_1(p)
		if(tok=="all"):
			self.policy_2(p)
		if(tok=="exists"):
			self.policy_3(p)


	def  policy_1(self,pol):

		lst=[]

		pol_1=policy_type_1(pol)

		pol_1.allow=self.id_list(lst)
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>pol 1 allow<<<"
		print pol_1.allow
			
		tok=self.lex()[0]
		if(tok!="access"):
			print "Error-no access"
			sys.exit(0)

		lst=[]
		pol_1.access=self.resource_id(lst)
		print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>pol 1 access<<<"
		print pol_1.access

		tok=self.lex()[0]
		if(tok=="allow"):		
			self.policy_1(pol)
		elif(tok=="policy"):
			self.f.seek(-len("policy"),1)
			self.policy_def()
		else:
			pass

	def  policy_2(self,pol):

		lst=[]
		pol_2=policy_type_2(pol)
		
		tok=self.lex()[0]
		if(tok!="identifier"):
			print "Error-put an id"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="colon"):
			print "Error-no colon"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="actor"):
			print "Error-no actor :("
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="dot" ):
			print "Error-no dot"
			sys.exit(0)
		
		tok=self.lex()[0]
		if(tok!="identifier"):
			print "Error-put an id"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="dot"):
			print "Error-no dot"
			sys.exit(0)

		dic_value={}

		# Taking the value of the actor field as the condition
		tok,val1=self.lex()
		if(tok!="identifier"):
			print "Error-put an id"
			sys.exit(0)
		
		tok=self.lex()[0]
		
		if(tok!="equals"):
			print "Error no equals"
			sys.exit(0)

		tok,val2=self.lex()
		if(tok!="identifier"):
			print "Error-put an id"
			sys.exit(0)

		dic_value[val1]=val2

		pol_2.actor_field=dic_value


		tok=self.lex()[0]
		if(tok!="arrow"):
			print "Error-no arrow"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok=="allow"):
		
			print "BEFORE:lets see the pol lists in policy 2"
			print pol.policy_1_list

			self.policy_1(pol)

			print "AFTER:lets see the pol lists in policy 2"
			print pol.policy_1_list

			
			
		
	def policy_3(self,pol):

		lst=[]
		pol_3=policy_type_3(pol)
		
		tok=self.lex()[0]
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="in"):
			print "Error-no in"
			sys.exit(0)

		tok,val=self.lex()
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)
		#Type of group

		pol_3.group=val		
		
		tok=self.lex()[0]
		if(tok!="colon"):
			print "Error- no Colon"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="actor"):
			print "Error-no actor :("
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="dot"):
			print "Error-no dot"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok!="dot"):
			print "Error-no dot"
			sys.exit(0)

		#An empty dictionary for the dictionary
		dic={}
		
		tok,val1=self.lex()
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)
		
		
		tok=self.lex()[0]
		if(tok!="equals"):
			print "Error no equals"
			sys.exit(0)

		tok,val2=self.lex()
		if(tok!="identifier"):
			print "Error-identifier"
			sys.exit(0)

		dic[val1]=val2
		
		pol_3.condition=dic		
		
		tok=self.lex()[0]
		if(tok!="arrow"):
			print "Error-no arrow"
			sys.exit(0)

		tok=self.lex()[0]
		if(tok=="allow"):
			print "BEFORE:lets see the pol lists in policy 2"
			print pol.policy_1_list

			self.policy_1(pol)

			print "AFTER:lets see the pol lists in policy 2"
			print pol.policy_1_list
			

#--------------------------------------------------------------------------------------------------------------------------------------------
lexer()
#print ', '.join(i.id for i in actors_list)
#print actors_list[2].fields[1]
#print policies_list[0].policy_1_list[0].access[1].id
#print policies_list[1].policy_2_list[0].pol1.allow

print "------------------------------------------------"
print ','.join(i.id for i in policies_list)
print policies_list[0].policy_1_list[3].access
print "------------------------------------------------"
print policies_list[1].policy_2_list[0]
print policies_list[1].policy_1_list
print "------------------------------------------------"
print policies_list[2].policy_3_list[0].condition


