'''
Created on Mar 6, 2019

@author: Chi.Zhang
'''


class CQEntry(object):
    '''
    classdocs
    '''

    def __init__(self, Qid, status, cid, sqid, time, address, packet, type="CQ Entry"):
        '''
        Constructor
        '''
        self.type = type
        self.Qid = Qid
        self.status = status
        self.cid = cid
        self.address = address
        self.time = time
        self.packet = packet

    def show(self):
        print('type=', self.type)
        print('CQid=0x%x' % self.Qid)
        print('cid=0x%x' % self.cid)
        print('status=0x%x' % self.status)
        print("address[high]=0x%X" % self.address['high'])
        print("address[low]=0x%8X" % self.address['low'])
        print('time=', self.time)
        print('%s - %d' % (self.packet.type, self.packet.ID))


class SQEntry(object):
    
    def __init__(self, Qid, cid, cmdcode, address , time, packet, PRP1=0x0, PRP2=0x0, type="SQ Entry"):
        self.type = type
        self.Qid = Qid
        self.cid = cid
        self.cmdcode = cmdcode
        self.PRP1 = PRP1
        self.PRP2 = PRP2
        self.address = address
        self.time = time
        self.packet = packet

    def show(self):
        print('type=', self.type)
        print('SQid=0x%x' % self.Qid)
        print('cid=0x%x' % self.cid)
        print('cmdcode=0x%x' % self.cmdcode)
        print("address[high]=0x%X" % self.address['high'])
        print("address[low]=0x%8X" % self.address['low'])
        print('time=', self.time)
        print('%s - %d' % (self.packet.type, self.packet.ID))

        
class SQDoorbell(object):

    def __init__(self, Qid, DoorbellValue, address, time, packet, type="SQ Doorbell"):
        self.type = type
        self.Qid = Qid
        self.DoorbellValue = DoorbellValue
        self.address = address
        self.time = time
        self.packet = packet

    def show(self):
        print('type=', self.type)
        print('SQid=0x%x' % self.Qid)
        print('DoorbellValue=0x%x' % self.DoorbellValue)
        print("address[high]=0x%X" % self.address['high'])
        print("address[low]=0x%8X" % self.address['low'])
        print('time=', self.time)
        print('%s - %d' % (self.packet.type, self.packet.ID))


class CQDoorbell(object):

    def __init__(self, Qid, DoorbellValue, address, time, packet, type="CQ Doorbell"):
        self.type = type
        self.Qid = Qid
        self.DoorbellValue = DoorbellValue
        self.address = address
        self.time = time
        self.packet = packet

    def show(self):
        print('type=', self.type)
        print('CQid=0x%x' % self.Qid)
        print('DoorbellValue=0x%x' % self.DoorbellValue)
        print("address[high]=0x%X" % self.address['high'])
        print("address[low]=0x%8X" % self.address['low'])
        print('time=', self.time)
        print('%s - %d' % (self.packet.type, self.packet.ID))
