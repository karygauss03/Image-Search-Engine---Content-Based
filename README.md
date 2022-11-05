Welcome to our Image Search Engine 🔮️ 
=============================

- [Introduction](#Introduction)
- [Overview](#Overview)
- [Dependencies](#Required-Packages)

- [Project Description](#Project-Description)
- [Main steps](#Main-steps)
	- [step 1 : feature extraction](#step-1-:-feature-extraction)
    - [step 2 : Index vector representations in Elasticsearch](#step-2-:-Index-vector-representations-in-Elasticsearch)
	- [step 3 : Similarity query](#step-3-:-Similarity-query)

- [Tips](#Tips)



# Introduction

Just like Google image search, here we have built a simple Image search engine using the Deep learning model VGG16. 

This search app features elasticsearch for fast results and uses image feature vectors extracted with VGG16 model to find related images with greater context.

Matching images based on similarity of image embeddings offers higher recall of semantically relevant results, helping you find what your looking for faster!

# Overview

# Dependencies 
- Elasticsearch
- FastAPI
- Streamlit

# Project Description

Given a query image, we use Elasticsearch to find other images which look similar.

To implement a similarity search by feature matching, we follow these three steps:

    1. Convert image to feature vectors with the use of VGG16 model.
    2. Index the images and corresponding vector representations in Elasticsearch
    3. Calculate similarity between a query document and documents in the index for scoring

These steps are elaborated in the remainder of this README.md


# Main steps

To implement our image search engine, we used the images from our +10k dataset to train our model.


## Step 1 : Feature extraction
we convert our images into the size 224x224x3 because the input to VGG16 should always be 224x224x3.

we extract the deep features from all the images in the training dataset.

To extract the deep features, we are passing our input images through the 16 layered VGG model. 

We then convert the data to an n-dimensional array and perform data pre-processing.

```python
class FeatureExtractor:
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, img):
        img = img.resize((224, 224)) 
        img = img.convert('RGB')  
        x = image.img_to_array(img) 
        x = np.expand_dims(x, axis=0)  
        x = preprocess_input(x)  
        feature = self.model.predict(x)[0] 
        return feature / np.linalg.norm(feature) 
```

## Step 2 : Index vector representations in Elasticsearch
First, an index mapping with a elastiknn_dense_float_vector type must be created.

elastiknn_dense_float_vector is a Elastiknn datatype which lets you store vectors as a field in an ES doc. 
The query lets you provide a vector and retrieve the docs containing the nearest neighbors to that vector.

```python
mapping = {
  "dynamic": False,
  "properties": {
      "feature_vector": {
          "type": "elastiknn_dense_float_vector",
          "elastiknn": {
            "dims": 4096,
            "model": "exact",
            "similarity": "l2",
            "L": 60,
            "k": 3,
            "w": 2
          }
    },
    "image_path":{"type":"text","index":False}
  }
}
```
Afterwards we use our image feature extrctor to create vector representations for all images in our dataset.
The created features vector can then be stored in the Elasticsearch index.

## Step 3 : Similarity query
Thanks to the predefined functions for vector fields in Elastiknn, getting images with similar style is only a query away.

To measure similarity between vectors we can use cosine similarity as in the predefined function 'Angular'. 

Cosine similarity measures the angle between two vectors.

```python
{
    "query": {
            "elastiknn_nearest_neighbors": {
                "vec": feature_vector,
                "field": "feature_vector",
                "similarity": "l2",
                "model": "exact",
            }
        }
}
```


The result of the query is used for scoring to get the most similar images from the index.

To get the query input image and to display the output images to the website, we are using FastAPI.


# Tips


- Install elasticsearch and always check if elastic search process is running before launching main.py.

- To index all your images, paste the path to your images in the indexing-images.ipynb file. 
If your data is divided into class folders then you're ready to go.

    If not then make sure to remove the line looping over classes folders :

```python
my_path = "../your-data-path/"
for clas in class_dir : #class_dir is directory to class folders
    classpath = my_path + clas + '/'
    img_files = [f for f in listdir(classpath) if isfile(join(classpath, f))]
    .
    .
```
Instead, simply loop over your data folder :
```python
#remove 
my_path = "../your-data-path/"
img_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
for _file in img_files:	
    .
    .
```
- Run elasticsearch ```elasticsearch.bat```
- Run the FastAPI app ```uvicorn app.main:app --reload``` 
- Run the Streamlit app and navigate to http://localhost:8501/ ```streamlit run front/main.py```

    You can drop any image of a scene resembling what you are searching for and the app will return the most similar indexed images.


