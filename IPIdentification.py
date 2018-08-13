from IPy import IP

class IPIdentification(object):
    def __init__(self,ip, port='any'):
        #self.index = index
        if ip =='any':
            ip = '0.0.0.0/0'
        self.ip = ip 
        # type is string, convert IP between string
        self.port = port
    
    def getIP(self):
        return self.ip
    
    def getPort(self):
        return self.port

    #if two IPIdentification objects have same ip address, 
    # they are regarded as the same/equal
    #input: ip2, IPIdentification object
    #output : boolean result 
    def isEqual(self,ip2):
        result = False
        #ip2 is a IPIdentification object

        if (self.ip == ip2.getIP()):
            result = True
        else:
            result = False
        return result

    #two IP objects are not correlction if they are not same AND they do not 
    #overlaps with each other
    #input: ip2, IPIdentificat
    #output : boolean result 

    def isCorrelation(self,ip2):
        result = False

        ipEqual = (self.ip == ip2.getIP())
            #convert string ip into IP object, and call overlaps to decide
            # overlap = 0, no overlaps
            # 1/ -1, they overlaps
        ipOverlaps = (IP(self.ip).overlaps(IP(ip2.getIP())))
        #print ('iseqaul = ', ipEqual, '   ipoverlaps = ', ipOverlaps)
        if( (ipEqual == False) and (ipOverlaps == 0)):
            result = False
        else:
            result = True
        return result 

    #compare two IPIdentification objects, and identify if ip1 is a subset of ip2

    def isSubset(self, ip2):
        result = False
            
        #unless ip1 differs ip2, and they have correlation
        #there is possibility that ip1 is a subset of ip2
        if ((self.isEqual(ip2) == False) and (self.isCorrelation(ip2) == True)):
           
            #if ip1 is in ip2, that means ip1 is ip2's subset
            inOrOut = (IP(self.ip) in IP(ip2.getIP()))
            
            if (inOrOut == True):
                #print ('in is true', inOrOut)
                result = True
            else:
                result = False
                #print ('is not in ',inOrOut)
        else:
            result = False

        return result

    def isSuperset(self, ip2):

        result = False
            
        #unless ip1 differs ip2, and they have correlation
        #there is possibility that ip1 is a superset of ip2
        if ((self.isEqual(ip2) == False) and (self.isCorrelation(ip2) == True)):
            inOrOut = (IP(self.ip) in IP(ip2.getIP()))
            #if ip1 is in ip2, that means ip1 is ip2's subset, not the superset

            if (inOrOut == False):
                result = True
            else:
                result = False
                #print ('in is true, ',inOrOut)
        else:
            result = False
        return result

#ip1 = IPIdentification(1,'10.10.0.0/24')

#ip2 = IPIdentification(1,'10.10.0.0/16')

#print(ip1.isEqual(ip2))
#print(ip1.isSuperset(ip2))