from pathlib import Path

import pandas as pd
import streamlit as st
import pydeck as pdk

from constants import RISK_LEVELS

BASE_PATH = Path(__file__).resolve().parent
ICON_PATH = './app/static/map_pin.png'  # TODO: Publish this icon on /static

ICON_DATA = {
    "url": ICON_PATH,  # TODO: Use published icon
    "width": 242,
    "height": 242,
    "anchorY": 242,
}


def hex_to_rgb(hex_color: str) -> list:
    """
    Converts hex color to rgb
    :param hex_color: hex color
    :return: rgb color
    """
    hex_color = hex_color.lstrip('#')
    return list(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def report_map(df_city_data: pd.DataFrame, df_region_data: pd.DataFrame, city_id: int, field_latitude: str = 'latitude', field_longitude: str = 'longitude') -> st.pydeck_chart:
    """
    Returns the map for the report
    :return: map
    """

    # Configure map
    center_lat = df_city_data.loc[city_id, field_latitude]
    center_lon = df_city_data.loc[city_id, field_longitude]
    zoom = 5
    pitch = 0

    df_city_data["icon_data"] = None
    for i, row in df_city_data.iterrows():
        row["icon_data"] = ICON_DATA

    df_region_data["fill_color"] = (df_region_data["risk_level"].astype(int)
                                    .apply(lambda x: RISK_LEVELS[x]['color'])
                                    .apply(hex_to_rgb))

    # TODO: Configure mapbox token
    r = pdk.Deck(
        map_style=None,
        views=[
            pdk.View(type="MapView", controller=None),
        ],
        initial_view_state=pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=zoom,
            pitch=pitch,
        ),
        layers=[
            pdk.Layer(
                "GeoJsonLayer",
                df_region_data,
                opacity=0.1,
                stroked=True,
                filled=True,
                # extruded=True,
                # wireframe=True,
                get_fill_color='fill_color',
                get_line_color=[255, 255, 255],
                auto_highlight=True,
                pickable=True,
            ),
            pdk.Layer(
                'IconLayer',
                data=df_city_data,
                get_position=[field_longitude, field_latitude],
                get_size=4,
                size_scale=15,
                get_icon='icon_data',
            ),
        ],
    )

    return st.pydeck_chart(r)


def on_clic_handler(widget_instance, payload):
    # Prepare parameters
    params = {
        'coordinates': payload['coordinates']
    }

    # Call handler
    print(params)
    # handler(params)
