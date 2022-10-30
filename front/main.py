import streamlit as st
from PIL import Image
import requests

def main():
    selected_box = st.sidebar.selectbox(
        "Choose an option",
        ("Home", "Image Retrieval", "About the project")
    )
    if selected_box == "Home":
        home()
    if selected_box == "Image Retrieval":
        image_query()
    if selected_box == "About the project":
        about()

def home():
    st.title("Content based Image Retrieval")
    st.subheader("A search engine application...")

def image_query():
    st.header("Import your image")
    image_upload = st.file_uploader("Upload an image",type = ["jpg","png"],help="Drag and drop your image here")
    search_res_numbers = st.slider("Number of search results",min_value=1,max_value=50,value=10,help="Select the number of resulted queries")
    params = {"size":search_res_numbers}
    if st.button("Search") and image_upload != None:
        st.subheader("Your input image 👇")
        st.image(image_upload, width = 224)
        st.subheader("🥳 Search results 👇")
        res = requests.post("http://localhost:8000/image_query", files = {"image": image_upload}, params = params)
        response = res.json()
        for hit in response:
            img = Image.open('./bdimage/' + hit['_source']['image_path'])
            st.image(img)

def about():
    pass
    
if __name__ == '__main__':
    main()
