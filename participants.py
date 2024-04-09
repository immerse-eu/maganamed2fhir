# Required Libraries
import numpy as np
import pandas as pd

# Function to read participant list into a dataframe
def readParticipants(config):

    # Load participant list from exported CSV file
    dfParticipants = pd.read_csv(config["localPaths"]["basePath"] + "/export/participants.csv", sep=";")

    # Load "Kind of Participant" eCRF from exported CSV file
    dfKindOfParticipant = pd.read_csv(config["localPaths"]["basePath"] + "/export/Kind-of-participant.csv", sep=";")

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

    # Load "Smartphone_Doc ESM Random" eCRF from exported CSV file
    dfSmartphone = pd.read_csv(config["localPaths"]["basePath"] + "/export/Smartphone_Doc-ESM-Randomization.csv", sep=";")

    # Select & rename relevant columns of Smartphone dataframe
    dictRemap = {"participant_identifier": "participant_identifier",
                 "Doc_02": "movisensxs_id"}
    dfSmartphone = dfSmartphone.rename(columns=dictRemap)[dictRemap.values()]

    # Convert data type of movisensxs_id column to integer
    try:
        dfSmartphone["movisensxs_id"] = dfSmartphone["movisensxs_id"].astype("Int64")
    except:
        dfSmartphone["movisensxs_id"] = ""

    # Load "Demographics (Patients)" eCRF from exported CSV file
    dfDemographicsPatients = pd.read_csv(config["localPaths"]["basePath"] + "/export/Demographics-(Patients).csv", sep=";")

    # Select & rename relevant columns of Demographics Patient dataframe
    dictRemap = {"participant_identifier": "participant_identifier",
                 "MRC_gender": "participant_patient_gender"}
    dfDemographicsPatients = dfDemographicsPatients.rename(columns=dictRemap)[dictRemap.values()]

    # Map values of Demographics Patient gender column to human-interpretable codes
    dictRemap = {0.0: "MALE",
                 1.0: "FEMALE",
                 2.0: "NON-BINARY",
                 3.0: "OTHER"}
    dfDemographicsPatients.replace({"participant_patient_gender": dictRemap}, inplace=True)

    # Load "Demographics (Clinicians)" eCRF from exported CSV file
    dfDemographicsClinicians = pd.read_csv(config["localPaths"]["basePath"] + "/export/Demographics-(Clinicians).csv", sep=";")

    # Select & rename relevant columns of Demographics Clinicians dataframe
    dictRemap = {"participant_identifier": "participant_identifier",
                 "Gender": "participant_clinician_gender"}
    dfDemographicsClinicians = dfDemographicsClinicians.rename(columns=dictRemap)[dictRemap.values()]

    # Map values of Demographics Clinician gender column to human-interpretable codes
    dictRemap = {0.0: "MALE",
                 1.0: "FEMALE",
                 2.0: "NON-BINARY",
                 3.0: "OTHER"}
    dfDemographicsClinicians.replace({"participant_clinician_gender": dictRemap}, inplace=True)

    # Load "Demographics (Clinicians)" eCRF from exported CSV file
    dfScreeningChecklist = pd.read_csv(config["localPaths"]["basePath"] + "/export/Screening-Checklist.csv", sep=";")

    # Select & rename relevant columns of Screening Checklist dataframe
    dictRemap = {"participant_identifier": "participant_identifier",
                 "decision": "included_in_study"}
    dfScreeningChecklist = dfScreeningChecklist.rename(columns=dictRemap)[dictRemap.values()]

    # Map values of Demographics Clinician gender column to human-interpretable codes
    dictRemap = {0.0: "not_included",
                 1.0: "included",
                 np.NAN: "undefined"}
    dfScreeningChecklist.replace({"included_in_study": dictRemap}, inplace=True)

    # Merge participant kind data to base participant identities using left outer join
    dfParticipants = pd.merge(dfParticipants, dfKindOfParticipant, how="left", on=["participant_identifier"])

    # Merge Smartphone dataframe using left outer join
    dfParticipants = pd.merge(dfParticipants, dfSmartphone, how="left", on=["participant_identifier"])

    # Merge Demographics Patients dataframe using left outer join
    dfParticipants = pd.merge(dfParticipants, dfDemographicsPatients, how="left", on=["participant_identifier"])

    # Merge Demographics Clinicians dataframe using left outer join
    dfParticipants = pd.merge(dfParticipants, dfDemographicsClinicians, how="left", on=["participant_identifier"])

    # Merge Screening Checklist dataframe using left outer join
    dfParticipants = pd.merge(dfParticipants, dfScreeningChecklist, how="left", on=["participant_identifier"])

    # Return participant dictionary
    return dfParticipants
