
import streamlit as st
import qdrant_client
import sys
import os

st.title("Qdrant Debugger")

st.write(f"Python Executable: {sys.executable}")
st.write(f"Qdrant Client Version: {qdrant_client.__version__}")
st.write(f"Qdrant Client File: {qdrant_client.__file__}")

from qdrant_client import QdrantClient

st.write("### QdrantClient Attributes")
client = QdrantClient(":memory:")
has_search = hasattr(client, 'search')
st.write(f"Has 'search' method: **{has_search}**")

st.write("### Dir(client)")
st.write(dir(client))

try:
    from langchain_community.vectorstores import Qdrant
    st.write("LatnChain Community Qdrant Imported")
except Exception as e:
    st.error(f"LangChain Import Error: {e}")
