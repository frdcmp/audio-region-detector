import os
import pandas as pd
import streamlit as st

def load_data(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".xlsx":
        return pd.read_excel(file_path)
    elif ext == ".csv":
        return pd.read_csv(file_path)
    else:
        return None

def main():
    st.set_page_config(layout="wide")  # Set the app layout to wide
    
    st.title("File Names Importer")
    
    # List all files in the "./markers" folder
    files = [f for f in os.listdir("./markers") if f.endswith(".xlsx") or f.endswith(".csv")]
    
    # File upload
    uploaded_file = st.file_uploader("Upload the list of file names here:", type=["csv", "xlsx"])
    
    # Dataframe to store the File Names
    filenames_df = None
    
    # Validate and process the uploaded file
    if uploaded_file is not None:
        try:
            filenames_df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
            if "File Names" not in filenames_df.columns:
                st.error('The uploaded file should have a column named "File Names".')
                filenames_df = None
            else:
                st.success("File structure validated successfully!")
                # Number of rows for File Names (including header)
                row_counter = len(filenames_df)
                # Display row counter on the right side of the data preview for File Names
                st.info(f"Number of rows for File Names (including header): {row_counter}")
                
                # Display the rows of filenames_df in a dropdown list
                st.subheader("File Names:")
                rows_list = filenames_df["File Names"].tolist()
                selected_row = st.selectbox("File name list:", rows_list)




        except Exception as e:
            st.error(f"Error: {e}")

    st.write("---")

    # Add the "Select a file" dropdown to the left
    selected_file = st.selectbox("Select a file from the 'markers' folder:", files)
    
    # Add a text above the "Import File Names" button
    st.subheader("Instructions:")
    st.write("Select a file from the dropdown and click the 'Import File Names' button to load the data.")
    
    # Add the "Import File Names" button to the right
    if st.button("Import File Names") and selected_file:
        file_path = os.path.join("./markers", selected_file)
        markers_df = load_data(file_path)
        
        if markers_df is not None:
            # Check if the number of rows in the two dataframes differs
            if filenames_df is not None and len(filenames_df) != len(markers_df):
                st.warning("The number of rows in the two dataframes differs!")
                st.warning(f"Number of rows in File Names dataframe: {len(filenames_df)}")
                st.warning(f"Number of rows in Markers dataframe: {len(markers_df)}")
                
            # Merge dataframes by concatenating the columns
            merged_df = pd.concat([filenames_df, markers_df], axis=1)
            st.subheader("Merged Data Preview:")
            st.write(merged_df)
            row_counter = len(merged_df)  # Including the header
            st.info(f"Number of rows in the merged dataframe (including header): {row_counter}")
        else:
            st.error("Unsupported file format. Only xlsx and csv files are supported.")


        # Download Text button
        text_data = "start_region_table\n"
        text_data += merged_df.apply(lambda row: f"{row['Start Time']} {row['End Time']} {row['File Names']}", axis=1).str.cat(sep='\n')
        text_data += "\nend_region_table"
        st.download_button(
            label="Download Text",
            data=text_data,
            file_name='regions.txt',
            mime='text/plain'
        )


if __name__ == "__main__":
    main()
