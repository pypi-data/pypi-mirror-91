import sys
import math
import os

TP = 1
transitionProbDict = {}
emissionProbDict = {}
obsSeqList = []
tagStateList = []
tagStateDict = {}
outgoingTagCountDict = {}
noOfTag = 0
AllWordsList = {}
# Viterbi


def Viterbi(seq):
    score = 0
    Seq = seq.split()
    T = len(Seq)
    h, w = noOfTag + 1, T
    viterbi = [[0 for x in range(w)] for y in range(h)]
    backtrack = [[0 for x in range(w)] for y in range(h)]
    for s in tagStateDict.keys():

        emiKey = Seq[0] + '|' + tagStateDict[s]
        if Seq[0] not in AllWordsList.keys():
            multPE = 1
        elif emiKey not in emissionProbDict.keys():
            multPE = 0
        else:
            multPE = emissionProbDict[emiKey]
        tranKey = 'Q0-'+tagStateDict[s]
        if tranKey not in transitionProbDict:
            multPT = 1 / (outgoingTagCountDict['Q0'] + noOfTag)
        else:
            multPT = transitionProbDict[tranKey]
        viterbi[s][0] = multPT * multPE
        backtrack[s][0] = 0
    for t in range(1, T):
        for s_to in tagStateDict.keys():
            for s_from in tagStateDict.keys():
                emiKey = Seq[t] + '|' + tagStateDict[s_to]
                if Seq[t] not in AllWordsList.keys():
                    multPE = 1
                elif emiKey not in emissionProbDict.keys():
                    multPE = 0
                else:
                    multPE = emissionProbDict[emiKey]
                tranKey = tagStateDict[s_from] + '-' + tagStateDict[s_to]
                if tranKey not in transitionProbDict:
                    multPT = 1 / \
                        (outgoingTagCountDict[tagStateDict[s_from]] + noOfTag)
                else:
                    multPT = transitionProbDict[tranKey]
                score = viterbi[s_from][t-1] * multPT * multPE
                if score > viterbi[s_to][t]:
                    viterbi[s_to][t] = score
                    backtrack[s_to][t] = s_from
                else:
                    continue
    best = 0
    for i in tagStateDict.keys():
        if viterbi[i][T-1] > viterbi[best][T-1]:
            best = i
    path = [Seq[T-1]+'/'+tagStateDict[best]]
    nice_path = [tagStateDict[best]]
    for t in range(T-1, 0, -1):
        best = backtrack[best][t]
        path[0:0] = [Seq[t-1]+'/'+tagStateDict[best]]
        nice_path[0:0] = [tagStateDict[best], '--%s-->' % (Seq[t - 1],)]
        nice_path_string = ' '.join(nice_path)
    return (path)

model_path = os.path.dirname(__file__)
model_path = model_path + '/storage/hmmmodel.txt'
modelFile = open(model_path, 'r')
iCount = 0
for line in modelFile:
    if iCount == 0:
        iCount = iCount + 1
        noOfTag = int(line.split(':')[1])
        continue
    if iCount == 1:
        # tags
        iCount = iCount + 1
        tagSet = line.split(':')[1]
        tagSet = tagSet.strip('\n')
        tagStateList = tagSet.split(',')
        continue
    if line == 'Outgoing Count:\n':
        TP = 2
        continue
    if line == 'Transition Probability:\n':
        TP = 1
        continue
    if TP == 2:
        d = line.split(':')
        # print(d[0])
        outgoingTagCountDict[d[0]] = int(d[1].strip('\n'))
    if line == 'Emission Probability:\n':
        TP = 0
        continue
    if TP == 1:
        data = line.split(':')
        if len(data[0]) < 4:
            continue
        tp = data[0]  
        tp = tp.replace('Begin', 'Q0')
        transitionProbDict[tp] = float(data[1].strip('\n'))
    if TP == 0:
        data = line.split(':->')
        tagE = data[0]
        tagE = tagE[2:len(tagE) - 1]
        corpusWord = tagE.split('|')[0]
        AllWordsList[corpusWord] = 1
        emissionProbDict[tagE] = float(data[1].strip('\n'))
# read input file
c = 0
for tagNm in tagStateList:
    tagStateDict[c] = tagNm
    c += 1

def pos_tag(sentences):
    inputText = sentences
    line = inputText
    path = Viterbi(line)
    st = '$'
    for i in path:
        st = st + i + ' '
    st = st.strip('$')
    st = st.strip(' ')
    st = st + '\n'

    return st

