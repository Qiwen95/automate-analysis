#!/usr/bin/env python

# title: surveySetup.py
# author: Paula Conn
# version: 2
# status: development
# python_version: 3.5.2
# description: This python script can be used after each IST and SWEN data collection period. It will automatically select a survey winner among eligible students (Eligible-Participants.csv), output repeated entries, and format the results to numeric values with no extraneous columns created by SurveyMonkey.

import pandas as pd
import numpy as np
import re
from random import randint

def formatScale (column_list, data, scale):
    data.iloc[:,column_list] = data.iloc[:,column_list].applymap(lambda s: scale.get(s) if s in scale else s)

# import and format column headers
df=pd.read_csv('Survey-for-ISTE-and-SWEN.csv')
df.columns.values[13:33] = df.iloc[0,13:33]
df.columns.values[43:67] = df.iloc[0,43:67]
df.columns.values[43:51] = [str(col) + '_web' for col in df.columns[43:51]]
df.columns.values[34:42] = df.iloc[0,34:42]
df.columns.values[34:42] = [str(col) + '_exp' for col in df.columns[34:42]]
df.columns=df.columns.str.replace('[^\w\s]','')

# format student e-mails
df.iloc[:,10] = df.iloc[:,10].str.lower()
df.iloc[:,10] = df.iloc[:,10].str.replace('@rit.edu','')
df.iloc[:,10] = df.iloc[:,10].str.replace('@g.rit.edu','')

# subset current collection list
df_ISTE = df.loc[df['Collector ID'] == 98658412].dropna(axis=1, how='all')
df_SWEN= df.loc[df['Collector ID'] == 98658411].dropna(axis=1, how='all')

# combine both survey sets and remove empty columns created by Survey Monkey
df_ISTE_SWEN = df_ISTE.append(df_SWEN)
if ('IP Address' in df_ISTE_SWEN.columns):
    df_ISTE_SWEN = df_ISTE_SWEN.drop('IP Address', 1)

# check eligible students (completed 80% of the survey) and choose winner
eligible = df_ISTE_SWEN.copy()
raffle_threshold = len(df_ISTE_SWEN.columns)*.2

# document and display warning if any entries are duplicates
try:
    dup_emails = pd.concat(g for _, g in eligible.groupby(eligible.iloc[:, 5])if len(g) > 1)
    dup_emails.to_csv('Duplicate-Entries.csv', sep=",")

    dup_eligible  = list(set(dup_emails.iloc[:, 5]).intersection(set(eligible.iloc[:, 5])))
    for dup in dup_eligible:
        if (eligible.iloc[:,5] == dup).sum()>1:
            print("Warning duplicate: " + dup)
except:
    print("No duplicate entries\n")

# add a column calculating the incomplete answers for future reference
eligible['Total Incomplete Answers']= pd.isnull(eligible).astype(int).sum(axis=1)
eligible = eligible.loc[eligible['Total Incomplete Answers']<=raffle_threshold]

# select the raffle winner
random_winner = randint(0,len(eligible))
print('Raffle Winner: ', eligible.iloc[random_winner,4], eligible.iloc[random_winner,5])
eligible.to_csv('Eligible-Participants.csv', sep=",")

# place numeric equivalents for likert questions
defaultScale = {'Agree very much': 6, 'Agree pretty much': 5, 'Agree a little': 4, 'Disagree a little': 3, 'Disagree pretty much': 2, 'Disagree very much': 1}
IDPcolumns = [i for i in range(8,28) if i not in (17,21,22)]
formatScale (IDPcolumns, df_ISTE_SWEN, defaultScale)

# place reverse numeric equivalents for likert (scale:1-6) questions: 10,14,15
reverseScale = {'Agree very much': 1, 'Agree pretty much': 2, 'Agree a little': 3, 'Disagree a little': 4, 'Disagree pretty much': 5, 'Disagree very much': 6}
df_ISTE_SWEN = df_ISTE_SWEN.replace({'I am aware of the problems that disabled people face': reverseScale, 'I dont pity them': reverseScale, 'After frequent contact I find I just notice the person not the disability': reverseScale})

# change questions for experience questions
expScale = {'I have personal experience with this': 2, 'I have knowledge of this': 1}
formatScale (list(range(29,37)), df_ISTE_SWEN, expScale)

# # change software questions
swScale = {'I have heard or read about this': 1, 'I have done this before': 2}
formatScale (list(range(38,46)), df_ISTE_SWEN, swScale)

# change web design questions
webScale = {'I’m familiar with this issue': 1, 'I have taken this issue into account to make the site more accessible for people with disabilities': 2, 'I have taken this issue into account to make it more accessible for people with disabilities': 2}
formatScale (list(range(46,62)), df_ISTE_SWEN, webScale)

# change boolean questions
booleanScale = {"Yes": 1, "No": 0}
formatScale ([62,63], df_ISTE_SWEN, booleanScale)

df_ISTE_SWEN.to_csv('Formatted-Data.csv', sep=",")

