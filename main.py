# Required Libraries
# - install packages: pandas, PyYAML, openpyxl
import os
import zipfile
import yaml

# Required modules
import codebook
import participants

# Read configuration file
with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Create extraction directory unless it already exists
if not os.path.isdir(config["localPaths"]["basePath"] + "/export"):
    os.mkdir(config['localPaths']['basePath'] + "/export")

# Extract Maganamed export file (must be named "export.zip"
with zipfile.ZipFile(config["localPaths"]["basePath"] + "/export.zip", "r") as zip_ref:
    zip_ref.extractall(config["localPaths"]["basePath"] + "/export")

# Parse Codebook
dictCodebook = codebook.parseCodebook(config)

# Store codebook in YAML format
with open(config['localPaths']['basePath'] + "/codebook.yaml", 'w') as outfile:
    yaml.dump(dictCodebook, outfile, default_flow_style=False)

dictParticipants = participants.readParticipants(config)

# Iterate over eCRFs
# for ecrfId in dictCodebook["eCRFs"]:
#     print(ecrfId)
#     ecrfFilename = dictCodebook["eCRFs"][ecrfId]["ecrfFilename"]
#     if not os.path.isfile(config["localPaths"]["basePath"] + "/export/" + ecrfFilename):
#         print(ecrfFilename)
