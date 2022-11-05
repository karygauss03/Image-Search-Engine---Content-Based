import streamlit as st
from PIL import Image
import requests

def main():
    selected_box = st.sidebar.selectbox(
        "Choose an option",
        ("Home", "Image Retrieval")
    )
    if selected_box == "Home":
        home()
    if selected_box == "Image Retrieval":
        image_query()

def home():
    st.title("Content based Image Retrieval")
    st.subheader("A search engine application developed by EYA Gourar & KARIM Omrane using VGG16, FastAPI, Streamlit and Elasticsearch ! Enjoy ❤️")

def image_query():
    st.header("Import your image")
    image_upload = st.file_uploader("Upload an image",type = ["jpg","png"],help="Drag and drop your image here")
    search_res_numbers = st.slider("Number of search results",min_value=1,max_value=50,value=10,help="Select the number of resulted queries")
    params = {"size":search_res_numbers}
    if st.button("Search") and image_upload != None:
        st.info("Your input image 👇", icon="ℹ️")
        st.image(image_upload, width = 224)
        res = requests.post("http://localhost:8000/image_query", files = {"image": image_upload}, params = params)
        response = res.json()
        results = []
        for hit in response:
            results.append(Image.open('./bdimage/' + hit['_source']['image_path']))
        st.success("🥳 Search results 👇", icon="✅")
        for img in results:
            st.image(img)    
    
if __name__ == '__main__':
    main()
