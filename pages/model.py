import streamlit as st
import pandas as pd
import base64
import xgboost as xgb

# Configuration de la page
st.set_page_config(layout="wide", page_title="Sélection des Équipes - Football Analytics Dashboard", initial_sidebar_state="collapsed")

# Charger les données
try:
    team_categories = pd.read_csv('data/teams.csv')
    team_categories = team_categories['team'].astype('category')
    players_scores = pd.read_csv('data/players_scores.csv', delimiter=';', encoding='utf-8')
    schedule = pd.read_csv('data/schedule.csv', encoding='utf-8')
    if 'home_team' not in schedule.columns or 'away_team' not in schedule.columns:
        raise ValueError("Colonnes 'home_team' ou 'away_team' absentes dans schedule.csv")
    home_score_model = xgb.XGBRegressor()
    home_score_model.load_model('data/home_score_model.json')
    away_score_model = xgb.XGBRegressor()
    away_score_model.load_model('data/away_score_model.json')
except Exception as e:
    st.error(f"Erreur lors du chargement des données : {e}")
    st.stop()

# Charger l'image de fond
with open("images/background.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# CSS personnalisé avec suppression de la couleur rouge dans le multiselect
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
    .stSelectbox div {{
        background-color: black;
        color: white;
        padding: 3px;
    }}
    .stSelectbox div:hover {{
        background-color: grey;
    }}
    .player-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 5px;
    }}
    .player-name {{
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 1.0) !important;
        font-size: 0.9em !important;
        margin-top: -5px !important;
        margin-bottom: 0px !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .spacer {{
        width: 50px;
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

    /* Style des options dans la liste déroulante du multiselect */
    div[data-baseweb="select"] div[role="option"] {{
        font-size: 12px !important;
        padding: 4px 8px !important;
        color: inherit !important;              /* Texte couleur normale */
        background-color: transparent !important; /* Pas de fond rouge */
        box-shadow: none !important;            /* Pas d'ombre/contour */
        border: none !important;                 /* Pas de bordure */
    }}

    /* Style des éléments sélectionnés (badges) dans le multiselect */
    div[data-baseweb="select"] span {{
        font-size: 12px !important;
        padding: 2px 6px !important;
        margin: 1px !important;
        line-height: 1 !important;
        color: white !important;                 /* Texte blanc pour les badges */
        background: transparent !important;     /* Pas de fond */
        box-shadow: none !important;             /* Pas d'ombre */
        border: none !important;                  /* Pas de bordure */
    }}
    .prediction-result {{
        color: white;
        font-size: 4em;  /* Taille encore plus grande */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        margin-top: 10px;
        text-align: center;  /* Centrage du texte */
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
st.markdown("<h1>Sélection des Équipes</h1>", unsafe_allow_html=True)

# Gérer l'état de la sidebar
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

# Sélection des deux équipes
col1, spacer, col2 = st.columns([1, 0.5, 1])
with col1:
    home_team = st.selectbox("Équipe à domicile", sorted(players_scores["Team"].unique()), key="home_team_select")
with col2:
    away_team = st.selectbox("Équipe extérieure", sorted(players_scores["Team"].unique()), key="away_team_select")

# Filtrer les joueurs par équipe
home_players_df = players_scores[players_scores["Team"] == home_team].sort_values(by=["Pos"], ascending=[True])
away_players_df = players_scores[players_scores["Team"] == away_team].sort_values(by=["Pos"], ascending=[True])

# Liste des joueurs avec position et séparation
positions = ["GK", "DF", "MF", "FW"]
home_player_options = []
for pos in positions:
    pos_players = home_players_df[home_players_df["Pos"].str.contains(pos)]
    if not pos_players.empty:
        home_player_options.extend([f"{player} ({pos})" for player, pos in zip(pos_players["Player"], pos_players["Pos"])])
        if pos != "FW":
            home_player_options.append("-------")
away_player_options = []
for pos in positions:
    pos_players = away_players_df[away_players_df["Pos"].str.contains(pos)]
    if not pos_players.empty:
        away_player_options.extend([f"{player} ({pos})" for player, pos in zip(pos_players["Player"], pos_players["Pos"])])
        if pos != "FW":
            away_player_options.append("-------")

# Sélection des joueurs
with col1:
    st.markdown(f"<h2>Joueurs de {home_team}</h2>", unsafe_allow_html=True)
    home_selected_players = st.multiselect("Choisir les joueurs", home_player_options, default=None, max_selections=11, key="home_players_select")
    gk_count_home = sum(1 for player in home_selected_players if " (GK)" in player)
    if gk_count_home > 1:
        st.error("Vous ne pouvez sélectionner qu'un seul gardien (GK) !")
        home_selected_players = [p for p in home_selected_players if " (GK)" not in p]

with col2:
    st.markdown(f"<h2>Joueurs de {away_team}</h2>", unsafe_allow_html=True)
    away_selected_players = st.multiselect("Choisir les joueurs", away_player_options, default=None, max_selections=11, key="away_players_select")
    gk_count_away = sum(1 for player in away_selected_players if " (GK)" in player)
    if gk_count_away > 1:
        st.error("Vous ne pouvez sélectionner qu'un seul gardien (GK) !")
        away_selected_players = [p for p in away_selected_players if " (GK)" not in p]

# Fonctions de prédiction
def calculate_last_h2h_stats(home_team, away_team, schedule, nb_matches=3):
    h2h_matches = schedule[((schedule['home_team'] == home_team) & (schedule['away_team'] == away_team)) |
                           ((schedule['home_team'] == away_team) & (schedule['away_team'] == home_team))]
    h2h_matches = h2h_matches.sort_index(ascending=False).head(nb_matches)
    for index, row in h2h_matches.iterrows():
        if row['home_team'] == away_team:
            h2h_matches.at[index, 'home_score'], h2h_matches.at[index, 'away_score'] = row['away_score'], row['home_score']
            h2h_matches.at[index, 'home_xg'], h2h_matches.at[index, 'away_xg'] = row['away_xg'], row['home_xg']
    goal_diff = h2h_matches['home_score'] - h2h_matches['away_score']
    xg_diff = h2h_matches['home_xg'] - h2h_matches['away_xg']
    if len(goal_diff) > 0 and len(xg_diff) > 0:
        goal_diff_sum = goal_diff.sum()
        xg_diff_sum = xg_diff.sum()
    else:
        goal_diff_sum = pd.NA
        xg_diff_sum = pd.NA
    return goal_diff, xg_diff, goal_diff_sum, xg_diff_sum

def calculate_team_score(team, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11):
    missing_players = []
    print(f"Débogage : Vérification de l'équipe {team} dans players_scores")
    if 'Team' not in players_scores.columns:
        print("Erreur : Colonne 'Team' absente dans players_scores")
        return 0, missing_players
    team_df = players_scores[players_scores['Team'] == team]
    selected_players = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]
    team_df = team_df[team_df['Player'].isin([p for p in selected_players if p is not None])]
    if team_df.shape[0] < 11:
        missing_players = set([p for p in selected_players if p is not None]) - set(team_df['Player'])
        print(f"Attention : Joueurs manquants pour {team} : {missing_players}")
        for player in missing_players:
            found = players_scores[players_scores['Player'] == player]
            if not found.empty:
                team_df = pd.concat([team_df, found], ignore_index=True)
        missing_players = set([p for p in selected_players if p is not None]) - set(team_df['Player'])
    if team_df.shape[0] < 11:
        average_score = players_scores['player_score'].mean()
        for player in missing_players:
            team_df = pd.concat([team_df, pd.DataFrame({
                'Player': [player],
                'Team': [team],
                'player_score': [average_score]
            })], ignore_index=True)
    team_score = team_df['player_score'].sum()
    return team_score, missing_players

def get_match_result(home_team, home_p1, home_p2, home_p3, home_p4, home_p5, home_p6, home_p7, home_p8, home_p9, home_p10, home_p11,
                     away_team, away_p1, away_p2, away_p3, away_p4, away_p5, away_p6, away_p7, away_p8, away_p9, away_p10, away_p11):
    X_pred = pd.DataFrame({'home_team': [home_team], 'away_team': [away_team]})
    if home_team not in list(team_categories) or away_team not in list(team_categories):
        print(f"Erreur : L'équipe {home_team} ou {away_team} n'est pas dans les équipes connues.")
        return pd.NA, pd.NA
    X_pred['home_team'] = pd.Categorical(X_pred['home_team'], categories=team_categories)
    X_pred['away_team'] = pd.Categorical(X_pred['away_team'], categories=team_categories)
    goal_diff, xg_diff, goal_diff_sum, xg_diff_sum = calculate_last_h2h_stats(home_team, away_team, schedule, nb_matches=3)
    X_pred['h2h_goal_diff_sum'] = goal_diff_sum
    X_pred['h2h_xg_diff_sum'] = xg_diff_sum
    home_players = [home_p1, home_p2, home_p3, home_p4, home_p5, home_p6, home_p7, home_p8, home_p9, home_p10, home_p11]
    away_players = [away_p1, away_p2, away_p3, away_p4, away_p5, away_p6, away_p7, away_p8, away_p9, away_p10, away_p11]
    home_team_players_score, home_missing_players = calculate_team_score(home_team, *home_players)
    away_team_players_score, away_missing_players = calculate_team_score(away_team, *away_players)
    if len(home_missing_players) > 0 or len(away_missing_players) > 0:
        print(f"Avertissement : Joueurs manquants pour {home_team} vs {away_team} : {home_missing_players} {away_missing_players}")
    X_pred['home_team_players_score'] = home_team_players_score
    X_pred['away_team_players_score'] = away_team_players_score
    X_pred['h2h_goal_diff_sum'] = pd.to_numeric(X_pred['h2h_goal_diff_sum'], errors='coerce')
    X_pred['h2h_xg_diff_sum'] = pd.to_numeric(X_pred['h2h_xg_diff_sum'], errors='coerce')
    X_pred['home_team_players_score'] = pd.to_numeric(X_pred['home_team_players_score'], errors='coerce')
    X_pred['away_team_players_score'] = pd.to_numeric(X_pred['away_team_players_score'], errors='coerce')
    home_goals = home_score_model.predict(X_pred)
    away_goals = away_score_model.predict(X_pred)
    return (round(float(home_goals.item()), 1), round(float(away_goals.item()), 1))

# Bouton pour lancer la prédiction
if st.button("Prédire le score"):
    if len(home_selected_players) == 11 and len(away_selected_players) == 11:
        # Extraire les noms des joueurs sans les positions
        home_players = [player.split(' (')[0] for player in home_selected_players]
        away_players = [player.split(' (')[0] for player in away_selected_players]
        home_pred, away_pred = get_match_result(home_team, *home_players, away_team, *away_players)
        if pd.isna(home_pred) or pd.isna(away_pred):
            st.error("Erreur dans la prédiction. Vérifiez les équipes sélectionnées.")
        else:
            # Déterminer les couleurs selon le score (uniquement pour les valeurs)
            if home_pred > away_pred:
                home_color, away_color = "green", "red"
            elif away_pred > home_pred:
                home_color, away_color = "red", "green"
            else:
                home_color, away_color = "white", "white"  # Égalité
            st.markdown(
                f'<div class="prediction-result" style="text-align: center;">'
                f'{home_team} <span style="color: {home_color};">{home_pred}</span> - '
                f'<span style="color: {away_color};">{away_pred}</span> {away_team}</div>',
                unsafe_allow_html=True
            )
    else:
        st.error("Veuillez sélectionner exactement 11 joueurs pour chaque équipe.")

# Affichage des joueurs sélectionnés avec photos
if home_selected_players or away_selected_players:
    st.markdown("<h3>Joueurs sélectionnés :</h3>", unsafe_allow_html=True)
    col1_display, spacer_display, col2_display = st.columns([1, 0.1, 1])
    with col1_display:
        if home_selected_players:
            players = home_selected_players[:11]  # Limite à 11
            if len(players) > 0:
                # Première photo seule
                player_with_pos = players[0] if players[0] != "-------" else None
                if player_with_pos:
                    player_name = player_with_pos.split(" (")[0]
                    player_data = home_players_df[home_players_df["Player"] == player_name].iloc[0]
                    player_id = player_data["Player_URL"].split("/")[-2]
                    image_url = f"https://fbref.com/req/202302030/images/headshots/{player_id}_2022.jpg"
                    st.markdown(
                        f'<div class="player-container"><img src="{image_url}" width=50>'
                        f'<div class="player-name">{player_name}</div></div>',
                        unsafe_allow_html=True
                    )
            # Trois rangées de trois
            for i in range(1, 10, 3):
                if len(players) > i:
                    cols = st.columns(3)
                    for j in range(3):
                        idx = i + j
                        if idx < len(players):
                            player_with_pos = players[idx] if players[idx] != "-------" else None
                            if player_with_pos:
                                player_name = player_with_pos.split(" (")[0]
                                player_data = home_players_df[home_players_df["Player"] == player_name].iloc[0]
                                player_id = player_data["Player_URL"].split("/")[-2]
                                image_url = f"https://fbref.com/req/202302030/images/headshots/{player_id}_2022.jpg"
                                with cols[j]:
                                    st.markdown(
                                        f'<div class="player-container"><img src="{image_url}" width=50>'
                                        f'<div class="player-name">{player_name}</div></div>',
                                        unsafe_allow_html=True
                                    )
            # Dernière photo seule
            if len(players) == 11:
                player_with_pos = players[10] if players[10] != "-------" else None
                if player_with_pos:
                    player_name = player_with_pos.split(" (")[0]
                    player_data = home_players_df[home_players_df["Player"] == player_name].iloc[0]
                    player_id = player_data["Player_URL"].split("/")[-2]
                    image_url = f"https://fbref.com/req/202302030/images/headshots/{player_id}_2022.jpg"
                    st.markdown(
                        f'<div class="player-container"><img src="{image_url}" width=50>'
                        f'<div class="player-name">{player_name}</div></div>',
                        unsafe_allow_html=True
                    )
    with col2_display:
        if away_selected_players:
            players = away_selected_players[:11]
            if len(players) > 0:
                # Première photo seule
                player_with_pos = players[0] if players[0] != "-------" else None
                if player_with_pos:
                    player_name = player_with_pos.split(" (")[0]
                    player_data = away_players_df[away_players_df["Player"] == player_name].iloc[0]
                    player_id = player_data["Player_URL"].split("/")[-2]
                    image_url = f"https://fbref.com/req/202302030/images/headshots/{player_id}_2022.jpg"
                    st.markdown(
                        f'<div class="player-container"><img src="{image_url}" width=50>'
                        f'<div class="player-name">{player_name}</div></div>',
                        unsafe_allow_html=True
                    )
            # Trois rangées de trois
            for i in range(1, 10, 3):
                if len(players) > i:
                    cols = st.columns(3)
                    for j in range(3):
                        idx = i + j
                        if idx < len(players):
                            player_with_pos = players[idx] if players[idx] != "-------" else None
                            if player_with_pos:
                                player_name = player_with_pos.split(" (")[0]
                                player_data = away_players_df[away_players_df["Player"] == player_name].iloc[0]
                                player_id = player_data["Player_URL"].split("/")[-2]
                                image_url = f"https://fbref.com/req/202302030/images/headshots/{player_id}_2022.jpg"
                                with cols[j]:
                                    st.markdown(
                                        f'<div class="player-container"><img src="{image_url}" width=50>'
                                        f'<div class="player-name">{player_name}</div></div>',
                                        unsafe_allow_html=True
                                    )
            # Dernière photo seule
            if len(players) == 11:
                player_with_pos = players[10] if players[10] != "-------" else None
                if player_with_pos:
                    player_name = player_with_pos.split(" (")[0]
                    player_data = away_players_df[away_players_df["Player"] == player_name].iloc[0]
                    player_id = player_data["Player_URL"].split("/")[-2]
                    image_url = f"https://fbref.com/req/202302030/images/headshots/{player_id}_2022.jpg"
                    st.markdown(
                        f'<div class="player-container"><img src="{image_url}" width=50>'
                        f'<div class="player-name">{player_name}</div></div>',
                        unsafe_allow_html=True
                    )