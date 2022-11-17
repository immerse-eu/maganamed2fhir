# Required Libraries
import os.path as p
import pandas as pd

# Function to parse a Maganamed codebook and return as a dictionary of eCRFs, items and answers
def parseCodebook(config):

    # Initialize codebook dictionary for YAML export
    dictCodebook = {}
    dictCodebook["eCRFs"] = {}

    # Iterate over eCRFs from config file
    for ecrfId in config["eCRFs"]:

        # Extract tab- & filename of current eCRF
        ecrfTabname = config["eCRFs"][ecrfId]["tabname"]
        ecrfFilename = config["eCRFs"][ecrfId]["filename"]

        print("id=", ecrfId, "tabname=", ecrfTabname, "filename=", ecrfFilename)

        # Create entry for current eCRF in YAML dictionary
        dictCodebook["eCRFs"][ecrfId] = {
            "ecrfTabname": config["eCRFs"][ecrfId]["tabname"],
            "ecrfFilename": config["eCRFs"][ecrfId]["filename"]
        }

        # Extract codebook of current eCRF from Excel file
        ecrfCodebook = pd.read_excel(config["localPaths"]["basePath"] + "/export/codebook.xlsx", sheet_name=ecrfTabname, header=0, usecols="A:E")

        # Remove first 6 empty rows from codebook
        ecrfCodebook.drop(ecrfCodebook.index[0:6], inplace=True)

        # Iterate over rows of current eCRF codebook tab
        itemId = 0
        prvItemCode = ""
        missingPromptFlag = 0
        answerTexts = []
        for rowIndex, rowContent in ecrfCodebook.iterrows():

            # question column filled?
            if (not pd.isnull(rowContent["question"])) or rowContent["codebook"] != prvItemCode:

                # Check if previous question had no prompt
                if missingPromptFlag == 1:
                    commonPrefix = p.commonprefix(answerTexts)
                    if len(commonPrefix) > 0:
                        dictCodebook["eCRFs"][ecrfId][itemId]["itemPrompt"] = commonPrefix
                        dictCodebook["eCRFs"][ecrfId][itemId]["itemPromptSubstituted"] = 1

                # Initialize new item
                itemId += 1
                answerId = 0
                answerTexts = []

                # Substitute an item prompt if none was given
                itemPrompt = ""
                if pd.isnull(rowContent["question"]):
                    itemPrompt = "[No question text given]"
                    missingPromptFlag = 1
                else:
                    itemPrompt = rowContent["question"]
                    missingPromptFlag = 0

                # Create entry for current question in YAML dictionary
                dictCodebook["eCRFs"][ecrfId][itemId] = {
                    "itemId": itemId,
                    "itemCode": rowContent["codebook"],
                    "itemDataType": rowContent["answer type"],
                    "itemPrompt": itemPrompt
                }
                dictCodebook["eCRFs"][ecrfId][itemId]["answers"] = {}

            # Store code of current row for comparison with next one
            prvItemCode = rowContent["codebook"]

            # Answer line filled?
            if not pd.isnull(rowContent["answer"]):
                answerId += 1
                answerTexts.append(rowContent["answer"])
                dictCodebook["eCRFs"][ecrfId][itemId]["answers"][answerId] = {
                    "answerCode": rowContent["encoding"],
                    "answerText": rowContent["answer"]
                }

    # Return codebook dictionary
    return dictCodebook
