import streamlit as st
from urllib.parse import urlparse, parse_qs
import os
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import YoutubeLoader

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# Function to get video information


def get_info(url, lang):
    url_data = urlparse(url)
    video_id = parse_qs(url_data.query)["v"][0]
    if not video_id:
        st.error('Video ID not found. ❌')
        return None

    loader = YoutubeLoader.from_youtube_channel(
        link, add_video_info=False, language=lang)
    loader.load()
    loader_info = YoutubeLoader.from_youtube_channel(
        link, add_video_info=True, language=lang)
    info = loader_info.load()
    title = info[0].metadata['title']
    author = info[0].metadata['author']
    return title, author

# Function to answer YouTube questions


def answer_ytb(url, query, lang):
    url_data = urlparse(url)
    video_id = parse_qs(url_data.query)["v"][0]
    if not video_id:
        st.error('Video ID not found. ❌')
        return None

    try:
        loader = YoutubeLoader.from_youtube_channel(
            link, add_video_info=False, language=lang)
        loader.load()
        index = VectorstoreIndexCreator().from_loaders([loader])
        response = index.query(query)
        return response
    except Exception as e:
        st.error('An error occurred while retrieving the transcript. ❌')
        st.error(e)
        return None


if __name__ == '__main__':
    st.markdown('<h1 align="center">YouTube Question Answering 🎥</h1>',
                unsafe_allow_html=True)
    st.subheader('')
    try:
        link = st.text_input('Enter the video link')
        if link:
            lang = st.selectbox('Select the video language', [
                                'en', 'fr', 'de', 'es'])
            if lang:
                title, author = get_info(link, lang)
                st.markdown(
                    f'<h2 align="center">Title : {title} </h2>', unsafe_allow_html=True)
                st.markdown(
                    f'<h2 align="center">Author : {author} </h2>', unsafe_allow_html=True)

                if st.checkbox('Is this the correct video? ✅'):
                    query = st.text_input('Ask your question')
                    if query and lang:
                        response = answer_ytb(link, query, lang)
                        st.markdown(
                            '<h3 align="center">Answer to your question</h3>', unsafe_allow_html=True)
                        st.write(response)
    except:
        st.error('An error occurred. Is the correct language selected? ❌')
