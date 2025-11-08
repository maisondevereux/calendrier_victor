import pandas as pd
import streamlit as st

# -----------------------------
# ⚙️ Configuration générale
# -----------------------------
st.set_page_config(page_title="Calendrier Victor", layout="wide")

st.title("📅 Calendrier de garde Victor — 2025-2026")

# -----------------------------
# 📂 Chargement des données
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_excel("calendrier_garde_victor_2025_2026_essai.xlsx")

df = load_data()

# -----------------------------
# 🎨 Fonction de coloration des lignes
# -----------------------------
def color_row(row):
    # Priorité : férié > vacances > parent
    if pd.notna(row["nom_ferie"]) and str(row["nom_ferie"]).strip().lower() not in ["none", ""]:
        color = "#f9d5d3"  # rouge clair : jour férié
    elif pd.notna(row["Vacances_scolaires"]) and str(row["Vacances_scolaires"]).strip().lower() not in ["none", ""]:
        color = "#e3d8ff"  # violet : vacances
    elif "Jerome" in str(row["parent"]):
        color = "#d2f8d2"  # vert clair : Jérôme
    elif "Sanou" in str(row["parent"]):
        color = "#cce0ff"  # bleu clair : Sanou
    else:
        color = "white"
    return [f"background-color: {color}"] * len(row)

# -----------------------------
# 📅 Sélecteur de mois
# -----------------------------
mois_uniques = df["mois"].dropna().unique().tolist()
mois_selection = st.selectbox("Mois :", sorted(mois_uniques, key=lambda x: str(x).lower()))

df_filtre = df[df["mois"] == mois_selection]

# -----------------------------
# 🖌️ Application du style
# -----------------------------
styled_df = df_filtre.style.apply(color_row, axis=1)

# -----------------------------
# 🧾 Affichage
# -----------------------------
st.markdown("""
### 🗂️ Légende :
- 🟩 **Jérôme**
- 🟦 **Sanou**
- 🟪 **Vacances scolaires**
- 🔴 **Jours fériés**
""")

st.dataframe(styled_df, use_container_width=True)

# -----------------------------
# 🧠 Note
# -----------------------------
st.markdown(
    "<p style='color:gray; font-size:13px;'>"
    "Cette application affiche les périodes de garde de Victor, les vacances scolaires "
    "et les jours fériés, avec des couleurs distinctes pour Jérôme et Sanou."
    "</p>",
    unsafe_allow_html=True
)
