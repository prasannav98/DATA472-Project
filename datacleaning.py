import pandas as pd
import os
import numpy as np
import re
import fnmatch


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

current_directory = os.path.dirname(os.path.realpath(__file__))

files_in_directory = os.listdir(current_directory)
# Get the names of all sheets in the Excel file
excel_files = [file for file in files_in_directory if file.endswith('.xlsx') or file.endswith('.xls')]

dfs = {}

for file in excel_files:
    # Read the Excel file into a dictionary of DataFrames
    xl = pd.ExcelFile(file)
    # Loop through each sheet in the Excel file
    for sheet_name in xl.sheet_names:
        # Check if the sheet name matches the desired name
        if sheet_name == "Summary table-current":
            # Read the sheet into a DataFrame
            dfs[f"{file}_{sheet_name}"] = xl.parse(sheet_name)
            dfs[f"{file}_{sheet_name}"] = dfs[f"{file}_{sheet_name}"].iloc[3:].reset_index()
            dfs[f"{file}_{sheet_name}"] = dfs[f"{file}_{sheet_name}"].transpose()

def transform_df(df):
    df = df.iloc[2:]
    df = df[df.iloc[:, 1] != '%']
    df = df.drop(df.columns[1], axis=1)
    # Iterate through each column in the DataFrame
    for i in range(len(df.columns)):
        # Check if the first row of the column is NaN
        if pd.isna(df.iloc[0, i]):
            # If NaN, fill it with the value from the first row of the previous column
            if i > 0:
                df.iloc[0, i] = df.iloc[0, i-1]
    df.iloc[0], df.iloc[1] = df.iloc[1].copy(), df.iloc[0].copy()
    # Assign 'subtype' to the first row of the first column
    df.iloc[0, 0] = 'Subtype'

    # Assign 'type' to the second row of the first column
    df.iloc[1, 0] = 'Type'
    # Get the columns to swap
    column_17 = df[17].copy()
    column_18 = df[18].copy()

    # Swap the columns
    df[17] = column_18
    df[18] = column_17    
    # Generate new column names from 1 to n
    new_columns = [str(i) for i in range(1, len(df.columns) + 1)]

    # Assign the new column names to the DataFrame
    df.columns = new_columns
    return df

def clean_df(df, i):
    df = transform_df(df)
    df.to_csv(f"test_{i}.csv")
    df = pd.read_csv(f"test_{i}.csv")
    # Drop column: 'Unnamed: 0'
    df = df.drop(columns=['Unnamed: 0'])
    df = df.iloc[:, :-2]
    # Get the values of the last column's second row and first row
    value_second_row = df.iloc[1, -1]
    value_first_row = df.iloc[0, -1]

    # Exchange the values
    df.iloc[1, -1] = value_first_row
    df.iloc[0, -1] = value_second_row
    df.iloc[1, 16] = "Ethnic group"

    df.columns = df.iloc[0]
    df = df.drop(0)
    df = df.transpose()
    # Explicitly set the column names
    df.columns = df.iloc[0]
    return df

def final_clean(df, i):
    df = clean_df(df, i)
    df['Subtype'] = df.index
    columns = df.columns.tolist()

    # Specify the index of the column you want to move
    column_to_move = 7 

    # Move the column to the desired position (second position)
    columns.insert(1, columns.pop(column_to_move))

    # Reorder the DataFrame with the new column order
    df = df[columns]
    # Step 1: Melt the DataFrame to pivot the columns from 3rd to 8th as row entries
    melted_df = pd.melt(df, id_vars=['Type', 'Subtype'], value_vars=['Jobseeker Support', 'Sole Parent Support', 
                                                                        'Supported Living Payment', 'Youth Payment and Young Parent Payment',
                                                                        'Other Main Benefits', 'Total'],
                            var_name='Benefit Type', value_name='Numbers')

    # Step 2: Reorder the DataFrame to place the melted columns as the second column
    columns_reordered = ['Type', 'Subtype', 'Benefit Type', 'Numbers']
    final_df = melted_df[columns_reordered]
    filtered_df = melted_df[melted_df['Type'] != 'Type']
    date = re.search(r'national-benefit-tables-(.*?)\.x', i).group(1)
    filtered_df["Date"] = date
    date_column = filtered_df['Date']

    # Remove the 'Date' column from the DataFrame
    filtered_df = filtered_df.drop(columns=['Date'])

    # Insert the 'Date' column as the first column
    filtered_df.insert(0, 'Date', date_column)    
    # Convert the 'date' column to datetime format
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%B-%Y')

    # Format the 'date' column as yyyymmdd
    filtered_df['Date'] = filtered_df['Date'].dt.strftime('%Y%m%d')
    return filtered_df

for i in dfs.keys():
    if (dfs[i].shape[1] + dfs[i].shape[0] == 36):
        df = final_clean(dfs[i], i)
        df.to_csv(f"final_{i}.csv", index= False)

def delete_csv_files():
    files = os.listdir('.')
    csv_files = fnmatch.filter(files, '*.csv')
    
    # Separate CSV files into two lists based on whether they contain "final" in their name
    csv_without_final = [file for file in csv_files if 'final' not in file.lower()]

    # Delete CSV files without "final" in their name
    for file in csv_without_final:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except PermissionError:
            print(f"Permission denied to delete: {file}")
        except Exception as e:
            print(f"An error occurred while deleting {file}: {e}")

# Call the function to delete CSV files
delete_csv_files()

def merge_csv_files():
    files = os.listdir('.')
    csv_files = [file for file in files if file.endswith('.csv')]

    # Read each CSV file into a DataFrame and store them in a list
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)

    # Merge all DataFrames into one DataFrame
    merged_df = pd.concat(dfs, ignore_index=True)

    return merged_df

# Call the function to merge CSV files
merged_dataframe = merge_csv_files()
files = os.listdir('.')
csv_files = fnmatch.filter(files, '*.csv')
for file in csv_files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except PermissionError:
            print(f"Permission denied to delete: {file}")
        except Exception as e:
            print(f"An error occurred while deleting {file}: {e}")
merged_dataframe.to_csv("MasterTheBlaster.csv", index=False)