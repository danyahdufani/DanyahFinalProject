# Author
Danyah Dufani
Queen Mary University London 
Date: 23/12/2024 - 10/01/2025

# AIDS Mortality Analysis 

## Description of Project
This project analyses AIDS mortality rates across regions, income groups and over the years. It provides data visualisation and statistical analysis to understand trends and patterns in AIDS-related deaths globally.

## Data Source
The data used was sourced from the World Health Organisation using this link: https://www.who.int/data/inequality-monitor/data#PageContent_C687_Col00


## Table of Contents 
- [Repository](#RepositoryStructure)
- [Installation](#installation)
- [CircleCi](#circleci)



## RepositoryStructure
1.data/:
    This directory contains the input data files needed for analysis and plotting.
    -data.xlsx: An Excel file containing the primary data set with mortality estimates and income group classifications. This file is read and processed in the analysis.

2.maps/: Contains shapefiles used for mapping geographic data.
   -ne_110m_admin_0_countries.dbf: A database file for the shapefile that contains attributes for shapes (e.g., country information).
   -ne_110m_admin_0_countries.shx: The shape index file, which stores the positional index of the geometric objects in the .shp file.
   -ne_110m_admin_0_countries.shp: The actual shape file containing the geometric data for country boundaries.

3.output/: This directory stores the visual outputs generated by the scripts.
   -aids_mortality_by_income_group_bar_chart.png: A bar chart visualising AIDS mortality rates by income group.
   -aids_mortality_by_income_group_line_plot.png: A line plot showing AIDS mortality trends over the years categorised by income group.
   -global_aids_mortality_map_2022.png: A geographic map depicting AIDS-related deaths globally for the year 2022.

4.graphs.py: This script contains all functions related to data reading, processing, analysis, and visualisation. It includes functionalities for creating various plots and conducting statistical analysis of AIDS mortality data.

5.requirements.txt:A file that lists all dependencies required to run the project. This includes libraries like pandas, matplotlib, seaborn, geopandas, numpy, scipy, scikit-learn, pytest, and openpyxl. It allows easy installation of all required packages using pip.

6.unittesting.py: A script that contains unit tests for the functions defined in graphs.py, validating their correctness and ensuring expected behaviour.

7.unittestdescription.txt:
A text file which contains descriptions of each of the unit tests, helping explain their purpose

8.CircleCi.png - an image showing successful run with all unit tests passing, also includes date and time in top right corner


## Installation 
To run this project, clone the repository and install the required dependencies: 

1.Clone the Repository using this link:
https://github.com/danyahdufani/DanyahFinalProject.git

2.To run the analysis script use the following command:
python graphs.py 

# CircleCi
https://app.circleci.com/pipelines/circleci/LL5HkHxbczorHiL7dHKdYm/RzRvn63zpoaL2eexxBsgjD
Go to CircleCi.png - an image showing successful run with all unit tests passing, also includes date in top right corner

