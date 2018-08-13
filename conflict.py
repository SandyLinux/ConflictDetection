import json

global count1

class Conflict(object):
	# class conflict is used to store the confliction occurring b/w two rules
	# cid - identification for conflict
	# type - the type of this confilict, including masked, generialized....
	# rid - identification of the rule which it has conflict with 

	def __init__(self, cid, types, rid, comments=''):
		self.cid = cid
		self.types = types # a enumerate type
		self.rid = rid
		self.comments = comments
	def getType(self):
		return self.types
	def getConflictRuleId(self):
		return self.rid
	def printInfo(self):
		print ('index : ', self.cid, 'type is :', self.types, 'with Rule #:', self.rid, 'comments:',self.comments)
	def toJSON(self):
		value = json.dumps(self, default=lambda o:o.__dict__)
		return json.loads(value)

	def toObject(jsoninDB):
		xa = json.dumps(jsoninDB)
		xb = json.loads(xa)
		return namedtuple("Rule", xb.keys())(*xb.values())
