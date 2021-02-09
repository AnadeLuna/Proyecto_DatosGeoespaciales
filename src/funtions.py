import requests
import json
from dotenv import load_dotenv
import os
import sys
import pandas as pd
from functools import reduce
import operator
import geopandas as gpd
from pymongo import MongoClient,GEOSPHERE
import shapely.geometry


'''This Funtion it´s going to create a query and en return a GeoDataFrame'''
def query(query,limit,radius):

    '''tokens'''
    load_dotenv()
    token1 = os.getenv("token1")
    token2 = os.getenv("token2")

    '''url'''
    url_query = 'https://api.foursquare.com/v2/venues/explore'
    
    '''create the params'''
    parametros = {"client_id" : token1,
              "client_secret" : token2,
              "v": "20180323",
              "ll": "37.566879,-122.323895",
              "query": query,
              "limit": limit,
             "radius": radius}

    '''Create the request from the url and take the text from json '''
    resp = requests.get(url = url_query, params = parametros)
    data = json.loads(resp.text)    
    
    '''From the request take the response'''
    decoding_data = data.get("response")
    decoded = decoding_data.get("groups")[0]
    query_san_mateo = decoded.get("items")
    query_san_mateo

    '''The information I need to get '''
    m_name = ["venue","name"]
    m_latitud = ["venue","location","lat"]
    m_longitud = ["venue","location","lng"]

    '''A funtion to get the all the response from the query '''
    def getFromDict(dictionary,maps):
        return reduce (operator.getitem,maps,dictionary)

    '''Loop with the funtion to get the all the response from the query '''
    lst_query_san_mateo = []
    for dic in query_san_mateo:
        dict_query = {}
        dict_query["name"] = getFromDict(dic,m_name)
        dict_query["latitud"] = getFromDict(dic,m_latitud)
        dict_query["longitud"] = getFromDict(dic,m_longitud)
        lst_query_san_mateo.append(dict_query)

    '''Create a DataFrame with the all information from the query'''
    df_query_san_mateo = pd.DataFrame(lst_query_san_mateo)
    return df_query_san_mateo

'''This Funtion it´s going to create a GeoDataFrame'''
def geo_data(df_query_san_mateo):
    gdf_query_san_mateo = gpd.GeoDataFrame(df_query_san_mateo, geometry = gpd.points_from_xy(df_query_san_mateo.longitud,df_query_san_mateo.latitud))
    return gdf_query_san_mateo



'''This Funtion it´s going to create geometry points'''
def point_geometry(gdf_query_san_mateo):
    gdf_query_san_mateo["geometry"] = gdf_query_san_mateo["geometry"].apply(lambda x: shapely.geometry.mapping(x))
    return gdf_query_san_mateo


