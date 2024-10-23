# -*- coding: utf-8 -*-
"""Project-1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Qd33SFG3KlF2dGVScXD5iQRzguUxBXq9
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("churn.csv")

df

df.describe()

sns.set_style(style="whitegrid")

plt.figure(figsize=(12,10))

sns.countplot(x="Exited", data=df)
plt.title("Distribution of Churn")

sns.histplot(data=df, x="Age", kde=True)
plt.title("Age Distribution")

sns.scatterplot(data=df, x="CreditScore", y="Age", hue="Exited")
plt.title("Credit Score vs Age")

sns.boxplot(x="Exited", y="Balance" , data=df)
plt.title("Balance Distribution by Churn")

sns.boxplot(x="Exited", y="CreditScore" , data=df)
plt.title("Credit Score Distribution by Churn")

features = df.drop("Exited", axis =1) #axis 1 dropping a column not a row

features

target = df["Exited"]

target

features = features.drop(["RowNumber", "CustomerId", "Surname"], axis =1)

features

features= features.dropna() # handle missing values

features

features = pd.get_dummies(features, columns=["Geography", "Gender"]) # one hot encoding

features

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)

X_train[0]

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import xgboost as xgb

from sklearn.ensemble import RandomForestClassifier
#I added this one
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB



lr_model = LogisticRegression(random_state=42)

lr_model.fit(X_train, y_train)

lr_predictions = lr_model.predict(X_test)

lr_predictions

lr_accuracy = accuracy_score(y_test, lr_predictions)

lr_accuracy

def evaulate_and_save_model(model, X_train, X_test, y_train, y_test, filename):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{model.__class__.__name__} Accuracy: {accuracy:.4f}")
    print(f"\nClassification Report :\n{classification_report(y_test, y_pred)}")
    print("-------------------------")
    with open(filename, "wb") as file:
      pickle.dump(model, file)
    print(f"Model saved as {filename}")

xgb_model = xgb.XGBClassifier(random_state= 42)
evaulate_and_save_model(xgb_model , X_train, X_test, y_train, y_test, "xgb_model.pkl" )

dt_model = DecisionTreeClassifier(random_state = 42)
evaulate_and_save_model(dt_model , X_train, X_test, y_train, y_test, "dt_model.pkl" )

rf_model = RandomForestClassifier(random_state = 42)
evaulate_and_save_model(rf_model , X_train, X_test, y_train, y_test, "rf_model.pkl" )

nb_model = GaussianNB()
evaulate_and_save_model(nb_model , X_train, X_test, y_train, y_test, "nb_model.pkl" )

knn_model = KNeighborsClassifier()
evaulate_and_save_model(knn_model , X_train, X_test, y_train, y_test, "knn_model.pkl" )

svm_model = SVC(random_state = 42)
evaulate_and_save_model(svm_model , X_train, X_test, y_train, y_test, "svm_model.pkl" )

# Initialize the Bagging Classifier
bc_model = BaggingClassifier(random_state=42)

# Evaluate and save the Bagging Classifier model
evaulate_and_save_model(bc_model, X_train, X_test, y_train, y_test, "bc_model.pkl")

feature_importances = xgb_model.feature_importances_
feature_names = features.columns

feature_importances

feature_names

feature_importances_df = pd.DataFrame(
    {
        'feature' :feature_names,
        'importance':feature_importances
    }
)

feature_importances_df

feature_importances_df = feature_importances_df.sort_values('importance', ascending =False)

feature_importances_df

plt.figure(figsize=(10,6))
plt.bar(feature_importances_df['feature'], feature_importances_df['importance'])
plt.xticks(rotation=90)
plt.xlabel('features')
plt.ylabel('importance')
plt.tight_layout()
plt.show()

features

features['CLV'] = df['Balance']*df['EstimatedSalary'] / 100000

features

features['AgeGroup'] = pd.cut(df['Age'], bins=[0,30, 45, 60, 100], labels =['Young', 'MiddleAge','Senior', 'Elderly'])

features

features['TenureAgeRatio'] = df['Tenure']/ df['Age']

features

features = pd.get_dummies(features, drop_first=True)
features

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
X_train

xgboost_model = xgb.XGBClassifier(random_state=42)
evaulate_and_save_model(xgboost_model, X_train, X_test, y_train, y_test, "xgboost-featureEngineered.pkl")

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state = 42)

X_resampled , y_resampled = smote.fit_resample(X_train, y_train)
evaulate_and_save_model(xgboost_model, X_resampled, X_test, y_resampled, y_test, "xgboost-SMOTE.pkl")

from sklearn.ensemble import VotingClassifier



voting_clf = VotingClassifier(
    estimators = [('xgboost', xgb.XGBClassifier(random_state=42)),('rf', RandomForestClassifier(random_state=42)),('svm', SVC(random_state=42, probability=True))],
    voting = 'hard'
)

evaulate_and_save_model(voting_clf, X_resampled, X_test, y_resampled, y_test, "voting_clf.pkl")



