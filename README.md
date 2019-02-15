# automate-analysis
This script automates the analysis of the survey data for NSF-Ethics. Simply edit 
lines 160-163 to specify the type of data you would like to run. See file functionality 
below for more information.


## Files:
- surveySetup.py: This script automates the following tasks:
1. Reformats column headers and removes of extraneous SurveyMonkey columns
2. Reformats participant e-mail addresses to lowercase, without '@rit.edu' or '@g.rit.edu'
3. Subsets the data to the current data collection period. Update this ID in lines 160-163. 
The collection ID is provided in SurveyMonkey export.
4. Finds eligible participants, for the $100 award, who have completed at least 80% 
of the survey. Selects the winner randomly.
5. Identifies duplicate entries during IT and SE term collection. Duplicate entries 
are identified in the console and in the spreadsheet: Duplicate-Entries.csv. As per
protocol, they must be manually reviewed and chosen.
6. Formats text responses to their numeric equivalent scale, including items that 
are reverse-scored. The final formatted data is saved as: Formatted-Data.csv.
7. Rearranges all the columns to fit the master spreadsheet and factor analysis of 
the IDP scale.

- column-order.csv and cs-column-order.csv
These spreadsheets contain the column order used in master spreadsheet. These 
are referenced by surveySetup.py, depending if you choose the CS or IT/SE analysis.

## Requirements:
- Survey-for-ISTE-and-SWEN.csv: download this file from SurveyMonkey, 
choosing the 'all responses' export option. Alternate surveys can also be used,
such as CS survey data, but the file name must be changed in line 168.
- Python 3.5.2 with pandas, numpy, sys, and re installed. Earlier versions of Python
are not adequate as they import the CSV files with incorrect ASCII characters.

## Outputs:
- Duplicate-Entries.csv: list of duplicate survey entries. Resolve these manually in the
Survey-for-ISTE-and-SWEN.csv and run the code again to obtain the final formatted data.
- Eligible-Participants.csv: list of eligible participants for the raffle. Raffle winners
are randomly selected and printed on the console.
- Formatted-Data.csv: formatted survey data

### Notes:
Duplicate entries should not be automatically removed. They must be manually reviewed
on a case-by-case basis. Below are some recommended practices for most instances:

1. Run the surveySetup.py script. The script will identify duplicate entries 
based on the participants' name and email.
2. Review the Duplicate-Entries.csv and select the best entry for each participant.
Generally, the row with the least missing values (e.g., last entry) can be selected. 
If the number of missing values are the same, select the most recent submission. 
Do not combine responses. 
3. Remove duplicate rows from the Survey-for-ISTE-and-SWEN.csv file. Keep only
the entries that are the best collection of the participant's response. 
Document all duplicate entries, removals, and removal methods in the 
'recruitment-counts.csv' file in Dropbox. 
4. Rerun the 'surveySetup.py' script to select the raffle winner and 
obtain the final formatted csv file.
