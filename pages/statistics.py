import streamlit as st
import base64
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Statistiques - Football Analytics Dashboard", initial_sidebar_state="collapsed")

# Charger l'image de fond en base64
with open("images/background.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Utilisation de CSS personnalisé
st.markdown(
    f"""
    <style>
    body {{
        background-image: url('data:image/jpg;base64,{encoded_image}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        height: 100vh;
        overflow: auto;
        margin: 0;
        padding: 0;
        position: relative;
    }}
    .stApp {{
        background: transparent;
    }}
    h1, h3 {{
        color: white;
        text-align: left;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }}
    h1 {{
        font-size: 4em;
        margin-top: 20px;
    }}
    h3 {{
        font-size: 1.5em;
    }}
    .navbar {{
        background-color: rgba(0, 0, 0, 1);
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 1px;
        margin-bottom: 20px;
    }}
    .stSelectbox div {{
        background-color: black;
        color: white;
        padding: 3px;
    }}
    .stSelectbox div:hover {{
        background-color: red;
    }}
    .team-label {{
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        color: white;
    }}
    .row_heading {{
        display: none;
    }}
    .blank {{
        display: none;
    }}
    .back-button {{
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
    }}
    .back-button .stButton>button {{
        background-color: black;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1em;
    }}
    .back-button .stButton>button:hover {{
        background-color: #333;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Bouton de retour fixe en haut à gauche
st.markdown('<div class="back-button">', unsafe_allow_html=True)
if st.button("⬅ Retour à l'Accueil"):
    st.switch_page("accueil.py")
st.markdown('</div>', unsafe_allow_html=True)

# Titre de la page
st.markdown("<h1>Statistiques par ligue</h1>", unsafe_allow_html=True)

# Gérer l'état de la sidebar
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

# Charger les données
try:
    data = pd.read_csv("data/merged_teams_data.csv", delimiter=";")
except FileNotFoundError:
    st.stop()

# Créer une barre horizontale avec une liste déroulante pour choisir la ligue
st.markdown('<div class="navbar">', unsafe_allow_html=True)
leagues = data['League'].unique().tolist()  # Liste des ligues uniques
selected_league = st.selectbox("Choisir une ligue", leagues, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# Filtrer les données pour la ligue sélectionnée
league_data = data[data['League'] == selected_league]

# Section 1 : Tableau pour chaque ligue
st.markdown(f"<h3>Tableau des performances pour {selected_league}</h3>", unsafe_allow_html=True)
table_data = league_data[['Rk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Pts']]
st.table(table_data.style.set_properties(**{
    'background-color': 'rgba(1, 0, 20, 0.6)',
    'color': 'white',
    'border': '1px solid #gris',
    'text-align': 'center',
    'font-size': '0.9em',
    'padding': '10px'
}).set_table_styles([{
    'selector': 'th',
    'props': [('background-color', 'rgba(0, 0, 0, 0.9)'), ('color', "#CDCDCD"), ('border', '1px solid #45B7D1'), ('font-size', '1em')]
}]))

# Section 2 : Bar plot groupé pour GF, GA, et GD avec ombrage sur les étiquettes
st.markdown(f"<h3>Comparaison des buts pour {selected_league}</h3>", unsafe_allow_html=True)
fig1 = px.bar(league_data, x="Squad", y=["GF", "GA", "GD"],
              title=f"{selected_league}",
              labels={"value": "Nombre de buts", "variable": "Type de buts", "Squad": "Équipe"},
              color_discrete_map={"GF": "#F50000", "GA": "#00129E", "GD": "#00EC1F"},
              barmode="group")
fig1.update_traces(texttemplate='%{y}', textposition="auto", textfont=dict(size=10, family="Arial", color="white"))
fig1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    title=dict(font=dict(color="white")),
    xaxis=dict(title=dict(font=dict(color="white")), tickfont=dict(color="white", size=10, family="Arial", style="normal"), tickangle=45),
    yaxis=dict(title=dict(font=dict(color="white")), tickfont=dict(color="white")),
    legend=dict(font=dict(color="white"))
)
st.plotly_chart(fig1, use_container_width=True)