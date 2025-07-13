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
    for file_index, uploaded_file in enumerate(uploaded_files, start=1):
        file_content = uploaded_file.read().decode("utf-8")
        st.subheader(f"Results for {uploaded_file.name}")
        logparser = LogParser(file_content)
        records_dfs = logparser.parse_log()

        if records_dfs:
            for index, record_df in enumerate(records_dfs, start=1):
                record_df = ui.calculate_velocity(record_df)
                ui.display_data_table(record_df, f"Data for Record {index}:")
                ui.download_dataframe_csv(
                    record_df, f"{uploaded_file.name}_record{index}.csv"
                )
                ui.display_sampling_interval_analysis(record_df, index, file_index=file_index)
                ui.select_and_plot_curve(record_df, index, file_index=file_index)
        else:
            st.write("No records found under '[Recorded curves]'.")

ui.display_footer(app_version="0.3",company_name="Festo SE & Co. KG")
