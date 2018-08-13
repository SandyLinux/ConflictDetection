import pymongo

#setup the connection to mongodb
def dbConn():

    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
#get all the database names in the database 
    dblist = myClient.database_names()

#check if the collection RulesDB1 is in the database
    if "RulesDB1" in dblist:
	    print('the database exists')
	#if the collection exists, use it
	    mydb = myClient['RulesDB1']
	#check if the  collection/table PaloRules is in current database
	    if('PaloRules1' in mydb.list_collection_names()):
		    print ('the collection exist')
	    else:
		    print ('the collection does not exist')
    else:
	    print('db does not exist, creating a new database')
	    mydb = myClient['RulesDB1']
    
    mycol = mydb['PaloRules1']
    
#clear all records in the collection
    #mycol.remove({})

    results = mycol.find({})

    item_count = mycol.count_documents({})



    #print ('a = ', item_count)
    return mycol

def dbConn2():

    myClient = pymongo.MongoClient("mongodb://localhost:27017/")
#get all the database names in the database 
    dblist = myClient.database_names()

#check if the collection RulesDB1 is in the database
    if "RulesDB1" in dblist:
	    print('the database exists')
	#if the collection exists, use it
	    mydb = myClient['RulesDB1']
	#check if the  collection/table PaloRules is in current database
	    if('conflict' in mydb.list_collection_names()):
		    print ('the collection exist')
	    else:
		    print ('the collection does not exist')
    else:
	    print('db does not exist, creating a new database')
	    mydb = myClient['RulesDB1']
    
    mycol = mydb['conflict']
    mycol.remove({})
    
#clear all records in the collection
    #mycol.remove({})

    #results = mycol.find({})

    #item_count = mycol.count_documents({})



    #print ('a = ', item_count)
    return mycol
