#This python file Is used to store helper functions such as the ones 
#for loading in and cleaning up data
import pandas as pd
    
def readInAndGetWantedColumns(path, type, cols):
    """
    ***DO NOT CHANGE/UPDATE, may mess up visual 1***
    
    One part of data cleaning process, getting only the necessary columns from the dataset,
    and returning a copy of the dataframe so the original one stays intact

    path: path to dataset as string
    type: type of file, such as txt, csv, tsv (string)
    df: the dataframe you want to get the columns for (dataframe)
    cols: a list of strings of the columns you want to keep (list: string)
    
    returns new dataframe with only the wanted columns
    """
    if type == "txt" or type == "tsv":
        df = pd.read_table(path,low_memory=False)
    elif type == "csv":
        df = pd.read_csv(path,low_memory=False)

    df = df[cols]

    return df

def cleanUpCoreTrends(df, id, values):
    """
    ***DO NOT CHANGE/UPDATE, may mess up visual 1***

    df: Core Trends dataframe (Dataframe)
    id = the columns to include in id_vars for melting as a list of strings
    values: columns to include in variable for value_vars as list of strings
    year: year of dataset as int
    dropNA: boolean to whether you want to drop NaN values
    returns cleaned up dataframe in long form
    """

    #Drop column because all values are empty
    df = df.drop(columns=['sns2a'])

    df = df.apply(pd.to_numeric, errors='coerce')

    #Remove refused ages
    df = df[df['age'] < 98]

    #Put age into bins
    df['age'] = pd.cut(df['age'], bins=[0, 26, 35, 50, 65, 97],
                       labels=['18-25', '26-34', '35-49', '50-64', '65+'])

    #Convert to long form
    df = pd.melt(df, id_vars=id, value_vars=values)

    #Put value into bin, useful for labelling later
    #*****Might need to change this in new function if using sns1a - sns1e instead
    df['value'] = pd.cut(df['value'], bins=[0,1,2],
                    labels=['Uses Social Media', 'Doesnt Use Social Media'])

    df = df.dropna()

    return df

def cleanUpNSDUH(df, id, values):
    """
    ***CAN ADD NEW BUCKETS FOR COLUMNS AS NEEDED***

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

    #Simply here for easier finding variables when experimenting
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
        #****Write new buckets here

        
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
        #*******Write new buckets here

        longForm = pd.melt(df, id_vars=id, value_vars=values)
        longForm=longForm.rename(columns={'AGE3': 'age'})

    #Drop any rows where all values are NaN
    longForm = longForm.dropna()

    return longForm


def getPercentage(df, filterVal, groupByCol, year):
    """
    ***DO NOT CHANGE/UPDATE, may mess up visual 1***

    Get percentage for a value in a group

    df: dataframe to get percentage for
    filterVal: value in column you want percentage for. e.g. "yes"
    groupByCol: Column you want to group by. e.g. age
    """

    #Total instances in the group
    totalCount = df.groupby([groupByCol]).agg(count=('value', 'count'))

    #Get only the data you want a percentage for
    filtered = df[df['value'] == filterVal]
    
    #Get count for the filtered results
    filteredCount = filtered.groupby([groupByCol]).agg(count=('value', 'count'))

    #Calculate percentage
    perc = pd.merge(totalCount, filteredCount, left_on='age', right_index=True, suffixes=('_total', '_uses'))
    perc['percentage'] = (perc['count_uses'] / perc['count_total']) * 100

    finalDf = perc.reset_index()

    dataLabel = f"{str(year)} - {filterVal}"
    finalDf['dataset'] = dataLabel

    return finalDf


def allFuncsCoreTrends():
    pass

def allFuncsNSDUH():
    pass