import streamlit as st
import pandas as pd
from functions import convert_srt_to_csv, download_file


def main():
    st.title("SRT to CSV Converter")

    st.write("Upload your SRT file:")
    srt_file = st.file_uploader("Choose an SRT file", type=['srt'])

    file_format = st.selectbox("Select output file format:", ('csv', 'xlsx', 'json', 'txt', 'vtt'))

    if srt_file is not None:
        srt_text = srt_file.read().decode('utf-8')
        df = convert_srt_to_csv(srt_text)
        st.write("Converted CSV:")
        st.dataframe(df)

        if st.button("Download"):
            file_data, file_mime = download_file(df, file_format)
            if file_data and file_mime:
                st.download_button(
                    label=f"Download as {file_format.upper()}",
                    data=file_data,
                    file_name=f"converted_file.{file_format}",
                    mime=file_mime
                )


if __name__ == '__main__':
    main()
