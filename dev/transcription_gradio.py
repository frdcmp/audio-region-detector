import os
import gradio as gr

def list_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    return files

def read_file_contents(file_path):
    with open(file_path, "r") as file:
        contents = file.read()
    return contents

def transcription_gradio(folder_path):
    file_list = list_files_in_folder(folder_path)
    return file_list

def file_contents_gradio(file_path):
    contents = read_file_contents(file_path)
    return contents

folder_inputs = gr.inputs.Textbox(label="Folder Path", default="./audio")
file_outputs = gr.outputs.Textbox(label="File List")
file_inputs = gr.inputs.Dropdown(choices=[], label="Select a File")
content_outputs = gr.outputs.Textbox(label="File Contents")

def update_file_list(folder_path):
    file_list = list_files_in_folder(folder_path)
    file_inputs.choices = file_list
    return folder_path

iface = gr.Interface(
    fn=transcription_gradio,
    inputs=folder_inputs,
    outputs=file_outputs,
    title="Transcription Gradio",
    description="List files in a folder",
    examples=[["./audio"]]
)

iface.launch()

content_interface = gr.Interface(
    fn=file_contents_gradio,
    inputs=file_inputs,
    outputs=content_outputs,
    title="File Contents Gradio",
    description="Display file contents",
)

content_interface.launch()
