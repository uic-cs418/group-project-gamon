import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, Ridge, Lasso
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, RobustScaler, Normalizer, QuantileTransformer, PowerTransformer
from sklearn.metrics import mean_squared_error, r2_score
from helper_code import readInAndGetWantedColumns, cleanUpNSDUH

# INTMOB - Access internet on a mobile device of somesort - (1 Yes, 2 No)
# INTFREQ - Internet Frequency - 1 Constantly, 2 Several Times, 3 About once a day, 4 Several times a week, 5 Less often, 6 Dont know, Refused
# SNSINT2 - Use of Facebook, Twitter, Instagram - 1 Yes, 2 No, 3 Dont know, 4 Refused
# WEB1a Use of Twitter 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1b Use of Instagram 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1c Use of Facebook 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1d Use of Snapchat 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1e Use of YouTube 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1f Use of WhatsApp 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1g Use of Pinterest 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1h Use of LinkedIn 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1i Use of Reddit 1 Yes, 2 No, 3 Dont Know, 4 Refused
# WEB1j Use of TikTok 1 Yes, 2 No, 3 Dont Know, 4 Refused
# Inc - Income ranges
def predictUsageOfAgeGroups(data: pd.DataFrame):
    """
        
    """
    data['age'] = pd.cut(data['age'], bins=[0, 24, 34, 44, 54, 64, float('inf')],
                       labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+'])
    selected = ['intfreq', 'web1a', 'web1b', 'web1c', 'web1d', 'web1e', 'web1f', 'web1g',
                'web1h', 'sex']
    X = data[selected]
    y = data['age']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    scaler = StandardScaler()
    X_train_scaled  = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    svm_classifier = SVC(kernel='rbf', C=1, random_state=42)
    svm_classifier.fit(X_train_scaled, y_train)

    y_pred = svm_classifier.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")

    # print("Classification Report:")
    # print(classification_report(y_test, y_pred))

    # Commenting out for the purpose of space on notebook
    # print("Confusion Matrix:")
    # print(confusion_matrix(y_test, y_pred))


def feature_selection(X: pd.DataFrame, y: pd.Series, n_features=None):
    """ 
        X should be the entire dataframe
        Y should be the 'target' variable
        n_features should be the number of features you want to select/keep
    """
    model = LinearRegression()
    rfe = RFE(model, n_features_to_select=n_features)
    rfe.fit(X, y)
    selected_features = X.columns[rfe.support_]
    feature_ranking = pd.Series(rfe.ranking_, index=X.columns)
    print("Selected_features")
    print(selected_features)

    print("Feature ranking:")
    print(feature_ranking)

def convertObjects(data: pd.DataFrame) -> pd.DataFrame:
    """
        This will grab columns in the data frame that are of type object
        and convert them to integer, most likely floats which is still fine
    """
    copy = data.copy()
    columns = copy.select_dtypes(include=['object'])
    for column in columns.columns:
        copy[column] = pd.to_numeric(copy[column], errors='coerce', downcast='integer')
    copy.fillna(-1, inplace=True)
    return copy

def randomForest(data: pd.DataFrame, target):
    """
    X: entire dataframe
    y: target series, i.e what you want to train
    target: name of target column

    """
    y = data[target]
    X = data.drop([target], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Commenting out for the sake of space in notebook
    # cm = confusion_matrix(y_test, y_pred)
    # print(f'Confusion Matrix:\n{cm}')

    # cr = classification_report(y_test, y_pred, zero_division=1)
    # print(f'Classification report:\n{cr}')



def linearRegression(target, dataset):

    if dataset == "NSDUH":
        data = concatAndCleanNSDUH()
    elif dataset == "CoreTrends":
        data = concatAndCleanCoreTrends(True)


    y = data[[target]]
    print(y.head())
    print()

    y = y.values.reshape(-1,1)
    X = data.drop([target], axis=1)

    print(X.head())


    standardScaler = StandardScaler().fit_transform(y)
    min_max_scaler = MinMaxScaler().fit_transform(y)
    max_abs_scaler = MaxAbsScaler().fit_transform(y)
    robust_scaler = RobustScaler().fit_transform(y)
    normalizer = Normalizer().fit_transform(y)
    quantile_transformer = QuantileTransformer().fit_transform(y)
    power_transformer = PowerTransformer().fit_transform(y)

    scalers = [ (y,"no scalar"), (standardScaler, "standard scalar"), (min_max_scaler, 'min_max_scaler'),(max_abs_scaler, 'max_abs_scaler'),(robust_scaler, 'robust_scaler'),(normalizer, 'normalizer'),(quantile_transformer, 'quantile_transformer'),(power_transformer, 'power_transformer')]
    test_split = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

    min_mse = float('inf')
    max_r2 = float("-inf")
    best_model = {}
    for (scaler, name) in scalers:
        for i in test_split:
            X_train, X_test, y_train, y_test = train_test_split(X, scaler, test_size=i, random_state=333)
            clf = LinearRegression().fit(X_train, y_train)
            # clf = Lasso(alpha=0.7).fit(X_train, y_train)
            y_pred = clf.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            print(clf.score(X_train, y_train))
            print(scaler[:5])
            print(f'MSE log regression {name} test-split-{i} | MSE: {mse :.2f} r2: {r2 :.2f}')
            print()

            if (mse < min_mse and r2 > max_r2) and (mse != 0 and r2 != 1):
                min_mse = mse
                max_r2 = r2
                best_model["Scalar"] = name
                best_model["test-split"] = i
                best_model["MSE"] = mse
                best_model["r2"] = r2

    print("Best MSE")
    print(best_model)


def concatAndCleanNSDUH():
    #read in data
    print("Reading in datasets")
    NSDUH2021Cols = ["CATAG6", "AGE3","IRSEX","AUINPYR","AURXYR","YEATNDYR","YESCHFLT","YEPRBSLV","DSTNRV30","DSTHOP30","DSTCHR30","DSTNGD30","DSTWORST","DSTNRV12","DSTHOP12","DSTCHR12","DSTNGD12","IMPCONCN","IMPGOUT","IMPPEOP","IMPSOC","IMPSOCM","SUICTHNK","SUIPLANYR","ADDPREV"]
    NSDUH201819Cols = ["CATAG6", "AGE2", "IRSEX", "AUINPYR","AURXYR","YEATNDYR","YESCHFLT","YEPRBSLV","DSTNRV30","DSTHOP30","DSTCHR30","DSTNGD30","DSTWORST","DSTNRV12","DSTHOP12","DSTCHR12","DSTNGD12","IMPCONCN","IMPGOUT","IMPPEOP","IMPSOC","IMPSOCM","SUICTHNK","ADDPREV"]
    print("NSDUH2019: ")
    NSDUH2019_wantedCols = readInAndGetWantedColumns("datasets/National Survey on Drug Use and Health 2019/NSDUH_2019_Tab.txt", "txt", NSDUH201819Cols)
    print(" - Done")
    print("NSDUH2018: ")
    NSDUH2018_wantedCols = readInAndGetWantedColumns("datasets/National Survey on Drug Use and Health 2018/NSDUH_2018_Tab.tsv", "tsv", NSDUH201819Cols)
    print(" - Done")
    print("NSDUH2021: ")
    NSDUH2021_wantedCols = readInAndGetWantedColumns("datasets/National Survey on Drug Use and Health 2021/NSDUH_2021_Tab.txt", "txt", NSDUH2021Cols)
    print(" - Done")
    print("Finished reading datasets")

    # NSDUH2021_wantedCols.rename(columns={'AGE3': 'AGE2'}, inplace=True)

    # #Create buckets for consistent labels for age
    # NSDUH2018_wantedCols['AGE2'] = pd.cut(NSDUH2018_wantedCols['AGE2'], bins=[0, 13, 15, 16, 17, float('inf')],
    #                     labels=[0, 1, 2, 3, 4])
    # NSDUH2019_wantedCols['AGE2'] = pd.cut(NSDUH2019_wantedCols['AGE2'], bins=[0, 13, 15, 16, 17, float('inf')],
    #                     labels=[0, 1, 2, 3, 4])
    # NSDUH2021_wantedCols['AGE2'] = pd.cut(NSDUH2021_wantedCols['AGE2'], bins=[0, 7, 9, 10, 11, float('inf')],
    #                     labels=[0, 1, 2, 3, 4])

    NSDUH_all = pd.concat([NSDUH2019_wantedCols,NSDUH2018_wantedCols, NSDUH2021_wantedCols], ignore_index=True)

    NSDUH_slim = NSDUH_all[['CATAG6', 'IRSEX', 'DSTCHR12', 'DSTHOP12', 'IMPSOC']]
    NSDUH_slim = NSDUH_slim.apply(pd.to_numeric, errors='coerce')
    NSDUH_slim.fillna(0, inplace=True)

    #Remove refused vals
    NSDUH_slim = NSDUH_slim[NSDUH_slim['DSTCHR12'] < 85]
    NSDUH_slim = NSDUH_slim[NSDUH_slim['IMPSOC'] < 85]
    NSDUH_slim = NSDUH_slim[NSDUH_slim['DSTHOP12'] < 85]

    return NSDUH_slim




def concatAndCleanCoreTrends(getSums: bool) -> pd.DataFrame:
    """
    getSums: whether or not you want to get sums of web1(which social media they use) and sns(how frequently they use social media)
    returns: combined dataframe of all CoreTrend years
    """
    #read in data
    CoreTrends2021Cols = ["web1a", "web1b", "web1c", "web1d", "web1e","sns2a", "sns2b", "sns2c", "sns2d", "sns2e","gender", "age"]
    CoreTrends2019Cols = ["web1a", "web1b", "web1c", "web1d", "web1e","sns2a", "sns2b", "sns2c", "sns2d", "sns2e","sex", "age"]
    CoreTrends2018Cols = ["web1a", "web1b", "web1c", "web1d", "web1e","sns2a", "sns2b", "sns2c", "sns2d", "sns2e","sex", "age"]
    CoreTrends2021_wantedCols = readInAndGetWantedColumns("datasets/Jan-25-Feb-8-2021-Core-Trends-Survey/Jan 25-Feb 8, 2021 - Core Trends Survey - CSV.csv", "csv", CoreTrends2021Cols)
    CoreTrends2019_wantedCols = readInAndGetWantedColumns("datasets/January-8-February-7-2019-Core-Trends-Survey-SPSS/January 8-February 7, 2019 - Core Trends Survey - CSV.csv", "csv", CoreTrends2019Cols)
    CoreTrends2018_wantedCols = readInAndGetWantedColumns("datasets/January 3-10, 2018 - Core Trends Survey/January 3-10, 2018 - Core Trends Survey - CSV.csv", "csv", CoreTrends2018Cols)

    CoreTrends2021_wantedCols.rename(columns={'gender': 'sex'}, inplace=True)
    CoreTrends_all = pd.concat([CoreTrends2018_wantedCols,CoreTrends2019_wantedCols, CoreTrends2021_wantedCols], ignore_index=True)

    #Concat all dataframes and convert answers to numeric
    CoreTrends_all = CoreTrends_all.apply(pd.to_numeric, errors='coerce')
    CoreTrends_all.fillna(0, inplace=True)

    web1_SMused = ["web1a", "web1b", "web1c", "web1d", "web1e"]
    sns_SMfrequency = ["sns2a", "sns2b", "sns2c", "sns2d", "sns2e"]

    CoreTrends_all = CoreTrends_all[CoreTrends_all['age'] < 98]
    CoreTrends_all = CoreTrends_all[CoreTrends_all['sex'] < 98]
    mask = CoreTrends_all[["sns2a", "sns2b", "sns2c", "sns2d", "sns2e","web1a", "web1b", "web1c", "web1d", "web1e"]] >= 8
    CoreTrends_all[~mask.any(axis=1)]
    CoreTrends_all[web1_SMused] = CoreTrends_all[web1_SMused].replace(2,0)

    # 0: 18-25 | 1: 26-35 | 2: 35-49 | 3: 50-64 | 4: 65+
    CoreTrends_all['age'] = pd.cut(CoreTrends_all['age'], bins=[0, 26, 35, 50, 65, 97],
                    labels=[0, 1, 2, 3, 4])
    
    #create sum columns
    if getSums:
        # CoreTrends_all['SM_usedTotal'] = CoreTrends_all[web1_SMused].sum(axis=1)
        CoreTrends_all['SM_frequencySum'] = CoreTrends_all[sns_SMfrequency].sum(axis=1)
        # CoreTrends_all = CoreTrends_all.drop(["web1a", "web1b", "web1c", "web1d", "web1e","sns2a", "sns2b", "sns2c", "sns2d", "sns2e"], axis=1)
        CoreTrends_all = CoreTrends_all.drop(sns_SMfrequency, axis=1)

    print(CoreTrends_all.head())
    return CoreTrends_all


# Pretty much playground code, ignore for now
if __name__ == '__main__':
    drop_columns = ['usr', 'pial5b', 'pial5c', 'pial5d', 'pial11a', 'pial11ao@', 'pial12']
    nsduh2018 = pd.read_csv('datasets/January 3-10, 2018 - Core Trends Survey/January 3-10, 2018 - Core Trends Survey - CSV.csv')
    nsduh2019 = pd.read_csv('datasets/January-8-February-7-2019-Core-Trends-Survey-SPSS/January 8-February 7, 2019 - Core Trends Survey - CSV.csv')
    nsduh2021 = pd.read_csv('datasets/Jan-25-Feb-8-2021-Core-Trends-Survey/Jan 25-Feb 8, 2021 - Core Trends Survey - CSV.csv')
    # nsduh2019.info()
    # nsduh2021.info()
    # merged = pd.concat([nsduh2018, nsduh2019, nsduh2021], axis=0)
    # print('====================================================================')
    # merged.info()
    # cleaned_data = to_numeric(merged, 'intfreq')
    # merged.info()
    # cleaned_data.value_counts()

    # nsduh2018 = nsduh2018.drop(drop_columns, axis=1)
    # nsduh2018 = convertObjects(nsduh2018)
    # nsduh2018.info()
    # randomForest(nsduh2018, 'intfreq')

    print("---linear Regression---")
    linearRegression("IMPSOC", "NSDUH")
    print()

    # print("KNN frequency")
    # KNN('SM_frequencySum')

    # print("\nKNN usedTotal")
    # KNN('SM_usedTotal')
