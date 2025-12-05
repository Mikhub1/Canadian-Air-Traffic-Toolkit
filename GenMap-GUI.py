#Copyright (c) 2025 National Research Council Canada
import sys
import os
import pandas as pd
import numpy as np
import webbrowser
import geopandas as gpd
import math
import folium
from folium import Choropleth, Circle, Marker, plugins
from folium.plugins import HeatMap, MarkerCluster, GroupedLayerControl
import pandas as pd
import branca
import matplotlib as matplot

import tkinter as tk
import tkinter.filedialog

#from tkinterweb import HtmlFrame #import the HTML browser
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import colorsys

#define function to set working directory
def setworkdir(event):
     global folder_path
     global checkfolder
     folder_path = tkinter.filedialog.askdirectory(title = 'Select working directory')
     if folder_path == "":
          t1.delete("1.0","end")
          t1.insert(INSERT,"A working directory must be selected")
     else:
          os.chdir(folder_path)
          checkfolder = folder_path + '/file_names.txt'
          t1.delete("1.0","end")
          t1.insert(INSERT,folder_path)
     return

#define function to set shapefile directory
def setshpfiledir(event):
     global shp_path
     shp_path = tkinter.filedialog.askdirectory(title = 'Select shapefile directory')
     t2.delete("1.0","end")
     t2.insert(INSERT,shp_path)
     return shp_path

#define function to verify all shapefiles are in the shapefiles directory
def verifydir(checkfolder, shp_path):
     # Define the function to read a file and store lines as a list
     def read_file_to_list(file_path):
         lines = []
         with open(file_path, 'r') as file:
             # Read each line and strip any extra whitespace or newline characters
             lines = [line.strip() for line in file.readlines()]
         return lines

     # Define the function to verify files in a directory
     def verify_files_in_directory(directory_path, filenames):
         # Get the list of files in the directory
         files_in_directory = os.listdir(directory_path)
    
         # Check if each file is present in the directory
         missing_files = [filename for filename in filenames if filename not in files_in_directory]
    
         if not missing_files:
              t3.delete("1.0","end")
              t3.insert(INSERT,"All files are present in the directory.")
         else:
              t3.delete("1.0","end")
              t3.insert(INSERT,"Files are missing from the directory.")

     directory_path = shp_path
     file_path = checkfolder
     filenames = read_file_to_list(file_path)
     verify_files_in_directory(directory_path, filenames)

     return 
#define the code to generate the map
def genmap(folder_path, shp_path,table,p1,p2):
     shp = shp_path
     
     # Load in the class shapefiles
     dfcla = gpd.read_file(shp+'/class A.shp')
     dfclb = gpd.read_file(shp+'/class B.shp')
     dfclc = gpd.read_file(shp+'/class C.shp')
     dfcld = gpd.read_file(shp+'/class D.shp')
     dfcle = gpd.read_file(shp+'/class E.shp')
     dfclf = gpd.read_file(shp+'/class F.shp')
     # Load in the type shapefiles 
     dftaw = gpd.read_file(shp+'/AWY LF.shp')
     dftcae = gpd.read_file(shp+'/CAE.shp')
     dftcya = gpd.read_file(shp+'/CYA.shp')
     dftcyr = gpd.read_file(shp+'/CYR.shp')
     dftcyd = gpd.read_file(shp+'/CYD.shp')
     dftcz = gpd.read_file(shp+'/CZ.shp')
     dftta = gpd.read_file(shp+'/TA.shp')
     dftca = gpd.read_file(shp+'/TCA.shp')
     dfttsp = gpd.read_file(shp+'/TSP RQ.shp')
     # Load in the Arc shapefiles
     dfarca = gpd.read_file(shp+'/arc_a_prod.geojson')
     dfarcb = gpd.read_file(shp+'/arc_b_prod.geojson')
     dfarcc = gpd.read_file(shp+'/arc_c_prod.geojson')
     dfarcd = gpd.read_file(shp+'/arc_d_prod.geojson')
     dfsfoc = gpd.read_file(shp+'/SFOC_Mask_20231207.shp')

     #set the gepgraphic reference for the shapefiles
     cl = "epsg:4326"
     dfcla.crs = cl
     dfclb.crs = cl
     dfclc.crs = cl
     dfcld.crs = cl
     dfcle.crs = cl
     dfclf.crs = cl

     dftcya.crs = cl
     dftcyr.crs = cl
     dftcyd.crs = cl
     dftcae.crs = cl
     dftcz.crs = cl
     dftaw.crs = cl
     dftta.crs = cl
     dftca.crs = cl
     dfttsp.crs = cl
     
     #-----------------------------------------------------------------------------------
     # Create a map
     #-----------------------------------------------------------------------------------
     m = folium.Map(location=[45.32,-75.0589], tiles="OpenStreetMap", zoom_start=5)
     minimap = plugins.MiniMap(position="bottomleft")
     m.add_child(minimap)
     #-----------------------------------------------------------------------------------
     #define the structure and content of the pop-up for the airspace classes when clicked
     popclassa = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     popclassb = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     popclassc = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     popclassd = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     popclasse = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     popclassf = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)

     poptcya = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     poptcae = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     poptaw = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     poptcyd = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     poptcyr = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     poptcz = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     poptta = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     poptca = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)
     popttsp = folium.GeoJsonPopup(fields=["name","class","altlow","althigh"],aliases=["Name:","Class:","Lower Altitude (ft):","Upper Altitude (ft):"],localize=True,labels=True)

     #define the color style for the individual classes
     style1 = {'fillColor': 'lightpink', 'color': 'hotpink'}
     style2 = {'fillColor': 'lightgreen', 'color': 'darkseagreen'}
     style3 = {'fillColor': 'paleturquoise', 'color': 'turquoise'}
     style4 = {'fillColor': 'peachpuff', 'color': 'sandybrown'}
     style5 = {'fillColor': 'gainsboro', 'color': 'silver'}
     style6 = {'fillColor': 'lightsteelblue', 'color': 'cornflowerblue'}
     #define color style for the types
     style7 = {'fillColor': 'pink', 'color': 'lightcoral'}
     style8 = {'fillColor': 'lightcyan', 'color': 'cyan'}
     style9 = {'fillColor': 'slateblue', 'color': 'darkslateblue'}
     style10 = {'fillColor': 'yellowgreen', 'color': 'olivedrab'}
     style11 = {'fillColor': 'lightgrey', 'color': 'grey'}
     style12 = {'fillColor': 'indianred', 'color': 'firebrick'}
     style13 = {'fillColor': 'lightskyblue', 'color': 'dodgerblue'}
     style14 = {'fillColor': 'mediumpurple', 'color': 'rebeccapurple'}
     style15 = {'fillColor': 'darkcyan', 'color': 'darkslategrey'}
     #Define color style for the ARCS
     style16 = {'fillColor': 'palegoldenrob', 'color': 'khaki'}
     style17 = {'fillColor': 'wheat', 'color': 'tan'}
     style18 = {'fillColor': 'aquamarine', 'color': 'turquoise'}
     style19 = {'fillColor': 'lavender', 'color': 'slateblue'}
     style20 = {'fillColor': 'mistyrose', 'color': 'salmon'}

     #create the polygon feature and add it to the map
     #-------------------------------------------- Classes ----------------------------------------------------------------------------------------
     clagr = folium.FeatureGroup(name='<span style=\\"color: red;\\">Class A</span>',show = False)
     clbgr = folium.FeatureGroup(name='<span style=\\"color: red;\\">Class B</span>',show = False)
     clcgr = folium.FeatureGroup(name='<span style=\\"color: red;\\">Class C</span>',show = False)
     cldgr = folium.FeatureGroup(name='<span style=\\"color: red;\\">Class D</span>',show = False)
     clegr = folium.FeatureGroup(name='<span style=\\"color: red;\\">Class E</span>',show = False)
     clfgr = folium.FeatureGroup(name='<span style=\\"color: red;\\">Class F</span>',show = False)

     folium.GeoJson(dfcla, name = "Class A", popup=popclassa,style_function=lambda x:style1,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False).add_to(clagr)
     folium.GeoJson(dfclb, name = "Class B", popup=popclassb,style_function=lambda x:style2,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False).add_to(clbgr)
     folium.GeoJson(dfclc, name = "Class C", popup=popclassc,style_function=lambda x:style3,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False).add_to(clcgr)
     folium.GeoJson(dfcld, name = "Class D", popup=popclassd,style_function=lambda x:style4,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False).add_to(cldgr)
     folium.GeoJson(dfcle, name = "Class E", popup=popclasse,style_function=lambda x:style5,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False).add_to(clegr)
     folium.GeoJson(dfclf, name = "Class F", popup=popclassf,style_function=lambda x:style6,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False).add_to(clfgr)

     clagr.add_to(m)
     clbgr.add_to(m)
     clcgr.add_to(m)
     cldgr.add_to(m)
     clegr.add_to(m)
     clfgr.add_to(m)
     #-------------------------------------------- Types ------------------------------------------------------------------------------------------
     taw = folium.FeatureGroup(name='<span style=\\"color: red;\\">AWY LF</span>',show = False)
     cya = folium.FeatureGroup(name='<span style=\\"color: red;\\">CYA</span>',show = False)
     cae = folium.FeatureGroup(name='<span style=\\"color: red;\\">CAE</span>',show = False)
     cyr = folium.FeatureGroup(name='<span style=\\"color: red;\\">CYR</span>',show = False)
     cz = folium.FeatureGroup(name='<span style=\\"color: red;\\">CZ</span>',show = False)
     cyd = folium.FeatureGroup(name='<span style=\\"color: red;\\">CYD</span>',show = False)
     ta= folium.FeatureGroup(name='<span style=\\"color: red;\\">TA</span>',show = False)
     tca = folium.FeatureGroup(name='<span style=\\"color: red;\\">TCA</span>',show = False)
     tsp = folium.FeatureGroup(name='<span style=\\"color: red;\\">TSP RQ</span>',show = False)

     folium.GeoJson(dftaw, name = "AWY LF", popup=poptaw,style_function=lambda x:style7,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(taw)
     folium.GeoJson(dftcya, name = "CYA", popup=poptcya,style_function=lambda x:style8,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(cya)
     folium.GeoJson(dftcae, name = "CAE", popup=poptcae,style_function=lambda x:style9,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(cae)
     folium.GeoJson(dftcyr, name = "CYR", popup=poptcyr,style_function=lambda x:style10,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(cyr)
     folium.GeoJson(dftcz, name = "CZ", popup=poptcz,style_function=lambda x:style11,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(cz)
     folium.GeoJson(dftcyd, name = "CYD", popup=poptcyd,style_function=lambda x:style12,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(cyd)
     folium.GeoJson(dftta, name = "TA", popup=poptta,style_function=lambda x:style13,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(ta)
     folium.GeoJson(dftca, name = "TCA", popup=poptca,style_function=lambda x:style14,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(tca)
     folium.GeoJson(dfttsp, name = "TSP RQ", popup=popttsp,style_function=lambda x:style15,
                    highlight_function=lambda feature: {"fillColor": ("blue" if "e" in feature["properties"]["name"].lower() else "#ffff00"),},
                    zoom_on_click=False, show = False).add_to(tsp)
     taw.add_to(m)
     cya.add_to(m)
     cae.add_to(m)
     cyr.add_to(m)
     cz.add_to(m)
     cyd.add_to(m)
     ta.add_to(m)
     tca.add_to(m)
     tsp.add_to(m)

     #-------------------------------------------- ARC --------------------------------------------------------------------------------------------
     aa = folium.FeatureGroup(name='<span style=\\"color: red;\\">ARC A</span>',show = False)
     ab = folium.FeatureGroup(name='<span style=\\"color: red;\\">ARC B</span>',show = False)
     ac = folium.FeatureGroup(name='<span style=\\"color: red;\\">ARC C</span>',show = False)
     ad = folium.FeatureGroup(name='<span style=\\"color: red;\\">ARC D</span>',show = False)
     sfoc = folium.FeatureGroup(name='<span style=\\"color: red;\\">SFOC MASK</span>',show = False)

     folium.GeoJson(dfarca, name = "ARC A",style_function=lambda x:style16,
                    highlight_function=lambda feature: {"fillColor": ("blue"),},
                    zoom_on_click=False, show = False).add_to(aa)
     folium.GeoJson(dfarcb, name = "ARC B",style_function=lambda x:style17,
                    highlight_function=lambda feature: {"fillColor": ("blue"),},
                    zoom_on_click=False, show = False).add_to(ab)
     folium.GeoJson(dfarcc, name = "ARC C",style_function=lambda x:style18,
                    highlight_function=lambda feature: {"fillColor": ("blue"),},
                    zoom_on_click=False, show = False).add_to(ac)
     folium.GeoJson(dfarcd, name = "ARC D",style_function=lambda x:style19,
                    highlight_function=lambda feature: {"fillColor": ("blue"),},
                    zoom_on_click=False, show = False).add_to(ad)
     folium.GeoJson(dfsfoc, name = "SFOC MASK",style_function=lambda x:style20,
                    highlight_function=lambda feature: {"fillColor": ("blue"),},
                    zoom_on_click=False, show = False).add_to(sfoc)
     aa.add_to(m)
     ab.add_to(m)
     ac.add_to(m)
     ad.add_to(m)
     sfoc.add_to(m)

     #-------------------------------------------- END --------------------------------------------------------------------------------------------
     #----------------------------------- Add Shapefile Layer--------------------------------------------
     #-------------- User Input, only change the next four lines--------------------------------
     
     province = p1 # spell out the province
     pr = table[p1] # Select province by abbreviation, see below

     pr1 = table[p2] # Select province by abbreviation, see below
     province1 = p2 # spell out the province

     df1 = gpd.read_file(shp+'/'+pr+'1.shp')
     df2 = gpd.read_file(shp+'/'+pr+'2.shp')
     df3 = gpd.read_file(shp+'/'+pr+'3.shp')
     df4 = gpd.read_file(shp+'/'+pr1+'1.shp')
     df5 = gpd.read_file(shp+'/'+pr1+'2.shp')
     df6 = gpd.read_file(shp+'/'+pr1+'3.shp')

     #set the geographic reference for the shapefiles
     cl = "epsg:4326"
     df1.crs = cl
     df2.crs = cl
     df3.crs = cl
     df4.crs = cl
     df5.crs = cl
     df6.crs = cl

     #add the popup to the data
     pop1 = folium.GeoJsonPopup(fields=["Density","Area","Normalized_","min_alt","max_alt"],
                                aliases=["Normalized Traffic Density (fs/hrkm\u00b2):","Area (km\u00b2):","Density (fs/hr):","Minimum Altitude (ft):","Maximum Altitude (ft):"],
                                localize=True,labels=True)
     pop2 = folium.GeoJsonPopup(fields=["Density","Area","Normalized_","min_alt","max_alt"],
                                aliases=["Normalized Traffic Density (fs/hrkm\u00b2):","Area (km\u00b2):","Density (fs/hr):","Minimum Altitude (ft):","Maximum Altitude (ft):"],
                                localize=True,labels=True)
     pop3 = folium.GeoJsonPopup(fields=["Density","Area","Normalized_","min_alt","max_alt"],
                                aliases=["Normalized Traffic Density (fs/hrkm\u00b2):","Area (km\u00b2):","Density (fs/hr):","Minimum Altitude (ft):","Maximum Altitude (ft):"],
                                localize=True,labels=True)
     pop4 = folium.GeoJsonPopup(fields=["Density","Area","Normalized_","min_alt","max_alt"],
                                aliases=["Normalized Traffic Density (fs/hrkm\u00b2):","Area (km\u00b2):","Density (fs/hr):","Minimum Altitude (ft):","Maximum Altitude (ft):"],
                                localize=True,labels=True)
     pop5 = folium.GeoJsonPopup(fields=["Density","Area","Normalized_","min_alt","max_alt"],
                                aliases=["Normalized Traffic Density (fs/hrkm\u00b2):","Area (km\u00b2):","Density (fs/hr):","Minimum Altitude (ft):","Maximum Altitude (ft):"],
                                localize=True,labels=True)
     pop6 = folium.GeoJsonPopup(fields=["Density","Area","Normalized_","min_alt","max_alt"],
                                aliases=["Normalized Traffic Density (fs/hrkm\u00b2):","Area (km\u00b2):","Density (fs/hr):","Minimum Altitude (ft):","Maximum Altitude (ft):"],
                                localize=True,labels=True)

     #define the colormap
     viridis_colors = matplot.colormaps['viridis']

     perc = [0.1*i for i in range(0, 11)]
     dens_pow10 = [((p-0.65)/0.18) for p in perc]
     dens = [10**((p-0.65)/0.18) for p in perc]
     colour_rgb = [viridis_colors(p) for p in perc]
     colour_hex = ["#" + "".join("%02X" % round(i*255) for i in colour[0:3]) for colour in colour_rgb]

     dens_pow10_str = [str(round(v,1)) for v in dens_pow10] 
     colormap = branca.colormap.LinearColormap(colors = colour_hex, vmin = -4, vmax = 2.5, index = dens_pow10 ,caption="10^x, s/hr*km^2", tick_labels = dens_pow10_str)
     
     #define the color style for the individual shapefile layer
     def st_fun(feature):
          density = feature["properties"]["Density"]
          
          if density > 0:
             percentile = 100*((math.log10(density)*0.18 + 0.65))
          else:
             percentile = 0
             
          if percentile > 100:
             percentile = 100
          elif percentile < 0:
             percentile = 0

          viridis_colors = matplot.colormaps['viridis']
          rgb_colour = viridis_colors(percentile/100)
          rgbhex = "#" + "".join("%02X" % round(i*255) for i in rgb_colour[0:3])

          ss = {
               "fillColor": rgbhex,
               "fillOpacity": 0.4,
               "weight": 0,
          }
          return ss

     #create the group to be added to the map
     group1 = folium.FeatureGroup(name= province+' 0-400 ft')
     group2 = folium.FeatureGroup(name= province+' 400-1000 ft')
     group3 = folium.FeatureGroup(name= province+' 1000-2000 ft')
     group4 = folium.FeatureGroup(name= province1+' 0-400 ft')
     group5 = folium.FeatureGroup(name= province1+' 400-1000 ft')
     group6 = folium.FeatureGroup(name= province1+' 1000-2000 ft')

     #create the polygon feature and add it to the map
     folium.GeoJson(df1,
                    name = province,
                    style_function=st_fun,
                    zoom_on_click=False,
                    popup=pop1
                    ).add_to(group1)
     folium.GeoJson(df2,
                    name = province,
                    style_function=st_fun,
                    zoom_on_click=False,
                    popup=pop2
                    ).add_to(group2)
     folium.GeoJson(df3,
                    name = province,
                    style_function=st_fun,
                    zoom_on_click=False,
                    popup=pop3
                    ).add_to(group3)
     folium.GeoJson(df4,
                    name = province,
                    style_function=st_fun,
                    zoom_on_click=False,
                    popup=pop4
                    ).add_to(group4)
     folium.GeoJson(df5,
                    name = province,
                    style_function=st_fun,
                    zoom_on_click=False,
                    popup=pop5
                    ).add_to(group5)
     folium.GeoJson(df6,
                    name = province,
                    style_function=st_fun,
                    zoom_on_click=False,
                    popup=pop6
                    ).add_to(group6)

     #add the group top the map
     group1.add_to(m)
     group2.add_to(m)
     group3.add_to(m)
     group4.add_to(m)
     group5.add_to(m)
     group6.add_to(m)

     #-------------------------------------------- add grouped layer control ---------------------------------------------------------------------
     GroupedLayerControl(
         groups={
           '---------Province Layers--------': [group1,group2,group3,group4,group5,group6],
           '--------AIRSPACE CLASSES--------':[clagr,clbgr,clcgr,cldgr,clegr,clfgr],
           '---------AIRSPACE TYPES---------':[taw,cya,cae,cyr,cz,cyd,ta,tca,tsp],
           '--------------ARCS--------------':[aa,ab,ac,ad,sfoc],
         },
         exclusive_groups=False,
         collapsed=True
     ).add_to(m)

     #--------------------------------------------------------------------------------------------------------------------------------------
     #folium.plugins.HeatMap(data = latlonden, name = "Density",max_zoom = 1000, radius = 1, blur = 1,gradient = gradient_map).add_to(m_1)
     folium.LayerControl().add_to(m)

     colormap.add_to(m)

     t4.delete("1.0","end")
     t4.insert(INSERT,"Map Generation Complete!")
     
     # Display the map
     m.save(folder_path+"/"+province+"_"+province1+".html")
     url = "file:///"+folder_path+"/"+province+"_"+province1+".html"
     webbrowser.open(url,new=2)

#-------------------------- Define GUI Code -----------------------------------------------
#Initialize main window
w = tk.Tk()
w.geometry("1200x200")
w.title("Traffic Density Visualization Tool")
l1 = Label(w,text = "Select Provinces and/or Territories to Visualize Data:")
l1.place(x = 0, y = 95)

#define buttons
bwd = b1 = tk.Button(w,text = "Set Working Directory", height = 1, width = 17, command = setworkdir)
b1.place(x=0,y=0)
b1.bind('<Button-1>', setworkdir)

b1 = tk.Button(w,text = "Set Shapefile Directory", height = 1, width = 17, command = setshpfiledir)
b1.place(x=0,y=30)
b1.bind('<Button-1>', setshpfiledir)

b2 = tk.Button(w,text = "Verify Directory", height = 1, width = 17, command =lambda: verifydir(checkfolder,shp_path))
b2.place(x=0,y=60)
b2.bind('<Button-2>', verifydir)

b3 = tk.Button(w,text = "Generate Map", height = 1, width = 17, command =lambda: genmap(folder_path,shp_path,table,p1,p2))
b3.place(x=0,y=150)
b3.bind('<Button-2>', genmap)

#define the text regions that are updated during code execution
t1 = tk.Text(w, height = 1,width = 130, bg = "light cyan")
t1.place(x = 150, y = 3)
t2 = tk.Text(w, height = 1,width = 130, bg = "light cyan")
t2.place(x = 150, y = 33)
t3 = tk.Text(w, height = 1,width = 130, bg = "light cyan")
t3.place(x = 150, y = 63)
t4 = tk.Text(w, height = 1,width = 50, bg = "light cyan")
t4.place(x = 150, y = 153)

#Define table of provinces and abbreviations
table = { 
    'British Columbia': 'BC', 
    'Alberta': 'AB',
    'Manitoba': 'MB', 
    'Saskatchewan':'SK', 
    'Ontario':'ON', 
    'Quebec':'QC', 
    'New Brunswick':'NB',
    'Northwest Territories':'NWT',
    'Prince Edward Island':'PEI',
    'Newfoundland':'NL',
    'Nova Scotia':'NS',
    'Nunavut':'NU'
}

# Dropdown menu options 
options = [ 
    "Alberta",
    "British Columbia",  
    "Manitoba",
    "New Brunswick",
    "Newfoundland",
    "Northwest Territories",
    "Nova Scotia",
    "Nunavut",
    "Ontario",
    "Prince Edward Island",
    "Quebec", 
    "Saskatchewan"    
] 
  
# datatype of menu text 
clicked1 = StringVar(w)
clicked2 = StringVar(w)

# Create Dropdown menu
#initialize the selection of the drop down
p1 = "Alberta"
p2 = "Alberta"
drop1 = OptionMenu( w , clicked1,options[0], *options ) 
drop1.place(x = 25, y = 123)
drop2 = OptionMenu( w , clicked2, options[0], *options ) 
drop2.place(x = 150, y = 123)

#update selection from drop down
def ch(*args):
     global p1
     p1 = clicked1.get()
     #print(p1,table[p1])
     return p1
def ch2(*args):
     global p2
     p2 = clicked2.get()
     #print(p2,table[p2])
     return p2

clicked1.trace('w',ch)
clicked2.trace('w',ch2)

w.mainloop()

