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

    if type == "txt":
        data = pd.read_table(path)
    elif type == "csv" or type == "tsv":
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