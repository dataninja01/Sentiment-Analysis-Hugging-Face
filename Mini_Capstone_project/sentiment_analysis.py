# -*- coding: utf-8 -*-
"""Sentiment analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j29qTTah2JvZiP7D5FsdOU2T1VEcIRLs
"""

import nltk
nltk.download('vader_lexicon')
import pandas as pd
import numpy as np

import sklearn 
from sklearn.pipeline import Pipeline
from sklearn.metrics import *

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from pathlib import Path
import joblib
import os
#%%
# store model version
sklearn_version = sklearn.__version__

#%%

from datasets import load_dataset

dataset = load_dataset("imdb")
#%%
train= dataset['train']

test= dataset['test']
#%%
df_train = pd.DataFrame.from_dict(train)

df_test = pd.DataFrame.from_dict(test)

#%%
#Checking for null and blank reviews in training dataset

df_train.dropna(inplace=True)


blanks1 = []  # start with an empty list
for i,rv, lb, in df_train.itertuples():  # iterate over the DataFrame
    if type(rv)==str:            # avoid NaN values
        if rv.isspace():         # test 'review' for whitespace
            blanks1.append(i)     # add matching index numbers to the list
df_train.drop(blanks1, inplace=True)
#%%
#Checking for null and blank reviews in test dataset

df_test.dropna(inplace=True)


blanks2 = []  # start with an empty list

for i,rv, lb, in df_test.itertuples():  # iterate over the DataFrame
    if type(rv)==str:            # avoid NaN values
        if rv.isspace():         # test 'review' for whitespace
            blanks2.append(i)     # add matching index numbers to the list
df_test.drop(blanks2, inplace=True)
#%%
#Text classification using Linear Support VEctor Classifier
text_clf = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC(max_iter=5000))])
#%%
y_train = df_train['label']
X_train = df_train['text']
y_test = df_test['label']
X_test = df_test['text']
#%%
text_clf.fit(X_train, y_train)
#%%
predictions = text_clf.predict(X_test)
#%%
test_accuracy = accuracy_score(y_test,predictions)
#%%
# store job objects & metadata
text_clf_pipeline_param = {}
text_clf_pipeline_param['pipeline'] = text_clf
text_clf_pipeline_param['class labels'] = {0:"negative", 1: "positive"}
text_clf_pipeline_param['sklearn version'] = sklearn_version
text_clf_pipeline_param['test accuracy'] = test_accuracy

# %%
# create models dir if not present
Path(os.path.join(os.getcwd(),"models")).mkdir(parents=True, exist_ok=True)
# dump pipeline w metadata
out_filename = "models/pipe_clf_checkpoint.joblib"
joblib.dump(text_clf_pipeline_param, out_filename)