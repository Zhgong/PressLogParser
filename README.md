# PressLogParser


PressLogParser is a simple tool for parsing log files from Festo press machines. It offers an interactive Streamlit interface for exploring the curves contained in the log.

## Installation

This project uses [Poetry](https://python-poetry.org/) to manage dependencies:


```bash
pip install poetry
poetry install
```

## Running

Launch the Streamlit app:

```bash
poetry run streamlit run app.py
```

The metadata at the top of each log file is displayed as a simple list rather
than a table.


## Testing

Run the unit tests:


```bash
poetry run pytest
```

## Project Layout

```
app.py             # Streamlit application entry
src/               # Log parsing and visualization code
tests/             # Unit tests
pyproject.toml     # Poetry configuration
```

## Features

- Parse records inside the `[Recorded curves]` section
- Parse metadata only from the first four header lines. Supported fields are
  Part no., Program name, Part ID, Timestamp, Result, Max. position, Max.
  force, NOK source, MAC Address and Serial number
- Compute and visualize sampling intervals and velocity curves
- Interactive data display in Streamlit using Plotly

---

Documentation is also available in [Chinese](docs/README.zh.md) and [German](docs/README.de.md).
