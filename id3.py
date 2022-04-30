from parser import parseInputData, getAllPossibleAttributes, getKeyAttribute
from common import informationGain

DATA = parseInputData()
KEY_ATTRIBUTE = getKeyAttribute()
ALL_POSSIBLE_ATTRIBUTES = getAllPossibleAttributes()
INPUT_DATA_LENGTH = len(DATA)
GENERATED_TREE = []

# Find information entropy for decision attribute
recordsPerDecisionAttribute = {}
quantityOfRecordsPerDecisionAttribute = []
for record in DATA:
    if recordsPerDecisionAttribute.get(record[KEY_ATTRIBUTE]) is None:
        recordsPerDecisionAttribute[record[KEY_ATTRIBUTE]] = 1
    else:
        recordsPerDecisionAttribute[record[KEY_ATTRIBUTE]] += 1

for attr, value in recordsPerDecisionAttribute.items():
    quantityOfRecordsPerDecisionAttribute.append(value)

CLASSES_INFO_GAIN = informationGain(quantityOfRecordsPerDecisionAttribute)

# Divide input data on subsets by attributes
ALL_POSSIBLE_SUBSETS = {}
ALL_POSSIBLE_SUBSETS_COPY = {}

for attr, value in ALL_POSSIBLE_ATTRIBUTES.items():
    if attr != KEY_ATTRIBUTE:
        ALL_POSSIBLE_SUBSETS[attr] = value

for attr, value in ALL_POSSIBLE_SUBSETS.items():

    for record in DATA:
        for recAttr, recValue in record.items():
            if attr == recAttr:

                for attrSubset, valueSubset in value.items():
                    if recValue == valueSubset and ALL_POSSIBLE_SUBSETS_COPY.get(attr) is None:
                        ALL_POSSIBLE_SUBSETS_COPY[attr] = {}
                        ALL_POSSIBLE_SUBSETS_COPY[attr][attrSubset] = [record[KEY_ATTRIBUTE]]
                    elif recValue == valueSubset and ALL_POSSIBLE_SUBSETS_COPY.get(attr) is not None:
                        if ALL_POSSIBLE_SUBSETS_COPY[attr].get(attrSubset) is None:
                            ALL_POSSIBLE_SUBSETS_COPY[attr][attrSubset] = {}
                            ALL_POSSIBLE_SUBSETS_COPY[attr][attrSubset] = [record[KEY_ATTRIBUTE]]
                        else:
                            ALL_POSSIBLE_SUBSETS_COPY[attr][attrSubset].append(record[KEY_ATTRIBUTE])

for attr, value in ALL_POSSIBLE_SUBSETS_COPY.items():
    print(attr, value)
