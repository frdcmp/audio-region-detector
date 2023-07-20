import os
import stable_whisper
import streamlit as st
import pandas as pd
from tqdm import tqdm
from functions import load_srt_to_dataframe, transcribe_audio_files
from st_aggrid import GridOptionsBuilder, AgGrid
from st_aggrid.shared import GridUpdateMode, DataReturnMode
import torch


# Set Streamlit layout to wide
st.set_page_config(layout="wide")

# Set up Whisper client
st.title("Transcription")

# Define the model options
model_options = ["tiny", "base", "small", "medium", "large"]

# Create a select box for model selection with default value "base"
model_name = st.selectbox("Select model size", model_options, index=1)
model = stable_whisper.load_model(model_name)
st.success("Whisper model loaded.")

st.write("---")

# Streamlit app
def main():
    
    # Input field for audio file location with default value "audio"
    files_folder = st.text_input("Enter the location of the audio files", value="audio")

    # Transcription button
    if st.button("Start Transcription"):
        # Check if input location is provided
        if not files_folder:
            st.warning("Please enter the location of the audio files.")
        else:
            # Call the transcribe_audio_files function
            speech = transcribe_audio_files(model, files_folder)
            speech.to_srt_vtt('./temp/trans.srt', word_level=False)
            st.success("Transcription complete.")
    
    # Load DataFrame button
    if st.button("Load DataFrame"):
        # Check if the .srt file exists
        srt_path = './temp/trans.srt'
        if os.path.exists(srt_path):
            # Load DataFrame from the .srt file
            trans_df = load_srt_to_dataframe(srt_path)
            if trans_df is not None:
                # Display the DataFrame
                st.dataframe(trans_df)
        else:
            st.warning("The .srt file does not exist. Please transcribe the audio files first.")
    
    # Convert to CSV button
    if st.button("Convert to CSV"):
        srt_path = './temp/trans.srt'
        csv_path = './temp/trans.csv'
        if os.path.exists(srt_path):
            # Load DataFrame from the .srt file
            trans_df = load_srt_to_dataframe(srt_path)
            if trans_df is not None:
                # Keep only the desired columns
                trans_df = trans_df[["Subtitle", "Start Time", "End Time"]]
                # Convert and save DataFrame to CSV
                trans_df.to_csv(csv_path, index=False)
                st.success("SRT file converted and saved as CSV: trans.csv")
                
                # Read the CSV file into a new DataFrame
                csv_df = pd.read_csv(csv_path)
                # Display the new DataFrame
                st.write("New DataFrame (csv_df) from trans.csv:")
                st.dataframe(csv_df)
        else:
            st.warning("The .srt file does not exist. Please transcribe the audio files first.")

# Run the Streamlit app
if __name__ == '__main__':
    main()
