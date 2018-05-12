from multiprocessing import process
from db import dbConn
from Patterns import ADN
from _01_Replication_Begins import ReplicationBegins


# Challenges:
ID_CHALLENGE_ClumpFindingProblemOpt = 0

if __name__ == "__main__":


    if False:
        oConn = dbConn()
        dicTasks = oConn.GetAnalysisByStatus(ID_CHALLENGE_ClumpFindingProblemOpt)
        if oConn.ID_READY in dicTasks:
            aAnalysisReady = dicTasks[oConn.ID_READY]
            print(aAnalysisReady)

            for itAnalysis in aAnalysisReady:
                sPathGen, lenGen, lenPattern, nCurrPos = oConn.GetInfo4ClumpFindingProblemOpt(itAnalysis)
                oPatterns = Patterns()
                #ClumpFindingProblemOpt
                #---> Cridar a la funció






    if True:
        #oADN = ADN('./DataTest/DataSet_Test_00.txt')
        oADN = ADN('./DataTest/ecoli.txt')

        oRepBegins = ReplicationBegins()
        bResult = oRepBegins.ClumpFindingProblemOpt(oADN, 15, 500, 25)

        print(bResult)
        #nFound = oPatterns.PatternCount('CGCATGTCG')
    
        #dictMostFrequentPatterns = oPatterns.FrequentWords(3, 'CGGAGGACTCTAGGTAACGCTTATCAGGTCCATAGGACATTCA', True)
        #dictMostFrequentPatterns = oPatterns.FrequentWords(11, '', True)
    
        #oPatterns.ReverseComplement(True)

        #num, aPos = oPatterns.PatternCount('CGC')
        #for it in aPos:
        #    print(str(it) + ' ')

        #aPatternsClump = oPatterns.ClumpFindingProblem(11, 566, 18)
        #print(aPatternsClump)