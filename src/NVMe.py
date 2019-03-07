'''
Created on Mar 6, 2019

@author: Chi.Zhang
'''
import os.path
import sys
from Packet import Packet
from Queue import Queue
from NVMe_Packet import CQEntry
from NVMe_Packet import SQEntry
from NVMe_Packet import CQDoorbell
from NVMe_Packet import SQDoorbell
from email._header_value_parser import Address

#########################################################
MAX_QUEUE_NUM = 16


#########################################################
class NVMe(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''        
        self.CollectNVMeInfo('NVMe.xml')
        self.SQEntryBaseAddressArray = list()
        self.CQEntryBaseAddressArray = list()
        self.SQSizeArray = list()
        self.CQSizeArray = list()
        self.CollectQueueInfo()
#         sys.exit()
        
    def show(self):
        print('*******************************************')
        print('SQ Doorbell')
        self.SQDoorbell.show()
        print('SQ Entry')
        self.SQEntry.show()
        print('CQ Entry')
        self.CQEntry.show()
        print('CQ Doorbell')
        self.CQDoorbell.show()
        print('*******************************************')

    def CollectQueueInfo(self):
        for i in range(MAX_QUEUE_NUM):
            address = {'low':0x0, 'high':0x0}
            self.SQEntryBaseAddressArray.append(address)
            self.CQEntryBaseAddressArray.append(address)
            self.SQSizeArray.append(0)
            self.CQSizeArray.append(0)
        
        for i in range(MAX_QUEUE_NUM):
            for Q in self.Queue_info:
#                 print (Q.Type, Q.Qid)
                if 'SQ' in Q.Type and Q.Qid == i:
                    self.SQEntryBaseAddressArray[i] = Q.Address
                elif 'CQ' in Q.Type and Q.Qid == i:
                    self.CQEntryBaseAddressArray[i] = Q.Address
        for i in range(MAX_QUEUE_NUM):
            for Q in self.Queue_info:
#                 print(Q.Size)
                if 'SQ' in Q.Type and Q.Qid == i:
                    self.SQSizeArray[i] = Q.Size
                elif 'CQ' in Q.Type and Q.Qid == i:
                    self.CQSizeArray[i] = Q.Size 
#         for i in self.SQSizeArray:
#             print(i)
#         for i in self.CQSizeArray:
#             print(i)
#         pass
    
    def CollectNVMeInfo(self, filename):
        self.Queue_info = list()
        Config_filename = '../Trace_Files/%s' % filename
        if os.path.exists(Config_filename) == False:
            print("There is no Config file exists.")
            sys.exit()
        else:
            fo = open(Config_filename, 'r')
            buf = fo.readlines()
            for line in buf:
                if '<Queue TYPE=' in line:
                    start = line.index(r'TYPE="') + len(r'TYPE="')
                    end = line.index(r'"', start + 1)
                    Type = line[start:end]
                    start = line.index(r'SIZE="') + len(r'SIZE="')
                    end = line.index(r'"', start + 1)
                    Size = int(line[start: end], 10)
                    start = line.index(r'ADDRESS="') + len(r'ADDRESS="')
                    end = line.index(r'"', start + 1)
                    Address = int(line[start: end], 16)
                    start = line.index(r'QID="') + len(r'QID="')
                    end = line.index(r'"', start + 1)
                    Qid = int(line[start: end], 10)
                    q = Queue(Type, Size, Address, Qid)
                    self.Queue_info.append(q)
#                     q.show()
                elif r'<MBAR ID="0"' in line:
                    start = line.index(r'VALUE="') + len(r'VALUE="')
                    end = line.index(r'"', start + 1)
                    BAR0 = int(line[start:end], 16)
                    self.BAR0 = {'high':BAR0 >> 32, 'low':BAR0 & 0xFFFFFFFF}
                elif r'DSTRD="' in line:
                    start = line.index(r'DSTRD="') + len(r'DSTRD="')
                    end = line.index(r'"', start + 1)
                    self.DSTRD = int(line[start:end], 10)

    def CombineNVMe(self):
        
        pass

    def CollectSQDoorbell(self, packet):
        if packet.Length != 1:
            return False
        if packet.Address['high'] != self.BAR0['high']:
            return False
        for qid in range(MAX_QUEUE_NUM):
            if packet.Address['low'] == self.BAR0['low'] + 0x1000 + self.DSTRD * 2 * qid:
#                 print('This is SQ Doorbell. QID=', qid)
#                 packet.show()
                nvme_packet = SQDoorbell(Qid=qid,
                                         DoorbellValue=packet.Data[0],
                                         address=packet.Address,
                                          time=packet.Time_stamp,
                                          packet=packet)
                return nvme_packet
        return False    

    def CollectCQDoorbell(self, packet):
        if packet.Length != 1:
            return False
        if packet.Address['high'] != self.BAR0['high']:
            return False
        for qid in range(MAX_QUEUE_NUM):
            if packet.Address['low'] == self.BAR0['low'] + 0x1008 + self.DSTRD * 2 * qid:
#                 print('This is CQ Doorbell. QID=', qid)
#                 packet.show()
                nvme_packet = CQDoorbell(Qid=qid,
                                         DoorbellValue=packet.Data[0],
                                         address=packet.Address,
                                          time=packet.Time_stamp,
                                          packet=packet)
                return nvme_packet
        return False

    def CollectSQEntry(self, packet):
        if packet.Length != 16:
            return False
        
        for q in self.Queue_info:
            if packet.Address['low'] & q.MASK == q.Address['low']:
                if 'SQ' in q.Type:
#                     print('This is SQ Entry. QID=', q.Qid)
#                     packet.show()
                    cid = packet.Data[0] >> 16
                    cmdcode = packet.Data[0] & 0xFF
                    nvme_packet = SQEntry(Qid=q.Qid,
                                          cid=cid,
                                          cmdcode=cmdcode,
                                          address=packet.Address,
                                          time=packet.Time_stamp,
                                          packet=packet)
                    return nvme_packet
        return False

    def CollectCQEntry(self, packet):
        if packet.Length != 4:
            return False
        
        for q in self.Queue_info:
            if packet.Address['low'] & q.MASK == q.Address['low']:
                if 'CQ' in q.Type:
#                     print('This is CQ Entry. QID=', q.Qid)
#                     packet.show()
                    status = packet.Data[3] >> 17
                    cid = packet.Data[3] & 0xFFFF
                    sqid = packet.Data[2] >> 16
                    nvme_packet = CQEntry(Qid=q.Qid, cid=cid, status=status, sqid=sqid,
                                          address=packet.Address,
                                          time=packet.Time_stamp,
                                          packet=packet)
                    return nvme_packet
        return False


if __name__ == "__main__":
    nvme = NVMe()

