import os
import sys
import types
import importlib
import unittest
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DummyStreamlit(types.SimpleNamespace):
    def __init__(self):
        super().__init__()
        self.slider_calls = []
        self.selectbox_calls = []
        self.multiselect_calls = []
        self.download_button_calls = []
        self.tabs_calls = []
        self.uploaded_files = []


    def slider(self, *args, **kwargs):
        self.slider_calls.append(kwargs.get("key"))
        return kwargs.get("value", 50)

    def title(self, *args, **kwargs):
        pass

    def subheader(self, *args, **kwargs):
        pass

    def file_uploader(self, *args, **kwargs):
        return self.uploaded_files

    def header(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def plotly_chart(self, *args, **kwargs):
        pass

    def download_button(self, *args, **kwargs):
        self.download_button_calls.append(kwargs.get("key"))

    class DummyTab:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    def tabs(self, names):
        self.tabs_calls.append(names)
        return [self.DummyTab() for _ in names]

    def markdown(self, *args, **kwargs):
        pass

    def dataframe(self, *args, **kwargs):
        pass

    def selectbox(self, *args, **kwargs):
        self.selectbox_calls.append(kwargs.get("key"))
        return None

    def multiselect(self, *args, **kwargs):
        self.multiselect_calls.append(kwargs.get("key"))

        return []

dummy_streamlit = DummyStreamlit()
sys.modules['streamlit'] = dummy_streamlit

ui = importlib.reload(importlib.import_module("src.ui_components"))

class TestUIComponents(unittest.TestCase):
    def setUp(self):
        # Reset dummy Streamlit and reload module for isolation
        self.streamlit = DummyStreamlit()
        sys.modules['streamlit'] = self.streamlit
        globals()['ui'] = importlib.reload(importlib.import_module("src.ui_components"))


    def test_sampling_slider_unique_keys(self):
        df = pd.DataFrame({
            "Point": [0, 1, 2],
            "Position": [0.0, 1.0, 2.0],
            "Force": [0.1, 0.2, 0.3],
            "Time (ms)": [0, 100, 200],
        })
        df = ui.calculate_velocity(df)

        ui.plot_sampling_interval = lambda *args, **kwargs: None
        ui.download_figure_png = lambda *args, **kwargs: None

        ui.display_sampling_interval_analysis(df, 1, file_index=1)
        ui.display_sampling_interval_analysis(df, 1, file_index=2)

        self.assertEqual(self.streamlit.slider_calls, ["sampling_bins_1_1", "sampling_bins_2_1"])

    def test_select_axis_unique_keys(self):
        df = pd.DataFrame({"A": [1], "B": [2], "C": [3]})
        ui.select_axis(df, 1, file_index=1)
        ui.select_axis(df, 1, file_index=2)

        self.assertEqual(self.streamlit.selectbox_calls, ["x_axis_1_1", "x_axis_2_1"])
        self.assertEqual(self.streamlit.multiselect_calls, ["y_axis_1_1", "y_axis_2_1"])

    def test_download_button_unique_keys(self):
        df = pd.DataFrame({"A": [1]})
        dummy_fig = types.SimpleNamespace(to_image=lambda format="png": b"img")

        ui.download_dataframe_csv(df, "file.csv", key="csv_1_1")
        ui.download_dataframe_csv(df, "file.csv", key="csv_2_1")
        ui.download_figure_png(dummy_fig, "plot.png", key="fig_1_1")
        ui.download_figure_png(dummy_fig, "plot.png", key="fig_2_1")

        expected = ["csv_1_1", "csv_2_1", "fig_1_1", "fig_2_1"]
        self.assertEqual(self.streamlit.download_button_calls, expected)


class TestAppLayout(unittest.TestCase):
    def setUp(self):
        self.streamlit = DummyStreamlit()
        sys.modules['streamlit'] = self.streamlit

        class DummyParser:
            def __init__(self, content):
                pass

            def parse_log(self):
                return []

        parser_module = importlib.import_module("src.log_parser")
        self.original_logparser = parser_module.LogParser
        parser_module.LogParser = DummyParser

        class DummyFile(types.SimpleNamespace):
            def read(self):
                return b""

        self.streamlit.uploaded_files = [DummyFile(name="a.log"), DummyFile(name="b.log")]

        ui_module = importlib.import_module("src.ui_components")
        self.original_logfileui = ui_module.LogFileUI

        class DummyLogFileUI:
            def __init__(self, *args, **kwargs):
                pass

            def display_record(self, *args, **kwargs):
                pass

        ui_module.LogFileUI = DummyLogFileUI

        importlib.import_module("app")

        parser_module.LogParser = self.original_logparser
        ui_module.LogFileUI = self.original_logfileui

    def test_tabs_created_for_uploaded_files(self):
        self.assertEqual(self.streamlit.tabs_calls, [["a.log", "b.log"]])


if __name__ == "__main__":
    unittest.main()
