from xml.dom.minidom import parse
import xml.dom.minidom
import ssl
import json
import xml.etree.ElementTree as ET
import urllib
from urllib.request import urlopen
from IPy import IP
from enum import Enum 
from collections import namedtuple
from enum import Enum,unique
#import cPickle as pickle

import json
import pymongo



ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = "https://10.10.140.134/api/?type=config&action=get&key=LUFRPT1mRHZuQUwxc3VNUFZmd2ZpNWpRMVRhU0hzZWM9ZGthOU0zRUlBM2ZmRXpLazhRaWt6Zz09&xpath=/config/predefined/application/entry[@name='hotmail']/references/entry[@name='Wikipedia']/link"
#url = "https://10.10.140.134/api/?type=config&action=get&key=LUFRPT1mRHZuQUwxc3VNUFZmd2ZpNWpRMVRhU0hzZWM9ZGthOU0zRUlBM2ZmRXpLazhRaWt6Zz09&xpath=/config/predefined/application/entry[@name='hotmail']"
#url = "https://10.10.140.144/api/?type=config&action=get&key=LUFRPT1mRHZuQUwxc3VNUFZmd2ZpNWpRMVRhU0hzZWM9ZGthOU0zRUlBM2ZmRXpLazhRaWt6Zz09&xpath=/config/devices/entry/vsys/entry/rulebase/security"
#url = "https://10.10.140.144/api/?1mRHZuQUwxc3VNUFZmd2ZpNWpRMVRhU0hzZWM9ZGthOU0zRUlBM2ZmRXpLazhRaWt6Zz09&xpath=/config/devices/entry/vsys/entry/rulebase/security"

url = "https://10.10.140.144/api/?type=keygen&user=sandy&password=cisco1234"

#https:///api/?type=config&action=get&Key=&xpath=/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/service

#print url
#response = urllib.urlopen(url)
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
        print('key is %s' % keys.childNodes[0].data)

        #print('rules is %s ' % rules.childNodes[0].data)

#entry_len = rules.getElementsByTagName('entry').length
