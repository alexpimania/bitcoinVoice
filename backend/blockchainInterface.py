#############################################################################################
#
# Bitcoin Voice - Web API connecting bitcoinVoice DB
#
#############################################################################################

from plDatabaseInterface import *

# returns a list of aggregated public labels that are unspent and calculates the subtotals
def getPublicLabelAggregates(chainID, startPos, endPos, startDate, endDate, searchTerm):
    publicLabels = {}
    output = []

    # get a list of filtered unaggregated unspent public labels
    records = getFilteredPublicLabels(chainID, searchTerm, startDate, endDate, "")

    # loop each sub public label into the aggregate list
    for record in records:
        if record["unixTimeSpent"] == 0:
            if record["publicLabel"] in publicLabels:
                publicLabels[record["publicLabel"]] += record["amountInSatoshis"]/100000000
            else:
                publicLabels[record["publicLabel"]] = record["amountInSatoshis"]/100000000
        else:
            if not record["publicLabel"] in publicLabels:
                publicLabels[record["publicLabel"]] = 0

    # sort the aggregated list
    i = 0
    for key, value in sorted(publicLabels.items(), key=lambda i: i[1], reverse=True):
        i+= 1
        output.append({"rank": i, "label": key, "amt": value})
    output = output[endPos:startPos]
    return output



# returns a list of non-aggregated public labels that are unspent so aggregate layer can use drill down on a label
def getPublicLabelOutputs(chainID, startDate, endDate, publicLabel, searchByTxID):
    utxos = []
    publicLabels = {}

    # get a list of filtered unaggregated unspent public labels
    records = getFilteredPublicLabels(chainID, publicLabel, startDate, endDate, "")
    for record in records:
        if record["txID"] == searchByTxID or not searchByTxID:
            publicLabels[record["txID"]] = record["unixTimeCreated"]

    # sort the list by unixTimeCreated
    i = 0
    for key, value in sorted(publicLabels.items(), key=lambda i: i[1], reverse=True):
        i+= 1
        for record in records :
            if record["txID"] == key :
                utxos.append({"txid": record["txID"],
                                "amt": record["amountInSatoshis"]/100000000,
                                "plblockHeightCreated": record["plBlockHeightCreated"],
                                "txOutputSequence": record["txOutputSequence"],
                                "unixTimeCreated": record["unixTimeCreated"],
                                "unixTimeSpent": record["unixTimeSpent"],
                                "txIDSpent": record["txIDSpent"],
                                "plBlockHeightSpent": record["plBlockHeightSpent"],
                                "publicLabel": record["publicLabel"]})

    #utxos = utxos[endPos:startPos]

    return utxos

