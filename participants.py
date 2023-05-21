# Required Libraries
import pandas as pd

# Function to read participant list into a dataframe
def readParticipants(config):

    # Load participant list from exported CSV file
    dfParticipants = pd.read_csv(config["localPaths"]["basePath"] + "/export/participants.csv", sep=";")

    # Load "Kind of Participant" eCRF from exported CSV file
    dfKindOfParticipant = pd.read_csv(config["localPaths"]["basePath"] + "/export/Kind-of-participant.csv", sep=";")

    # Load "Smartphone_Doc ESM Random" eCRF from exported CSV file
    dfSmartphone = pd.read_csv(config["localPaths"]["basePath"] + "/export/Smartphone_Doc-ESM-Randomization.csv", sep=";")

    # Select & rename relevant columns of KindOfParticipant dataframe
    dictRemap = {"participant_identifier": "participant_identifier",
                 "PARTICIPANT_01": "participant_kind",
                 "PARTICIPANT_02": "participant_language",
                 "Site": "participant_center"}
    dfKindOfParticipant = dfKindOfParticipant.rename(columns=dictRemap)[dictRemap.values()]

    # Map values of participant kind column to human-interpretable codes
    dictRemap = {0.0: "PATIENT",
                 1.0: "CLINICIAN",
                 2.0: "ADMIN",
                 3.0: "FINANCE"}
    dfKindOfParticipant.replace({"participant_kind": dictRemap}, inplace=True)

    # Map values of participant language column to human-interpretable codes
    dictRemap = {0.0: "EN",
                 1.0: "DE",
                 2.0: "BE",
                 3.0: "SK"}
    dfKindOfParticipant.replace({"participant_language": dictRemap}, inplace=True)

    # Map values of participant center column to human-interpretable codes
    dictRemap = {1.0: "Lothian",
                 2.0: "Lothian CAMSH",
                 3.0: "Mannheim",
                 4.0: "Wiesloch",
                 5.0: "Leuven",
                 6.0: "Bierbeek",
                 7.0: "Bratislava",
                 8.0: "Kosice"}
    dfKindOfParticipant.replace({"participant_center": dictRemap}, inplace=True)

    # Select & rename relevant columns of Smartphone dataframe
    dictRemap = {"participant_identifier": "participant_identifier",
                 "Doc_02": "movisensxs_id"}
    dfSmartphone = dfSmartphone.rename(columns=dictRemap)[dictRemap.values()]

    # Convert data type of movisensxs_id column to integer
    dfSmartphone["movisensxs_id"] = dfSmartphone["movisensxs_id"].astype("Int64")

    # Merge participant kind data to base participant identities using left outer join
    dfParticipants = pd.merge(dfParticipants, dfKindOfParticipant, how="left", on=["participant_identifier"])

    # Merge Smartphone dataframe using left outer join
    dfParticipants = pd.merge(dfParticipants, dfSmartphone, how="left", on=["participant_identifier"])

    # Return participant dictionary
    return dfParticipants
