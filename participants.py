# Required Libraries
import pandas as pd

# Function to read participant list into a dataframe
def readParticipants(config):

    # Load participant list from CSV file
    dfParticipants = pd.read_csv(config["localPaths"]["basePath"] + "/export/participants.csv", sep=";")

    # Rename columns
    dfParticipants.rename(columns={"participant_number": "study_id", "study": "site"}, inplace=True)

    print(dfParticipants.to_string())

    # Return participant dictionary
    return dfParticipants
