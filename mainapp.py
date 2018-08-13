from apiReader2 import *
from ruleEnums import *

rulelists =[]

#read all rules from database via XML api
rulelists = function1()

#print (f'there are {len(rulelists)} records ')


print ('--------------------------------------')
print ('|                                    |')
print ('|            Result Analysis         |')
print ('|            SYSTEM TESTING          |')
print ('|                                    |')
print ('--------------------------------------')

#mock data used in system test, and delete it later

rules_list =[ \
	Rule( 1,'rule1', '69.212.128.0/30',   '202.103.29.60', 'deny',  'tcp')\
	,Rule(2,'rule2', '69.212.128.1',   '202.103.29.60',  'allow', 'tcp')\
	,Rule(3,'rule3', '0.0.0.0/0',   '201.103.29.60', 'deny',  'tcp')\
	,Rule(4,'rule4', '60.212.128.1',   '0.0.0.0/0',  'allow', 'tcp')\
	,Rule(5,'rule4', '60.212.128.1',   '0.0.0.0/0',  'allow', 'tcp')\
	]

for i_index,i in enumerate(rules_list):
	
	for j_index,j in enumerate(rules_list):
		#j_index = index
		
		if i_index == j_index:
			print(' ')		
		else:
			print (f'\ncomparing rule {i_index} and rule {j_index}')
			#print ('      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~-----|')
			#print ('----   result analysis               |')

			resl = i.detectConflict(j)
			if (resl == conflictType.noConflict):
				print (resl.name)

#connect to database and save all updates firewall rules into 'PaloRules1' collection
mycoll = dbConn()
for i in rules_list:
	#show rules data
	i.printRule()
	# insert data into database
	mycoll.insert_one(i.toJSON())
