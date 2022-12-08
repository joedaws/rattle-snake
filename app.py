"""
defines the streamlit app for interacting with maps
"""
from typing import Dict
import streamlit as st

from rattle_snake.constants import BeingCulture
from rattle_snake.plane_map import PlaneMap
from rattle_snake.db_helpers import create_connection, get_num_circles

db_file = "./beings-2022-12-07-22-41-32.db"

st.title("Project Rattle Snake")

st.markdown(
    "An app for generating places for [beings](https://github.com/joedaws/beings) to live"
)


@st.cache
def load_weird_map():
    return PlaneMap(db_file=db_file, being_culture=BeingCulture.WEIRD)


@st.cache
def load_dream_map():
    return PlaneMap(db_file=db_file, being_culture=BeingCulture.DREAM)


@st.cache
def load_deep_map():
    return PlaneMap(db_file=db_file, being_culture=BeingCulture.DEEP)


map_generating_state = st.text("Loading data...")

conn = create_connection(db_file=db_file)
cur = conn.cursor()
cur.execute("""SELECT COUNT(*) from nodes""")
rows = cur.fetchall()
st.markdown(f"DB File: {db_file}")
st.markdown(f"Query returned: {rows}")

num_circles = get_num_circles(db_file=db_file, plane="deep_denizen")
st.markdown(f"Num circles query Query returned: {num_circles}")

# maps = {
#    BeingCulture.WEIRD: load_weird_map(),
#    BeingCulture.DEEP: load_deep_map(),
#    BeingCulture.DREAM: load_dream_map,
# }

map_generating_state.text("Using cached data")

current_map = load_deep_map()
