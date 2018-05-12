class ADN(object):
    """description of class"""

    sPathADN = ''
    sADN = ''

    nLenADN     = 0
    nPosIni     = 0
    nCurrPos    = 0
    fileADN     = None

    dicCode2Num = {}

    def __init__(self, sPathADN, nPosIni=0):
        self.sPathADN = sPathADN
        self.nPosIni = nPosIni

        self.dicCode2Num['A'] = 0
        self.dicCode2Num['C'] = 1
        self.dicCode2Num['G'] = 2
        self.dicCode2Num['T'] = 3

    #def __init__(self, sPathADN, nLenADN, nLenPattern, nWindowLen, nTimesMin):
    #    self.sPathADN       = sPathADN
    #    self.nLenADN        = nLenADN
    #    self.nLenPattern    = nLenPattern
    #    self.nWindowLen     = nWindowLen
    #    self.nTimesMin      = nTimesMin

    # nBuffer:  Número de nucleòtids que llegirem.
    # nBackPositions: Número de nucleòtids que tornarem a llegir.
    def ReadADN(self, nBuffer=500, nSeekPos=0):

        if self.fileADN == None:
            self.fileADN = open(self.sPathADN, 'r')
            # Ens posicionem:
            self.fileADN.seek(self.nPosIni)
        else:
            self.fileADN.seek(nSeekPos)
        
            # Llegim en blocs de tamany nBuffer        
        self.sADN = self.fileADN.read(nBuffer)
        self.nCurrPos = self.nCurrPos + nBuffer

        return len(self.sADN)



    def PrintADN(self):
        print(self.sADN)


    def Pattern2Number(self, sPattern):
        if sPattern == '':
            return 0
        sym = sPattern[-1:]
        sPrefix = sPattern[:-1]
        return (4 * self.Pattern2Number(sPrefix)) + self.dicCode2Num[sym]
        




    # 1A: Compute the Number of Times a Pattern Appears in a Text
    # 1D: Find all occurrences of a Pattern in a string
    def PatternCount(self, sPattern, bShowInfo = False):
        nCount = 0
        aPositions = []
        if self.sADN != '' and sPattern != '':
            nPatternLen = len(sPattern)
            for iPos in range(len(self.sADN)):
                 if self.sADN[iPos:iPos+nPatternLen] == sPattern:
                     nCount = nCount + 1
                     aPositions.append(iPos)
        
        if bShowInfo:
            print('Found ' + str(nCount) + ' matches of ' + sPattern)
        
        return nCount, aPositions

    # 1B: Find the Most Frequant Words in a String   
    def FrequentWords(self, nLenPattern, sADN='', bShowInfo = False):

        if sADN == '':
            sADN = self.sADN

        dictPatternsDone = {}
        dictMostFrequent = {}

        nCurrPos = 0
        while len(sADN) > (nLenPattern + nCurrPos):
            sCurrPattern = sADN[nCurrPos:nCurrPos+nLenPattern]
            if sCurrPattern not in dictPatternsDone.keys():
                nPatternCount, dummy = self.PatternCount(sCurrPattern)
                dictPatternsDone[sCurrPattern] = nPatternCount
                if nPatternCount in dictMostFrequent:
                    aPatternsByFrequency = dictMostFrequent[nPatternCount]
                    aPatternsByFrequency.append(sCurrPattern)
                else:
                    aPatternsByFrequency = [sCurrPattern]

                dictMostFrequent[nPatternCount] = aPatternsByFrequency
            nCurrPos = nCurrPos + 1
        nMostFrequent = max(dictMostFrequent.keys())
        
        dictMostFrequentPatterns = {}
        for sMostFreqPattern in dictMostFrequent[nMostFrequent]:
            dictMostFrequentPatterns[sMostFreqPattern] = dictPatternsDone[sMostFreqPattern]

        if bShowInfo:
            print(str(len(dictMostFrequentPatterns.items())) + ' Patterns found')
            print(dictMostFrequentPatterns)
        return dictMostFrequentPatterns, nMostFrequent
        
    # 1C: Find the Reverse Complement of a ADN String
    def ReverseComplement(self, bShowInfo = False):
        dicComplement = {}
        # Init:
        dicComplement['A'] = 'T'
        dicComplement['G'] = 'C'
        dicComplement['T'] = 'A'
        dicComplement['C'] = 'G'

        sComplement = ''
        for c in self.sADN:
            sComplement = sComplement + dicComplement[c]
        
        sComplement = sComplement[::-1]

        if bShowInfo:
            print(sComplement)

        return sComplement

    # 1E: Find patterns forming clumps in a string
    # Dins d'un Genoma, dividir-ho en finestres de longitud [nWindowLen] i trobar els patrons de longitud [nLenPattern]
    # que es repeteixin [nTimesMin] com a mínim.
    def ClumpFindingProblem(self, nLenPattern, nWindowLen, nTimesMin):

        # És molt lent, fer que s'aprofiti la informació feta fins ara, és a dir, que cada finestra no
        # comenci desde 0.

        aPatternsClump = set()
        for iPos in range(len(self.sADN)-nWindowLen+1):
            sCurrADNWindow = self.sADN[iPos:iPos+nWindowLen]
            dictMostFrequentPatterns, nTimes = self.FrequentWords(nLenPattern, sCurrADNWindow)
            if nTimes >= nTimesMin:
                aPatternsClump.update(list(dictMostFrequentPatterns.keys()))
        return aPatternsClump



    # 1E_Optimized: Find patterns forming clumps in a string
    def ClumpFindingProblemOpt(self, idAnalysis, nBuffer, nIniPos, nTimesToReadBuffer = 5):
        
        dicPatternsFound = {}
        nGlobalPos = nIniPos
        
        # Read ADN
        while self.ReadADN(nBuffer, nIniPos) and (nTimesToReadBuffer > 0):
            nTimesToReadBuffer = nTimesToReadBuffer - 1
            
            for nCurrPos in range(len(self.sADN)-self.nLenPattern):
                sCurrPattern = self.sADN[nCurrPos:nCurrPos+self.nLenPattern]
                if sCurrPattern in dicPatternsFound.keys():
                    aPatternPos = dicPatternsFound[sCurrPattern]
                else:
                    aPatternPos = [nIniPos]
                aPatternPos.append(nGlobalPos)
                dicPatternsFound[sCurrPattern] = aPatternPos
                nGlobalPos = nGlobalPos + 1
        return dicPatternsFound