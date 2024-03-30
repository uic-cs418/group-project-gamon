#This python file Is used to store helper functions such as the ones 
#for loading in and cleaning up data
import pandas as pd

def readInData(path, type):
    """
    path: path to dataset (string)
    type: type of file, such as txt, csv, tsv (string)

    returns a dataframe 
    """

    data = pd.DataFrame()

    #Read in the data based on file type
    if type == "txt":
        data = pd.read_table(path)
    elif type == "csv" or type == "tsv":
        data = pd.read_csv(path)
    else:
        print("Unsupported data format")
        return
    
    if data == None:
        print("Something went wrong reading in data")

    return data
    
def getWantedColumns(df, cols):
    """
    df: the dataframe you want to get the columns for (dataframe)
    cols: a list of strings of the columns you want to keep (list: string)
    """

    df_copy = df.copy(deep=True)
    df_copy = df_copy[cols]

    return df_copy