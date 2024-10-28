import pandas as pd

# Load the CSV file
file_path = '/mnt/data/survey_results_public_old.csv'
df = pd.read_csv(file_path)

# Define a function to remove duplicate languages in the "Languages" column
def remove_duplicates(languages):
    if pd.isna(languages):  # Handle NaN values
        return languages
    unique_languages = set(languages.split(', '))  # Split by ', ' and convert to set to remove duplicates
    return ', '.join(unique_languages)  # Join back to a string

# Apply the function to the "Languages" column
df['Languages'] = df['Languages'].apply(remove_duplicates)

# Save the updated DataFrame to a new CSV file
new_file_path = '/mnt/data/survey_results_public_cleaned.csv'
df.to_csv(new_file_path, index=False)

new_file_path
