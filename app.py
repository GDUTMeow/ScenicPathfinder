import streamlit as st
import atexit
from models.config import metadata
from models.data import data as raw_data
from context import get_workdir
from pages import *

__metadata__ = metadata()

if "app_data" not in st.session_state:
    print("New session started. Loading application data from file...")
    raw_data.read()
    st.session_state.app_data = raw_data
    print("Data loaded into session state.")
    print("Starting ScenicPathfinder application...")

data = st.session_state.app_data


def save_data_on_exit():
    print("Saving data before exit...")
    data.save()


def register_save_data():
    if "atexit_registered" not in st.session_state:
        atexit.register(save_data_on_exit)
        st.session_state.atexit_registered = True


if __name__ == "__main__":
    register_save_data()
    st.set_page_config(layout="wide")
    st.title(f"旅游区导航系统 {__metadata__.appname}")
    st.write(f"Version: {__metadata__.version}")
    st.write(f"Author: {__metadata__.author}")
    st.divider()
    pg = st.navigation(
        {
            "ScenicPathfinder": [HOME_PAGE],
            "游客": [
                GUEST_FIND_SPOT_PAGE,
                GUEST_FIND_SHORTEST_PATH_PAGE,
                GUEST_FIND_ALL_SIMPLE_PATH_PAGE,
                GUEST_GET_PLAN_PAGE,
                GUEST_VIEW_MAP_PAGE
            ],
            "管理员": [
                ADMIN_ADD_SPOT_PAGE,
                ADMIN_MODIFY_SPOT_PAGE,
                ADMIN_REMOVE_SPOT_PAGE,
                ADMIN_ADD_PATH_PAGE,
                ADMIN_MODIFY_PATH_PAGE,
                ADMIN_REMOVE_PATH_PAGE,
            ],
            "调试": [DEBUG_DATA_VIEW_PAGE, DEBUG_GENERATE_DATA_PAGE],
        },
        position="top",
    )
    pg.run()
