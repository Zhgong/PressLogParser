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

    def slider(self, *args, **kwargs):
        self.slider_calls.append(kwargs.get("key"))
        return kwargs.get("value", 50)

    def header(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def plotly_chart(self, *args, **kwargs):
        pass

    def download_button(self, *args, **kwargs):
        pass

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

if __name__ == "__main__":
    unittest.main()
