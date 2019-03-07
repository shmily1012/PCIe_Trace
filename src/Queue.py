'''
Created on Mar 6, 2019

@author: Chi.Zhang
'''


class Queue(object):
    '''
    classdocs
    '''

    def __init__(self, Type, Size, Address, Qid):
        '''
        Constructor
        '''
        self.Type = Type
        self.Size = Size
        self.Address = {'high':Address >> 32, 'low':Address & 0xFFFFFFFF}
        self.Qid = Qid
        if 'SQ' in self.Type:
            memory_size = 0x40 * (self.Size + 1)
        elif 'CQ' in self.Type:
            memory_size = 0x10 * (self.Size + 1)
        bit = 0
        while True:
            if memory_size == 1:
                break
            memory_size = memory_size >> 1
            bit += 1
#         print ('bit=', bit)
        mask = 0xFFFFFFFF
        mask2 = (mask << bit) & mask
#         print('%x' % mask2)
        self.MASK = mask2

    def show(self):
        print('Type=', self.Type)
        print('Size=', self.Size)
        print('Address=[0x%8x 0x%8x]' % (self.Address['high'], self.Address['low']))
        print('Qid=', self.Qid)
