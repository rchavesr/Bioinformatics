import sys

from Utils import DebugInfo
from Patterns import ADN


class ReplicationBegins(object):

    def __init__(self):
        pass



    # 1E_Optimized: Find patterns forming clumps in a string
    # oADN: Objecte del tipus ADN (per tractar la cadena de ADN)
    # K: Longitut cadena
    # L: Tamany finestra
    # t: Número de repeticions mínima
    def ClumpFindingProblemOpt(self, oADN: ADN, K, L, t):

        oDebugInfo = DebugInfo('ClumpFindingProblemOpt', False)

        # Guardem les posicions de cada patró (Codi --> []):
        dicPattern2Pos = {}
    
        # Caché per codificar només una vegada
        dicPattern2Code = {}

        nCycle = 0
        nPos=0
        while oADN.ReadADN(L,nPos) >= K:
            oDebugInfo.Print('Buffer actual:')
            oADN.PrintADN()
            nPosCycle = 0
            while nPosCycle <= (L-K):            
                sPattern = oADN.sADN[nPosCycle:nPosCycle+K]            
                if sPattern not in dicPattern2Code:
                    nCodePattern = oADN.Pattern2Number(sPattern)
                    dicPattern2Code[sPattern] = nCodePattern
                else:
                    nCodePattern = dicPattern2Code[sPattern]

                if nCodePattern in dicPattern2Pos:
                    dicPattern2Pos[nCodePattern].append(nPos)
                else:
                    dicPattern2Pos[nCodePattern] = [nPos]

                nPosCycle = nPosCycle + 1
                nPos = nPos + 1        
            nCycle = nCycle + 1


        dicPatts2PosOK = self.GetPatternsWithEnoughtReps(dicPattern2Pos, L, t)

        print('Nombre de patrons a analitzar --> {numToAnalize}'.format(numToAnalize=len(dicPattern2Pos)))
        print('Nombre de patrons amb repeticions mínimes = {numMin} --> {numPatronsOK}'.format(numMin=t, numPatronsOK=len(dicPatts2PosOK)))


        # write python dict to a file
        file = open('file.txt', 'w')
        file.write(str(dicPatts2PosOK))

        return False
   
    def GetPatternsWithEnoughtReps(self, dicPattern2Pos: {}, nDistance, nRepMin):
        dicPat2PosCandidate = {}
        for idPat,aPos in dicPattern2Pos.items():
            if len(aPos) >= nRepMin:
                nPosFound = self.CheckDistance(aPos, nDistance, nRepMin)
                if nPosFound != -1:
                    dicPat2PosCandidate[idPat] = aPos[nPosFound:]

        return dicPat2PosCandidate

    def CheckDistance(self, aPos, nDistance, nRepMin):
        
        bResult = False
        nPrevVal = -sys.maxsize
        for nCurrPos in list(range(len(aPos)-nRepMin))[1:]:
            nPrevVal = aPos[nCurrPos-1]
            nCount = 1
            for it in aPos:
                if (it-nPrevVal) < nDistance:
                    nCount = nCount + 1
                    if nCount >= nRepMin:
                        bResult = True
                        break
                else:
                    break
            if bResult:
                break
        if bResult:
            nPosRet  =nCurrPos
        else:
            nPosRet = -1

        return nPosRet
