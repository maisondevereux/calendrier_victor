import pandas as pd
import datetime
import streamlit as st

# --- Chargement du fichier ---
df = pd.read_csv("calendrier.csv", parse_dates=["date"])

# --- Tri chronologique ---
df = df.sort_values("date").reset_index(drop=True)

# --- Date du jour ---
today = pd.Timestamp(datetime.date.today())

# --- Trouver la ligne du jour (ou la plus proche) ---
index_today = df.index[df['date'].dt.date == today.date()]
if not index_today.empty:
    idx = index_today[0]
else:
    idx = (df['date'] - today).abs().idxmin()

# --- Fonction de coloration par ligne ---
def color_rows(row):
    if row['date'].date() == today.date():
        return ['background-color: #FFF59D'] * len(row)  # 🟡 ligne du jour
    elif row.get('nom_ferie') not in [None, "None"]:
        return ['background-color: #FFCDD2'] * len(row)  # 🔴 jour férié
    elif row['jour'] == 'vendredi':
        return ['background-color: #FFE082'] * len(row)  # 🟠 vendredi transition
    elif row['parent'] == 'Jerome':
        return ['background-color: #C8E6C9'] * len(row)  # 🟢 Jérôme
    elif row['parent'] == 'Sanou':
        return ['background-color: #BBDEFB'] * len(row)  # 🔵 Sanou
    else:
        return [''] * len(row)

# --- Mise en forme spéciale pour la colonne "Vacances_scolaires" ---
def color_vacances(val):
    if pd.notna(val) and val not in ["None", ""]:
        return 'background-color: #E1BEE7'  # 💜 violet uniquement ici
    return ''

# --- Titre et légende ---
st.markdown("""
### 📅 Légende :
- 🟢 **Jérôme**
- 🔵 **Sanou**
- 💜 **Vacances scolaires** *(uniquement la colonne dédiée)*
- 🟠 **Vendredi (jour de transition)**
- 🔴 **Jours fériés**
- 🟡 **→ Ligne du jour**
""")

# --- Position d’affichage ---
start = max(idx - 7, 0)
end = min(idx + 7, len(df))

# --- Application combinée des styles ---
styled_df = (
    df.style
    .apply(color_rows, axis=1)
    .applymap(color_vacances, subset=['Vacances_scolaires'])
)

# --- Affichage ---
st.dataframe(styled_df, use_container_width=True, height=550)

# --- Info ---
st.caption(f"📍 Position actuelle : {df.loc[idx, 'date'].strftime('%A %d %B %Y')}")
