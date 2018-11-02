#!/usr/bin/env python

# title: surveySetup.py
# author: Paula Conn
# version: 2
# status: development
# python_version: 3.5.2
# description: This python script can be used after each IST and SWEN data collection period. It will automatically select a survey winner among eligible students (Eligible-Participants.csv), output repeated entries, and format the results to numeric values with no extraneous columns created by SurveyMonkey.
# latest update: added encoding to work with other computers (11/1/18), added functionality for CS surveys and created ordered output in csv (11/2/18).

try:
    import sys
    import pandas as pd
    import numpy as np
    import re
    from random import randint
    import csv

except ImportError:
    print("Error: missing a library (pandas, numpy, random, re, etc.). Please install.")
    sys.exit()

def formatScale (column_list, data, scale):
    data.iloc[:,column_list] = data.iloc[:,column_list].applymap(lambda s: scale.get(s) if s in scale else s)

def assignScale(data):
    # place numeric equivalents for likert questions
    defaultScale = {'Agree very much': 6, 'Agree pretty much': 5, 'Agree a little': 4, 'Disagree a little': 3, 'Disagree pretty much': 2, 'Disagree very much': 1}
    IDPcolumns = [i for i in range(8,28) if i not in (17,21,22)]
    formatScale (IDPcolumns, data, defaultScale)

    # place reverse numeric equivalents for likert (scale:1-6) questions: 10,14,15
    reverseScale = {'Agree very much': 1, 'Agree pretty much': 2, 'Agree a little': 3, 'Disagree a little': 4, 'Disagree pretty much': 5, 'Disagree very much': 6}
    data = data.replace({'I am aware of the problems that disabled people face': reverseScale, 'I dont pity them': reverseScale, 'After frequent contact I find I just notice the person not the disability': reverseScale})

    # change questions for experience questions
    expScale = {'I have personal experience with this': 2, 'I have knowledge of this': 1}
    formatScale (list(range(29,37)), data, expScale)

    # change software questions
    swScale = {'I have heard or read about this': 1, 'I have done this before': 2}
    formatScale (list(range(38,46)), data, swScale)

    # change web design questions
    webScale = {'I’m familiar with this issue': 1, 'I have taken this issue into account to make the site more accessible for people with disabilities': 2, 'I have taken this issue into account to make it more accessible for people with disabilities': 2}
    formatScale (list(range(46,62)), data, webScale)

    # change boolean questions
    booleanScale = {"Yes": 1, "No": 0}
    formatScale ([62,63], data, booleanScale)
    return(data)

def selectRaffleWinner (df, university, collector1, collector2):
    # format student e-mails
    df.iloc[:,10] = df.iloc[:,10].str.lower()

    if university.lower() == 'rit':
        df.iloc[:,10] = df.iloc[:,10].str.replace('@rit.edu','')
        df.iloc[:,10] = df.iloc[:,10].str.replace('@g.rit.edu','')

    if university.lower() == 'unt':
        df.iloc[:,10] = df.iloc[:,10].str.replace('@unt.edu','')
        df.iloc[:,10] = df.iloc[:,10].str.replace('@g.unt.edu','')

    # subset current collection list
    df_ISTE = df.loc[df['Collector ID'] == collector1].dropna(axis=1, how='all')
    df_SWEN= df.loc[df['Collector ID'] == collector2].dropna(axis=1, how='all')

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
                print("\n Program stopped due to duplicates. Please resolve duplicate entries in the spreadsheet and run the program again. \n")
                sys.exit()
    except:
        print("No duplicate entries\n")

    # add a column calculating the incomplete answers for future reference
    eligible['Total Incomplete Answers']= pd.isnull(eligible).astype(int).sum(axis=1)
    eligible = eligible.loc[eligible['Total Incomplete Answers']<=raffle_threshold]

    # select the raffle winner
    random_winner = randint(0,len(eligible))
    print('Raffle Winner: ', eligible.iloc[random_winner,4], eligible.iloc[random_winner,5])
    eligible.to_csv('Eligible-Participants.csv', sep=",")

    return(df_ISTE_SWEN)

def arrangeData (data):
    # arrange data based on master spreadsheet
    try:
        order=pd.read_csv('Column-Order.csv', encoding = "utf-8")
    except (FileNotFoundError, OSError, UnicodeDecodeError):
        print('\nThe CSV file for the final column order was not found OR was not in utf-8 format. Please add the spreadsheet to the location of this file and name it: Column-Order.csv\n')
        sys.exit()

    # remove punctuation in column headers
    data.columns = data.columns.str.replace(r'[^\w\s]+', '')

    reordered_data = data.reindex(columns=list(order))

    mismatch_columns = list(set(reordered_data) - set(data))
    if len(mismatch_columns) > 0:
        print('\nColumns the columns do not match, please check both the Column-Order.csv and Survey-for-ISTE-and-SWEN.csv. Below are the mismatched columns:\n %s \n', mismatch_columns)
        sys.exit()

    return(reordered_data)

def main():
    ##################
    # Change the variables below to what you need:
    ##################
    collector1 = 99039395
    collector2 = None #Assign to None if CS  
    university = 'rit'
    isCS = False

    ################

    try:
        df=pd.read_csv('Survey-for-ISTE-and-SWEN.csv', encoding = "utf-8")
    except (FileNotFoundError, OSError):
        print('\nThe CSV file was not found. Please add the spreadsheet to the location of this file and name it: Survey-for-ISTE-and-SWEN.csv\n')
        sys.exit()

    # import and format column headers
    df.columns.values[13:33] = df.iloc[0,13:33]
    df.columns.values[43:67] = df.iloc[0,43:67]
    df.columns.values[43:51] = [str(col) + '_web' for col in df.columns[43:51]]
    df.columns.values[34:42] = df.iloc[0,34:42]
    df.columns.values[34:42] = [str(col) + '_exp' for col in df.columns[34:42]]
    df.columns=df.columns.str.replace('[^\w\s]','')

    if isCS:
        df = df.loc[df['Collector ID'] == collector1].dropna(axis=1, how='all')

        if ('IP Address' in df.columns):
            df = df.drop('IP Address', 1)

    else:
        if None in (collector1, collector2):
            print('\nA collector ID was not found. When running non-CS data, please enter both collector IDs for IT and SE students.\n')
            sys.exit()

        df = selectRaffleWinner(df, university, collector1, collector2)

    df = assignScale(df)
    df = arrangeData(df)
    df.to_csv('Formatted-Data.csv', sep=",", encoding = 'utf-8-sig')


if __name__ == '__main__':
    main()

