import streamlit as st
import atexit
from models.config import metadata
from models.data import ApplicationData
from context import get_workdir

print("Starting ScenicPathfinder application...")
__metadata__ = metadata()
data = ApplicationData()

def save_data_on_exit():
    print("Saving data before exit...")
    data.save()

if __name__ == "__main__":
    atexit.register(save_data_on_exit)
    print(f"Loading application data from {data.file}...")
    data.read()
    print("Data loaded successfully.")
    st.title(__metadata__.appname)
    st.write(f"Version: {__metadata__.version}")
    st.write(f"Author: {__metadata__.author}")
    