from apiReader2 import *

rulelists =[]
rulelists = function1()
print (len(rulelists))

#lists = iter(rules_list)
#print('totally there are ', len(rules_list),' records in the rule list')
print ('--------------------------------------')
print ('|                                    |')
print ('|            result analysis         |')
print ('|            UNIT TESTING            |')
print ('|                                    |')
print ('--------------------------------------')

rules_list =[ \
	Rule( 1,'rule1', '69.212.128.0/30',   '202.103.29.60', 'deny',  'tcp')\
	,Rule(2,'rule2', '69.212.128.1',   '202.103.29.60',  'allow', 'tcp')\
	,Rule(3,'rule3', '0.0.0.0/0',   '201.103.29.60', 'deny',  'tcp')\
	,Rule(4,'rule4', '60.212.128.1',   '0.0.0.0/0',  'allow', 'tcp')\
	,Rule(5,'rule4', '60.212.128.1',   '0.0.0.0/0',  'allow', 'tcp')\
	]

conflicts_list = []

for i_index,i in enumerate(rules_list):
	
	for j_index,j in enumerate(rules_list):
		#j_index = index
		
		if i_index == j_index:
			print(' ')		
		else:
			#if i.notAssociate(j)
			print ('\n\ncomparing rule  ', i_index, ' and rule  ',j_index, '\n\n')
		

			print ('---~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-----|')
			print ('|            result analysis         |')
			print ('--------------------------------------')

			resl = i.detectConflict(j)
			print (resl.name)
			

#print ('There are ', len(rules_list), ' masked conflict')

mycoll = dbConn()
for i in rules_list:
	
	i.printRule()
	mycoll.insert_one(i.toJSON())



