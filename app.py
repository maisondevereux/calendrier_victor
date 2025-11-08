import pandas as pd
import streamlit as st

# -----------------------------
# ⚙️ Configuration
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
# 🎨 Fonctions de coloration
# -----------------------------
def color_row(row):
    """
    Coloration par ligne complète (hors colonne Vacances_scolaires)
    """
    # Vendredi (couleur spéciale)
    if str(row["jour"]).strip().lower() == "vendredi":
        color = "#fff4cc"  # jaune clair

    # Jours fériés
    elif pd.notna(row["nom_ferie"]) and str(row["nom_ferie"]).strip().lower() not in ["none", ""]:
        color = "#f9d5d3"  # rouge clair

    # Parent Jérôme
    elif "Jerome" in str(row["parent"]):
        color = "#d2f8d2"  # vert clair

    # Parent Sanou
    elif "Sanou" in str(row["parent"]):
        color = "#cce0ff"  # bleu clair

    else:
        color = "white"

    return [f"background-color: {color}"] * len(row)


def color_vacances(val):
    """
    Coloration spécifique uniquement pour la colonne Vacances_scolaires
    """
    if pd.notna(val) and str(val).strip().lower() not in ["none", ""]:
        return "background-color: #e3d8ff"  # violet clair
    return ""


# -----------------------------
# 📅 Sélecteur de mois
# -----------------------------

# On suppose que df["date"] contient des dates réelles
# Si ce n'est pas le cas, adapte la colonne à celle où tu stockes les dates complètes
df["mois_annee"] = pd.to_datetime(df["date"]).dt.to_period("M")

# Création d'une liste unique et triée de périodes (mois + année)
mois_uniques = sorted(df["mois_annee"].unique())

# Génération des libellés lisibles, ex : "janvier 2026"
mois_labels = [p.strftime("%B %Y") for p in mois_uniques]

# Association entre libellé affiché et période réelle
mois_map = dict(zip(mois_labels, mois_uniques))

# Sélecteur Streamlit avec libellés triés chronologiquement
mois_label_selection = st.selectbox("Mois :", mois_labels)

# Conversion inverse pour filtrer le dataframe
mois_selection = mois_map[mois_label_selection]

# Filtrage des lignes correspondant au mois choisi
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
- 🔴 **Jours fériés**
""")

st.dataframe(styled_df, use_container_width=True)

# -----------------------------
# 🧠 Note de bas de page
# -----------------------------
st.markdown(
    "<p style='color:gray; font-size:13px;'>"
    "Les vacances scolaires apparaissent uniquement dans leur colonne en violet. "
    "Les vendredis sont surlignés en jaune clair. "
    "Les autres couleurs indiquent les gardes de Jérôme et Sanou."
    "</p>",
    unsafe_allow_html=True
)
