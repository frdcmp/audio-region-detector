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
import re


def transcribe_audio_files(model, root_folder):
    # Get the number of wav files in the root folder and its sub-folders
    num_files = sum(1 for dirpath, dirnames, filenames in os.walk(root_folder) for filename in filenames if filename.endswith(".wav"))

    # Transcribe the wav files and display a progress bar
    with tqdm(total=num_files, desc="Transcribing Files") as pbar:
        for dirpath, dirnames, filenames in os.walk(root_folder):
            for filename in filenames:
                if filename.endswith(".wav"):
                    filepath = os.path.join(dirpath, filename)
                    speech = model.transcribe(filepath)
   
    return speech


def load_srt_to_dataframe(srt_path):
    with open(srt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    data = []
    current_entry = {}
    for line in lines:
        line = line.strip()
        if line.isdigit():
            if current_entry:
                data.append(current_entry)
                current_entry = {}
            current_entry["Index"] = int(line)
        elif "-->" in line:
            start, end = line.split("-->")
            current_entry["Start Time"] = start.strip()
            current_entry["End Time"] = end.strip()
        elif line:
            # Clean up the subtitle text
            subtitle = re.sub(r"<[^>]+>", "", line)  # Remove HTML tags if any
            subtitle = re.sub(r"\\[a-zA-Z0-9]{3}", "", subtitle)  # Remove \N{...} unicode characters
            current_entry.setdefault("Subtitle", "")
            current_entry["Subtitle"] += subtitle + " "

    if current_entry:
        data.append(current_entry)

    return pd.DataFrame(data, columns=["Index", "Start Time", "End Time", "Subtitle"])


def read_csv(filename):
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        st.error(f"Error: File '{filename}' not found. Please make sure the file exists in the 'temp' directory.")
        return None

def convert_time_to_seconds(df):
    # Extract hh:mm:ss and milliseconds from "Start Time" and "End Time" columns
    start_time_temp = pd.to_datetime(df["Start Time"], format="%H:%M:%S,%f")
    end_time_temp = pd.to_datetime(df["End Time"], format="%H:%M:%S,%f")

    # Convert datetime to seconds and milliseconds and create new columns "TimeIN" and "TimeOUT"
    df["TimeIN"] = start_time_temp.dt.hour * 3600 + \
                   start_time_temp.dt.minute * 60 + \
                   start_time_temp.dt.second + \
                   start_time_temp.dt.microsecond / 1e6

    df["TimeOUT"] = end_time_temp.dt.hour * 3600 + \
                    end_time_temp.dt.minute * 60 + \
                    end_time_temp.dt.second + \
                    end_time_temp.dt.microsecond / 1e6

    return df

def add_marker_column(df, time_range):
    # Add an empty column "Markers" to the left
    df.insert(0, "Markers", "")

    # Iterate through the DataFrame and modify the "Markers" column
    for i in range(len(df) - 1):
        time_diff = df.at[i + 1, "TimeIN"] - df.at[i, "TimeOUT"]
        if time_diff > time_range:
            df.at[i + 1, "Markers"] = "Marker"

    return df