import streamlit as st
import requests

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
