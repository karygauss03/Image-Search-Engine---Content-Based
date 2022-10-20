from index_image import create_exif_data
import glob
from os import listdir
from os.path import isfile, join
import argparse
#!pip install elasticsearch
# import the Elasticsearch low-level client
from elasticsearch import Elasticsearch
import numpy as np
# import the Image and TAGS classes from Pillow (PIL)
from PIL import Image

import base64 # convert image to b64 for indexing

parser = argparse.ArgumentParser()
parser.add_argument('--root_path', type=str,
                    default='bdimage/', help='root dir for data')
parser.add_argument('--split', type=str,
		    default='Objects', help='images group exp : object or texture')           
args = parser.parse_args()             


if __name__ == "__main__":

	# create a client instance of Elasticsearch
	elastic_client = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

	_index = "images"
	# create the "images" index for Elasticsearch if necessary
	#resp = elastic_client.indices.create(
	#index = _index,
    	#body = "{}",
    	#ignore = 400 # ignore 400 already exists code
    	#)
	#print ("\nElasticsearch create() index response -->", resp)
	
	#to index bdimage dataset with split = 'object' or 'texture'
	mypath = args.root_path + args.split + '/'
	class_dir = [f for f in listdir(mypath) if join(mypath, f)]
	img_nb = 1
	for clas in class_dir :
		classpath = mypath + clas + '/'
		img_files = [f for f in listdir(classpath) if isfile(join(classpath, f))]
		for _file in img_files:
			_id = img_nb
			img = Image.open(open(classpath + _file , 'rb'))
			# get the _source dict for Elasticsearch doc
			_source = create_exif_data(img, clas, args.split)	
			# store the file name in the Elasticsearch index
			_source['name'] = _file
			# covert NumPy of PIL image to simple Python list obj
			img_array = np.asarray( Image.open(classpath + _file ) ).tolist()
			# convert the nested Python array to a str
			img_str = str( img_array )
			# put the encoded string into the _source dict
			_source["raw_data"] = img_str

			# call the Elasticsearch client's index() method
			resp = elastic_client.index(
			index = _index,
			id = _id,
			doc_type = '_doc',
    			body = _source,
    			request_timeout=60)
    	
			print ("\nElasticsearch index() response -->", resp)
			img_nb += 1
