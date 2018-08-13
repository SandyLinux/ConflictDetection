from enum import Enum,unique
#define unique enum
@unique

class Relations(Enum):
	noCorrelation = 0
	subSet = 1
	equal = 2 
	superSet = 3
	correlation = 4
@unique
class conflictType(Enum):
	TBD = 100
	noConflict = 0
	
	masked = 1
	generalized  = 2
	correlation  = 3
	redundancy  = 4

#print (conflictAlertStatus.TBD.value)
