'''
Created on Mar 6, 2019

@author: Chi.Zhang
'''


class NVMeCMD(object):
    '''
    classdocs
    '''

    def __init__(self, ID):
        '''
        Constructor
        '''
        self.ID = ID
        self.CQDoorbell = None
        self.SQDoorbell = None
        self.CQEntry = None
        self.SQEntry = None

    def addCQDoorbell(self, packet):
        self.CQDoorbell = packet

    def addSQDoorbell(self, packet):
        self.SQDoorbell = packet

    def addCQEntry(self, packet):
        self.CQEntry = packet


    def addSQEntry(self, packet):
        self.SQEntry = packet


    def caculateDelta(self):
        
        self.time2SQEntry = self.SQEntry.time - self.SQDoorbell.time
        self.time2CQEntry = self.CQEntry.time - self.SQDoorbell.time
        self.time2CQDoorbell = self.CQDoorbell.time - self.SQDoorbell.time

    def show(self):
        self.caculateDelta()
        print("********************************************")
        self.SQDoorbell.show()
        self.SQDoorbell.packet.show()
        self.SQEntry.show()
        self.SQEntry.packet.show()
        print("----| %.6fs" % (self.time2SQEntry / 1000000000))
        self.CQEntry.show()
        self.CQEntry.packet.show()
        print("----| %.6fs" % (self.time2CQEntry / 1000000000))
        self.CQDoorbell.show()
        self.CQDoorbell.packet.show()
        print("----| %.6fs" % (self.time2CQDoorbell / 1000000000))
        print("********************************************")
        

if __name__ == "__main__":

    ca = 0x100
    print('ca=0x%x' % ca)
#     CQ_address = {'high':0x0, 'low':0x1110}
#     SQ_address = {'high':0x0, 'low':0x11110}
#     if CQ_address == SQ_address:
#         print('good')
    pass
