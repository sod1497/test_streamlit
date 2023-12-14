import sys
from pathlib import Path
import pandas as pd
import streamlit as st
from components.report_map_folium import report_map_folium
from components.report_map import report_map

BASE_PATH = Path(__file__).resolve().parent

sys.path.append(str(BASE_PATH.joinpath('../')))

from constants import RISK_LEVELS
from data import get_data


# Params

def get_query_param(param) -> [str]:
    """
    Returns the query params
    Compatible with the new and the experimental method (theoretically)
    https://github.com/streamlit/streamlit/issues/7665
    :return: query params
    """
    try:
        value = st.experimental_get_query_params().get(param)
        return value if isinstance(value, list) else [value]
    except Exception as e:
        print('Error getting query params using the experimental method. It should be changed to the new one.')
        return st.query_params.get_all(param)


try:
    CITY_ID = 0 if get_query_param('city-id')[0] != 'None' else int(get_query_param('city-id')[0])
except Exception as e:
    print(f"Couldn't load query parameters: {e}")

# Data

try:
    df_city_data, df_region_data, df_country_data = get_data(city_id=CITY_ID)
except Exception as e:
    print(f"Couldn't load data: {e}")


# Handlers

def get_city_id_selected(df_city_data: pd.DataFrame, last_clicked: dict) -> int:
    return 1


# Layout

if 'last_clicked' not in st.session_state:
    st.session_state['last_clicked'] = None

# Map and KPI country
last_clicked = None
if st.session_state['last_clicked'] is not None:
    last_clicked = st.session_state["last_clicked"]

out = report_map_folium(df_city_data=df_city_data, df_region_data=df_region_data, city_id=CITY_ID, last_clicked=last_clicked)

if out['last_clicked'] is not None and out['last_clicked'] != st.session_state["last_clicked"]:
    st.session_state["last_clicked"] = out['last_clicked']
    # city_id_selected = get_city_id_selected(df_city_data, out['last_clicked'])
    # st.experimental_set_query_params(**{'city-id': city_id_selected})  # Can't use this. It forces a full reload
    st.rerun()

# Destination and risk
c_dest, c_risk = st.columns(2, gap="small")

with c_dest:
    st.write('Destination: {}'.format(df_city_data['city'].values[0]))
    st.write('Date: {}, {}'.format(df_city_data['month'].values[0], df_city_data['year'].values[0]))

with c_risk:
    c_risk_l, c_risk_r = st.columns(2, gap="small")
    with c_risk_l:
        st.write('Area risk')

    with c_risk_r:
        st.markdown(
            '<img src="./app/static/mosquitoes.png" height="50" style="background-color: white">',
            unsafe_allow_html=True,
        )
        st.write(RISK_LEVELS[df_city_data['risk_area'].values[0]]['code'])

st.divider()

# KPIs
c_profilaxis, c_resistance = st.columns(2, gap="small")

with c_profilaxis:
    c_profilaxis_logo, c_profilaxis_content = st.columns(2, gap="small")

    with c_profilaxis_logo:
        st.markdown(
            '<img src="./app/static/profilaxis.png" height="50" style="background-color: white">',
            unsafe_allow_html=True,
        )

    with c_profilaxis_content:
        st.write('Profilaxis')
        st.write('Quimioprofilaxis only recommended in risk areas')

with c_resistance:

    c_resistance_logo, c_resistance_content = st.columns(2, gap="small")

    with c_resistance_logo:
        st.markdown(
            '<img src="./app/static/resistance.png" height="50" style="background-color: white">',
            unsafe_allow_html=True,
        )

    with c_resistance_content:
        st.write('Resistance')
        st.write('There is resistance to cloroquine')

st.divider()

c_population, c_altitude, c_temperature, c_precipitation = st.columns(4, gap="small")

with c_population:
    st.write('Population density')
    st.write(df_city_data['population_density'].values[0])
    st.write('inhabitants/km2')
    st.write('The population density is average, between {} inh/km2 and {} inh/km2. The risk is slightly reduced as mosquitoes prefer rural areas.'.format(500, 2500))

with c_altitude:
    st.write('Altitude')
    st.write(df_city_data['altitude_mean'].values[0])
    st.write('meters')
    st.write('The mean altitude is lower than {} m. The risk is not reduced as it is an ideal altitude for mosquitoes.'.format(1500))

with c_temperature:
    st.write('Temperature')
    st.write(df_city_data['temperature_mean'].values[0])
    st.write('centigrade degrees')
    st.write('The mean temperature for this month is medium-high, between {}ºC and {}ºC. The risk is not reduced as it\'s an ideal temperature for mosquitoes.'.format(25, 35))

with c_precipitation:
    st.write('Precipitation')
    st.write(df_city_data['precipitations_mean'].values[0])
    st.write('mm')
    st.write('The mean precipitations for this month are low, between {} mm and {} mm. The risk is reduced as mosquitoes prefer more humid areas.'.format(5, 20))

# Footer

