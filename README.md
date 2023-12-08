# Data Folder
Contains two CSV files from my watch - one before processing and one after.

## Overview
This suite of Python scripts is designed for cleaning, processing, and imputing data from CSV files. It's specifically tailored for datasets with a mix of features, some of which may have missing or 'unknown' values. The workflow efficiently manages large datasets, filters out non-informative columns, restructures the data, and applies various imputation techniques.

## Local Folder 
This folder holds raw files exported from my Garmin watch.

[](Row Files Folder.png)

### Workflow

1. **Data Loading and Initial Digest**: 
   - Loading CSV files, filtering out unnecessary records and columns.
   - Handling file read errors.
2. **Initial Cleaning**: 
   - Identifying and removing non-informative columns with a high percentage of 'unknown' or missing values.
3. **Feature Transformation**: 
   - Converting the dataset into a structured format, with each column representing a distinct feature.
4. **Imputation**: 
   - Implementing different imputation strategies based on the nature of each column.

### Functions

**def run_clean(data_folder_path, processed_folder_path=False)**
  - **Purpose**: Orchestrates the entire cleaning and processing flow.
  - **Input**:
    - `data_folder_path`: Path to the folder containing CSV files.
    - `processed_folder_path`: (Optional) Path to save the processed files.
  - **Output**: The final imputed DataFrame.

**def load_and_first_digest_data(path):**
  - **Purpose**: Loads a CSV file and performs initial data cleaning.
  - **Input**: File path.
  - **Output**: DataFrame containing relevant records for processing.

**def create_features_list(frame):**
  - **Purpose**: Identifies and lists all features present in the DataFrame.
  - **Input**: DataFrame.
  - **Output**: List of feature names.

**def transform_frame(frame, features_list):**
  - **Purpose**: Transforms the DataFrame into a structured format.
  - **Input**: Original DataFrame and a list of features.
  - **Output**: Transformed DataFrame.

**def imputation(frame):**
  - **Purpose**: Applies imputation techniques to the DataFrame.
  - **Input**: DataFrame.
  - **Output**: Imputed DataFrame.
  - **Methods**:
    - KNN Imputation: Used for columns like heart rate, cadence, and speed.
    - Custom Fill for Position: Location and altitude values are imputed based on closest recorded values.
    - Distance Calculation: Fills in missing distance values using time and speed data.

