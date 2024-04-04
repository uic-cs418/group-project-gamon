import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import numpy as np

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

    print("Classification Report:")
    print(classification_report(y_test, y_pred))

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

    cr = classification_report(y_test, y_pred)
    print(f'Classification report:\n{cr}')


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
    nsduh2018 = nsduh2018.drop(drop_columns, axis=1)
    nsduh2018 = convertObjects(nsduh2018)
    nsduh2018.info()
    randomForest(nsduh2018, 'intfreq')
