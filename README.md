# PressLogParser

A simple tool for parsing Festo press machine log files with an interactive interface.

[中文说明](docs/README.zh.md) | [Deutsche Anleitung](docs/README.de.md)

## Installation

This project manages dependencies with [Poetry](https://python-poetry.org/).

```bash
pip install poetry
poetry install
```

## Usage

Start the Streamlit application:

```bash
poetry run streamlit run app.py
```

## Tests

Run unit tests:

```bash
poetry run pytest
```

## Project Layout

```
app.py             # Streamlit app entry point
src/               # Parsing and visualization code
tests/             # Unit tests
pyproject.toml     # Poetry configuration
```

## Features

- Parses entries in the `[Recorded curves]` section
- Calculates sampling intervals and velocity curves
- Displays data interactively with Plotly in Streamlit
