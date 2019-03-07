'''
Created on Mar 5, 2019

@author: Sasha
'''
import os.path
import sys
from Packet import Packet
from Queue import Queue
from NVMe import NVMe
from NVMeCMD import NVMeCMD


class Trace(object):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.trace = list()
        self.filename = "../Trace_Files/%s" % filename
        if os.path.exists(self.filename) == False:
            print('The file, %s, does not exist.' % filename)
            sys.exit()

        fo = open(self.filename, 'r')
        self.buf = fo.readlines()
        fo.close()
        boundary_list = list()
        line_number = 0
#         for line in self.buf[:500]:  # for Test
        for line in self.buf:
#             print(line)
            if '_______|______________________________________________________________________' in line:
                boundary_list.append(line_number)
            line_number += 1
        id = 0
        while id < len(boundary_list) - 1:
            self.trace.append(self.translate(self.buf[boundary_list[id]: boundary_list[id + 1]]))
#             print (boundary_list[id], boundary_list[id + 1])
            id += 1
#         p = self.translate(self.buf[boundary_list[id - 1]: boundary_list[id]])
#         p.show()
#         sys.exit()
#         self.nvme = NVMe()
#         for item in self.trace:
#             item.show()
    
    def translate(self, buf):
        for line in buf:
#             print(line)
            if 'Link Tra' in line:
                type = 'Link Tra'
                start = line.index('Link Tra(') + len('Link Tra(')
                end = line.index(')', start + 1)
                ID = int(line[start:end], 10) 
            elif 'Split Tra' in line:
                type = 'Split tra'
                start = line.index('Split Tra(') + len('Split Tra(')
                end = line.index(')', start + 1)
                ID = int(line[start:end], 10) 
            if 'Upstream' in line:
                stream = 'Upstream'
            elif 'Downstream' in line:
                stream = 'Downstream'
            if 'Mem MWr(' in line:
                Memory = {"Type":'Write', 'Bits':0}
                start = line.index('Mem MWr(') + len('Mem MWr(')
                end = line.index(')', start + 1)
                Memory['Bits'] = int(line[start:end], 10) 
#                 print(Memory)
            elif 'Mem MRd(' in line:
                Memory = {"Type":'Read', 'Bits':0}
                start = line.index('Mem MRd(') + len('Mem MRd(')
                end = line.index(')', start + 1)
                Memory['Bits'] = int(line[start:end], 10) 
#                 print(Memory)
            if 'Length' in line:
                start = line.index('Length(') + len('Length(')
                end = line.index(')', start + 1)
                Length = int(line[start:end], 10) 
            if 'RequesterID(' in line:
                RequestID = {'bus':0,
                 'device':0,
                 'function':0}
                start = line.index('RequesterID(') + len('RequesterID(')
                end = line.index(')', start + 1)
                RequesterID_str = line[start:end]
                temp = RequesterID_str.split(':')
                RequestID['bus'] = int(temp[0], 10) 
                RequestID['device'] = int(temp[1], 10)
                RequestID['function'] = int(temp[2], 10)
#                 print(RequestID)
            if 'Tag(' in line:
                start = line.index('Tag(') + len('Tag(')
                end = line.index(')', start + 1)
                Tag = int(line[start:end], 10)
            if 'Address(' in line:
                
                Address = {'high':0x0, 'low':0x0}
                start = line.index('Address(') + len('Address(')
                end = line.index(')', start + 1)
                Address_str = line[start:end]
                if ':' in Address_str:
                    temp = Address_str.split(':')
                    Address['high'] = int(temp[0], 16)
                    Address['low'] = int(temp[1], 16)
                else:
                    Address['low'] = int(Address_str, 16)
            if 'Data(' in line:
#                 print(line)
                Data = []
                start = line.index('Data(') + len('Data(')
                try:
                    end = line.index(')', start + 1)
                except ValueError:
                    Length = 16  # TODO: Error Handling
                else:
                    Data_str = line[start:end]
                    if ' ' in Data_str:
                        temp = Data_str.split(' ')
                        for d in temp:
                            Data.append(int(d, 16))
                    else:
                        Data.append(int(Data_str, 16))
#                 print(Data)
            if '__ 0:' in line:
                temp = line.split(' ')
                for i in temp[2:]:
#                     if '\n' in i:                    
#                         Data.append(int(i[:-1], 16))
#                     else:
#                         Data.append(int(i, 16))
#                     i = i.replace('\n', '')
#                     print(i)
                    if i != '\n':
                        Data.append(int(i, 16))
                continue
            elif '__ 8:' in line:
                temp = line[:-1].split(' ')
                for i in temp[2:]:
#                     if '\n' in i:                    
#                         Data.append(int(i[:-1], 16))
#                     else:
#                         Data.append(int(i, 16))
                        
                    i = i.replace(')', '')
                    Data.append(int(i, 16))
                continue
            if 'Time Stamp(' in line:
                Time_stamp = 0
                start = line.index('Time Stamp(') + len('Time Stamp(')
                end = line.index(')', start + 1)
                Time_stamp_str = line[start:end]
                if Time_stamp_str.endswith('s'):
                    temp = Time_stamp_str.split('.')
                    sec = int(temp[0], 10)
                    nano_sec = int(temp[1][:-1], 10) / 1000
                    Time_stamp = sec * 1000 * 1000 * 1000 + nano_sec
#                 print('Time_stamp=', Time_stamp)
        p = Packet(ID=ID,
                   type=type,
                   stream=stream,
                   Memory=Memory,
                   Length=Length,
                   RequestID=RequestID,
                   Tag=Tag,
                   Address=Address,
                   Data=Data,
                   Time_stamp=Time_stamp)
        return p

                
if __name__ == "__main__":
    nvme_cmd_list = list()
    nvme_list = list()
    t = Trace('Failure_trim_txt.txt')
#     t.translate(t.buf[153: 160])
    nvme = NVMe()
    for p in t.trace:
        if nvme.CollectCQDoorbell(p):
            item = nvme.CollectCQDoorbell(p)
            pass
        elif nvme.CollectSQDoorbell(p):
            item = nvme.CollectSQDoorbell(p)
            pass
        elif nvme.CollectCQEntry(p):
            item = nvme.CollectCQEntry(p)
            pass
        elif nvme.CollectSQEntry(p):
            item = nvme.CollectSQEntry(p)
            pass
#         else:
#             pass
        nvme_list.append(item)
    count = 0
    while len(nvme_list):
        print(len(nvme_list))
        cqdoorbell = None
        cqentry = None
        sqentry = None
        sqdoorbell = None
        
        packet = nvme_list.pop()
        nvmecmd = NVMeCMD(count)
        count += 1
        if packet.type != "CQ Doorbell":
            continue
        # Find last CQ Doorbell 
        cqdoorbell = packet
#         packet.show()
#         sys.exit()
        nvmecmd.addCQDoorbell(cqdoorbell)
        id = len(nvme_list) - 1
#         print('cqdoorbell.Qid=', cqdoorbell.Qid)
#         print('nvme.CQEntryBaseAddressArray=', nvme.CQEntryBaseAddressArray)
        CQ_address = {'high':0x0, 'low':0x0}
        if cqdoorbell.DoorbellValue == 0x0:
            CQ_address['low'] = (0x10 * nvme.CQSizeArray[cqdoorbell.Qid]) + nvme.CQEntryBaseAddressArray[cqdoorbell.Qid]['low']
        else:
            CQ_address['low'] = 0x10 * (cqdoorbell.DoorbellValue - 0x1) + nvme.CQEntryBaseAddressArray[cqdoorbell.Qid]['low']
        CQ_address['high'] = nvme.CQEntryBaseAddressArray[cqdoorbell.Qid]['high']
#         print ('CQ_address=0x%x 0x%x' % (CQ_address['high'], CQ_address['low']))

        # Find Match CQ Entry
#         for item in nvme_list[::-1]:
        while id > 0:
#             print('item.type=', nvme_list[id].type)
#             print('item.address=0x%x 0x%x' % (nvme_list[id].address['high'],
#                                               nvme_list[id].address['low']))
            if nvme_list[id].type == 'CQ Entry':
                if CQ_address == nvme_list[id].address:
                    cqentry = nvme_list[id]
                    nvmecmd.addCQEntry(cqentry)
                    nvme_list.pop(id)
                    id -= 1
                    break
            id -= 1
        if nvmecmd.CQEntry == None:
            print("Cannot FIND CQ Entry which matches with CQ Doorbell [qid=%x DoorbellValue=0x%x]" % (cqdoorbell.Qid, cqdoorbell.DoorbellValue))
            cqdoorbell.show()
#             sys.exit()
            continue
#             break
        # Find Match SQ Entry
#         for item in nvme_list[:id:-1]:
        while id > 0:
#             print('id=', id)
            if nvme_list[id].type == 'SQ Entry' :
                if nvme_list[id].Qid == cqentry.Qid and nvme_list[id].cid == cqentry.cid:
                    sqentry = nvme_list[id]
                    nvmecmd.addSQEntry(sqentry)
                    nvme_list.pop(id)
                    id -= 1
                    break
            id -= 1
        if nvmecmd.SQEntry == None:
            print("Cannot FIND SQ Entry which matches with CQ Entry [qid=%x cid=0x%x]" % (cqentry.Qid, cqentry.cid))
            cqentry.show()
#             sys.exit()
            continue
        
        # Find Match SQ Doorbell
        SQ_doorbell_value = 0x1 + ((sqentry.address['low'] - nvme.SQEntryBaseAddressArray[sqentry.Qid]['low']) / 0x40)
        if SQ_doorbell_value == (nvme.SQSizeArray[sqentry.Qid] + 1):
            SQ_doorbell_value = 0
#         print('sqentry.address[low]=0x%x' % sqentry.address['low'])
#         print('nvme.SQEntryBaseAddressArray[sqentry.Qid][low]=0x%x' % nvme.SQEntryBaseAddressArray[sqentry.Qid]['low'])
#         print ('SQ_doorbell_value=', SQ_doorbell_value)
#         for item in nvme_list[:id:-1]:
        while id > 0:
            if nvme_list[id].type == 'SQ Doorbell':
#                 print ('nvme_list[id].DoorbellValue=', nvme_list[id].DoorbellValue)
                if nvme_list[id].DoorbellValue == SQ_doorbell_value:
                    sqdoorbell = nvme_list[id]
                    nvmecmd.addSQDoorbell(sqdoorbell)
                    nvme_list.pop(id)
                    id -= 1
                    break
            id -= 1
        if nvmecmd.SQDoorbell == None:
            print("Cannot FIND SQ Doorbell which matches with SQ Entry [qid=%x cid=0x%x]" % (sqentry.Qid, sqentry.cid))
            sqentry.show()
#             sys.exit()
            continue
        nvmecmd.caculateDelta()
#         nvmecmd.show()
        nvme_cmd_list.append(nvmecmd)
#         sys.exit()
    duration_array = list()
    for nvme_cmd in nvme_cmd_list:
        duration_array.append(nvme_cmd.time2CQEntry)
    MAX_duration = max(duration_array)
    print('MAX_duration = %ds' % MAX_duration)
