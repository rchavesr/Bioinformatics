import os
import mysql.connector as mariadb

class dbConn(object):
    """description of class"""

    ID_READY        = 'Ready'
    ID_READY_COD    = '0'
    ID_RUNNING      = 'Running'
    ID_RUNNING_COD  = '1'
    ID_PAUSED       = 'Paused'
    ID_PAUSED_COD   = '2'
    ID_FINISHED     = 'Finished'
    ID_FINISHED_COD = '3'

    hostname = 'localhost'
    username = 'rchaves'
    password = '123000'
    database = 'bioinformatics'

    def __init__(self):
        self.dbconn = mariadb.connect( host=self.hostname, user=self.username, passwd=self.password, db=self.database )
        print('conectat')

        self.UpdateDB()

    
    def UpdateDB(self):
        # Actualitza la taula genoma
        self.UpdGenoma()

        # Crea les noves tasques:
        self.UpdAnalysis()


    # Revisa els nous genomes i estableix la seva longitud.
    def UpdGenoma(self):
        cursor = self.dbconn.cursor()
        sQuery = "SELECT idGenoma, sPath FROM genoma WHERE nLen=-1"
        cursor.execute(sQuery)

        for row in list(cursor):
            idGen = row[0]
            lenFile = os.stat(row[1]).st_size
            print('File ' + row[1] + ' long is: ' + str(lenFile))
            sQueryUPD = "UPDATE genoma SET nLen={parLen} WHERE idGenoma={parIdGen}".format(parLen=lenFile, parIdGen=idGen)
            cursor.execute(sQueryUPD)
            self.dbconn.commit()
        cursor.close()


    # Revisa les tasques noves i les afegeix a les execucions 'Ready'.    
    def UpdAnalysis(self):
        cursor = self.dbconn.cursor()
        sQuery = "SELECT idAnalysis FROM analysis WHERE bActive=1 and idAnalysis NOT IN (SELECT idAnalysis FROM execution)"
        cursor.execute(sQuery)

        for row in list(cursor):
            sQueryINS = "INSERT INTO execution(idAnalysis, idStatus) VALUES ({idAnalysis}, {idStatus})".format(idAnalysis=row[0], idStatus=self.ID_READY_COD)
            cursor.execute(sQueryINS)
            self.dbconn.commit()
        cursor.close()


    # Retorna un diccionari on cada Key correspón als diferents status del anàlisis [Ready, Running, Paused, Finished]
    # idChallenge
    def GetAnalysisByStatus(self, idChallenge):

        dicTasks = {}

        cursor = self.dbconn.cursor()
        sQuery = "SELECT idStatus, sStatus FROM executionstatus"
        cursor.execute(sQuery)
       
        for row in list(cursor):
            # Desc
            sKey = row[1]
            # Code
            sQuery = "SELECT idAnalysis FROM Execution WHERE idStatus = {status} and idAnalysis IN (SELECT idAnalysis FROM analysis WHERE idChallenge={challenge})".format(status=str(row[0]), challenge=idChallenge) 
            cursor.execute(sQuery)
            aAnalysis = []
            for rowExecution in list(cursor):
                aAnalysis.append(rowExecution[0])
            dicTasks[sKey] = aAnalysis
        cursor.close()

        return dicTasks

    # In: [IdAnalysis]
    # Out:
    #   - sPathGen      (genoma)
    #   - lenGen        (genoma)
    #   - lenPattern    (analysis)
    #   - nCurrPos      (execution)
    
    def GetInfo4ClumpFindingProblemOpt(self, idAnalysis):
        cursor = self.dbconn.cursor()
        sQuery = "SELECT lenPattern FROM analysis WHERE idAnalysis={analysis}".format(analysis=idAnalysis)
        cursor.execute(sQuery)
        for row in list(cursor):
            lenPattern = row[0]
                
        sQuery = "SELECT idGenoma, nCurrPos FROM execution WHERE idAnalysis={analysis}".format(analysis=idAnalysis)
        cursor.execute(sQuery)
        for row in list(cursor):
            idGenoma = row[0]
            nCurrPos = row[1]

        sQuery = "SELECT sPath, nLen FROM genoma WHERE idGenoma={gen}".format(gen=idGenoma)
        cursor.execute(sQuery)
        for row in list(cursor):
            sPathGen = row[0]
            lenGen = row[1]

        return sPathGen, lenGen, lenPattern, nCurrPos

