# %%
import pandas as pd 
import glob 
import os 


#col_names = ['SOS_VOTERID', 'LAST_NAME', 'FIRST_NAME', 'MIDDLE_NAME', 'SUFFIX', 'DATE_OF_BIRTH', 'RESIDENTIAL_ADDRESS1', 'RESIDENTIAL_SECONDARY_ADDR', 'RESIDENTIAL_CITY', 'RESIDENTIAL_STATE', 'RESIDENTIAL_ZIP']
#setting path to join the county files 
oh_files = os.path.join("/Users/adam/Documents/Git_Repos/TMC-Data-Engineering", "A*.csv")

#list of merged files returned using glob
oh_files = glob.glob(oh_files)

#now joining files via concat and read_csv
df = pd.concat(map(pd.read_csv, oh_files), ignore_index=False)

(df) 

# %%
import pandas as pd 
import glob 
import os 


col_names = ['SOS_VOTERID', 'LAST_NAME', 'FIRST_NAME', 'MIDDLE_NAME', 'SUFFIX', 'DATE_OF_BIRTH', 'RESIDENTIAL_ADDRESS1', 'RESIDENTIAL_SECONDARY_ADDR', 'RESIDENTIAL_CITY', 'RESIDENTIAL_STATE', 'RESIDENTIAL_ZIP']
#setting path to join the county files 
oh_files = os.path.join("/Users/adam/Documents/Git_Repos/TMC-Data-Engineering", "A*.csv")

#list of merged files returned using glob
oh_files = glob.glob(oh_files)

#now joining files via concat and read_csv
df = pd.concat(map(pd.read_csv, oh_files), ignore_index=False)

df.to_csv("/Users/adam/Documents/Git_Repos/TMC-Data-Engineering/OH_merged.csv") 

# %%
import pandas as pd 

## implementing the use of 'usecols' to trim processing power and stick to what is necessary for performing the match.
col_names= ['SOS_VOTERID', 'LAST_NAME', 'FIRST_NAME', 'MIDDLE_NAME', 'SUFFIX', 'DATE_OF_BIRTH', 'RESIDENTIAL_ADDRESS1', 'RESIDENTIAL_SECONDARY_ADDR', 'RESIDENTIAL_CITY', 'RESIDENTIAL_STATE', 'RESIDENTIAL_ZIP']

oh_vf = pd.read_csv("OH_merged.csv", 
                    usecols=col_names, 
                    dtype={'RESIDENTIAL_ZIP':object}
                    )

print(oh_vf)

# %%
# making null values set to '' so that even if data is not present, 
# it isn't weighing on our souls. 
oh_vf2 = oh_vf.fillna(value = '')

# creating what could potentially be a unique identifier, although given the extent of how much data is missing from the input file, 
# it stands to defer we may need 
# various additional linkages
oh_vf2['Name'] = oh_vf2['FIRST_NAME'] + ' ' + oh_vf2['MIDDLE_NAME'] + ' ' + oh_vf2['LAST_NAME'] + ' ' + oh_vf2['SUFFIX']

# aligning with the input file's birth_year structure 
oh_vf2['birth_year'] = pd.DatetimeIndex(oh_vf2['DATE_OF_BIRTH']).year

print(oh_vf2)

# %%
oh_vf2
# uploading input file to begin process of matching 
input_df = pd.read_csv('tmc_input.csv')

input_df = input_df.fillna(value = '')
# changed name of added birth year column in the county file 
# to create separation of the two fields. 
oh_vf2['year_of_birth'] = oh_vf2['birth_year']

oh_vf2.drop(columns=['birth_year'], inplace=True)

print(oh_vf2.dtypes)


# %%
import pandas as pd
from thefuzz import fuzz
from thefuzz import process


# empty lists for storing the matches later 
mat1 = []

# converting dataframe columns to lists of elements
# for 'fuzzy' matching 
input_list = input_df['name'].tolist()
oh_vf2_list = oh_vf2['Name'].tolist()

# setting threshold of match ration to 90 
threshold = 90


# %%
from thefuzz import process, fuzz 

#mat1 = mat1.fillna(value = '')
input_df['Matches'] = pd.Series(mat1)
input_df = input_df.fillna(value = ' ')

def match_vf(query, choices, limit=2) : 
    mat1 = process.extract(input_list, oh_vf2_list, limit=2)
    return mat1.title()

print(input_df)

# %%

# make new DataFrame, then convert to csv file to allow for overall visual understanding of matches. 
matched_input = pd.DataFrame(input_df)
matched_input.to_csv("/Users/adam/Documents/Git_Repos/TMC-Data-Engineering/matched_input_tmc.csv") 

# opened matched_input as DataFrame once again to reset
matched_input = pd.read_csv('matched_input_tmc.csv')
matched_input = matched_input.fillna(value = '')
matched_input['Matches'] = matched_input['Matches'].str.replace('[()]', " ", regex=True)
print(matched_input)


# split matches column successfully to separate names from match score
split_matches = matched_input.Matches.str.split(",", expand=True)
matched_input = matched_input.assign( 
    matched_name=split_matches[0], 
    matched_score=split_matches[1]
)
# remove unneeded characters from matched names string 
# by use of regular expression. 
matched_input['matched_name'] = matched_input['matched_name'].str.replace('\W', " ", regex=True)
print(matched_input)

# %%
import pandas as pd
from thefuzz import fuzz


def match_score(input_row, county_row):
  name_score = fuzz.token_set_ratio(input_row['matched_name'], county_row['Name'])
  address_score = fuzz.token_set_ratio(input_row['address'], county_row['RESIDENTIAL_ADDRESS1'])
  return (name_score + address_score) / 2, county_row['SOS_VOTERID']

# Create a new dataframe to store the matching rows
matching_df = pd.DataFrame(columns=matched_input.columns)

# Iterate through the rows of the input file and county voter file
for input_row, county_row in zip(matched_input.iterrows(), oh_vf2.iterrows()):
  matched_score, voter_id = match_score(input_row[1], county_row[1])
  if matched_score > 10:
    matching_df = matching_df.append(input_row[1], ignore_index=True)
    matching_df.loc[len(matching_df) - 1, 'SOS_VOTERID'] = voter_id

# Save the matching rows to a new file
#matching_df.to_csv("matched_records.csv", index=False)
print(matching_df)

# %%
# removing columns not desired in final product 
matching_df.drop(columns=['Matches', 'matched_name', 'matched_score'], inplace=True)

# renaming SOS_VOTERID to matched_voterid as to appease the assessment rubric
matching_df = matching_df.rename(columns={'SOS_VOTERID': 'matched_voterid'})

# publishing final product to csv for submission. This has been a fantastic assessment, thank you very much for the opportunity. 
matching_df.to_csv('/Users/adam/Documents/Git_Repos/TMC-Data-Engineering/tmc_final_matched_voter.csv')

print(matching_df)


