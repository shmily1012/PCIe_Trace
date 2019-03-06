'''
Created on Mar 5, 2019

@author: Sasha
'''


class Packet(object):
    '''
    classdocs
    '''
    ID = 0
    type = 'Link Tra'  # Link Tra or Split Tra
#     TLP_num = 0
    stream = None  # Downstream or Upstream
    Memory = {"Type":None,  # Read or Write
              "Bits":32}  # 32 or 64
    Length = 1
    RequestID = {'bus':0,
                 'device':0,
                 'function':0}
    Tag = 0
    Address = {'high':0x0, 'low':0x0}
    Data = []
    Time_stamp = 0  # ns

    def __init__(self, ID, type, stream, Memory, Length, RequestID, Tag, Address, Data, Time_stamp):
        '''
        Constructor
        '''
        self.ID = ID
        self.type = type
        self.stream = stream
        self.Memory = Memory
        self.Length = Length
        self.RequestID = RequestID
        self.Tag = Tag
        self.Address = Address
        self.Data = Data
        self.Time_stamp = Time_stamp
    
        self.show()

    def show(self):
        print('ID =', self.ID)
        print('type =', self.type)
        print('stream =', self.stream)
        print('Memory.Type =', self.Memory['Type'])
        print('Memory.Bits =', self.Memory['Bits'])
        print('Length =', self.Length)
        print('RequestId =', self.RequestID)
        print('Tag =', self.Tag)
        if self.Address['high'] == 0x0:
            print('Address = 0x%x' % self.Address['low'])
        else:
            print('Address = 0x%x %x' % (self.Address['high'], self.Address['low']))
        str = ''
        for d in self.Data:
            str += '0x%x\t' % d
        print('Data =[%s]' % str)
        print('Time_stamp =', self.Time_stamp)
