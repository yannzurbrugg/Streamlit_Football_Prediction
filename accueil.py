import streamlit as st
import base64

st.set_page_config(layout="wide", page_title="Football Analytics Dashboard", initial_sidebar_state="collapsed")

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
        overflow: hidden;
        margin: 0;
        padding: 0;
    }}
    .stApp {{
        background: transparent;
    }}
    h1 {{
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        font-size: 4em;
        margin-top: 20px;
    }}
    .card {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        transition: transform 0.3s;
    }}
    .card:hover {{
        transform: scale(1.05);
    }}
    .card img {{
        max-width: 100%;
        max-height: 70%;
        object-fit: contain;
    }}
    .card p {{
        font-size: 1.2em;
        margin: 10px 0;
        color: white;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
    }}
    .stButton>button {{
        background-color: black;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
    }}
    .stButton>button:hover {{
        background-color: #333;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Titre
st.markdown("<h1>Football Analytics Dashboard</h1>", unsafe_allow_html=True)

# Gérer l'état de la sidebar
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "collapsed"

# Conteneur pour les cartes
col1, col2, col3 = st.columns(3)

with col1:
    st.image("images/stats_icon.jpg", use_container_width=True)
    if st.button(" 📊 Voir les Statistiques"):
        st.session_state.sidebar_state = "collapsed"  # Forcer la sidebar à rester fermée
        st.switch_page("pages/statistics.py")

with col2:
    st.image("images/teams_icon.jpg", use_container_width=True)
    if st.button(" 👥 Voir les Équipes"):
        st.session_state.sidebar_state = "collapsed"  # Forcer la sidebar à rester fermée
        st.switch_page("pages/teams.py")

with col3:
    st.image("images/model_icon.jpg", use_container_width=True)
    if st.button(" 🧠 Utiliser le Modèle"):
        st.session_state.sidebar_state = "collapsed"  # Forcer la sidebar à rester fermée
        st.switch_page("pages/model.py")