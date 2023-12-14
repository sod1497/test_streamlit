from pathlib import Path
import folium
from folium.plugins import MousePosition
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd

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


def report_map_folium(df_city_data: pd.DataFrame, df_region_data: pd.DataFrame, city_id: int, field_latitude: str = 'latitude', field_longitude: str = 'longitude', field_popup: str = 'city', last_clicked: dict = None) -> st.pydeck_chart:
    """
    Returns the map for the report
    :return: map
    """

    # Configure map
    zoom = 5
    city_name = df_city_data.loc[city_id, field_popup]

    center_lat = df_city_data.loc[city_id, field_latitude]
    center_lon = df_city_data.loc[city_id, field_longitude]

    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)

    df_region_data["fill_color"] = (df_region_data["risk_level"].astype(int)
                                    .apply(lambda x: RISK_LEVELS[x]['color']))

    gdf_region_data = gpd.GeoDataFrame(df_region_data, crs='EPSG:31982', geometry='geom')
    geo_j = gdf_region_data.to_json()

    g = folium.GeoJson(
        geo_j,
        style_function=lambda x: {
            'fillColor': x['properties']['fill_color'],
            'color': '#000000',
            'fillOpacity': 0.3,
        },
        # tooltip=folium.GeoJsonTooltip(
        #     fields=['region', 'risk_level'],
        #     aliases=['Region', 'Risk level'],
        #     localize=True
        # ),
        # popup=folium.GeoJsonPopup(
        #     fields=['region', 'risk_level'],
        #     aliases=['Region', 'Risk level'],
        #     localize=True
        # )
    ).add_to(m)

    # Add marker for selected city
    fg = folium.FeatureGroup(name="Markers")
    if last_clicked is not None:
        fg.add_child(folium.Marker(
            [last_clicked['lat'], last_clicked['lng']]  # , popup=city_name, tooltip=city_name
        ))
    else:
        fg.add_child(folium.Marker([center_lat, center_lon], popup=city_name, tooltip=city_name))

    return st_folium(m, use_container_width=True, height=400, returned_objects=["last_clicked"], center=last_clicked, feature_group_to_add=fg)
