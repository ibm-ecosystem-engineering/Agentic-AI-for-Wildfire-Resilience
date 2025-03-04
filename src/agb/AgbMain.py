import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os
import ibmpairs.client as client
import ibmpairs.query as query
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os
import json
import rasterio
from IPython.display import display as display_summary
from IPython import display
import configparser
import folium,numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import branca.colormap as cm

from llm.LlmMain import LlmMain

from CommonConstants import *

class AgbMain(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def invoke(self, payload):
        self.logger.info("invoke started ... ")
        
        ### Retrive parameters
        question = payload["input"]

        api_key = os.getenv("api.api_key", "")
        tenant_id = os.getenv("api.tenant_id", "")
        org_id = os.getenv("api.org_id", "")


        EI_client_v4 = client.get_client(org_id    = org_id,
                                  tenant_id = tenant_id,
                                  api_key   = api_key,
                                  version   = 4
                                )

        # submit, checks the status and downloads the result of the query (this will poll until the result is ready)
        agb_historical_difference_v4_query_object = query.submit_check_status_and_download({ 
                "name": "Above Ground Biomass Difference - Portugal Olieros wildfire in 2020-07-25",
                "spatial": {
                    "geojson": {
                        "type": "Feature",
                        "geometry": {"type":"MultiPolygon",                             
                                    "coordinates":[[[[-7.916217137906241,39.976531662093905],
                                                    [-7.729339355956771,39.97686418483759],
                                                    [-7.735480699467551,39.805153130972634],
                                                    [-7.918191426621587,39.80469095468477],
                                                    [-7.916217137906241,39.976531662093905]]]],                          
                                    }   
                    }
                },
                "temporal": { "years": [2020, 2021]  },
                "layers": [ { "datalayer": "above-ground-biomass" } ]
                },EI_client_v4)

        agb_historical_difference_file_list = agb_historical_difference_v4_query_object.list_files()
        #This gets the folder location of where the query result is downloaded.
        download_location = agb_historical_difference_v4_query_object.get_download_folder() + agb_historical_difference_v4_query_object.id
        summary_file = download_location + '/' +'Above Ground Biomass-above ground biomass summary agb.json'

        summary = pd.read_json(summary_file)
        # display_summary(summary)

        # pd.set_option('display.max_colwidth', None)

        # v4qid=agb_historical_difference_v4_query_object.get_id()
        # self.Display_AGB_difference_between_2_years(v4qid, display_agb_summary_file=False)

        ### query watsonx model
        resp = {
            "msg" : "Success",
            "result" : summary
        }

        self.logger.info("invoke completed ... ")

        return resp


    def now():
        return datetime.datetime.utcnow().isoformat()

    def get_extent(self, f):
        with open(f, 'r') as ff:
            stats = json.load(ff)
        boundingBox=stats["boundingBox"]
        myextent = [boundingBox["minLongitude"],boundingBox["maxLongitude"],boundingBox["minLatitude"],boundingBox["maxLatitude" ] ]
        return myextent


    def display_raster(self, raster_file_name, colorMap, title = None, Max=None, Min=None, myextent=None):
        if  raster_file_name.endswith('.tiff'):
            with rasterio.open(raster_file_name) as raster_file:
                if not myextent:
                    myextent=self.get_extent(raster_file_name+".json")
                data = raster_file.read(1)
                plt.figure(figsize = (20, 12))
                if Max is None:
                    Max=data.max()
                if Min is None:
                    Min = data.min()
                plt.imshow(data, cmap = colorMap, vmin = Min, vmax = Max,extent = myextent)
                if not title:
                    title=os.path.basename(raster_file_name)
                plt.title(title)
                plt.colorbar()
                plt.show()        

    def Display_AGB_difference_between_2_years(self, qid, display_agb_summary_file=True):
        root_folder = './download/'+str(qid)+'/'
        output_info_file = root_folder+'output.info'
        query_info = pd.read_json(output_info_file)
        sorted_files = sorted(query_info.files, key=lambda x: x["timestamp"], reverse=False)  # , reverse=True

        # for now pick up the first 2 files to calculate the increase/decrease in AGB
        older=sorted_files[0]
        latest=sorted_files[1]

        # get the older data (2020)
        older_tiff_fn=root_folder+older["name"]+".tiff"
        older_tiff_file = rasterio.open(older_tiff_fn)
        older = older_tiff_file.read(1)
        older_extent= self.get_extent(older_tiff_fn+'.json')

        # get the latest data (2021)
        latest_tiff_fn=root_folder+latest["name"]+".tiff"
        later_tiff_file = rasterio.open(latest_tiff_fn)
        later = later_tiff_file.read(1)

        # set nodata to 0 for the sum
        older[older==-9999] = 0
        later[later==-9999] = 0

        #calculate the older agb density total for % calculation
        older_agbd = older.sum()
        print("2020 data -> agb density:",older_agbd, ", agb:",round(older_agbd*0.09,2), ", agb carbon tons:",round(0.5*older_agbd*0.09,2))

        #calculate the latest agb density total for % calculation
        later_agbd = later.sum()
        print("2021 data -> agb density:",later_agbd, ", agb:",round(later_agbd*0.09,2), ", agb carbon tons:",round(0.5*later_agbd*0.09,2))

        #Calculate difference in AGB density  at every pixels across the whole area
        agbdensity_diff = later-older
        #Calculate difference in AGB across the whole area
        total_agbd_diff = agbdensity_diff.sum()

        AGB_Difference_tiff_file = root_folder+'Above Ground Biomass-difference.tiff'
        # Write the difference tiff file on disk
        if os.path.isfile(AGB_Difference_tiff_file):
            os.remove(AGB_Difference_tiff_file)
        with rasterio.open(AGB_Difference_tiff_file,
                    'w',
                    driver='GTiff',
                    height=agbdensity_diff.shape[0],
                    width=agbdensity_diff.shape[1],
                    count=1,
                    dtype=agbdensity_diff.dtype,
                    crs=older_tiff_file.crs,
                    transform=older_tiff_file.transform,
                    compress="lzw") as outfile:
            outfile.write(agbdensity_diff, 1)

        older_tiff_file.close()
        later_tiff_file.close()
        if total_agbd_diff<0:
            agb_assessment= "decreased :"+str(round(0.09*total_agbd_diff/0.5,2))+' ('+str(round(100*total_agbd_diff/older_agbd,2))+'%)'
        else:
            agb_assessment= "increased :"+str(round(0.09*total_agbd_diff/0.5,2))+' ('+str(round(100*total_agbd_diff/older_agbd,2))+'%)'
        print("Total Above Ground Biomass Density",agb_assessment )
        self.display_raster(AGB_Difference_tiff_file, 'RdYlGn', title='Above Ground Biomass density '+ agb_assessment,myextent=older_extent)  
        plt.show()
        # in V3 there is no summary created to compare to.
        if display_agb_summary_file:
            AGB_info = pd.read_json(root_folder+'Above Ground Biomass-above ground biomass summary agb.json')
            display(AGB_info)        