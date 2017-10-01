# automate-analysis
Series of scripts and programs to automate NSF-Ethics analysis and improve result reliability

## Files:
- surveySetup.py: This script automates the following tasks:
1. Reformatting of columns and removal of extraneous SurveyMonkey columns
2. Reformatting participant entered e-mail addresses to lowercase, without '@rit.edu' or '@g.rit.edu'
3. Subsets the data to the current data collection period. Update this ID in row 33 and 34 to reflect what is necessary. The collection ID is provided in SurveyMonkey export (step 1).
4. Finds eligible participants, for the Amazon giftcard, who have completed at least 80% of the survey. Selects the winner randomly.
5. Formats text responses to their numeric equivalent scale. The final formatted data is saved as: Formatted-Data.csv.

## Requirements:
- Survey-for-ISTE-and-SWEN.csv: download this file from SurveyMonkey, choosing the 'all responses' export option. 
- Python 3.5.2 with pandas, numpy, and re installed.

## Outputs:
- Duplicate-Entries.csv: list of duplicate survey entries
- Eligible-Participants.csv: list of eligible participants that are randomly selected.
- Formatted-Data.csv: formatted survey data

### Notes:
- Duplicate entries should not be automatically removed, rather manually reviewed after each phase. The best method of removal is to run the surveySetup.py script once. Then, review the Duplicate-Entries.csv and select the best entry for each participant with duplicate entries (identified by repeated name AND email). Generally, the row with the least missing values (see last column) can be selected. If the missing values are the same, its possible to select the row with the most recent end date. However, each response should be reviewed on a case-by-case basis. All duplicate entries, removals, and removal methods can be updated in the dropbox file. Once the rows have been selected, remove any rows from the Survey-for-ISTE-and-SWEN.csv file. Finally, rerun the 'surveySetup.py' script to select the raffle winner and obtain the formatted csv file.
