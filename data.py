from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely import wkt
import streamlit as st

BASE_PATH = Path(__file__).resolve().parent
DATA_PATH = BASE_PATH.joinpath('data')


@st.cache_data
def read_data() -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    df_city_data = pd.read_csv(DATA_PATH.joinpath('city_data.csv'), header=0, encoding='UTF-8', sep=';')
    df_region_data = pd.read_csv(DATA_PATH.joinpath('region_data.csv'), header=0, encoding='UTF-8', sep=';')
    df_country_data = pd.read_csv(DATA_PATH.joinpath('country_data.csv'), header=0, encoding='UTF-8', sep=';')

    # TODO: save this transformed data to the file
    # TODO: simplify region shapes
    # Transform native x, y to lat, lon
    df_region_data['geom'] = df_region_data['geom'].apply(wkt.loads)
    gdf_region_data = gpd.GeoDataFrame(df_region_data, crs='EPSG:31982', geometry='geom')
    gdf_region_data = gdf_region_data.to_crs(epsg='4326')

    return df_city_data, gdf_region_data, df_country_data


def get_data(city_id: int) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Returns the data for the report
    :return: city_data, region_data, country_data
    """
    df_city_data, gdf_region_data, df_country_data = read_data()

    # with open(DATA_PATH.joinpath('region_data.json'), 'w') as f:
    #     f.write(gdf_region_data.to_json())
    df_city_data = df_city_data[df_city_data['city_id'] == city_id]

    return df_city_data, gdf_region_data, df_country_data
