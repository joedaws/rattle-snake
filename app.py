"""
defines the streamlit app for interacting with maps
"""
from typing import Dict
import streamlit as st

from rattle_snake.constants import BeingCulture
from rattle_snake.plane_map import PlaneMap

st.title("Project Rattle Snake")

st.markdown(
    "An app for generating places for [beings](https://github.com/joedaws/beings) to live"
)


@st.cache
def generate_data():
    return build_maps()


def build_maps() -> Dict[BeingCulture, PlaneMap]:
    weird_map = PlaneMap(being_culture=BeingCulture.WEIRD)
    deep_map = PlaneMap(being_culture=BeingCulture.DEEP)
    dream_map = PlaneMap(being_culture=BeingCulture.DREAM)

    return {
        BeingCulture.WEIRD: weird_map,
        BeingCulture.DEEP: deep_map,
        BeingCulture.DREAM: dream_map,
    }


map_generating_state = st.text("Generating data...")

maps = generate_data()

map_generating_state.text("Using cached maps")

st.text(f"{list(maps.keys())}")

selected_culture = st.selectbox(
    "Plane of existence",
    (BeingCulture.WEIRD.value, BeingCulture.DEEP.value, BeingCulture.DREAM.value),
)

selected_culture_map = st.text(f"SELECTED CULTURE: {selected_culture}")

if st.button("Show culture Map"):
    current_map = maps[BeingCulture(selected_culture)]
    current_map.draw()

    st.pyplot(current_map.fig)
