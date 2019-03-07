'''
Created on Mar 6, 2019

@author: Chi.Zhang
'''


class CQEntry(object):
    '''
    classdocs
    '''

    def __init__(self, Qid, status, cid, sqid, time, address, type="CQ Entry"):
        '''
        Constructor
        '''
        self.type = type
        self.Qid = Qid
        self.status = status
        self.cid = cid
        self.address = address
        self.time = time

    def show(self):
        print('type=', self.type)
        print('Qid=', self.Qid)
        print('cid=', self.cid)
        print('status=', self.status)
        print("address[high]=0x%X" % self.address['high'])
        print("address[low]=0x%8X" % self.address['low'])
        print('time=', self.time)


class SQEntry(object):
    
    def __init__(self, Qid, cid, cmdcode, address , time, PRP1=0x0, PRP2=0x0, type="SQ Entry"):
        self.type = type
        self.Qid = Qid
        self.cid = cid
        self.cmdcode = cmdcode
        self.PRP1 = PRP1
        self.PRP2 = PRP2
        self.address = address
        self.time = time

    def show(self):
        print('type=', self.type)
        print('Qid=', self.Qid)
        print('cid=', self.cid)
        print('cmdcode=', self.cmdcode)
        print("address[high]=0x%X" % self.address['high'])
        print("address[low]=0x%8X" % self.address['low'])
        print('time=', self.time)

        
class SQDoorbell(object):

    def __init__(self, Qid, DoorbellValue, address, time, type="SQ Doorbell"):
        self.type = type
        self.Qid = Qid
        self.DoorbellValue = DoorbellValue
        self.address = address
        self.time = time

    def show(self):
        print('type=', self.type)
        print('Qid=', self.Qid)
        print('DoorbellValue=', self.DoorbellValue)
        print("address[high]=0x%X" % self.address['high'])
        print("address[low]=0x%8X" % self.address['low'])
        print('time=', self.time)


class CQDoorbell(object):

    def __init__(self, Qid, DoorbellValue, address, time, type="CQ Doorbell"):
        self.type = type
        self.Qid = Qid
        self.DoorbellValue = DoorbellValue
        self.address = address
        self.time = time

    def show(self):
        print('type=', self.type)
        print('Qid=', self.Qid)
        print('DoorbellValue=', self.DoorbellValue)
        print("address[high]=0x%X" % self.address['high'])
        print("address[low]=0x%8X" % self.address['low'])
        print('time=', self.time)
