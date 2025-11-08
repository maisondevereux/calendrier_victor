# app.py
import streamlit as st
import pandas as pd

# --- CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Calendrier Garde Victor", layout="wide")

# --- CHARGEMENT DU FICHIER EXCEL
@st.cache_data
def load_data():
    url = "https://github.com/maisondevereux/calendrier_victor/raw/main/calendrier_garde_victor_2025_2026_essai.xlsx"
    df = pd.read_excel(url)
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# --- STYLE COULEUR
def couleur_ligne(row):
    if pd.notna(row['nom_ferie']):
        return ['background-color: #F4CCCC'] * len(row)   # rouge clair
    elif row['Vacances_scolaires'] not in ["", None]:
        return ['background-color: #EAD1DC'] * len(row)   # violet clair
    elif row['parent'] == 'Jerome':
        return ['background-color: #C6E0B4'] * len(row)   # vert clair
    elif row['parent'] == 'Sanou':
        return ['background-color: #BDD7EE'] * len(row)   # bleu clair
    else:
        return [''] * len(row)

# --- INTERFACE
st.title("📅 Calendrier de garde Victor")
st.markdown("Semaine par semaine, avec codes couleur : Jérôme / Sanou / Vacances / Fériés")

# Sélecteurs dynamiques
annees = sorted(df['annee'].unique())
annee_sel = st.selectbox("Année", annees, index=len(annees)-1)

mois = sorted(df.loc[df['annee'] == annee_sel, 'mois'].unique())
mois_sel = st.selectbox("Mois", mois)

# Filtrage
df_filtre = df[(df['annee'] == annee_sel) & (df['mois'] == mois_sel)]

# Affichage stylé
styled = df_filtre.style.apply(couleur_ligne, axis=1)
st.dataframe(styled, use_container_width=True)

st.caption("🟩 Jérôme  🟦 Sanou  🟪 Vacances scolaires  🔴 Fériés")
