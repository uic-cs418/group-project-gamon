# Additional Helper Function code written for 
# assisting in reading in and cleaning data differently
# and exploring the data for additional possible visuals

import pandas as pd
# Functions written by Synthia
from helper_code import readInAndGetWantedColumns as getColumns
from helper_code import cleanUpCoreTrends
from helper_code import cleanUpNSDUH

# build simplified and cleaned up core trends data frames
# for use with the eng.ipynb file
# CORE TRENDS DATA FRAMES
# output: a data frame containing the cleaned up data from the January-3-1-2018-Core-Trends-Survey file
def buildCoreTrends2018df():
    colNames = ["web1a", "web1b", "web1c", "web1d", "web1e","sns2a", "sns2b", "sns2c", "sns2d", "sns2e","sex", "age"]
    fileName = "datasets/January 3-10, 2018 - Core Trends Survey/January 3-10, 2018 - Core Trends Survey - CSV.csv"
    coreTrends2018df = getColumns(fileName, "csv", colNames)
    
    # Basic clean up
    coreTrends2018df = coreTrends2018df.drop(columns=['sns2a'])
    coreTrends2018df = coreTrends2018df.apply(pd.to_numeric, errors='coerce')
    coreTrends2018df = coreTrends2018df[coreTrends2018df['age'] < 98]
    coreTrends2018df.dropna()
    
    # Rename Columns for Readability
    coreTrends2018df = coreTrends2018df.rename(
        columns={
            'web1a': 'Web_Twitter',
            'web1b': 'Web_Instagram',
            'web1c': 'Web_Facebook',
            'web1d': 'Web_Snapchat',
            'web1e': 'Web_YouTube',
            'sns2b': 'Sns_Instagram',
            'sns2c': 'Sns_Facebook',
            'sns2d': 'Sns_Snapchat',
            'sns2e': 'Sns_YouTube'
        })
    return coreTrends2018df

# output: a data frame containing the cleaned up data from the January-8-February-7-2019-Core-Trends-Survey file
def buildCoreTrends2019df():
    colNames = ["web1a", "web1b", "web1c", "web1d", "web1e","sns2a", "sns2b", "sns2c", "sns2d", "sns2e","sex", "age"]
    fileName = "datasets/January-8-February-7-2019-Core-Trends-Survey-SPSS/January 8-February 7, 2019 - Core Trends Survey - CSV.csv"
    coreTrends2019df = getColumns(fileName, "csv", colNames)

    # Basic clean up
    coreTrends2019df = coreTrends2019df.drop(columns=['sns2a'])
    coreTrends2019df = coreTrends2019df.apply(pd.to_numeric, errors='coerce')
    coreTrends2019df = coreTrends2019df[coreTrends2019df['age'] < 98]
    coreTrends2019df.dropna()
    
    # Rename Columns for Readability
    coreTrends2019df = coreTrends2019df.rename(
        columns={
            'web1a': 'Web_Twitter',
            'web1b': 'Web_Instagram',
            'web1c': 'Web_Facebook',
            'web1d': 'Web_Snapchat',
            'web1e': 'Web_YouTube',
            'sns2b': 'Sns_Instagram',
            'sns2c': 'Sns_Facebook',
            'sns2d': 'Sns_Snapchat',
            'sns2e': 'Sns_YouTube'
        })
    return coreTrends2019df

# output: a data frame containing the cleaned up data from the Jan-25-Feb-8-2021-Core-Trends-Survey file
def buildCoreTrends2021df():
    colNames = ["web1a", "web1b", "web1c", "web1d", "web1e","sns2a", "sns2b", "sns2c", "sns2d", "sns2e","gender", "age"]
    fileName = "datasets/Jan-25-Feb-8-2021-Core-Trends-Survey/Jan 25-Feb 8, 2021 - Core Trends Survey - CSV.csv"
    coreTrends2021df = getColumns(fileName, "csv", colNames)

    # Basic clean up
    coreTrends2021df = coreTrends2021df.drop(columns=['sns2a'])
    coreTrends2021df = coreTrends2021df.apply(pd.to_numeric, errors='coerce')
    coreTrends2021df = coreTrends2021df[coreTrends2021df['age'] < 98]
    coreTrends2021df.dropna()
    
    # Rename Columns for Readability
    coreTrends2021df = coreTrends2021df.rename(
        columns={
            'web1a':  'Web_Twitter',
            'web1b':  'Web_Instagram',
            'web1c':  'Web_Facebook',
            'web1d':  'Web_Snapchat',
            'web1e':  'Web_YouTube',
            'sns2b':  'Sns_Instagram',
            'sns2c':  'Sns_Facebook',
            'sns2d':  'Sns_Snapchat',
            'sns2e':  'Sns_YouTube',
            'gender': 'sex' # Renamed to match previous years
        })
    return coreTrends2021df

# NATIONAL SURVEY ON DRUG USE AND HEALTH DATA FRAMES
# output: a data frame containing the cleaned up data from the National Survey on Drug Use and Health 2018
def buildNSDUH2018df():
    colNames = ["AGE2", "IRSEX", "AUINPYR","AURXYR","YEATNDYR","YESCHFLT","YEPRBSLV","DSTNRV30","DSTHOP30","DSTCHR30","DSTNGD30","DSTWORST","DSTNRV12","DSTHOP12","DSTCHR12","DSTNGD12","IMPCONCN","IMPGOUT","IMPPEOP","IMPSOC","IMPSOCM","SUICTHNK","ADDPREV"]
    fileName = "datasets/National Survey on Drug Use and Health 2018/NSDUH_2018_Tab.tsv"
    NSDUH2018df = getColumns(fileName, "tsv", colNames)
    
    # Basic clean up
    # Convert values from strings to numeric
    NSDUH2018df = NSDUH2018df.apply(pd.to_numeric, errors='coerce')
    # Remove values over 85 since those are Refused or otherwise useless
    NSDUH2018df = NSDUH2018df[NSDUH2018df < 85]
    # label ages
    NSDUH2018df['AGE2'] = pd.cut(NSDUH2018df['AGE2'], bins=[0, 13, 15, 16, 17, float('inf')],
                                labels=['18-25', '26-34', '35-49', '50-64', '65+'])
    # Rename Columns for Readability
    NSDUH2018df = NSDUH2018df.rename(
        columns = {
            "AGE2":     "age", 
            "IRSEX":    "sex", 
            "AUINPYR":  "in_hospital",
            "AURXYR":   "on_medication",
            "YEATNDYR": "school",
            "YESCHFLT": "like_school",
            "YEPRBSLV": "self_group",
            "DSTNRV30": "nervous_last30",
            "DSTHOP30": "hopeless_last30",
            "DSTCHR30": "depressed_last30",
            "DSTNGD30": "worthless_last30",
            "DSTWORST": "worse_month",
            "DSTNRV12": "worse_nervous",
            "DSTHOP12": "worse_hopeless",
            "DSTCHR12": "worse_depressed",
            "DSTNGD12": "worse_worthless",
            "IMPCONCN": "diff_concentration",
            "IMPGOUT":  "diff_leaving_house",
            "IMPPEOP":  "diff_strangers",
            "IMPSOC":   "diff_social",
            "IMPSOCM":  "diff_social2",
            "SUICTHNK": "suicidal_think",
            "ADDPREV":  "sad_period"
        }
    )
    return NSDUH2018df

# output: a data frame containing the cleaned up data from the National Survey on Drug Use and Health 2019
def buildNSDUH2019df():
    colNames = ["AGE2", "IRSEX", "AUINPYR","AURXYR","YEATNDYR","YESCHFLT","YEPRBSLV","DSTNRV30","DSTHOP30","DSTCHR30","DSTNGD30","DSTWORST","DSTNRV12","DSTHOP12","DSTCHR12","DSTNGD12","IMPCONCN","IMPGOUT","IMPPEOP","IMPSOC","IMPSOCM","SUICTHNK","ADDPREV"]
    fileName = "datasets/National Survey on Drug Use and Health 2019/NSDUH_2019_Tab.txt"
    NSDUH2019df = getColumns(fileName, "txt", colNames)

    # Basic clean up
    # Convert values from strings to numeric
    NSDUH2019df = NSDUH2019df.apply(pd.to_numeric, errors='coerce')
    # Remove values over 85 since those are Refused or otherwise useless
    NSDUH2019df = NSDUH2019df[NSDUH2019df < 85]
    #  label ages
    NSDUH2019df['AGE2'] = pd.cut(NSDUH2019df['AGE2'], bins=[0, 13, 15, 16, 17, float('inf')],
                                 labels=['18-25', '26-34', '35-49', '50-64', '65+'])
    # Rename Columns for Readability
    NSDUH2019df = NSDUH2019df.rename(
        columns = {
            "AGE2":     "age", 
            "IRSEX":    "sex", 
            "AUINPYR":  "in_hospital",
            "AURXYR":   "on_medication",
            "YEATNDYR": "school",
            "YESCHFLT": "like_school",
            "YEPRBSLV": "self_group",
            "DSTNRV30": "nervous_last30",
            "DSTHOP30": "hopeless_last30",
            "DSTCHR30": "depressed_last30",
            "DSTNGD30": "worthless_last30",
            "DSTWORST": "worse_month",
            "DSTNRV12": "worse_nervous",
            "DSTHOP12": "worse_hopeless",
            "DSTCHR12": "worse_depressed",
            "DSTNGD12": "worse_worthless",
            "IMPCONCN": "diff_concentration",
            "IMPGOUT":  "diff_leaving_house",
            "IMPPEOP":  "diff_strangers",
            "IMPSOC":   "diff_social",
            "IMPSOCM":  "diff_social2",
            "SUICTHNK": "suicidal_think",
            "ADDPREV":  "sad_period"
        }
    )
    return NSDUH2019df

# output: a data frame containing the cleaned up data from the National Survey on Drug Use and Health 2021
def buildNSDUH2021df():
    colNames = ["AGE3","IRSEX","AUINPYR","AURXYR","YEATNDYR","YESCHFLT","YEPRBSLV","DSTNRV30","DSTHOP30","DSTCHR30","DSTNGD30","DSTWORST","DSTNRV12","DSTHOP12","DSTCHR12","DSTNGD12","IMPCONCN","IMPGOUT","IMPPEOP","IMPSOC","IMPSOCM","SUICTHNK","SUIPLANYR","ADDPREV"]
    fileName = "datasets/National Survey on Drug Use and Health 2021/NSDUH_2021_Tab.txt"
    NSDUH2021df = getColumns(fileName, "txt", colNames)
    
    # Basic clean up
    #Convert values from strings to numeric
    NSDUH2021df = NSDUH2021df.apply(pd.to_numeric, errors='coerce')
    #Remove values over 85 since those are Refused or otherwise useless
    NSDUH2021df = NSDUH2021df[NSDUH2021df < 85]
    #label ages
    NSDUH2021df['AGE3'] = pd.cut(NSDUH2021df['AGE3'], bins=[0, 7, 9, 10, 11, float('inf')],
                    labels=['18-25', '26-34', '35-49', '50-64', '65+'])

    # Rename Columns for Readability
    NSDUH2021df = NSDUH2021df.rename(
        columns = {
            "AGE3":         "age", 
            "IRSEX":        "sex", 
            "AUINPYR":      "in_hospital",
            "AURXYR":       "on_medication",
            "YEATNDYR":     "school",
            "YESCHFLT":     "like_school",
            "YEPRBSLV":     "self_group",
            "DSTNRV30":     "nervous_last30",
            "DSTHOP30":     "hopeless_last30",
            "DSTCHR30":     "depressed_last30",
            "DSTNGD30":     "worthless_last30",
            "DSTWORST":     "worse_month",
            "DSTNRV12":     "worse_nervous",
            "DSTHOP12":     "worse_hopeless",
            "DSTCHR12":     "worse_depressed",
            "DSTNGD12":     "worse_worthless",
            "IMPCONCN":     "diff_concentration",
            "IMPGOUT":      "diff_leaving_house",
            "IMPPEOP":      "diff_strangers",
            "IMPSOC":       "diff_social",
            "IMPSOCM":      "diff_social2",
            "SUICTHNK":     "suicidal_think",
            "SUIPLANYR":    "suicidal_plans",
            "ADDPREV":      "sad_period"
        }
    )
    return NSDUH2021df