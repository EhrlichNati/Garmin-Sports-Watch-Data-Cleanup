README for Data Cleaning and Processing Workflow // make this a title.

Data folder:
2 files (csv) from my watch- before and after processing. 
        
Dependencise: # this can be converted into requirement.txt file
pandas 2.11 
python 3.10 
scikit-learn 1.3.2 




Overview

This collection of Python scripts is designed to clean, process, and impute data from CSV files. It is particularly tailored for data with various features, some of which may contain missing or 'unknown' values. The workflow is structured to handle large datasets, filter out non-informative columns, transform data into a structured format, and apply different imputation techniques based on the nature of the data.


Workflow

1. Data Loading and Initial Digest: The process begins with loading CSV files, filtering out unnecessary records and columns, and handling file read errors.
   
2. Initial Cleaning: Non-informative columns (those with a high percentage of 'unknown' or missing values) are identified and removed.
   
3. Feature Transformation: The dataset is transformed into a structured format where each column represents a distinct feature.
 
4. Imputation: The transformed data undergoes imputation. Different columns are imputed using different strategies based on their characteristics.
Functions


// make sure this is presented well in the repository root.
def run_clean(data_folder_path, processed_folder_path=False)
        Purpose: Orchestrates the entire cleaning and processing flow.
        Input:
        data_folder_path: Path to the folder containing CSV files.
        processed_folder_path: (Optional) Path to save the processed files.
        Output: The last imputed DataFrame.


def load_and_first_digest_data(path):
        Purpose: Loads a CSV file and performs initial data cleaning.        
        Input: File path.
        Output: DataFrame containig relavent records for processing.


def create_features_list(frame)
        Purpose: Identifies and lists all features present in the DataFrame.
        Input: DataFrame.
        Output: List of feature names.
        

def transform_frame(frame, features_list):
        Purpose: Transforms the DataFrame into a structured format.
        Input: Original DataFrame and a list of features.
        Output: Transformed DataFrame.
        

def imputation(frame):
        Purpose: Applies imputation techniques to the DataFrame.
        Input: DataFrame.
        Output: Imputed DataFrame.
        
        Methods:
        -KNN Imputation: Used for columns like heart rate, cadence, and speed. This method considers the k-nearest neighbors to impute missing values.
        -Custom Fill for Position: Location and altitude values are imputed based on the assumption that they remain constant from the closest recorded values.
        -Distance Calculation: For missing distance values, the function uses time and speed data to calculate and fill in the gaps.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



