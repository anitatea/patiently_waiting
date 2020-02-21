# model data

# from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
from sklearn.pipeline import make_pipeline
from sklearn_pandas import DataFrameMapper, CategoricalImputer

import pandas as pd
import pickle

# import clean data
df = pd.read_csv('data_final.csv')

X = df.drop(['OrgName', 'orgSort','WaitTime_percent_within_target', 'ResultType', 'Target', 'PriorityDescription'], axis=1)

target = 'WaitTime_mean'
X = X.drop(target, axis=1)

df.sample(1)
df.iloc[0,1]

y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

mapper = DataFrameMapper([
    ('Key', [CategoricalImputer(), LabelBinarizer()]),
    ('day', [LabelBinarizer()]),
    (['Org_ID'], [SimpleImputer(), PolynomialFeatures(include_bias=False), StandardScaler()]),
    (['WaitTime_90percentile'], [SimpleImputer(), PolynomialFeatures(include_bias=False), StandardScaler()]),
    (['case_per_day'], [SimpleImputer(), PolynomialFeatures(include_bias=False), StandardScaler()])
    # (['case_per_month'], [SimpleImputer(), PolynomialFeatures(include_bias=False), StandardScaler()])
])

# score of 0.9837560259894104
est = GradientBoostingRegressor(n_estimators=100, max_depth=1)
pipe = make_pipeline(mapper, est)
pipe.fit(X_train, y_train)
pipe.score(X_test, y_test)

pickle.dump(pipe, open('model/pipe.pkl', 'wb'))

# # load from a model
# del pipe
# pipe = pickle.load(open('model/pipe.pkl', 'rb'))
