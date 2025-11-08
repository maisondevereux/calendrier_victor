import pandas as pd
import streamlit as st

# -----------------------------
# ⚙️ Configuration
# -----------------------------
st.set_page_config(page_title="Calendrier Victor", layout="wide")

# 🔧 Bloc pour forcer un affichage lisible sur iPhone / iPad
st.markdown("""
    <style>
    /* Forcer le thème clair sur Safari iOS */
    html, body, [class*="css"]  {
        color: black !important;
        background-color: white !important;
    }

    /* Forcer le texte noir dans les tableaux */
    div[data-testid="stDataFrame"], table, th, td, span, p {
        color: black !important;
    }

    /* Uniformiser les couleurs dans le mode sombre forcé d’iOS */
    @media (prefers-color-scheme: dark) {
        html, body, [class*="css"] {
            color: black !important;
            background-color: white !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 📅 Titre de la page
# -----------------------------
st.title("📅 Calendrier de garde Victor — 2025-2026")
# -----------------------------
# 📂 Chargement et nettoyage des données
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("calendrier_garde_victor_2025_2026_essai.xlsx")

    # Conversion en date (sans heures)
    df["date"] = pd.to_datetime(df["date"]).dt.date

    # ➕ Extraction du numéro du jour dans le mois
    df["jour_num"] = pd.to_datetime(df["date"]).dt.day

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

    # 🧩 Réorganisation : insérer jour_num entre "jour" et "mois"
    cols = list(df.columns)
    if "jour_num" in cols and "jour" in cols and "mois" in cols:
        cols.insert(cols.index("mois"), cols.pop(cols.index("jour_num")))
        df = df[cols]

    # 🧩 Réorganisation : "parent" juste après "mois"
    if "parent" in cols and "mois" in cols:
        cols.insert(cols.index("mois") + 1, cols.pop(cols.index("parent")))
        df = df[cols]

    return df

df = load_data()

# -----------------------------
# 🎨 Fonctions de coloration
# -----------------------------
def color_row(row):
    """Coloration par ligne complète avec fond parent + texte rouge si jour férié"""
    # Déterminer le fond en fonction du parent
    if "Jerome" in str(row["parent"]):
        background = "#d2f8d2"  # vert clair
    elif "Sanou" in str(row["parent"]):
        background = "#cce0ff"  # bleu clair
    elif str(row["jour"]).strip().lower() == "vendredi":
        background = "#fff4cc"  # jaune clair
    else:
        background = "white"

    # Si jour férié, texte rouge mais garder fond du parent
    if pd.notna(row["nom_ferie"]) and str(row["nom_ferie"]).strip() != "":
        style = f"background-color: {background}; color: red; font-weight: bold;"
    else:
        style = f"background-color: {background};"

    return [style] * len(row)

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

# 🧩 Masquer les colonnes techniques
df_filtre_visu = df_filtre.drop(columns=["date", "mois_annee"])

# -----------------------------
# 🖌️ Application des styles
# -----------------------------
styled_df = (
    df_filtre_visu.style
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
- 🔴 **Jours fériés : texte rouge, fond du parent conservé**
""")

st.dataframe(styled_df, use_container_width=True)

# -----------------------------
# 🧠 Note de bas de page
# -----------------------------
st.markdown(
    "<p style='color:gray; font-size:13px;'>"
    "Les colonnes <b>date</b> et <b>mois_annee</b> sont masquées dans l'affichage. "
    "La colonne <b>jour_num</b> affiche le numéro du jour dans le mois. "
    "Les jours fériés sont en <b>texte rouge</b> sur le fond du parent. "
    "La colonne <b>parent</b> reste juste après <b>mois</b>. "
    "Les vacances scolaires sont en violet uniquement dans leur colonne."
    "</p>",
    unsafe_allow_html=True
)
