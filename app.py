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
        df[col] = df[col].astype(str).replace(["None", "nan", "NaT"], "")
        df[col] = df[col].fillna("")

    # Suppression colonne "annee" si présente
    if "annee" in df.columns:
        df = df.drop(columns=["annee"])

    # Suppression de la première colonne si elle s'appelle "observations" ou "Unnamed"
    first_col = df.columns[0]
    if "obs" in first_col.lower() or first_col.lower().startswith("unnamed"):
        df = df.drop(columns=[first_col])

    # Réorganisation : "parent" juste après "mois"
    cols = list(df.columns)
    if "parent" in cols and "mois" in cols:
        cols.insert(cols.index("mois") + 1, cols.pop(cols.index("parent")))
        df = df[cols]

    return df


df = load_data()

# -----------------------------
# 🎨 Fonctions de coloration
# -----------------------------
def color_row(row):
    """Coloration par ligne complète (hors colonne Vacances_scolaires)"""
    # Jours fériés → texte rouge pour toute la ligne
    if pd.notna(row["nom_ferie"]) and str(row["nom_ferie"]).strip() != "":
        return [f"color: red; font-weight: bold;"] * len(row)

    # Vendredi (couleur spéciale)
    elif str(row["jour"]).strip().lower() == "vendredi":
        return [f"background-color: #fff4cc;"] * len(row)

    # Parent Jérôme
    elif "Jerome" in str(row["parent"]):
        return [f"background-color: #d2f8d2;"] * len(row)

    # Parent Sanou
    elif "Sanou" in str(row["parent"]):
        return [f"background-color: #cce0ff;"] * len(row)

    else:
        return [""] * len(row)


def color_vacances(val):
    """Couleur violette uniquement sur la colonne Vacances_scolaires"""
    if pd.notna(val) and str(val).strip() != "":
        return "background-color: #e3d8ff"
    return ""


# -----------------------------
# 📅 Sélecteur de mois
# -----------------------------
df["mois_annee"] = pd.to_datetime(df["date"]).dt.to_period("M")
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
    df_filtre.style
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
- 🟪 **Vacances scolaires** (uniquement colonne dédiée)
- 🟨 **Vendredi** (jour de transition)
- 🔴 **Jours fériés (texte rouge sur toute la ligne)**
""")

st.dataframe(styled_df, use_container_width=True)

# -----------------------------
# 🧠 Note de bas de page
# -----------------------------
st.markdown(
    "<p style='color:gray; font-size:13px;'>"
    "Les jours fériés apparaissent désormais en <b>texte rouge sur toute la ligne</b>. "
    "La colonne <b>parent</b> est déplacée juste après la colonne <b>mois</b>. "
    "Les vacances scolaires restent violettes uniquement dans leur colonne. "
    "Les vendredis sont surlignés en jaune clair."
    "</p>",
    unsafe_allow_html=True
)
