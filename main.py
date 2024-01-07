import streamlit as st
import pandas as pd
import re


def process_excel(input_file):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(input_file, sheet_name='Sheet1', engine='openpyxl')

    # Create new columns for each tag
    tags = ['University', 'Program', 'Major', 'Percent_CGPA', 'US_GPA', 'ELA',
            'Number_of_Years', 'Number_of_backlogs', 'Missing_Docs',
            'Subjects_with_Backlogs', 'NAAC_Accredited', 'Degree_Conferred_Certificate']

    for tag in tags:
        df[tag] = df['Notes'].apply(
            lambda x: re.search(fr'{tag}:\s*(.*?)(?=\n|$)', str(x)).group(1) if re.search(fr'{tag}:\s*(.*?)(?=\n|$)',
                                                                                          str(x)) else None)

    return df


def main():
    st.title("GPA Notes Separator Application")

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file is not None:
        st.write("File uploaded successfully.")

        # Display a preview of the uploaded data
        df_preview = pd.read_excel(uploaded_file, sheet_name='Sheet1')
        st.write("Preview of the data:")
        st.write(df_preview)

        # Process the Excel file
        processed_df = process_excel(uploaded_file)

        # Display the processed data
        st.write("Processed Data:")
        st.write(processed_df)

        # Save the processed DataFrame to a new Excel file
        processed_df.to_excel('output_data.xlsx', index=False)
        st.success("Processing complete. Output saved as 'output_data.xlsx'.")


if __name__ == '__main__':
    main()
