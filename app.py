# app.py
import streamlit as st
from src.log_parser import LogParser
import src.ui_components as ui

# Streamlit app interface
st.title("Log File Parser with Interactive Curve Diagrams")
uploaded_files = st.file_uploader(
    "Choose log file(s)", type="log", accept_multiple_files=True
)

if uploaded_files:

    file_names = [file.name for file in uploaded_files]
    selected_name = st.sidebar.selectbox(
        "Available log files", file_names, key="file_selector"
    )
    selected_index = file_names.index(selected_name)
    uploaded_file = uploaded_files[selected_index]

    file_content = uploaded_file.read().decode("utf-8")
    st.subheader(f"Results for {uploaded_file.name}")
    logparser = LogParser(file_content)
    result = logparser.parse_log()
    if isinstance(result, tuple) and len(result) == 2:
        metadata, records_dfs = result
    else:
        metadata, records_dfs = {}, []
    file_ui = ui.LogFileUI(file_index=selected_index + 1, filename=uploaded_file.name)
    if hasattr(file_ui, "display_metadata"):
        file_ui.display_metadata(metadata)
    if records_dfs:
        for index, record_df in enumerate(records_dfs, start=1):
            file_ui.display_record(record_df, index)
    else:
        st.write("No records found under '[Recorded curves]'.")


ui.display_footer(app_version="0.3",company_name="Festo SE & Co. KG")
