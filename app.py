import pandas as pd
import streamlit as st

# -----------------------------
# ⚙️ Configuration
# -----------------------------
st.set_page_config(page_title="Calendrier Victor", layout="wide")

# 🔧 Bloc CSS iOS pour forcer thème clair et texte noir
st.markdown("""
    <style>
    /* Thème clair global */
    html, body, [class*="css"]  {
        background-color: white !important;
        color: black !important;
    }

    /* Force le fond blanc même si Safari passe en sombre */
    @media (prefers-color-scheme: dark) {
        html, body, [class*="css"] {
            background-color: white !important;
            color: black !important;
        }
    }

    /* Corrige les textes des tableaux Streamlit */
    div[data-testid="stDataFrame"], table, th, td, span, p, label, h1, h2, h3 {
        color: black !important;
        background-color: white !important;
    }

    /* Désactive la transparence / ombres en mode sombre */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: white !important;
        color: black !important;
    }

    /* Bordures subtiles */
    table, th, td {
        border: 1px solid #ddd !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 📅 Titre
# -----------------------------
st.title("📅 Calendrier de garde Victor — 2025-2026")

# -----------------------------
# 📂 Chargement des données
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_excel("calendrier_garde_victor_2025_2026_essai.xlsx")

df = load_data()

# -----------------------------
# 🧹 Nettoyage et préparation
# -----------------------------
df["date"] = pd.to_datetime(df["date"])
df["jour_num"] = df["date"].dt.day
df["mois_annee"] = df["date"].dt.to_period("M")

# Supprime les "None" visuels
df["nom_ferie"] = df["nom_ferie"].replace("None", "").replace("none", "")
df["Vacances_scolaires"] = df["Vacances_scolaires"].replace("None", "").replace("none", "")

# Réorganiser les colonnes (jour_num entre jour et mois, parent à droite de mois)
cols = ["jour", "jour_num", "mois", "parent", "nom_ferie", "Vacances_scolaires", "mois_annee"]
df = df[[c for c in cols if c in df.columns]]

# -----------------------------
# 🎨 Fonctions de coloration
# -----------------------------
def color_row(row):
    """
    Coloration du fond selon parent et vendredi.
    Les jours fériés gardent le fond du parent, mais texte rouge.
    """
    # Couleur de base selon parent
    if "Jerome" in str(row["parent"]):
        bg_color = "#d2f8d2"  # vert clair
    elif "Sanou" in str(row["parent"]):
        bg_color = "#cce0ff"  # bleu clair
    else:
        bg_color = "white"

    # Vendredi : couleur jaune claire
    if str(row["jour"]).strip().lower() == "vendredi":
        bg_color = "#fff4cc"

    # Couleur du texte pour jour férié
    text_color = "red" if pd.notna(row["nom_ferie"]) and str(row["nom_ferie"]).strip() != "" else "black"

    return [f"background-color: {bg_color}; color: {text_color};"] * len(row)


def color_vacances(val):
    """Coloration spécifique uniquement pour la colonne Vacances_scolaires"""
    if pd.notna(val) and str(val).strip() != "":
        return "background-color: #e3d8ff"  # violet clair
    return ""

# -----------------------------
# 📅 Sélecteur de mois
# -----------------------------
mois_uniques = sorted(df["mois_annee"].unique())
mois_labels = [p.strftime("%B %Y") for p in mois_uniques]
mois_map = dict(zip(mois_labels, mois_uniques))
mois_label_selection = st.selectbox("Mois :", mois_labels)
mois_selection = mois_map[mois_label_selection]
df_filtre = df[df["mois_annee"] == mois_selection]

# -----------------------------
# 🖌️ Application des styles
# -----------------------------
styled_df = (
    df_filtre.drop(columns=["mois_annee"], errors="ignore")
    .style
    .apply(color_row, axis=1)
    .applymap(color_vacances, subset=["Vacances_scolaires"])
)

# -----------------------------
# 🧾 Affichage
# -----------------------------
st.markdown("""
## 🗂️ Légende :
- 🟩 **Jérôme**
- 🟦 **Sanou**
- 🟪 **Vacances scolaires** (uniquement dans la colonne dédiée)
- 🟨 **Vendredi** (jour de transition)
- 🔴 **Jours fériés : texte rouge, fond du parent conservé**
""")

st.dataframe(styled_df, use_container_width=True)

# -----------------------------
# 🧠 Note de bas de page
# -----------------------------
st.markdown(
    "<p style='color:gray; font-size:13px;'>"
    "Les vacances scolaires apparaissent uniquement dans leur colonne en violet. "
    "Les vendredis sont surlignés en jaune clair. "
    "Les jours fériés apparaissent en rouge, sans changement de fond. "
    "Les autres couleurs indiquent les gardes de Jérôme et Sanou."
    "</p>",
    unsafe_allow_html=True
)
