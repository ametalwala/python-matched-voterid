import pandas as pd
import glob
import os
from thefuzz import fuzz
from thefuzz import process

# Define file paths
data_dir = "/Users/adam/Documents/Git_Repos/TMC-Data-Engineering"
input_file = "/Users/adam/Documents/Git_Repos/python-matched-voterid/cleanse-structuringdata/tmc_input.csv"
output_dir = "final-product"
output_file = "tmc_final_matched_voter.csv"

# Combine and save the files
oh_files = os.path.join(data_dir, "A*.csv")
oh_files = glob.glob(oh_files)
df = pd.concat(map(pd.read_csv, oh_files), ignore_index=False)
merged_file = os.path.join(data_dir, "OH_merged.csv")
df.to_csv(merged_file)

# Columns to use for matching
match_columns = ['SOS_VOTERID', 'LAST_NAME', 'FIRST_NAME', 'MIDDLE_NAME', 'SUFFIX', 'DATE_OF_BIRTH',
                 'RESIDENTIAL_ADDRESS1', 'RESIDENTIAL_SECONDARY_ADDR', 'RESIDENTIAL_CITY', 'RESIDENTIAL_STATE',
                 'RESIDENTIAL_ZIP']

# Load and preprocess Ohio voter file
oh_vf = pd.read_csv(merged_file, usecols=match_columns, dtype={'RESIDENTIAL_ZIP': object})
oh_vf.fillna('', inplace=True)
oh_vf['Name'] = oh_vf['FIRST_NAME'] + ' ' + oh_vf['MIDDLE_NAME'] + ' ' + oh_vf['LAST_NAME'] + ' ' + oh_vf['SUFFIX']
oh_vf['birth_year'] = pd.DatetimeIndex(oh_vf['DATE_OF_BIRTH']).year
oh_vf.drop(columns=['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'SUFFIX', 'DATE_OF_BIRTH'], inplace=True)

# Load and preprocess input file
input_df = pd.read_csv(input_file)
input_df.fillna('', inplace=True)

# Function to calculate the match score
def calculate_match_score(input_row, county_row):
    name_score = fuzz.token_set_ratio(input_row['name'], county_row['Name'])
    address_score = fuzz.token_set_ratio(input_row['address'], county_row['RESIDENTIAL_ADDRESS1'])
    return (name_score + address_score) / 2, county_row['SOS_VOTERID']

# Create a new DataFrame to store the matching rows
matching_df = pd.DataFrame(columns=input_df.columns)

# Iterate through the input rows and county voter rows to calculate match scores
for _, input_row in input_df.iterrows():
    input_row['Matches'] = process.extractOne(input_row['name'], oh_vf['Name'])
    if input_row['Matches'][1] >= 90:
        match_score, voter_id = calculate_match_score(input_row, oh_vf.loc[input_row['Matches'][2]])
        if match_score > 10:
            input_row['matched_name'] = input_row['Matches'][0]
            input_row['matched_score'] = match_score
            input_row['SOS_VOTERID'] = voter_id
            matching_df = matching_df._append(input_row)

# Drop unnecessary columns from the matching DataFrame
matching_df.drop(columns=['name', 'address', 'Matches'], inplace=True)

# Rename columns for final output
matching_df.rename(columns={'SOS_VOTERID': 'matched_voterid'}, inplace=True)

# Save the final matched voter DataFrame to CSV
output_path = os.path.join(output_dir, output_file)
matching_df.to_csv(output_path, index=False)

# final output
print(matching_df)
