from IPIdentification import *
from ruleEnums import *
from conflict import *
import json
from xml.dom.minidom import parse
import xml.dom.minidom
import ssl
import xml.etree.ElementTree as ET
import urllib
from urllib.request import urlopen
from IPy import IP
import pymongo
#dbConn module provide the method to connect the mongodb
from  dbConn import *
#in module test1, import global variable count1
from test1 import *

#setup a connection to table conflict
mycoll2 = dbConn2()

class Rule(object):
	# import global count number from module globalVars
	global count1
	
	def __init__(self, index, name, source, dest, action, protocol='tcp', conflictsList=[]):
		self.index = index
		self.name = name
		self.protocol = protocol
		self.source = IPIdentification(source) # string of Source ip generates an IPIdentification object
		self.dest = IPIdentification(dest) # string of dest ip generateds an IPIdentification object
		self.action = action
		self.conflictsList = []#containing the list of cid
		
	def getName(self):
		return self.name
	
	def getSourceIp(self):
		return self.source.getIP()
	
	def getDestIP(self):
		return self.dest.getIP()

	def printRule(self):
		print ('index : ', self.index, 'name:' , self.name,'; protocol:' , self.protocol, '; \
			source:', self.source.getIP(), 'source port : ', self.source.port, ';desct:', self.dest.getIP(), \
			'dest port is :', self.dest.port, '; action:', self.action)

		if (len(self.conflictsList) != 0):
			for i in self.conflictsList:
				print ('conflict index:', i)

	#function : rule x is a subset of rule y under the condition of 
	# i!= 0, j!= k , j, k values in {1,2};  j = 1 means source ip of ruleX is a subset
	# of that of ruleY; j = 2 means source ip of ruleX is equal to that of ruleY

	def getIValue(self, another):	
		#default i value is -1 meaning invalid
		i = -1
		if (self.protocol != another.protocol):
			# protocols are not same
			i = 0
		else:
			#protocols are same
			i = 1 
		return i
	
	def getJValue(self, another):
		j = -1
		#if them related/ overlaps? 
		#2 ips are not same, as well as is not subset/superset(overlaps), then there is not related

		if (self.source.isCorrelation(another.source) == False):
			j = 0  #not related 
		elif (self.source.isEqual(another.source) == True):
			j = 2 #2 ip  are equal
		elif (self.source.isSubset(another.source) == True):
			j = 1 # 1 means ip1 is a subnet of ip2
		elif (self.source.isSuperset(another.source) == True):
			j = 3 # superSet
		else:
			j = -1

		return j

	def getKValue(self, another):

		k = -1
		
		if (self.dest.isCorrelation(another.dest) == False):
			k = 0  #not related 
		elif (self.dest.isEqual(another.dest) == True):
			k = 2 #2 ip  are equal
		elif (self.dest.isSubset(another.dest) == True):
			k = 1 # 1 means ip1 is a subnet of ip2
		elif (self.dest.isSuperset(another.dest) == True):
			k = 3 # superSet
		else:
			k = -1

		return k

		
	
	def getIJKValue(self, another):

		#initial value is -1 (invalid value)
		i = j = k = -1 	
		#put the 3 values into a list
		
		
		#get the relation value for 3 criteria, protocol, source ip, destination ip

		i = self.getIValue(another)
		j = self.getJValue(another)
		k = self.getKValue(another)
		results = [i,j,k]
		return results

	def isSubSet(self,another):
		
		i = j = k = -1
		result = False
		
		i = self.getIValue(another)
		j = self.getJValue(another)
		k = self.getKValue(another)

		# i!=0 means two protocols for rule x and rule y are the same, either tcp or udp
		
		jkvalue = {j,k}
		
		jkvalue_pool = [{1,2},{2,1},{1,1}]

		m = jkvalue in jkvalue_pool

		if ((i!=0) and (m == True)):
			result = True
		else:
			result = False

		return result



	def isSuperSet(self, another):

		result = False

		i = j = k = -1 	

		
		i = self.getIValue(another)
		j = self.getJValue(another)
		k = self.getKValue(another)

		# i!=0 means two protocols for rule x and rule y are the same, either tcp or udp
		
		jkvalue = {j,k}

		jkvalue_pool = [{2,3},{3,2},{3,3}]

		m = jkvalue in jkvalue_pool

		if ((i!=0) and (m == True)):
			result = True
		else:
			result = False

		
		return result

	def isEqual(self, another):
		result  = False
		i = j = k = -1
		
		i = self.getIValue(another)
		j = self.getJValue(another)
		k = self.getKValue(another)

		if ((i == 1 )&(j == 2)&(k == 2)):
			result = True
		else:
			result = False

		return result

	def isNotCorrelation(self, another):
		
		result = False

		i_f = self.getIValue(another)
		j_f = self.getJValue(another)

		k_f = self.getKValue(another)

		#print ('=== i,j,k is: ===', i_f, j_f, k_f)

		m = (i_f == 0 or j_f == 0 or k_f == 0)
		
		if (m == True):
			print ('the two rules is NOT correlation!', m)
			result = True
		else:
			result = False
		return result
		#result finally


	def notAssociate(self, another):
		#in default, two rules are related
		result = False
		#Rijk means the relationship b/w Rx and Ry
		#i,j,k respectively stands for the relationship in terms of protocol, 
		#source, and destination
		# values of i range from 0, 1, meaning not equal and equal 
		# values of j/k range from 0,1,2,3  meaning not associated, subset, equal, and superset
		
		i =  j  = k = -1 # intial values are all 1 for i , j , k, assuming the 3 criteria are all related. 

		#if protocols are not equal for two rules, 
		#the relationship b/w them in terms of protocol are not associated, 
		if (self.protocol != another.protocol):
			#2 protocols are not 
			i = 0
			#print ('protocol is NOT SAME, so 2 rules NO RELATED, NO CONFLICT')
		else:
			i = 1 
			#print ('protocol is SAME, so 2 rules have risk conflict ')


		#print('**SOURCE side, ips for comparing  :', self.source.ip, another.source.ip)
		
		#if them related/ overlaps? 
		#2 ips are not same, as well as is not subset/superset(overlaps), then there is not related

		'''if (self.source.ip != another.source.ip) & (isRelated(self.source.ip, another.source.ip) == False):
			j = 0 # 0 means not related
			print ('source ip NOT related', j)

		else:
			j = 1
			print ('source ip RELATED', j)
		'''
		if (self.source.ip == another.source.ip):
			j = 1
			#print ('source ip RELATED', j, 'for they are same')
		elif (isRelated(self.source.ip, another.source.ip) == True):
			j = 1
			#print ('source ip RELATED', j, 'for they are overlaps')

		else:
			j = 0
			#print ('source ip NOT RELATED', j)
		
		#print('**DESTINATION side, ips for comparing :', self.dest.ip, another.dest.ip)
		
		if (self.dest.ip == another.dest.ip):
			k = 1
			#print ('destination ip RELATED', k, 'for they are same')
		elif (isRelated(self.dest.ip, another.dest.ip) == True):
			k = 1
			#print ('destination ip RELATED', k, 'for they are overlaps')

		else:
			k = 0
			#print ('destination ip NOT RELATED', j)

		'''if (self.dest.ip != another.dest.ip) & (isRelated(self.dest.ip, another.dest.ip) == False):
			k = 0 # 0 means not related 
			print ('dest ip NOT related', k)

		else:
			k = 1
			print ('dest ip RELATED', k)
		'''
		#print (' i , j , k : ', i, j ,k)

		m = (i == 0 or j == 0 or k == 0)
		if m == True:
			#print ('the two rules is NOT ASSOCIATED!', m)
			result = True
		#result finally

		return result


	def isCorrelation(self,another):
		result = False

		i = j = k = -1

		i = self.getIValue(another)
		j = self.getJValue(another)
		k = self.getKValue(another)

		# i!=0 means two protocols for rule x and rule y are the same, either tcp or udp
		
		jkvalue = {j,k}

		jkvalue_pool = [{1,3},{3,1}]

		m = jkvalue in jkvalue_pool

		if ((i != 0) and (m == True)):
			result = True
		else:
			result = False

	
		return result
	def hasMaskedConflict(self,another):
		result = False
		
		#global variable to record total number of conflict

		global count1
		if ((self.isEqual(another) == True) & (self.index < another.index) &(self.action != another.action)):

		#if ((i.isRuleEqual(j) == True) &(i.index < j.index) & (i.action != j.action)):
				print ('~~~~~~~~~found masked conflict between rule ', self.index, 'and rule ',another.index)

				result = True
				#def __init__(self, cid, types, rid):
				cfl = Conflict(count1, 'masked', another.index)
				self.conflictsList.append(count1)
				#cfl.printInfo()
				
				count1 += 1#self.count+ 1
				mycoll2.insert_one(cfl.toJSON())
	
		m = ((self.isSuperSet(another) == True) & (self.index < another.index) & (self.action != another.action))
		if (m == True):
				print ('~~~~~~~~~~~~~found masked conflict between rule ', self.index, 'and rule ',another.index)
				result = True
				
				cfl = Conflict(count1, 'masked', another.index)
				self.conflictsList.append(count1)
				count1 += 1
				mycoll2.insert_one(cfl.toJSON())
	
		return result

	def hasGeneralizationConflict(self,another):
		result = False
		global count1
		m = ((self.isSuperSet(another) == True) & (self.index > another.index) & (self.action != another.action))
		
		if (m == True):
				print (f'~~~~~~~~~~~~~found generalization conflict between rule {self.index} and {another.index}')
				result = True
				cfl = Conflict(count1, 'generalization', another.index)
				#print ('conflict add into list ', self.count)
				self.conflictsList.append(count1)

				count1 += 1
				mycoll2.insert_one(cfl.toJSON())
	
		else:
			result = False
		return result

	def hasCorrelationConflict(self, another):
		result = False
		global count1
		m = ((self.isCorrelation(another) == True) & (self.action != another.action))
		
		if (m == True):
				print ('~~~~~~~~~~~~~found correlation conflict between rule ', self.index, 'and rule ', another.index)
				result = True
				cfl = Conflict(count1, 'correlation', another.index)
				#print ('conflict add into list ', self.count)
				self.conflictsList.append(count1)

				count1 += 1
				mycoll2.insert_one(cfl.toJSON())
	
		else:
			result = False
		return result

	def hasRedundancyConflict(self, another):
		result = False
		global count1
		comments = ''

		m = ((self.isSubSet(another) == True) & (self.index > another.index)&(self.action == another.action))
		
		if (m == True):
			comments =  'rule ' + str(self.index) + ' will not be reached forever!'
			
		n = ((self.isEqual(another) == True) &(self.action == another.action))
		
		p = ((self.isSubSet(another) == True) & (self.index < another.index)&(self.action == another.action))
		
		if (p == True):
			comments = 'part of rule '+ str(self.index)+ '  is redundancy in rule '+str(another.index)

		if ((m == True) or (n == True) or (p == True)):
				print ('~~~~~~~~~~~~~found redundancy between rule ', self.index, ' and rule ', another.index)
				result = True
				cfl = Conflict(count1, 'redundancy', self.index, comments)
				#print ('conflict add into list ', self.count)
				self.conflictsList.append(count1)

				count1 += 1#self.count+ 1
				mycoll2.insert_one(cfl.toJSON())
	
		else:
			result = False
		return result
		
	def detectConflict(self, another):
		conflict_type = conflictType.noConflict

		if (self.hasMaskedConflict(another) == True):
			conflict_type = conflictType.masked
		elif (self.hasGeneralizationConflict(another) == True):
			conflict_type = conflictType.generalized
		elif (self.hasCorrelationConflict(another) == True):
			conflict_type = conflictType.correlation
		elif (self.hasRedundancyConflict(another) == True):
			conflict_type = conflictType.redundancy
		else:
			conflict_type = conflictType.noConflict
		
		return conflict_type

	def toJSON(self):
		value = json.dumps(self, default=lambda o:o.__dict__)
		return json.loads(value)

	def toObject(jsoninDB):
		xa = json.dumps(jsoninDB)
		xb = json.loads(xa)
		return namedtuple("Rule", xb.keys())(*xb.values())

