#This python file Is used to store helper functions such as the ones 
#for loading in and cleaning up data
import pandas as pd

def readInData(path, type):
    """
    Reads in the data into a dataframe, this function may be kinda useless but
    it can clean up the code and make changes a bit easier

    path: path to dataset (string)
    type: type of file, such as txt, csv, tsv (string)

    returns a dataframe 
    """

    if type == "txt" or type == "tsv":
        data = pd.read_table(path)
    elif type == "csv":
        data = pd.read_csv(path)
    else:
        print("Unsupported data format")
        return

    return data
    
def getWantedColumns(df, cols):
    """
    One part of data cleaning process, getting only the necessary columns from the dataset,
    and returning a copy of the dataframe so the original one stays intact

    df: the dataframe you want to get the columns for (dataframe)
    cols: a list of strings of the columns you want to keep (list: string)
    
    returns new dataframe with only the wanted columns
    """

    df_copy = df.copy(deep=True)
    df_copy = df_copy[cols]

    return df_copy

def cleanUpNSDUH(df):
    """
    Main code to clean up NSDUH dataset specifically

    df: NSDUH dataframe

    returns cleaned up dataframe
    """

    #Convert values from strings to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    #Remove values over 85 since those are Refused or otherwise useless
    df = df[df < 85]

    #Drop any rows where all values are NaN
    df.dropna(axis=0, how='all', inplace=True)

    return df

def convertAndMergeCoreTrendstoNSDUH(coreTrends_df, NSDUH_df, year):
    """
    This takes two datasets, matches the age column values and merges them
    *This may need to be updated to be more generalized

    df1: left dataframe
    df2: right dataframe
    year: which year is the dataset from (int)
    returns merged dataframe
    """

    #This dictionart works for Core Trends 2018 and 2019
    age_mapping_CoreToNSDUH2018 = { 12: 1, 13: 2, 14: 3, 15: 4, 16: 5, 17: 6, 18: 7, 19: 8, 20: 9, 21: 10, 22: 11, 23: 11, 24: 12, 25: 12, 
                                   **{age: 13 for age in range(26, 30)}, **{age: 14 for age in range(30, 35)}, **{age: 15 for age in range(35, 50)}, **{age: 16 for age in range(50, 65)}, **{age: 17 for age in range(65, 100)}
    }

    age_mapping_CoreToNSDUH2021 = {12: 1, 13: 1, 14: 2, 15: 2, 16: 3, 17: 3, 18: 4, 19: 4, 20: 4, 21: 5, 22: 5, 23: 5, 24: 6, 25: 6,
                                   **{age: 7 for age in range(26, 29)}, **{age: 8 for age in range(30, 34)}, **{age: 9 for age in range(35, 49)}, **{age: 10 for age in range(50, 64)}, **{age: 11 for age in range(65, 100)}
    }

    if year == 2018 or year == 2019:
        coreTrends_df['age'] = coreTrends_df['age'].map(age_mapping_CoreToNSDUH2018)
        coreTrends_df['age']  = coreTrends_df['age'].astype('Int64')
        # NSDUH_df['AGE2']  = NSDUH_df['AGE2'].astype('Int64')
        merged = pd.merge(coreTrends_df, NSDUH_df, left_on='age', right_on='AGE2', how='left')

    elif year == 2021:
        coreTrends_df['age'] = coreTrends_df['age'].map(age_mapping_CoreToNSDUH2021)
        coreTrends_df['age']  = coreTrends_df['age'].astype('Int64')
        merged = pd.merge(coreTrends_df, NSDUH_df, left_on='age', right_on='AGE3', how='right')
    else:
        print("Invalid year parameter")
        return
    
    #Convert all values to numeric, 
    #eliminate anything over 85 since those values are either refused or useless according to NSDUH
    # merged = merged.apply(pd.to_numeric, errors='coerce')
    # merged = merged[merged < 85] 

    return merged
