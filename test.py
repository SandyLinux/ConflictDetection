from IPIdentification import *

class Rule(object):
	def __init__(self,index,name,source,dest,action,protocol='tcp',conflictsList=[]):
		self.name = name
		self.index = index
		self.protocol = protocol
		self.source = IPIdentification(source) # string of Source ip generates an IPIdentification object
		self.dest = IPIdentification(dest) # string of dest ip generateds an IPIdentification object
		self.action = action
		#self.alert = alert
		self.conflictsList = conflictsList#containing the list of cid

	def getName(self):
		return self.name
	
	def getSourceIp(self):
		#ips = IP(self.source.ip)
		#return ips.strNormal(1)
		return self.source.getIP()
	
	def getDestIP(self):
		return self.dest.getIP()


	def printRule(self):
		print ('index : ', self.index, 'name:' , self.name,'; protocol:' , self.protocol, '; \
			source:', self.source.getIP(), 'source port : ', self.source.port, ';desct:', self.dest.ip, \
			'dest port is :', self.dest.port, '; action:', self.action)

ip1 = IPIdentification(1,'10.10.0.0/24')
rule1 = Rule(1,'rule1','10.1.1.1','192.168.1.1','allow')

rule1.printRule()
#self,name,index,source,dest,action,protocol='tcp',conflictsList=[]):
#ip2 = IPIdentification(1,'10.10.0.0/16')
