from datetime import datetime, time

class DebugInfo(object):

    bShow = False
    bToLog = False
    sLogFile = '.\Log_{yyyy}{mm}{dd}.log'.format(yyyy=datetime.now().year, mm=str(datetime.now().month).zfill(2), dd=str(datetime.now().day).zfill(2))
    
    fLog = None
    sLogTAG = ''

    def __init__(self, sLogTAG, bShow=True, bToLog=True):
        self.bShow = bShow
        self.bToLog = bToLog
        
        if self.bToLog:
            self.sLogTAG = sLogTAG
            self.fLog = open(self.sLogFile, 'a')

    def Print(self, sMsg):
        if self.bShow:
            print(sMsg)

        if self.bToLog:
            sTime = '{hh}:{mm}:{ss}'.format(hh=str(datetime.now().hour).zfill(2), mm=str(datetime.now().minute).zfill(2), ss=str(datetime.now().second).zfill(2))
            self.fLog.writelines('{time} - {TAG}:\t{msg}'.format(time=sTime, TAG=self.sLogTAG, msg=sMsg))