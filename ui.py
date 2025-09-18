# import streamlit as st
# import requests

# st.title("Multi-Agent Health News Summarizer")

# if st.button("Run Multi-Agent Pipeline"):
#     with st.spinner("Fetching and summarizing health news..."):
#         resp = requests.post("http://localhost:8000/predict", json={"max_items": 5})
#         if resp.status_code == 200:
#             data = resp.json()
#             st.success(f"Got {data['count']} results")
#             for item in data["results"]:
#                 st.subheader(item["title"])
#                 st.write(f"Link: {item['link']}")
#                 st.write(f"Published: {item['published']}")
#                 st.write(f"Source: {item['source']}")
#                 st.write(f"Category: {item['category']}")

#         else:
#             st.error("API error")
import threading
import uvicorn
from main import app  # your FastAPI app
import streamlit as st
import requests
import time

# Start FastAPI in background
def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=run_api, daemon=True).start()
time.sleep(2)  # wait a bit for server to start

# Streamlit UI
st.title("Multi-Agent Health News Summarizer")

if st.button("Run Multi-Agent Pipeline"):
    with st.spinner("Fetching and summarizing health news..."):
        resp = requests.post("http://localhost:8000/predict", json={"max_items": 5})
        if resp.status_code == 200:
            data = resp.json()
            st.success(f"Got {data['count']} results")
            for item in data["results"]:
                st.subheader(item["title"])
                st.write(f"Link: {item['link']}")
                st.write(f"Published: {item['published']}")
                st.write(f"Source: {item['source']}")
                st.write(f"Category: {item['category']}")
        else:
            st.error("API error")
