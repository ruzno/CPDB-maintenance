# TOOL TO PREPARE CLIMATE POLICY DATABASE DATA FOR BULK UPDATE
# This script is used to check whether the database meet the requirements for upload
# The source file must include  proper, unified names for the website taxonomy vocabularies
# This tool ensures the correct terms are included in the file or highlights instances that must be corrected

# Author:   Leonardo Nascimento
# Date:     October 2021
# Contact:  l.nascimento@newclimate.org

# ---
# INPUT: climatepolicydatabase source .csv file
# OUTPUT: results of this script are added the the folder results/
# ---

import pandas as pd

# import database

database_input = pd.read_csv(r'data/source_database_20052022.csv', encoding='latin1')

# variables to analyse
# !! it is important that the variables and taxonomies are ordered the same way

list_variables = [
    'policy_jurisdiction', 'policy_type_of_policy_instrument',
    'policy_sector_name', 'policy_type', 'policy_implementation_state',
    'policy_objective', 'impact_indicator_name_of_impact_indicator'
]

list_taxonomies = [
    'taxonomy_policy_jurisdiction.txt', 'taxonomy_policy_instrument.txt',
    'taxonomy_sector.txt', 'taxonomy_policy_type.txt', 'taxonomy_implementation_state.txt',
    'taxonomy_policy_objective.txt', 'taxonomy_impact_indicator.txt'
]

# this loops through all the variables above
for i in range(len(list_variables)):

    variable = database_input[list_variables[i]]

    taxonomy = pd.read_csv(r'data/taxonomies/' + list_taxonomies[i], header=None).squeeze()
    taxonomy = taxonomy.str.strip()

    # split text within column
    sp_variable = variable.astype(str)
    sp_variable = sp_variable.str.split(",", expand=True)
    sp_variable = sp_variable.fillna('For filter')

    # make sure no spaces in the beginning or end of the world exists
    for column in sp_variable:
        sp_variable[column] = sp_variable[column].str.strip()

    # singles out error in the database
    error = pd.DataFrame()

    for j in sp_variable.columns:
        error_j = database_input[~sp_variable[j].isin(taxonomy)]
        error = pd.concat([error, error_j], axis=0)

    name = list_variables[i]

    # exports error for each variable if there are any policies with mistakes
    # NO EXPORT MEANS NO ERRORS
    if list_variables[i] == 'impact_indicator_name_of_impact_indicator':
        error = error[~error['impact_indicator_name_of_impact_indicator'].isna()]

    if not error.empty:
        # noinspection PyTypeChecker
        error.to_csv('results/error_' + name + '.csv', index=False)
