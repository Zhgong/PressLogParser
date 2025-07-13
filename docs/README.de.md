# PressLogParser


Ein einfaches Werkzeug zum Parsen von Festo-Pressen-Logdateien mit interaktiver Kurvendarstellung.

## Installation

Das Projekt verwendet [Poetry](https://python-poetry.org/) zur Verwaltung der Abh\xE4ngigkeiten:

```bash
pip install poetry
poetry install
```

## Ausf\xFChren

Starte die Streamlit-App:

```bash
poetry run streamlit run app.py
```

Die Metadaten werden dabei als einfache Liste (keine Tabelle) angezeigt.

## Tests

F\xFChre Unit-Tests aus:

```bash
poetry run pytest
```

## Projektstruktur

```
app.py             # Einstiegspunkt der Streamlit-Anwendung
src/               # Code f\xFCr Log-Parsing und Visualisierung
tests/             # Unittests
pyproject.toml     # Poetry-Konfiguration
```

## Funktionsübersicht

- Parst die Aufzeichnungen im Abschnitt `[Recorded curves]`
- Liest Metadaten ausschlie\xDFlich aus den ersten vier Kopfzeilen. Unterst\xFCtzte Felder sind
  Part no., Program name, Part ID, Timestamp, Result, Max. position, Max.
  force, NOK source, MAC Address und Serial number
- Berechnet und zeigt Abtastintervalle sowie Geschwindigkeitskurven an
- Interaktive Datenanzeige in Streamlit mit Plotly

