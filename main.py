# Required Libraries
# - install packages: pandas, PyYAML, openpyxl
import os
import pandas as pd
import zipfile
import yaml

# Read configuration file
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Create extraction directory unless it already exists
if not os.path.isdir(config["localPaths"]["basePath"] + "/export"):
    os.mkdir(config['localPaths']['basePath'] + "/export")

# Extract maganamed export file (must be named "export.zip"
with zipfile.ZipFile(config["localPaths"]["basePath"] + "/export.zip", "r") as zip_ref:
    zip_ref.extractall(config["localPaths"]["basePath"] + "/export")

# Iterate over eCRFs from config file
for ecrfId in config["eCRFs"]:

    # Extract tab- & filename of current eCRF
    ecrfTabname = config["eCRFs"][ecrfId]["tabname"]
    ecrfFilename = config["eCRFs"][ecrfId]["filename"]

    print("id=", ecrfId, "tabname=", ecrfTabname, "filename=", ecrfFilename)

    # Extract codebook of current eCRF from Excel file
    ecrfCodebook = pd.read_excel(config["localPaths"]["basePath"] + "/export/codebook.xlsx", sheet_name=ecrfTabname, header=0, usecols="A:E")

    # Remove first 6 empty rows from codebook
    ecrfCodebook.drop(ecrfCodebook.index[0:6], inplace=True)

    print(ecrfCodebook)

    # Iterate over rows of current eCRF codebook
    itemId = 0
    for rowIndex, rowContent in ecrfCodebook.iterrows():

        # question column filled? Then we have a new item
        if rowContent["question"] != "nan":
            itemId += 1

        print("row=", rowIndex, "item=", itemId, "q=", rowContent["question"])
