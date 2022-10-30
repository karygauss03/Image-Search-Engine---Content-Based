import streamlit as st
from PIL import Image

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
    if st.button("Search") and image_upload != None:
        st.image(image_upload, caption='Uploaded Image.', use_column_width=True)

def about():
    pass
    
if __name__ == '__main__':
    main()
