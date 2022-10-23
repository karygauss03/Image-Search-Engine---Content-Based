from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np
from elasticsearch import Elasticsearch
import glob
from os import listdir
from os.path import isfile, join
import argparse
#!pip install elasticsearch
# import the Elasticsearch low-level client

import base64 # convert image to b64 for indexing

elastic_client = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# create the "images" index for Elasticsearch if necessary

resp = elastic_client.indices.create(
    index = "bdimage",
    body = { "settings" : {
            "index" : {
                "number_of_shards" : 1, 
                "number_of_replicas" : 0
            }
            },
            "mappings": {
                "obj": {
                "properties": {
                    "raw_data" : { "type": "string"},
                    "image_path": { "type": "string", "index": "not_analyzed"}
                    }
                }
            }
        },
    ignore = 400 # ignore 400 already exists code
    )
print ("\nElasticsearch create() index response -->", resp)

parser = argparse.ArgumentParser()
parser.add_argument('root_path', type=str,
                    default='bdimage/', help='root dir for data')
parser.add_argument('--split', type=str,
		    default='Objects', help='images group exp : object or texture')           
args = parser.parse_args()   

if __name__ == '__main__':
    fe = FeatureExtractor()
    _index = "bdimage"
    mypath = args.root_path + args.split + '/'
    class_dir = [f for f in listdir(mypath) if join(mypath, f)]
    img_nb = 1
    for clas in class_dir :
        classpath = mypath + clas + '/'
        img_files = [f for f in listdir(classpath) if isfile(join(classpath, f))]
        for _file in img_files:	
            print(_file)  # e.g., ./static/data/xxx.jpg
            image = Image.open(_file) ##FIX ME PATH
            feature = fe.extract(image)
            feature_path = Path("./static/features") / (_file.stem + ".npy")  # e.g., ./static/feature/xxx.npy
            np.save(feature_path, feature)
    
            # create a new dict obj for the Elasticsearch doc
            _source = {}
            _source["image_path"] = _file    	
    
    	    # convert the nested Python np.ndarray with the shape=(4096, ) to a str
            feature_str = str( feature )
    	    # put the encoded string into the _source dict
            _source["raw_data"] = feature_str

            _id = img_nb
  	        # call the Elasticsearch client's index() method
            resp = elastic_client.index(
	        	index = _index,
	        	id = _id,
	        	doc_type = '_doc',
	            	body = _source,
	            	request_timeout=60)

                        	    	    	
            print ("\nElasticsearch index() response -->", resp)
            img_nb += 1
