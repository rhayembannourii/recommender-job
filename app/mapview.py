# import pandas as pd
# import pymongo
# from pymongo import MongoClient
# import urllib.parse
# from data_base import *
# from geopy.exc import GeocoderTimedOut
# from geopy.geocoders import Nominatim
#
#
# def findGeocode(city):
#
#     try:
#         geolocator = Nominatim(user_agent="rhayem.bannouri@esprit.tn")
#         return geolocator.geocode(city)
#
#     except GeocoderTimedOut:
#
#         return findGeocode(city)
#
# df=get_All_collections()
# def get_country_code():
#     df=df[["Country"]]
#     longitude = []
#     latitude = []
#     for i in (df["Country"]):
#
#         if findGeocode(i) != None:
#
#             loc = findGeocode(i)
#
#             latitude.append(loc.latitude)
#             longitude.append(loc.longitude)
#
#         else:
#             latitude.append(np.nan)
#             longitude.append(np.nan)
#         # now add this column to dataframe
#     df["Longitude"] = longitude
#     df["Latitude"] = latitude
#
#     return df
