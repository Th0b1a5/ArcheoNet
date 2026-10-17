# ArcheoNet 🏺
Project for the FIRST LEGO League (FLL) 2025/2026 championships.

An interactive community archaeology mapping platform built with Streamlit, Folium, and PostgreSQL.

## Getting Started

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
