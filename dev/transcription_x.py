import os
import base64
import whisperx
import shutil
from tqdm import tqdm
import streamlit as st
import pandas as pd
from functions_x import transcribe_audio_files, format_timecode
from st_aggrid import GridOptionsBuilder, AgGrid
from st_aggrid.shared import GridUpdateMode, DataReturnMode
import gc 

device = "cuda" 
batch_size = 8 # reduce if low on GPU mem
compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)

# Function to read Excel file and update the DataFrame
def import_excel_data(df, file):
    excel_df = pd.read_excel(file)
    df['File Names'] = excel_df.iloc[:, 0]  # Assuming the first column of the Excel file should be inserted into 'File Names'
    st.success('Data imported successfully!')

# Set Streamlit layout to wide
st.set_page_config(layout="wide")

# Set up Whisper client
st.title("Transcription")

# Define the model options
model_options = ["tiny", "base", "small", "medium", "large"]

# Create a select box for model selection with default value "base"
model_name = st.selectbox("Select model size", model_options, index=1)
model = whisperx.load_model(model_name, device, compute_type=compute_type)


st.success("Whisper model loaded.")

st.write("---")

# Streamlit app
def main():


    # Check if speech DataFrame is already stored
    if 'speech_df' not in st.session_state:
        st.session_state.speech_df = None
    
    # Input field for audio file location with default value "audio"
    root_folder = st.text_input("Enter the location of the audio files", value="audio")

    # Transcription button
    if st.button("Start Transcription"):
        # Check if input location is provided
        if not root_folder:
            st.warning("Please enter the location of the audio files.")
        else:
            # Call the transcribe_audio_files function
            speech = transcribe_audio_files(model, root_folder, batch_size)
            
            st.success("Transcription complete.")
            st.session_state.speech_df = speech  # Store the speech DataFrame in speech_df
    
    # Display the DataFrame
    if st.session_state.speech_df is not None:
        st.title("Auto Region")

        # Create new DataFrame with only text, TimecodeIN, and TimecodeOUT columns
        regioned_df = st.session_state.speech_df.copy()
        regioned_df['TimecodeIN'] = regioned_df['start'].apply(format_timecode)
        regioned_df['TimecodeOUT'] = regioned_df['end'].apply(format_timecode)
        regioned_df['File Names'] = ''
        regioned_df = regioned_df[['File Names', 'text', 'TimecodeIN', 'TimecodeOUT']].copy()

        # Display an editable DataFrame
        temp_df = regioned_df.copy()

        markers_df = AgGrid(
            temp_df,
            reload_data=False,
            editable=True,
            theme="streamlit",
            data_return_mode=DataReturnMode.AS_INPUT,
            update_mode=GridUpdateMode.MODEL_CHANGED,
        )

        temp_df = markers_df['data']    # overwrite df with revised aggrid data; complete dataset at one go
        temp_df.to_csv('./temp/temp.csv', index=False)  # re/write changed data to CSV if/as required
        

    # Create a Streamlit button
    reload_button = st.button("Reload CSV")

    # Load CSV on button click
    if reload_button:
        filename = './temp/temp.csv'
        new_filename = './temp/temp2.csv'
        shutil.copyfile(filename, new_filename)

        # Remove the 'text' column from the DataFrame before saving to temp2.csv
        csv_df = pd.read_csv(new_filename)
        csv_df['TimecodeOUT'] = csv_df['TimecodeOUT'].shift(1)

        # Remove rows with empty 'File Names' column
        csv_df.dropna(subset=['File Names'], inplace=True)
        csv_df['TimecodeOUT'] = csv_df['TimecodeOUT'].shift(-1)
        csv_df.drop('text', axis=1, inplace=True)

        # Set the last 'TimecodeOUT' value to the last value in 'TimecodeOUT' from markers_df
        last_row = csv_df.tail(1).index.item()
        if last_row + 1 == len(csv_df):
            markers_df = pd.read_csv('./temp/temp.csv')
            last_timecode_out = markers_df['TimecodeOUT'].iloc[-1]
            csv_df.at[last_row, 'TimecodeOUT'] = last_timecode_out
        else:
            markers_df = pd.read_csv('./temp/temp.csv')
            last_timecode_out = markers_df['TimecodeOUT'].iloc[-1]
            csv_df.at[last_row, 'TimecodeOUT'] = last_timecode_out

        # Save the DataFrame as "regioned.csv"
        csv_df.to_csv('./temp/regioned.csv', index=False)
        st.success('CSV file saved!')


        # Display the Dataframe csv_df
        st.dataframe(csv_df)

        # Download Text button
        text_data = "start_region_table\n"
        text_data += csv_df.apply(lambda row: f"{row['TimecodeIN']} {row['TimecodeOUT']} {row['File Names']}", axis=1).str.cat(sep='\n')
        text_data += "\nend_region_table"
        st.download_button(
            label="Download Text",
            data=text_data,
            file_name='regions.txt',
            mime='text/plain'
        )


if __name__ == '__main__':
    main()