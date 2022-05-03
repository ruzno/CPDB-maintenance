# SCRIPT TO PREPARE CLIMATE POLICY DATABASE FOR STATISTICAL ANALYSES

# filters out variables that are only relevant for backend database management;
# categorises each policy into policy matrix options and;
# creates boolean variables for the columns for the various relevant indicators.

# Author:   Leonardo Nascimento
# Date:     June 2021
# Contact:  l.nascimento@newclimate.org

# ---
# INPUT: climatepolicydatabase source .csv file
# OUTPUT: results of this script are added the the folder results/datasets
# ---

# %% import packages

import numpy as np
import pandas as pd

from pandas import DataFrame
from functions.functions_policy_indicators import *

# %% import data and define period of analysis

# all data is available in the project folder
policies_import = pd.read_csv('data/source_database_03052022.csv', encoding='latin1')

# creates a copy so changes can be compared to the import
df_temp = policies_import.copy(deep=True)

range_end = 2021

# %% DATA CLEANING

# --------------------------------------------------------------------
# DATA CLEANING: drops columns and adjust data types
# --------------------------------------------------------------------

# removes columns that are  irrelevant to the analysis
df_temp = df_temp.drop(columns=['policy_title', 'policy_name',
                                'policy_supranational_region',
                                'policy_subnational_region_or_state', 'policy_city',
                                'policy_description', 'policy_stringency',
                                'policy_objective', 'policy_source_or_references',
                                'impact_indicator_comments',
                                'impact_indicator_name_of_impact_indicator', 'impact_indicator_value',
                                'impact_indicator_base_year', 'impact_indicator_target_year'])

# removes entries that are irrelevant to the analysis
df_temp = df_temp[
    (df_temp['policy_jurisdiction'] == 'Country') &
    (df_temp['policy_type_of_policy_instrument'].notnull()) &
    (~df_temp['policy_date_of_decision'].isna()) &
    (df_temp['policy_sector_name'].notnull())]

# %% DATA PREPARATION

# --------------------------------------------------------------------
# DATA PREPARATION: creates new columns necessary for the analysis
# --------------------------------------------------------------------

# Estimates the first year for the policy to be considered in the analysis
# For policies with adoption date, the first year is the start date
# For policies without the adoption date but with implementation date, the start date is the implementation date

condition = [df_temp['policy_date_of_decision'].notna(),
             df_temp['policy_start_date_of_implementation'].notna()]

result = [df_temp['policy_date_of_decision'],
          df_temp['policy_start_date_of_implementation']]

df_temp['policy_start_date_analysis'] = np.select(condition, result, default=0)

df_temp = df_temp[df_temp['policy_start_date_analysis'] != 0]
assert df_temp[df_temp['policy_start_date_analysis'] == 0].empty

# Estimates the last year for the policy to be considered in the analysis
# For policies with end date, the last year is the end date
# For policies in force, the final date to be considered is the last analysis year

condition = [df_temp['policy_end_date_of_implementation'].notna(),
             df_temp['policy_implementation_state'] == 'In force']

result = [df_temp['policy_end_date_of_implementation'],
          range_end]

df_temp['policy_end_date_analysis'] = np.select(condition, result, default=0)

df_temp = df_temp[df_temp['policy_end_date_analysis'] != 0]
assert df_temp[df_temp['policy_end_date_analysis'] == 0].empty

# adjusts data types
list_category_columns = ['policy_country', 'policy_country_iso_code', 'policy_jurisdiction',
                         'policy_type_of_policy_instrument', 'policy_sector_name', 'policy_type',
                         'policy_implementation_state', 'policy_high_impact']

list_numeric_columns = ['policy_end_date_of_implementation',
                        'policy_start_date_of_implementation', 'policy_end_date_analysis',
                        'policy_date_of_decision', 'policy_start_date_analysis']

for col in list_category_columns:
    df_temp[col] = df_temp[col].astype('category')

for col in list_numeric_columns:
    df_temp[col] = df_temp[col].astype('str')
    df_temp[col] = df_temp[col].str.strip()
    df_temp[col] = df_temp[col].astype('float').astype('Int32')

# %% ADD INDICATOR VARIABLES (SECTORS, POLICY INSTRUMENT, SECTORAL COVERAGE AND SECTOR SPECIFICITY)
# ---------------------------------------
# INDICATORS: creates main categorisation indicators
# See all functions in python module functions_policy_indicators.py
# ---------------------------------------

# creates boolean PolicyInstrument columns
# this step extracts information from the column 'policy instrument'
df_temp = add_pi(df_temp)

# Calls function that adds policy options to the table
df_temp = add_policy_options(df_temp)

# creates boolean sector columns
# this step extracts information from the 'sector name'
df_temp = add_sec(df_temp)

# calculates fuzziness for each individual policy
df_temp = add_f(df_temp)

# calculates sector specificity for each individual policy
df_temp = add_sp(df_temp)

# changes column types
list_boolean_columns = ['GeneralSector', 'ElectricitySector',
                        'IndustrySector', 'BuildingsSector', 'TransportSector', 'LandSector',
                        'DirectInvestment', 'FiscalFinancialIncentives',
                        'Market-basedInstruments', 'CodesStandards',
                        'OtherRegulatoryInstruments', 'RDD', 'InformationEducation',
                        'PolicySupport', 'VoluntaryApproaches', 'BarrierRemoval',
                        'ClimateStrategy', 'Target']

for col in list_boolean_columns:
    df_temp[col] = df_temp[col].astype(bool)

policies_tidy_clean: DataFrame = df_temp.copy(deep=True)
policies_tidy_clean.to_csv(r'results/datasets/treated_policy_database.csv', index=False)