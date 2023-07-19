import streamlit as st

def main():
    st.title('Audio Region Detector')
    st.markdown('## GitHub Repository')
    st.markdown('[GitHub Repository](https://github.com/frdcmp/audio-region-detector)')

    st.markdown('## Overview')
    st.markdown('Audio Region Detector is a Python-based application that provides multiple features for audio processing and analysis. It includes an SRT converter, audio transcription, and automatic regioning capabilities. This versatile tool enables users to extract meaningful information from audio files and perform various tasks related to audio data.')

    st.markdown('## Key Features')
    st.markdown('### SRT Converter')
    st.markdown('Audio Region Detector allows users to convert audio files into SubRip Subtitle (SRT) format. This feature is useful for generating subtitles or captions for videos.')

    st.markdown('### Audio Transcription')
    st.markdown('The application includes a powerful audio transcription feature that utilizes speech recognition technology to convert spoken words in audio files into written text. This can be helpful for tasks such as transcribing interviews, lectures, or podcasts.')

    st.markdown('### Auto Regioning')
    st.markdown('With the auto regioning feature, users can automatically divide audio files into distinct regions based on specific criteria. This enables efficient segmentation and analysis of different parts of the audio.')

    st.markdown('## How to Use')
    st.markdown('1. Install the necessary dependencies by running `pip install -r requirements.txt`.')
    st.markdown('2. Run the app with Streamlit by executing the command `streamlit run audio-region-detector.py`.')
    st.markdown('3. Use the Streamlit interface to select the desired feature (SRT Converter, Audio Transcription, or Auto Regioning).')
    st.markdown('4. Provide the necessary input files or directories for processing.')
    st.markdown('5. Adjust any relevant settings or parameters for the chosen feature.')
    st.markdown('6. Click the appropriate buttons to start the processing and view the results.')

    st.markdown('## Contributing')
    st.markdown('Contributions to Audio Region Detector are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please submit a pull request.')

    st.markdown('## License')
    st.markdown('Audio Region Detector is released under the MIT License. Feel free to use, modify, and distribute the software according to the terms of the license.')

# Create the Streamlit app
if __name__ == '__main__':
    main()
