import streamlit as st
import pandas as pd
import base64
import plotly.express as px

# Configuration de la page
st.set_page_config(layout="wide", page_title="Équipes - Football Analytics Dashboard", initial_sidebar_state="collapsed")

# Charger les données CSV
df_players = pd.read_csv("data/players_data.csv", delimiter=";")
df_matches = pd.read_csv("data/matches_history.csv", delimiter=";")

# Charger l'image de fond
with open("images/background.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# CSS personnalisé
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
    h1, h2, h3 {{
        color: white;
        text-align: left;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }}
    h1 {{
        font-size: 4em;
        margin-top: 20px;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.9);
    }}
    h2 {{
        font-size: 1.5em;
        margin-bottom: 10px;
    }}
    h3 {{
        font-size: 0.5em;
    }}
    .navbar {{
        background-color: rgba(0, 0, 0, 1);
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .stSelectbox div {{
        background-color: black;
        color: white;
        padding: 3px;
    }}
    .stSelectbox div:hover {{
        background-color: grey;
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
    .player-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 0px;
    }}
    .player-name {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 1.0) !important;
        font-size: 0.9em !important;
        margin-top: -5px !important;
        margin-bottom: 0px !important;
    }}
    .stats-container {{
        margin-top: 0px;
    }}
    .stats-label {{
        color: white !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4) !important;
        font-weight: 600;
        font-size: 0.95em;
        margin-right: 2px;
    }}
    .stats-value {{
        color: white !important;
        font-style: italic;
        font-weight: 500;
        font-size: 0.95em;
        margin-left: 3px;
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

# Titre
st.markdown("<h1>Information d'équipe</h1>", unsafe_allow_html=True)

# Respecter l'état de la sidebar
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

# Sélection d'équipe
selected_team = st.selectbox("Choisir une équipe", sorted(df_players["Team"].unique()))

# Filtrer les joueurs
players_df = df_players[df_players["Team"] == selected_team].sort_values(by=["Pos", "MP"], ascending=[True, False])
positions = ["GK", "DF", "MF", "FW"]

# Diviser la page en deux colonnes
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<h2>Joueurs de {selected_team}</h2>", unsafe_allow_html=True)
    for pos in positions:
        pos_players = players_df[players_df["Pos"].str.contains(pos)]
        if not pos_players.empty:
            if pos == "GK":
                st.markdown("### Gardiens")
            elif pos == "DF":
                st.markdown("### Défenseurs")
            elif pos == "MF":
                st.markdown("### Milieux")
            elif pos == "FW":
                st.markdown("### Attaquants")
            for _, player in pos_players.iterrows():
                player_id = player["Player_URL"].split("/")[-2]
                image_url = f"https://fbref.com/req/202302030/images/headshots/{player_id}_2022.jpg"
                col_inner1, col_inner2 = st.columns([1, 4])
                with col_inner1:
                    st.markdown('<div class="player-container">', unsafe_allow_html=True)
                    st.image(image_url, width=100)
                    st.markdown(f'<div class="player-name">{player["Player"]}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col_inner2:
                    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
                    st.markdown(
                        f'''
                        <p>
                            <span class="stats-label">Âge:</span><span class="stats-value">{player["Age"]}</span>
                              
                            <span class="stats-label">Poste:</span><span class="stats-value">{player["Pos"]}</span>
                        </p>
                        <p>
                            <span class="stats-label">Matchs:</span><span class="stats-value">{player["MP"]}</span>
                              
                            <span class="stats-label">90 min:</span><span class="stats-value">{player["90s"]}</span>
                              
                            <span class="stats-label">Buts:</span><span class="stats-value">{player["Gls"]}</span>
                              
                            <span class="stats-label">Passes D:</span><span class="stats-value">{player["Ast"]}</span>
                        </p>
                        <p>
                            <span class="stats-label">Cartons J:</span><span class="stats-value">{player["CrdY"]}</span>
                              
                            <span class="stats-label">Cartons R:</span><span class="stats-value">{player["CrdR"]}</span>
                        </p>
                        ''',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("-------")

with col2:
    st.markdown(f"<h2>Historique des matchs de {selected_team}</h2>", unsafe_allow_html=True)
    # Filtrer les matchs pour l'équipe sélectionnée
    matches_df = df_matches[df_matches["Team"] == selected_team].sort_values(by="Date", ascending=False)
    if not matches_df.empty:
        # Utiliser st.table avec style similaire à la page statistique
        styled_df = matches_df[['Comp', 'Round', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'Date']].style.set_properties(**{
            'background-color': 'rgba(1, 0, 20, 0.6)',
            'color': 'white',
            'border': '1px solid rgba(69, 183, 209, 0.5)',
            'text-align': 'center',
            'font-size': '0.9em',
            'padding': '10px'
        }).set_table_styles([{
            'selector': 'th',
            'props': [('background-color', 'rgba(0, 0, 0, 0.9)'), ('color', '#CDCDCD'), ('border', '1px solid rgba(69, 183, 209, 0.5)'), ('font-size', '1em')]
        }])
        st.table(styled_df)

        # Diagramme circulaire pour matchs gagnés, perdus, égalités
        result_counts = matches_df['Result'].value_counts()
        pie_data = pd.DataFrame({
            'Result': ['Gagnés', 'Perdus', 'Égalités'],
            'Count': [result_counts.get('W', 0), result_counts.get('L', 0), result_counts.get('D', 0)]
        })
        fig = px.pie(pie_data, names='Result', values='Count', title=f'Historique des matchs de {selected_team}',
                     color_discrete_sequence=['#00EC1F', '#F50000', '#00129E'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title=dict(font=dict(color='white'), x=0.5, xanchor='center')
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("<p>Aucun match trouvé pour cette équipe.</p>", unsafe_allow_html=True)