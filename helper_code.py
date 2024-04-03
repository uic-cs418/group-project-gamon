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

def cleanUpCoreTrends(df, id, values, year, dropNA):
    """
    df: Core Trends dataframe (Dataframe)
    id = the columns to include in id_vars for melting as a list of strings
    values: columns to include in variable for value_vars as list of strings
    year: year of dataset as int
    dropNA: boolean to whether you want to drop NaN values
    returns cleaned up dataframe in long form
    """

    #Drop column because all values are empty
    df = df.drop(columns=['sns2a'])

    #Remove refused ages
    df = df[df['age'] < 98]

    df['age'] = pd.cut(df['age'], bins=[0, 26, 35, 50, 65, 97],
                       labels=['18-25', '26-34', '35-49', '50-64', '65+'])

    try:
        if year == 2021:
            pass
        df = pd.melt(df, id_vars=id, value_vars=values)
        # df['age'] = df['age'].map(age_mapping_CoreToNSDUH2018)
    except:
        df = pd.melt(df, id_vars=id, value_vars=values)
        # df['age'] = df['age'].map(age_mapping_CoreToNSDUH2021)

    if dropNA:
        df = df.dropna()

    return df

def cleanUpNSDUH(df, id, values, year):
    """
    Main code to clean up NSDUH dataset specifically

    df: NSDUH dataframe
    id = the columns to include in id_vars for melting as a list of strings
    values: columns to include in variable for value_vars as list of strings
    year: year of dataset as int
    returns cleaned up dataframe in long format
    """

    #Convert values from strings to numeric
    df = df.apply(pd.to_numeric, errors='coerce')

    #Remove values over 85 since those are Refused or otherwise useless
    df = df[df < 85]

    holder = ['IRSEX', 'AUINPYR', 'AURXYR', 'YEATNDYR', 'YESCHFLT',
            'YEPRBSLV', 'DSTNRV30', 'DSTHOP30', 'DSTCHR30', 'DSTNGD30', 'DSTWORST',
            'DSTNRV12', 'DSTHOP12', 'DSTCHR12', 'DSTNGD12', 'IMPCONCN', 'IMPGOUT',
            'IMPPEOP', 'IMPSOC', 'IMPSOCM', 'SUICTHNK', 'ADDPREV']
    
    #Convert to long form
    try:
        df['AGE2'] = pd.cut(df['AGE2'], bins=[0, 13, 15, 16, 17, float('inf')],
                       labels=['18-25', '26-34', '35-49', '50-64', '65+'])
        df['DSTCHR30'] = pd.cut(df['DSTCHR30'], bins=[0, 4, 5],
                       labels=['some depressed', 'little-no depression'])
        df['IMPCONCN'] = pd.cut(df['IMPCONCN'], bins=[0, 2, 5],
                       labels=['No Concentration Issues', 'Concentration Issues'])
        df['DSTNRV12'] = pd.cut(df['DSTNRV12'], bins=[0, 4, 5],
                       labels=['Nervous', 'Not Nervous'])
        df['DSTCHR12'] = pd.cut(df['DSTCHR12'], bins=[0, 4, 5],
                       labels=['Depressed', 'Not Depressed'])
        
        longForm = pd.melt(df, id_vars=id, value_vars=values)
        longForm=longForm.rename(columns={'AGE2': 'age'})
    except:
        df['AGE3'] = pd.cut(df['AGE3'], bins=[0, 7, 9, 10, 11, float('inf')],
                       labels=['18-25', '26-34', '35-49', '50-64', '65+'])
        #Create buckets, at least some depression and little to no depression
        df['DSTCHR30'] = pd.cut(df['DSTCHR30'], bins=[0, 1, 4],
                       labels=['some depressed', 'little-no depression'])
        df['IMPCONCN'] = pd.cut(df['IMPCONCN'], bins=[0, 2, 5],
                       labels=['No Concentration Issues', 'Concentration Issues'])
        df['DSTNRV12'] = pd.cut(df['DSTNRV12'], bins=[0, 4, 5],
                       labels=['Nervous', 'Not Nervous'])
        df['DSTCHR12'] = pd.cut(df['DSTCHR12'], bins=[0, 4, 5],
                       labels=['Depressed', 'Not Depressed'])

        longForm = pd.melt(df, id_vars=id, value_vars=values)
        longForm=longForm.rename(columns={'AGE3': 'age'})

    #Drop any rows where all values are NaN
    longForm = longForm.dropna()

    return longForm
