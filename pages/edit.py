import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid
from st_aggrid.shared import GridUpdateMode, DataReturnMode
import shutil
import os
from functions import read_csv, convert_time_to_seconds, add_marker_column

def main():
    st.title("Read CSV and Create DataFrame")

    # Add a slider for time range
    time_range = st.slider("Select Time Range (seconds)", 0.5, 2.0, 1.0, step=0.1)

    # Check if the file "trans.csv" exists in the same directory as the script
    df = read_csv("./temp/trans.csv")

    if df is not None:
        # Perform data processing and conversions
        df = convert_time_to_seconds(df)
        df = add_marker_column(df, time_range)

        markers_df = AgGrid(
            df,
            reload_data=False,
            editable=True,
            theme="streamlit",
            data_return_mode=DataReturnMode.AS_INPUT,
            update_mode=GridUpdateMode.MODEL_CHANGED,
        )

        temp_df = markers_df['data']    # overwrite df with revised aggrid data; complete dataset at one go
        temp_df.to_csv('./temp/temp.csv', index=False)  # re/write changed data to CSV if/as required
        # Create a Streamlit button
        reload_button = st.button("Update Changes in the CSV")

        # Load CSV on button click
        if reload_button:
            filename = './temp/temp.csv'
            new_filename = './temp/temp2.csv'
            shutil.copyfile(filename, new_filename)

            csv_df = pd.read_csv(new_filename)

            # Shift the End Time
            csv_df['End Time'] = csv_df['End Time'].shift(1)

            # Remove excessive tabs
            csv_df.drop('TimeIN', axis=1, inplace=True)
            csv_df.drop('TimeOUT', axis=1, inplace=True)

            # Remove rows with empty 'Subtitle' column
            csv_df.dropna(subset=['Markers'], inplace=True)
            csv_df['End Time'] = csv_df['End Time'].shift(-1)

            # Set the last 'End Time' value to the last value in 'End Time' from markers_df
            last_row = csv_df.tail(1).index.item()
            if last_row + 1 == len(csv_df):
                markers_df = pd.read_csv('./temp/temp.csv')
                last_timecode_out = markers_df['End Time'].iloc[-1]
                csv_df.at[last_row, 'End Time'] = last_timecode_out
            else:
                markers_df = pd.read_csv('./temp/temp.csv')
                last_timecode_out = markers_df['End Time'].iloc[-1]
                csv_df.at[last_row, 'End Time'] = last_timecode_out

            # Get the name of the first .wav file present in the './audio' folder
            audio_files = [file for file in os.listdir('./audio') if file.endswith('.wav')]
            first_audio_file = audio_files[0] if audio_files else 'audio_file.xlsx'

            # Save DataFrame to an Excel file with the first .wav file name
            excel_filename = f"./markers/{os.path.splitext(first_audio_file)[0]}.xlsx"
            csv_df.to_excel(excel_filename, index=False)
            st.success('Excel file saved!')

if __name__ == "__main__":
    main()
