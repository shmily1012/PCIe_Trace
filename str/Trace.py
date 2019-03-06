'''
Created on Mar 5, 2019

@author: Sasha
'''
import os.path
import sys
from Packet import Packet


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
        for line in self.buf[:500]:
#             print(line)
            if '_______|______________________________________________________________________' in line:
                boundary_list.append(line_number)
            line_number += 1
        id = 0
        while id < len(boundary_list) - 1:
            self.trace.append(self.translate(self.buf[boundary_list[id]: boundary_list[id + 1]]))
            print (boundary_list[id], boundary_list[id + 1])
            id += 1
#         print(boundary_list)

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
                print(line)
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
    t = Trace('Failure_trim_txt.txt')
    t.translate(t.buf[153: 160])
