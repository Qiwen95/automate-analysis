# automate-analysis
This script automates the analysis of the survey data for NSF-Ethics. Simply edit lines 126-129 to specify the type of data you would like to run. See file functionality below for more information.

Note: This script does not identify duplicate CS entries. Duplicate CS entries are identified during reimbursement eligibility.

## Files:
- surveySetup.py: This script automates the following tasks:
1. Reformatting of columns and removal of extraneous SurveyMonkey columns
2. Reformatting participant entered e-mail addresses to lowercase, without '@rit.edu' or '@g.rit.edu'
3. Subsets the data to the current data collection period. Update this ID in lines 126-129 to reflect what is necessary. The collection ID is provided in SurveyMonkey export (step 1).
4. Finds eligible participants, for the $100 award, who have completed at least 80% of the survey. Selects the winner randomly.
5. Identifies duplicate entries during IT and SE term collection. Duplicate entries are identified in the console and in the spreadsheet:
Duplicate-Entries.csv
6. Formats text responses to their numeric equivalent scale, including items that are reverse-scored. The final formatted data is saved as: Formatted-Data.csv.
7. Rearranges all the columns to fit the master spreadsheet and factor analysis of the IDP scale.

## Requirements:
- Survey-for-ISTE-and-SWEN.csv: download this file from SurveyMonkey, choosing the 'all responses' export option. 
- Python 3.5.2 with pandas, numpy, sys, and re installed.

## Outputs:
- Duplicate-Entries.csv: list of duplicate survey entries
- Eligible-Participants.csv: list of eligible participants that are randomly selected.
- Formatted-Data.csv: formatted survey data

### Notes:
Duplicate entries should not be automatically removed, rather manually reviewed after each phase:

1. The best method of removal is to run the surveySetup.py script once. 
2. Review the Duplicate-Entries.csv and select the best entry for each participant with duplicate entries (identified by repeated name AND email). Generally, the row with the least missing values (see last column) can be selected. If the missing values are the same, its possible to select the row with the most recent end date. However, each response should be reviewed on a case-by-case basis. 
3. Once the rows have been selected, remove any rows from the Survey-for-ISTE-and-SWEN.csv file. Document all duplicate entries, removals, and removal methods in the dropbox folder. 
4. Rerun the 'surveySetup.py' script to select the raffle winner and obtain the final formatted csv file.
