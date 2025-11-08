import pandas as pd
import streamlit as st

# -----------------------------
# ⚙️ Configuration
# -----------------------------
st.set_page_config(page_title="Calendrier Victor", layout="wide")
st.title("📅 Calendrier de garde Victor — 2025-2026")

# -----------------------------
# 📂 Chargement et nettoyage des données
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("calendrier_garde_victor_2025_2026_essai.xlsx")

    # Conversion en date (sans heures)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    # Nettoyage des colonnes texte
    for col in ["nom_ferie", "Vacances_scolaires"]:
        df[col] = df[col].astype(str).replace(["None", "nan", "NaT", ""], "")

    # Suppression colonne "annee" si présente
    if "annee" in df.columns:
        df = df.drop(columns=["annee"])

    # Suppression de la première colonne si elle s'appelle "observations" ou est inutile
    first_col = df.columns[0]
    if "obs" in first_col.lower() or first_col.lower().startswith("unnamed"):
        df = df.drop(columns=[first_col])

    return df

df = load_data()

# -----------------------------
# 🎨 Fonctions de coloration
# -----------------------------
def color_row(row):
    """Coloration par ligne complète (hors colonne Vacances_scolaires)"""
    if str(row["jour"]).strip().lower() == "vendredi":
        color = "#fff4cc"  # jaune clair
    elif "Jerome" in str(row["parent"]):
        color = "#d2f8d2"  # vert clair
    elif "Sanou" in str(row["parent"]):
        color = "#cce0ff"  # bleu clair
    else:
        color = "white"
    return [f"background-color: {color}"] * len(row)

def color_text(val):
    """Texte rouge pour jours fériés"""
    if pd.notna(val) and str(val).strip() != "":
        return "color: red; font-weight: bold;"
    return ""

def color_vacances(val):
    """Couleur violette uniquement sur colonne Vacances_scolaires"""
    if pd.notna(val) and str(val).strip() != "":
        return "background-color: #e3d8ff"
    return ""

# -----------------------------
# 📅 Sélecteur de mois
# -----------------------------
df["mois_annee"] = pd.to_datetime(df["date"]).astype("datetime64[M]")
mois_uniques = sorted(df["mois_annee"].unique())
mois_labels = [pd.to_datetime(p).strftime("%B %Y") for p in mois_uniques]
mois_map = dict(zip(mois_labels, mois_uniques))
mois_label_selection = st.selectbox("Mois :", mois_labels)
mois_selection = mois_map[mois_label_selection]
df_filtre = df[pd.to_datetime(df["mois_annee"]) == pd.to_datetime(mois_selection)]

# -----------------------------
# 🖌️ Application des styles
# -----------------------------
styled_df = (
    df_filtre.style
    .apply(color_row, axis=1)
    .applymap(color_vacances, subset=["Vacances_scolaires"])
    .applymap(color_text, subset=["nom_ferie"])
)

# -----------------------------
# 🧾 Affichage
# -----------------------------
st.markdown("""
## 🗂️ Légende :
- 🟩 **Jérôme**
- 🟦 **Sanou**
- 🟪 **Vacances scolaires** (uniquement colonne dédiée)
- 🟨 **Vendredi** (jour de transition)
- 🔴 **Jours fériés (texte rouge)**
""")

st.dataframe(styled_df, use_container_width=True)

# -----------------------------
# 🧠 Note
# -----------------------------
st.markdown(
    "<p style='color:gray; font-size:13px;'>"
    "La colonne des observations et celle de l’année ont été supprimées. "
    "Les jours fériés apparaissent en <b>texte rouge</b> sans fond coloré. "
    "Les vacances scolaires apparaissent uniquement dans leur colonne en violet. "
    "Les vendredis sont surlignés en jaune clair. "
    "Les autres couleurs indiquent les gardes de Jérôme et Sanou."
    "</p>",
    unsafe_allow_html=True
)
