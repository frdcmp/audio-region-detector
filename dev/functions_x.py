import numpy as np
import matplotlib.pyplot as plt
import librosa
import soundfile as sf
import tempfile
import shutil
import os
import pandas as pd
from io import BytesIO
from tqdm import tqdm
import math


def plot_waveform(audio_path, st):
    # Load the audio file using Librosa
    audio, sr = librosa.load(audio_path, sr=None)

    # Create the waveform plot
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(audio, alpha=0.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Amplitude')
    ax.set_title('Waveform')

    # Display the plot in Streamlit
    st.pyplot(fig)

def save_temp_file(audio_file):
    # Create a temporary WAV file
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

    # Save the uploaded audio file to the temporary file
    shutil.copyfileobj(audio_file, temp_wav)
    temp_wav.close()

    return temp_wav.name

def remove_temp_file(file_path, st):
    try:
        os.remove(file_path)
        st.success("Temporary file removed successfully.")
    except OSError as e:
        st

def convert_srt_to_csv(srt_text):
    lines = srt_text.strip().split('\n\n')
    data = []
    for line in lines:
        parts = line.split('\n')
        if len(parts) >= 3:
            idx = int(parts[0])
            timecodes = parts[1].split(' --> ')
            text = ' '.join(parts[2:])
            data.append([idx, timecodes[0], timecodes[1], text])
    df = pd.DataFrame(data, columns=['ID', 'TimecodeIN', 'TimecodeOUT', 'Text'])
    return df

def transcribe_audio_files(model, root_folder, batch_size):
    # Get the number of wav files in the root folder and its sub-folders
    num_files = sum(1 for dirpath, dirnames, filenames in os.walk(root_folder) for filename in filenames if filename.endswith(".wav"))

    # Initialize an empty list to store transcription results
    transcriptions = []

    # Transcribe the wav files and display a progress bar
    with tqdm(total=num_files, desc="Transcribing Files") as pbar:
        for dirpath, dirnames, filenames in os.walk(root_folder):
            for filename in filenames:
                if filename.endswith(".wav"):
                    filepath = os.path.join(dirpath, filename)
                    result = model.transcribe(filepath, batch_size=batch_size)
                    transcription = result['segments']

                    # Split the transcription into lines
                    lines = transcription.splitlines()

                    # Create a DataFrame from the segments dictionary
                    speech = pd.DataFrame.from_dict(result['segments'])
    
    return speech



def format_timecode(seconds):
    decimal, milliseconds = math.modf(seconds)
    milliseconds = int(decimal * 1000)
    
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = int(seconds % 60)

    timecode = f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    return timecode



def download_file(df, file_format):
    if file_format == 'csv':
        csv_data = df.to_csv(index=False)
        return csv_data, 'text/csv'
    elif file_format == 'xlsx':
        excel_data = BytesIO()
        with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        excel_data.seek(0)
        return excel_data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif file_format == 'json':
        json_data = df.to_json(indent=4)
        return json_data, 'application/json'
    elif file_format == 'txt':
        txt_data = df.to_string(index=False)
        return txt_data, 'text/plain'
    elif file_format == 'vtt':
        vtt_data = 'WEBVTT\n\n'
        for index, row in df.iterrows():
            vtt_data += f'{row["ID"]}\n{row["TimecodeIN"]} --> {row["TimecodeOUT"]}\n{row["Text"]}\n\n'
        return vtt_data, 'text/vtt'
    else:
        return None, None
    if file_format == 'csv':
        csv_data = df.to_csv(index=False)
        return csv_data, 'text/csv'
    elif file_format == 'xlsx':
        excel_data = BytesIO()
        with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        excel_data.seek(0)
        return excel_data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif file_format == 'json':
        json_data = df.to_json(indent=4)
        return json_data, 'application/json'
    elif file_format == 'txt':
        txt_data = df.to_string(index=False)
        return txt_data, 'text/plain'
    elif file_format == 'vtt':
        vtt_data = 'WEBVTT\n\n'
        for index, row in df.iterrows():
            vtt_data += f'{row["ID"]}\n{row["TimecodeIN"]} --> {row["TimecodeOUT"]}\n{row["Text"]}\n\n'
        return vtt_data, 'text/vtt'
    else:
        return None, None
    if file_format == 'csv':
        csv_data = df.to_csv(index=False)
        return csv_data, 'text/csv'
    elif file_format == 'xlsx':
        xlsx_data = df.to_excel(index=False)
        return xlsx_data, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif file_format == 'json':
        json_data = df.to_json(indent=4)
        return json_data, 'application/json'
    elif file_format == 'txt':
        txt_data = df.to_string(index=False)
        return txt_data, 'text/plain'
    elif file_format == 'vtt':
        vtt_data = 'WEBVTT\n\n'
        for index, row in df.iterrows():
            vtt_data += f'{row["ID"]}\n{row["TimecodeIN"]} --> {row["TimecodeOUT"]}\n{row["Text"]}\n\n'
        return vtt_data, 'text/vtt'
    else:
        return None, None


    # Get the number of wav files in the root folder and its sub-folders
    num_files = sum(1 for dirpath, dirnames, filenames in os.walk(root_folder) for filename in filenames if filename.endswith(".wav"))

    # Initialize an empty list to store transcription results
    transcriptions = []

    # Transcribe the wav files and display a progress bar
    with tqdm(total=num_files, desc="Transcribing Files") as pbar:
        for dirpath, dirnames, filenames in os.walk(root_folder):
            for filename in filenames:
                if filename.endswith(".wav"):
                    filepath = os.path.join(dirpath, filename)
                    result = model.transcribe(filepath, fp16=False, verbose=True)
                    transcription = result['text']

                    # Split the transcription into lines
                    lines = transcription.splitlines()

                    # Create a DataFrame from the segments dictionary
                    speech = pd.DataFrame.from_dict(result['segments'])

    return speech 