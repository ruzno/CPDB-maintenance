# CPDB_Maintenance

Project that includes tools used to manage the data in the Climate Policy Database- CPDB (climatepolicydatabase.org). Other tools will be added over time. 

Note that this repository does not include the scripts to manage the website itself. These are included in the Assembla environment and is managed by WAAT.

The prefix DT means data treatment, it currently includes:
- the script **DT_pre_upload** is used to ensure the file used for bulk upload matches all taxonomies on the website.
- the script **DT_data_handling** is used to prepare the data for statistical analyses over time, it: 
  - filters out variables that are only relevant for backend database management;
  - categorises each policy into policy matrix options and;
  - creates boolean variables for the columns for the various relevant indicators.
