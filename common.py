import math
from parser import getData
INPUT_DATA_LENGTH = len(getData())
GENERATED_TREE = []


def informationGainForClass(gainsPerAttribute, gainsPerAttributeItems):
    infoGainForClass = 0

    for x, gain in enumerate(gainsPerAttribute):
        infoGainForClass += (sum(gainsPerAttributeItems[x])/INPUT_DATA_LENGTH) * gain

    return float(format(infoGainForClass, ".3f"))


def information(X):
    infoGain = 0

    totalSumOfX = sum(X)
    for x in X:
        infoGain += informationEntropy(x, totalSumOfX)

    return float(format(infoGain, ".3f"))


def informationEntropy(x, y):
    if x == 0 or y == 0:
        return 0
    return -1 * (x/y) * math.log2((x/y))


def countItems(array):
    result = {}
    for item in array:
        if result.get(item) is None:
            result[item] = 1
        else:
            result[item] += 1

    return result


def extractTreeData(data):
    gainsList = []
    for attr, value in data.items():
        gainsList.append(value['gain'])

    for attr, value in data.items():
        if value['gain'] == max(gainsList):
            print(attr, value)
    return


def generateTree():
    return


def printTree():
    return
