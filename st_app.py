import streamlit as st
from streamlit.column_config import LinkColumn
import pandas as pd
import script
from descriptor import AnimeDescriptor
import plotly.express as px
import plotly.graph_objects as go
import ast

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MALFinder Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS (Primary Blue Theme with Cyan/Teal Accents)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

    /* Global Reset & Font */
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        color: #0D47A1; /* Dark Blue Text */
    }

    /* Main Background - Light at Bottom, Darker at Top to pop Glassmorphism */
    .stApp {
        background: linear-gradient(0deg, #E3F2FD 0%, #BBDEFB 50%, #90CAF9 100%);
        background-attachment: fixed;
    }
    
    /* Offset Top Padding */
    .block-container {
        padding-top: 6rem;
        padding-bottom: 2rem;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.35);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    [data-testid="stSidebar"] * {
        color: #0D47A1 !important;
    }

    /* --- Title Container --- */
    .title-glass {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 20px 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.7);
        box-shadow: 0 10px 30px rgba(25, 118, 210, 0.15); /* Blue shadow */
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .title-glass h1 {
        margin: 0;
        padding: 0;
        font-size: 2.8rem;
        /* Gradient Text: Blue to Teal */
        background: linear-gradient(45deg, #1565C0, #009688);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }

    /* --- KPI CARD STYLING --- */
    .kpi-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 8px 24px rgba(13, 71, 161, 0.08);
        height: 140px;
        display: flex;
        flex-direction: row; /* Layout: Text Left, Icon Right */
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(13, 71, 161, 0.15);
        background: rgba(255, 255, 255, 0.8);
    }

    .kpi-content {
        z-index: 2;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .kpi-icon-box {
        opacity: 0.15;
        transform: scale(1.2);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .kpi-card:hover .kpi-icon-box {
        opacity: 0.25;
        transform: scale(1.3) rotate(5deg);
    }
    
    .kpi-title {
        color: #1976D2; /* Primary Blue */
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    
    .kpi-value {
        color: #0D47A1; /* Darker Blue */
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .kpi-subtitle {
        color: #0097A7; /* Teal Accent */
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 4px;
    }

    /* --- BEAUTIFIED FILTERS --- */
    
    /* Selectbox (Genre) */
    div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.7) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(25, 118, 210, 0.2) !important;
        transition: border 0.3s ease;
    }
    
    div[data-baseweb="select"]:hover {
        border-color: #1976D2 !important; /* Blue hover */
    }

    /* Filter Labels */
    .stSelectbox label, .stSlider label {
        color: #1565C0 !important;
        font-family: 'Roboto', sans-serif;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px;
    }

    /* Slider (Score) */
    .stSlider > div > div > div {
        /* Gradient Track: Blue to Cyan */
        background: linear-gradient(to right, #42A5F5, #00BCD4) !important;
    }
    
    .stSlider > div > div > div > div {
        background-color: #0D47A1 !important;
        border: 2px solid white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Reset Button */
    .stButton > button {
        background: linear-gradient(135deg, #1976D2 0%, #0097A7 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 15px rgba(25, 118, 210, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(25, 118, 210, 0.4);
        background: linear-gradient(135deg, #2196F3 0%, #00BCD4 100%);
    }

    /* Dataframe & Headers */
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(25, 118, 210, 0.2);
    }

    h1, h2, h3 {
        color: #0D47A1 !important;
    }
    
    /* Plotly Backgrounds */
    .js-plotly-plot .plotly .modebar {
        display: none !important;
    }

    /* Dropdown Options */
    ul[role="listbox"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px;
    }
    li[role="option"]:hover {
        background-color: rgba(187, 222, 251, 0.4) !important; /* Light Blue Hover */
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('Data/AnimeFiltered.csv')
    
    def safe_eval(x):
        try:
            return ast.literal_eval(x)
        except:
            return []
            
    df['Genres_List'] = df['Genres'].apply(safe_eval)
    df['Themes_List'] = df['Themes'].apply(safe_eval)
    df['Demographics_List'] = df['Demographics'].apply(safe_eval)
    return df

try:
    anime_filtered = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### MALFinder Analytics")
    st.markdown("---")
    
    page_selection = st.radio(
        "Navigation", 
        ["Dashboard", "Semantic Search"],
        label_visibility="visible"
    )
    
    st.markdown("---")
    st.caption("v2.2 | Modern Blue & Icons")

# =============================================================================
# DASHBOARD PAGE
# =============================================================================
if page_selection == "Dashboard":
    
    # --- HEADER SECTION ---
    c_title, c_genre, c_score, c_reset = st.columns([3.5, 2, 2, 0.5])
    
    with c_title:
        st.markdown("""
        <div class="title-glass">
            <h1>MyAnimeList Overview</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with c_genre:
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        all_genres = sorted(list(set([g for genres in anime_filtered['Genres_List'] for g in genres])))
        selected_genre = st.selectbox("Genre Filter", ["All Genres"] + all_genres, key="genre_filter")
    
    with c_score:
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        score_range = st.slider("Rating Score", 1.0, 10.0, (1.0, 10.0), 0.1, key="score_range")
    
    with c_reset:
        st.markdown("<div style='margin-top: 36px;'></div>", unsafe_allow_html=True) 
        if st.button("⟲", use_container_width=True, help="Reset Filters"):
            st.rerun()
    
    # Apply Filters
    dashboard_df = anime_filtered.copy()
    
    if selected_genre != "All Genres":
        dashboard_df = dashboard_df[dashboard_df['Genres_List'].apply(lambda x: selected_genre in x)]
    
    dashboard_df = dashboard_df[(dashboard_df['Score'] >= score_range[0]) & (dashboard_df['Score'] <= score_range[1])]
    
    st.markdown("###")
    
    # --- ROW 1: KPI CARDS WITH ICONS ---
    k1, k2, k3, k4 = st.columns(4)
    
    # Calculate Metrics
    total_titles = len(dashboard_df)
    avg_score = dashboard_df['Score'].mean()
    delta_score = avg_score - anime_filtered['Score'].mean()
    total_members_m = dashboard_df['Members'].sum() / 1_000_000
    
    # Calculate average episodes (exclude 'Unknown')
    eps_df = dashboard_df[dashboard_df['Episodes'] != 'Unknown'].copy()
    eps_df['Episodes_Numeric'] = pd.to_numeric(eps_df['Episodes'], errors='coerce')
    avg_eps = eps_df['Episodes_Numeric'].mean()

    # SVG Icons
    icon_mal = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#1976D2" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"></path></svg>"""
    icon_star = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#0097A7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>"""
    icon_users = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#009688" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>"""
    icon_clock = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#00BCD4" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>"""

    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-content">
                <div class="kpi-title">Total Titles</div>
                <div class="kpi-value">{total_titles:,}</div>
                <div class="kpi-subtitle">Anime in Dataset</div>
            </div>
            <div class="kpi-icon-box">{icon_mal}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        color_delta = "#00BCD4" if delta_score >= 0 else "#E57373"
        symbol = "↑" if delta_score >= 0 else "↓"
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #00BCD4;">
            <div class="kpi-content">
                <div class="kpi-title">Average Score</div>
                <div class="kpi-value">{avg_score:.2f}</div>
                <div class="kpi-delta" style="color: {color_delta}; font-weight:600;">{symbol} {abs(delta_score):.3f} vs avg</div>
            </div>
            <div class="kpi-icon-box">{icon_star}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #009688;">
            <div class="kpi-content">
                <div class="kpi-title">Audience Reach</div>
                <div class="kpi-value">{total_members_m:.1f}M</div>
                <div class="kpi-subtitle">Total Members</div>
            </div>
            <div class="kpi-icon-box">{icon_users}</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #4DD0E1;">
            <div class="kpi-content">
                <div class="kpi-title">Average Length</div>
                <div class="kpi-value">{avg_eps:.0f}</div>
                <div class="kpi-subtitle">Episodes per Series</div>
            </div>
            <div class="kpi-icon-box">{icon_clock}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("###")

    # --- ROW 2: PRIMARY CHARTS ---
    c1, c2 = st.columns([3, 2])
    
    with c1:
        st.markdown("### Top 15 Anime by Score")
        
        top_15 = dashboard_df.nlargest(15, 'Score')[['Title', 'Score', 'Members']].reset_index(drop=True)
                
        fig_top15 = go.Figure()
        
        fig_top15.add_trace(go.Bar(
            y=top_15['Title'][::-1],
            x=top_15['Score'][::-1],
            orientation='h',
            text=top_15['Score'][::-1].round(2),
            textposition='outside',
            marker=dict(
                color=top_15['Score'][::-1],
                # Gradient: Light Blue -> Teal Blue -> Dark Blue
                colorscale=[[0, '#B3E5FC'], [0.5, '#4FC3F7'], [1, '#0277BD']],
                showscale=False,
                line=dict(color='rgba(255,255,255,0.5)', width=1)
            ),
            hovertemplate='<b>%{y}</b><br>Score: %{x:.3f}<extra></extra>'
        ))
        
        fig_top15.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'size': 11, 'family': 'Roboto'}, # Dark Blue Text
            margin=dict(l=10, r=60, t=10, b=10),
            height=450,
            xaxis=dict(
                showgrid=True, 
                gridcolor='rgba(25, 118, 210, 0.1)',
                range=[top_15['Score'].min() - 0.1, top_15['Score'].max() + 0.3],
                color='#0D47A1'
            ),
            yaxis=dict(showgrid=False, color='#0D47A1'),
            hoverlabel=dict(bgcolor="rgba(255,255,255,0.9)", font_color="#0D47A1")
        )
        
        st.plotly_chart(fig_top15, use_container_width=True)

    with c2:
        st.markdown("### Score Distribution")
        
        fig_hist = go.Figure()
        
        fig_hist.add_trace(go.Histogram(
            x=dashboard_df['Score'],
            nbinsx=30,
            marker=dict(
                color='#29B6F6', # Light Blue
                line=dict(color='rgba(255,255,255,0.5)', width=1)
            ),
            hovertemplate='Score: %{x}<br>Count: %{y}<extra></extra>'
        ))
        
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'family': 'Roboto'},
            margin=dict(l=20, r=20, t=10, b=20),
            height=450,
            xaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Score", color='#0D47A1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Frequency", color='#0D47A1'),
            hoverlabel=dict(bgcolor="rgba(255,255,255,0.9)", font_color="#0D47A1")
        )
        
        st.plotly_chart(fig_hist, use_container_width=True)

    # --- ROW 3: DETAILED ANALYSIS ---
    c3, c4, c5 = st.columns([2, 2, 1])
    
    with c3:
        st.markdown("### Genre Popularity")
        
        genres_expanded = dashboard_df.explode('Genres_List')
        genre_counts = genres_expanded['Genres_List'].value_counts().reset_index().head(12)
        genre_counts.columns = ['Genre', 'Count']
        
        genre_scores = genres_expanded.groupby('Genres_List')['Score'].mean().reset_index()
        genre_scores.columns = ['Genre', 'AvgScore']
        
        genre_data = genre_counts.merge(genre_scores, on='Genre')
        
        fig_bubble = px.scatter(
            genre_data,
            x='Count',
            y='AvgScore',
            size='Count',
            color='AvgScore',
            text='Genre',
            # Blue-Teal Scale
            color_continuous_scale=['#4DD0E1', '#29B6F6', '#0288D1', '#01579B'], 
            size_max=50
        )
        
        fig_bubble.update_traces(
            textposition='top center',
            textfont=dict(size=10, color='#0D47A1', family='Roboto'),
            marker=dict(line=dict(color='rgba(255,255,255,0.5)', width=1))
        )
        
        fig_bubble.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'family': 'Roboto'},
            margin=dict(l=20, r=20, t=10, b=20),
            height=400,
            xaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Number of Anime", color='#0D47A1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Average Score", color='#0D47A1'),
            coloraxis_showscale=False,
            hoverlabel=dict(bgcolor="rgba(255,255,255,0.9)", font_color="#0D47A1")
        )
        
        st.plotly_chart(fig_bubble, use_container_width=True)
    
    with c4:
        st.markdown("### Top Themes")
        
        themes_expanded = dashboard_df.explode('Themes_List')
        theme_counts = themes_expanded['Themes_List'].value_counts().reset_index().head(10)
        theme_counts.columns = ['Theme', 'Count']
        theme_counts = theme_counts.sort_values('Count', ascending=True)
        
        fig_themes = go.Figure()
        
        fig_themes.add_trace(go.Bar(
            y=theme_counts['Theme'],
            x=theme_counts['Count'],
            orientation='h',
            text=theme_counts['Count'],
            textposition='outside',
            marker=dict(
                color=theme_counts['Count'],
                colorscale=[[0, '#B3E5FC'], [0.5, '#29B6F6'], [1, '#0277BD']],
                showscale=False,
                line=dict(color='rgba(255,255,255,0.5)', width=1)
            ),
            hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
        ))
        
        fig_themes.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'family': 'Roboto'},
            margin=dict(l=10, r=40, t=10, b=10),
            height=400,
            xaxis=dict(showgrid=False, showticklabels=False, color='#0D47A1'),
            yaxis=dict(showgrid=False, color='#0D47A1'),
            hoverlabel=dict(bgcolor="rgba(255,255,255,0.9)", font_color="#0D47A1")
        )
        
        st.plotly_chart(fig_themes, use_container_width=True)
    
    with c5:
        st.markdown("### Type Split")
        
        type_counts = dashboard_df['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        
        fig_donut = go.Figure()
        
        fig_donut.add_trace(go.Pie(
            labels=type_counts['Type'],
            values=type_counts['Count'],
            hole=0.6,
            marker=dict(
                colors=['#0288D1', '#03A9F4', '#29B6F6', '#4FC3F7', '#81D4FA'],
                line=dict(color='rgba(255,255,255,0.5)', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(color='#0D47A1', size=10, family='Roboto'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
        ))
        
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'family': 'Roboto'},
            margin=dict(l=10, r=10, t=10, b=10),
            height=400,
            showlegend=False,
            hoverlabel=dict(bgcolor="rgba(255,255,255,0.9)", font_color="#0D47A1")
        )
        
        st.plotly_chart(fig_donut, use_container_width=True)

    # --- ROW 4: SCATTER PLOT ---
    st.markdown("### Episodes vs Score Analysis")
    
    scatter_df = dashboard_df[dashboard_df['Episodes'] != 'Unknown'].copy()
    scatter_df['Episodes_Numeric'] = pd.to_numeric(scatter_df['Episodes'], errors='coerce')
    scatter_df = scatter_df.dropna(subset=['Episodes_Numeric'])
    
    if len(scatter_df) > 1000:
        scatter_df = scatter_df.sample(1000)
    
    fig_scatter = px.scatter(
        scatter_df,
        x='Episodes_Numeric',
        y='Score',
        size='Members',
        color='Type',
        hover_data=['Title'],
        # Blue spectrum
        color_discrete_sequence=['#01579B', '#0288D1', '#03A9F4', '#29B6F6', '#4FC3F7'],
        opacity=0.7
    )
    
    fig_scatter.update_traces(
        marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=1))
    )
    
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#0D47A1', 'family': 'Roboto'},
        margin=dict(l=20, r=20, t=10, b=20),
        height=400,
        xaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Number of Episodes", color='#0D47A1'),
        yaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Score", color='#0D47A1'),
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(25, 118, 210, 0.3)',
            borderwidth=1,
            font=dict(color='#0D47A1')
        ),
        hoverlabel=dict(bgcolor="rgba(255,255,255,0.9)", font_color="#0D47A1")
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

# =============================================================================
# SEMANTIC SEARCH PAGE
# =============================================================================
elif page_selection == "Semantic Search":
    st.title("Semantic Search")
    
    st.info("Uses vector embeddings to understand the 'meaning' of your query rather than just matching keywords.")
    
    query = st.text_input("What are you looking for?", placeholder="e.g. A heartwarming story about raising a child")
    
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        top_n = st.slider("Dataset Size", 100, int(anime_filtered.shape[0]), 5000, 100)
    with col_s2:
        st.write("")
        st.write("")
        search_btn = st.button("Find Anime", type="primary", use_container_width=True)
        
    if query or search_btn:
        with st.spinner("Searching vector database..."):
            df_output = script.find_anime(query, n_rows=top_n)
            
        cols_to_show = ['Title', 'Description', 'Score', 'Type', 'Episodes', 'Url']
        display_df = df_output[cols_to_show].copy()
        display_df.index += 1
        
        st.subheader(f"Top Matches for: '{query}'")
        
        st.dataframe(
            display_df,
            column_config={
                "Url": st.column_config.LinkColumn("MAL Link", display_text="Open"),
                "Score": st.column_config.NumberColumn("Score", format="%.2f")
            },
            use_container_width=True
        )
        
        st.download_button("Download Results (CSV)", display_df.to_csv(), "results.csv")