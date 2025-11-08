import pandas as pd
import streamlit as st

# Chargement
df = pd.read_excel("calendrier_garde_victor_2025_2026_essai.xlsx")

# Styles couleur
def color_row(row):
    if row["nom_ferie"] != "None":
        color = "#f9d5d3"  # rouge clair
    elif row["Vacances_scolaires"] != "None":
        color = "#e3d8ff"  # violet pâle
    elif "Jerome" in str(row["parent"]):
        color = "#d2f8d2"  # vert clair
    elif "Sanou" in str(row["parent"]):
        color = "#cce0ff"  # bleu clair
    else:
        color = "white"
    return [f"background-color: {color}"] * len(row)

styled_df = df.style.apply(color_row, axis=1)

st.markdown("### 📅 Calendrier de garde Victor")
st.dataframe(styled_df, use_container_width=True)
