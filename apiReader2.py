from xml.dom.minidom import parse
import xml.dom.minidom
import ssl
import json
import xml.etree.ElementTree as ET
import urllib
from urllib.request import urlopen
from IPy import IP
import pymongo
import json
from rule import Rule
from  dbConn import *
#import test2

def  function1():
    while True:
        try:
            nb = input('choose a ip number:')
            ips = IP(nb)
            break
        except ValueError:
            print ('invalid ip format')


    print ('get the ips ', ips.strNormal(1))


    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE


    urlhead = "https://" + ips.strNormal(1)

    url = urlhead +"/api/?type=keygen&user=sandy&password=cisco1234"

    response = urllib.request.urlopen(url,context=ctx)

    DOMTree = xml.dom.minidom.parse(response)

    response = DOMTree.documentElement



    #setup the connection to mongodb

    if response.hasAttribute('status'):

            print ("Root element :%s" % response.getAttribute('status'))

    results = response.getElementsByTagName('result')



    for result in results:
            keys = result.getElementsByTagName('key')[0]

            # do not delete the line below

            str = 'key is ----' + keys.childNodes[0].data
    print (str)

    url = urlhead + "/api/?type=config&action=get&key=" + keys.childNodes[0].data  + "&xpath=/config/devices/entry/vsys/entry/rulebase/security"

    #url = "https://10.10.140.134/api/?type=config&action=get&key=LUFRPT1mRHZuQUwxc3VNUFZmd2ZpNWpRMVRhU0hzZWM9ZGthOU0zRUlBM2ZmRXpLazhRaWt6Zz09&xpath=/config/predefined/application/entry[@name='hotmail']/references/entry[@name='Wikipedia']/link"
    #url = "https://10.10.140.134/api/?type=config&action=get&key=LUFRPT1mRHZuQUwxc3VNUFZmd2ZpNWpRMVRhU0hzZWM9ZGthOU0zRUlBM2ZmRXpLazhRaWt6Zz09&xpath=/config/predefined/application/entry[@name='hotmail']"
    #url = "https://10.10.140.144/api/?type=config&action=get&key=LUFRPT1mRHZuQUwxc3VNUFZmd2ZpNWpRMVRhU0hzZWM9ZGthOU0zRUlBM2ZmRXpLazhRaWt6Zz09&xpath=/config/devices/entry/vsys/entry/rulebase/security"

    #https:///api/?type=config&action=get&Key=&xpath=/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/service

    response = urllib.request.urlopen(url,context=ctx)


    rules_list = []
    #count = 0

    DOMTree = xml.dom.minidom.parse(response)
    response = DOMTree.documentElement

    #read the xml file from firewall

    if response.hasAttribute('status'):
        print ("Root element :%s" % response.getAttribute('status'))
        
    results = response.getElementsByTagName('result')

    for result in results:
        security = result.getElementsByTagName('security')[0]
        # do not delete the line below
        #print('security is %s' % security.childNodes[0].data)

        rules = security.getElementsByTagName('rules')[0]
        # do not delete the line below
        #print('rules is %s ' % rules.childNodes[0].data)

    entry_len = rules.getElementsByTagName('entry').length

    #declare a list to save all the rule objects
    rules_list=[]
    #iteration by which every firewall rule is saved in the database
    #put all rule objects into a list 

    #setup a 
    mycoll = dbConn()

    #clean up the table of previous firewall rule 
    mycoll.delete_many({})

    for index in range(entry_len):
        entry = rules.getElementsByTagName('entry')[index]
        entry_name = entry.getAttribute('name')
        
        #get the data of member of group
        #get the data of source 
        source_data = entry.getElementsByTagName('source')[0]
        member = source_data.getElementsByTagName('member')[0]
        source = member.childNodes[0].data
        
        #get the data of destination 
        destination_data = entry.getElementsByTagName('destination')[0]
        member = destination_data.getElementsByTagName('member')[0]
        dest = member.childNodes[0].data
        
        #get the data of action
        action_data = entry.getElementsByTagName('action')[0]
        action = action_data.childNodes[0].data
        
        protocol = ''
        if protocol =='':
            #if protocol is not defined in firewall, use its default value tcp
            r = Rule(index, entry_name, source, dest, action)
        else:
            #if protocol is defined in firewall rule
            r = Rule(index, entry_name, source, dest, action, protocol)

        #save class into database
        mycoll.insert_one(r.toJSON())
        #add current rule object into the list
        rules_list.append(r)
        
    return rules_list
