# PressLogParser

Ein einfaches Tool zur Analyse von Festo-Presse-Logdateien mit interaktiven Kurvendiagrammen.

## Installation

Das Projekt verwendet [Poetry](https://python-poetry.org/), um Abhängigkeiten zu verwalten:

```bash
pip install poetry
poetry install
```

## Ausführung

Starte die Streamlit-Anwendung:

```bash
poetry run streamlit run app.py
```

## Tests

Unit-Tests ausführen:

```bash
poetry run pytest
```

## Projektstruktur

```
app.py             # Streamlit-Anwendung
src/               # Code zur Logauswertung und Visualisierung
tests/             # Unit-Tests
pyproject.toml     # Poetry-Konfiguration
```

## Funktionen

- Parst Einträge im Abschnitt `[Recorded curves]`
- Berechnet Abstände und Geschwindigkeitskurven
- Interaktive Anzeige der Daten mit Plotly in Streamlit
