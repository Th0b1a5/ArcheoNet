# ArcheoNet
Project for the FIRST LEGO League (FLL) 2025/2026 championships.

An interactive community archaeology mapping platform built with Streamlit, Folium, and PostgreSQL.

This thing is INSANELY broken and clunky.

Doesnt include Postgres with the docker compose.

# Getting Started

### Dont forget to fill in the login secrets!

## A) Docker

### 1. Build image
```bash
docker build -t archeonet .
```

### 2. Run it
```bash
docker run -p 8501:8501 archeonet
```

## B) Python

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Streamlit
Copy the secrets template:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Fill in your database and OAuth credentials in `.streamlit/secrets.toml`.

### 3. Run the app
```bash
streamlit run login.py
```
