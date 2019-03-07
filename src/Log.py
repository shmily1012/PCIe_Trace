'''
Created on Mar 7, 2019

@author: Chi.Zhang
'''
from time import gmtime, strftime
import time


class Log(object):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        timestamp = strftime("%d-%b-%Y-%H-%M-%S", gmtime())
        if '.' in filename:
            temp = filename.split('.')
            self.filename = '../Log/%s-%s.csv' % (temp[0], timestamp)
        else:
            self.filename = '../Log/%s-%s.csv' % (filename, timestamp)
    
    def LogNVMeCMD(self, nvme_cmd_list, limit):
        fi = open(self.filename, 'w')
        fi.write('ID, SQ Doorbell, TIME, SQ Entry, TIME, CQ Entry, TIME, CQ Doorbell, TIME,\n')
        fi.close()
        for nvme_cmd in nvme_cmd_list:
            if nvme_cmd.time2CQDoorbell / 1000000000 > limit:
                try:
                    fi = open(self.filename, 'a')
                except PermissionError:
                    fi.close()
                    time.sleep(1)
                    fi = open(self.filename, 'a')
                else:
                    pass
                str = '%d,%s-%d,%.6f,%s-%d,%.6f,%s-%d,%.6f,%s-%d,%.6f\n' % (nvme_cmd.ID,
                                                                           nvme_cmd.SQDoorbell.packet.type,
                                                                           nvme_cmd.SQDoorbell.packet.ID,
                                                                           0,
                                                                           nvme_cmd.SQEntry.packet.type,
                                                                           nvme_cmd.SQEntry.packet.ID,
                                                                           nvme_cmd.time2SQEntry / 1000000000,
                                                                           nvme_cmd.CQEntry.packet.type,
                                                                           nvme_cmd.CQEntry.packet.ID,
                                                                           nvme_cmd.time2CQEntry / 1000000000,
                                                                           nvme_cmd.CQDoorbell.packet.type,
                                                                           nvme_cmd.CQDoorbell.packet.ID,
                                                                           nvme_cmd.time2CQDoorbell / 1000000000,)
                fi.write(str)
                fi.close()
