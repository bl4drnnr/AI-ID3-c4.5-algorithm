import math
from parser import getData, getKeyAttribute
DATA = getData()
KEY_ATTRIBUTE = getKeyAttribute()
INPUT_DATA_LENGTH = len(getData())
GENERATED_TREE = []
ITERATOR = 0


def informationGainForClass(gainsPerAttribute, gainsPerAttributeItems):
    infoGainForClass = 0
    quantityOfAllAttributes = 0
    for item in gainsPerAttributeItems:
        quantityOfAllAttributes += sum(item)

    for x in range(len(gainsPerAttribute)):
        infoGainForClass += (sum(gainsPerAttributeItems[x])/quantityOfAllAttributes) * gainsPerAttribute[x]

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


def getAllPossibleSubsets(data, ALL_POSSIBLE_SUBSETS_ITEMS):
    allPossibleSubsets = {}

    for attr, value in ALL_POSSIBLE_SUBSETS_ITEMS.items():
        for record in data:
            for recAttr, recValue in record.items():
                if attr == recAttr:

                    for attrSubset, valueSubset in value.items():
                        if recValue == valueSubset and allPossibleSubsets.get(attr) is None:
                            allPossibleSubsets[attr] = {}
                            allPossibleSubsets[attr][attrSubset] = [record[KEY_ATTRIBUTE]]
                        elif recValue == valueSubset and allPossibleSubsets.get(attr) is not None:
                            if allPossibleSubsets[attr].get(attrSubset) is None:
                                allPossibleSubsets[attr][attrSubset] = {}
                                allPossibleSubsets[attr][attrSubset] = [record[KEY_ATTRIBUTE]]
                            else:
                                allPossibleSubsets[attr][attrSubset].append(record[KEY_ATTRIBUTE])

    return allPossibleSubsets


def getInformationEntropyPerSubset(ALL_POSSIBLE_SUBSETS, DECISION_CLASSES_INFO_GAIN):
    attributesInfoGainRes = {}
    for attr, value in ALL_POSSIBLE_SUBSETS.items():
        oneAttributeInfo = {'qor': []}

        attributesInfoGainItems = []
        extractedSubsetInfoItems = []

        for key, val in value.items():
            oneAttributeInfo[key] = 0
            countSubsetInfo = countItems(val)
            extractedSubsetInfo = []

            for x, y in countSubsetInfo.items():
                extractedSubsetInfo.append(y)

            info = information(extractedSubsetInfo)

            oneAttributeInfo[key] = info
            oneAttributeInfo['qor'].append({'attribute': key, 'len': len(val)})
            attributesInfoGainItems.append(info)

            extractedSubsetInfoItems.append(extractedSubsetInfo)

        infoGain = DECISION_CLASSES_INFO_GAIN - informationGainForClass(attributesInfoGainItems,
                                                                        extractedSubsetInfoItems)
        attributesInfoGainRes[attr] = {**oneAttributeInfo, 'gain': float(format(infoGain, ".3f"))}
    return attributesInfoGainRes


def updateRecordsPerAttribute(data):
    recordsPerDecisionAttribute = {}
    quantityOfRecordsPerDecisionAttribute = []
    for record in data:
        if recordsPerDecisionAttribute.get(record[KEY_ATTRIBUTE]) is None:
            recordsPerDecisionAttribute[record[KEY_ATTRIBUTE]] = 1
        else:
            recordsPerDecisionAttribute[record[KEY_ATTRIBUTE]] += 1

    for attr, value in recordsPerDecisionAttribute.items():
        quantityOfRecordsPerDecisionAttribute.append(value)

    return information(quantityOfRecordsPerDecisionAttribute)


def extractTreeData(data):
    gainsList = []
    for attr, value in data.items():
        gainsList.append(value['gain'])

    for attr, value in data.items():
        if value['gain'] == max(gainsList):
            return generateTree(attr, data)


def generateTree(node, nextData):
    global ITERATOR
    tabulator = '\t' * ITERATOR
    attributesToContinue = {node: []}
    GENERATED_TREE.append(tabulator + node)

    # Sort data in node, just to make it print in right way
    sortedNodeData = {}
    for attr, value in nextData[node].items():
        if attr != 'qor':
            sortedNodeData[attr] = value
    sortedNode = {}
    for item in sorted(sortedNodeData.values()):
        for attr, value in nextData[node].items():
            if item == value:
                sortedNode[attr] = value

    # Print tree
    for attr, value in sortedNode.items():
        qor = None
        for item in nextData[node]['qor']:
            if item['attribute'] == attr:
                qor = item['len']
        if value == 0 and attr != 'gain' and attr != 'qor':
            GENERATED_TREE.append(f"{tabulator} -- {attr} -- {qor}")
            GENERATED_TREE.append(f"{tabulator}|")
        elif attr != 'gain' and attr != 'qor':
            GENERATED_TREE.append(f"{tabulator} -- {attr}")
            GENERATED_TREE.append(f"{tabulator}|")
            attributesToContinue[node].append(attr)

    ITERATOR += 1
    return attributesToContinue


def printTree():
    for node in GENERATED_TREE[:-1]:
        print(node)
