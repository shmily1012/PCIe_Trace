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

    def show(self):
        print("********************************************")
        self.SQDoorbell.show()
        self.SQDoorbell.show()
        self.CQEntry.show()
        self.CQDoorbell.show()
        print("********************************************")
        

if __name__ == "__main__":

    ca = 0x100
    print('ca=0x%x' % ca)
#     CQ_address = {'high':0x0, 'low':0x1110}
#     SQ_address = {'high':0x0, 'low':0x11110}
#     if CQ_address == SQ_address:
#         print('good')
    pass
