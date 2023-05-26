# TMC Data Engineering Assessment: VF Matching

## Description

This README covers the <b>TMC Data Engineering Assessment:</b> Conducting voter_id match between a <i>raw</i>, user-input file, and a County voter file by use of various Python packages. 

</br>

## Table of Contents
1. [Description](#description)
2. [Table of Contents](#table-of-contents)
3. [Usage](#usage)
4. [Dependencies](#dependencies)
4. [Installation](#installation)
5. [Process](#process)
6. [Technologies Employed](#technologies-employed)
6. [Future Development](#future-development)
8. [Contributing](#contributing)
9. [Tests](#tests)
10. [Questions](#questions)

</br>

## Usage 
This process is used throughout the progressive political space for numerous reasons: 
1. To improve current process of voter outreach through analysis and reporting 
2. Identifying limitations in geographical approach and improving allocation of resources 
3. Audit tracking of state KPI methodology to maintain standardization of data
4. Understanding voter trends and behavior based on various demographics
5. Assuring composition of internal voter file data 

</br>

## Dependencies
In order to implement the scripts in this assessment, you will need to install the <i>following</i> Python packages & Extension: 
* [pandas](https://pandas.pydata.org/docs/getting_started/overview.html): Library of data manipulation tools and analysis 
* [OS](https://docs.python.org/3/library/os.html): Library that provides ports to use operating systems dependent on functionality. 
* [glob](https://docs.python.org/3/library/glob.html): Module that locates all pathnames matching a specified pattern according to rules implemented by shell. 
* [thefuzz](https://github.com/seatgeek/thefuzz): Ulitizes Levenshtein Distance to calculate the difference between sequences across various compilations of data.  
* [Jupyter Notebook](https://jupyter.org/): VSCode Extension, web-based interactive environment for coding.


</br>



## Installation
All Python packages listed under [Dependencies](#Dependencies) can be installed within the built-in Terminal CLI of VSCode by writing: </br>
```pip install pandas glob thefuzz os```


</br>

## Process 
### Raw File vs. County Data [Steps 1-2]
Raw data <i>(known in the script in chronological order:</i> `input_df/matched_input/matching_df`) was provided by TMC to perform the `voter_id` match, with instructions to locate county voter file data online. The initial steps were taken as followed:  
1. Locate county voter file data from state SOS website. 
    * It is important to note that since the criteria of the assessment stated to download the first county files, I downloaded counties: 'ADAMS', 'ALLEN', 'ASHLAND', & 'ASHTABULA' from OH's SOS website.
2. import python package `pandas`, to open csv. files in Jupyter Notebook by using the `pd.read_csv("[filename].csv")`.
3. Understanding decrepencies in the data. 

### Preparing for Match [Steps 3-4]
Prequisites to successfully completing a Voter_ID match:
1. Clean, structured data 
2. Unique Identifier 
3. Name columns in each file + state voter_id must be present in at least 1 file. 
### Cleaning & Structuring [Step 5]
</b>Cleaning the data served to also introduce a unique identifier, since both files lacked a shared `unique_id`. The name column in the `Raw File` was filled with incomplete names, while the `County file` had 4 separate columns dedicated to `FIRST_NAME`, `LAST_NAME`, `MIDDLE_NAME`, & `SUFFIX`. </br> </br>
</b>Due to this, a new column was added to the county_file that concatenated the name columns into 1 column, looking as similiar as possible to the `name` column in the raw_file. </br> </br>
</b>Additionally, several columns were stripped away after combining the 4 county voter files into 1 DataFrame so that only columns necessary to perform the match were present, cutting down significantly on processing time. </br> </br>
</b>Customer `null` values were set for both DataFrames.
* Prior to removing columns from the county_file, I took deliberate steps to export the county voter files as soon as they were merged. This means the compiled data from the state is untouched and can be later implemented throughout analysis and reporting procedures.

</br>

### Performing Match [Steps 6-7]:
The first step taken to perform the match was to import `fuzz` from `thefuzz` which offers a lil' something known as <b>"fuzzy</b>. Then, converting the name columns from each DataFrame into Lists(): </br>
```input_list = input_df['name'].tolist()``` </br> 
```oh_vf2_list = oh_vf2['Name'].tolist()```

</br>

<b>Next</b>, Creating a function that defines the parameters of the match in conjunction with `thefuzz` is crucial here. 

```
def match_vf(query, choices, limit=2) :
mat1 = process.extract(input_list, oh_vf2_list, limit=2)
return mat1.title()        
    
print(input_df)
```

</br>

### Assessing Outcome
This brought me to the intial matched DataFrame. Where the Matched Items look as such: </br>

```(ADAM METALWALA , 95)```

</br>

### Cleaning & Structuring, Round 2 FIGHT! [Step 8]:
This newly matched output was saved to a new DataFrame = `matched_input`, where the entirety of the next script focused on cleaning <i>and</i> structuring this column, while also splitting the column between `matched_name` & `matched_score`, respectfully. The metamorphosis of this column into two separate ones went as followed: </br>
```
1. `(ADAM METALWALA , 95)`

2. matched_name: ( ADAM METALWALA 
matched_score: , 95 )

3. matched_name: ADAM METALWALA 
matched_score: 95 
```

This was successful <i>and</i> simple due to the implementation of [Regular Expressions](https://gist.github.com/isayani/81768ad7ebdc0a66abb6ac48d7229ab7). 

### Matching DataFrames to pull Voter_id Information [Step 9]:
With the data cleaned twice and matched once, retrieving a match on `matched_name` and `address` allowed for a fruitful match of voter_id to `matching_df`, the DataFrame formerly known as `input_df`. 

</br>

### QC DataFrame Structure, last minute cleaning, and export [Step 10]: 
Lastly, I made sure columns not necessary to the desired final product were dropped, and `SOS_VOTERID` was renamed to `Matched_voterid` as required in the prompt. 

The file was then exported as a csv. using the `to_csv.` call in pandas and saved as `tmc_final_matched_voter.csv`

</br>


## Technologies Employed
Python packages used in order: pandas, os, glob, and thefuzz (formerly known as fuzzywuzzy). The assessment in its entirety was completed using [Jupyter Notebook](https://jupyter.org/), solely to utilize the run-by-cell functionality and assure output was accurate throughout the steps taken to produce the final product. 

However, the script was revamped utilizing VS Code and its intergrated terminal to improve proficiency and processing speed while ensuring accuracy in the final results. 

</br>

## Future Development

It would make sense to perform this procedure based on the stack provided in a designated workplace. Throughout my time in conducting the assessment, serveral ideas came to mind as to how this process can and <i>should</i> be improved. 

For starters, after completing the first match, where `thefuzz` gave a dedicated score and name, uploading the files as a `.csv` to a Data Warehouse (e.g. Google BigQuery, Civis Analytics Platform) after cleaning the matches would have easily been a viable solution and a great timesaver. Additionally, utilizing the `pd.read_sql` call via `pandas` could serve as an alternative. However, with the Python packages listed under [Dependencies](#Dependencies), it was quite simple and effecient to remain in Python and carry out the process. 

Understandably, this process is on par with Data Engineering, and I enjoy performing tasks of this nature, however, in my experience in progressive data, applications like TargetSmart offers a tool 'SmartMatching' which cut out data management tasks like voter file matching serve as a great tool when performing analysis on voter_file data on a day-to-day basis. In my <i>present-visualization-queries repository</i>, the folder `VR_Matched_&_Counts` showcases the efficiency of utilizing tools like <i>SmartMatch</i>, where raw data-entry of Voter outreach canvassers are matched back to a state or national `voter_id`.

Lastly, I'd like to recreate this process utilizing [Splink](https://moj-analytical-services.github.io/splink/) as a record-lnkage python package. `thefuzz` was implemented solely due to a lack of exposure on my end as to what python packages can and <i>should</i> be used for matching these two sources of data. 

Now that the assessment is long over, I look to turn this into a personal project by testing different python packages, trying different ideas, and continue learning as much as I can. At this point, it's not as much important to find the correct solution as it is to learn more and further develop my understanding and comprehension for python, data engineering, and everything else this process potentially entails. 

</br>

## Contributing
Contributions can be made at your nearest foodbank

</br>

## Tests
At every iteration of DataFrame, where a pivotal change occurred, I made sure to export the contents to a csv. file. For example, I made sure to export the initial merge of the county voter file data because having a compiled, structured file of that stature will serve reporting and analytic needs infinitely. 


</br>

## Questions
[Find me on GitHub](https://github.com/ametalwala)</br>
[Email me directly](adammetalwala@gmail.com)

- - -
© 2022 TMC Data Engineering Assessment: VF Matching by ametalwala, Confidential and Proprietary. All Rights Reserved.
