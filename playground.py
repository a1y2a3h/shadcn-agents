
import streamlit as st
import os
from dotenv import load_dotenv
from agents_library.workflows.summarize_and_email_graph import build_workflow as build_summary_workflow
from agents_library.workflows.translate_and_email_graph import build_workflow as build_translate_workflow
from agents_library.workflows.scrape_and_summarize_graph import build_workflow as build_scrape_summarize_workflow

load_dotenv()

st.title("shadcn-agent Playground")

workflow = st.selectbox("Choose a workflow", ["Summarize + Email", "Translate + Email", "Scrape + Summarize"])

if workflow == "Summarize + Email":
    url = st.text_input("URL to summarize", "https://en.wikipedia.org/wiki/Artificial_intelligence")
    recipient = st.text_input("Recipient Email", "test@example.com")
    if st.button("Run Workflow"):
        app = build_summary_workflow()
        summarize_input = {"url": url, "recipient": recipient}
        st.write("## Workflow Output:")
        for step in app.stream(summarize_input):
            st.json(step)
elif workflow == "Translate + Email":
    text = st.text_area("Text to translate", "Hello, how are you?")
    target_lang = st.text_input("Target Language (e.g., fr, es, de)", "fr")
    recipient = st.text_input("Recipient Email", "test@example.com")
    if st.button("Run Workflow"):
        app = build_translate_workflow()
        translate_input = {"text": text, "target_lang": target_lang, "recipient": recipient}
        st.write("## Workflow Output:")
        for step in app.stream(translate_input):
            st.json(step)
elif workflow == "Scrape + Summarize":
    url = st.text_input("URL to scrape and summarize", "https://en.wikipedia.org/wiki/Artificial_intelligence")
    if st.button("Run Workflow"):
        app = build_scrape_summarize_workflow()
        scrape_input = {"url": url}
        st.write("## Workflow Output:")
        for step in app.stream(scrape_input):
            st.json(step)
