import streamlit as st
import pandas as pd
import script
import image_scrap # Import the new scraping module
import plotly.express as px
import plotly.graph_objects as go
import ast
import time

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
# CUSTOM CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap');

    /* --- HIDE STREAMLIT TOP BAR --- */
    [data-testid="stHeader"] {
        display: none;
    }

    /* --- GLOBAL TEXT SIZE --- */
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        color: #0D47A1;
        font-size: 1.15rem; 
    }

    /* Main Background - DEFAULT STATE */
    .stApp {
        background: linear-gradient(0deg, #E3F2FD 0%, #BBDEFB 50%, #90CAF9 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.35);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.5);
    }

    /* --- GLASS TITLE CONTAINER --- */
    .title-glass {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 20px 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.7);
        box-shadow: 0 10px 30px rgba(25, 118, 210, 0.15);
        display: block;
        width: 105%;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .title-glass h1 {
        margin: 0;
        padding: 0;
        font-size: 2.7rem; 
        background: linear-gradient(45deg, #1565C0, #009688);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -1px;
        line-height: 1.1;
        white-space: nowrap;
    }

    /* --- FILTER & BUTTON STYLING --- */
    
    /* Filter Labels */
    .filter-label-text {
        font-family: 'Roboto', sans-serif;
        font-weight: 800;
        font-size: 1.8rem;
        background: linear-gradient(45deg, #1565C0, #009688);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: right;
        display: flex; 
        justify-content: flex-end; 
        align-items: center; 
        height: 100%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.5;
    }
    
    /* Integrated Button Styling */
    [data-testid="stPopover"] > button, 
    div.stButton > button {
        background: rgba(255, 255, 255, 0.55) !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        color: #1565C0 !important;
        border-radius: 12px !important;
        padding: 0.4rem 0.8rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
        height: auto !important;
        min-height: 45px !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    [data-testid="stPopover"] > button:hover,
    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #009688 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
    }

    div.stButton > button {
        width: 100%;
    }

    /* --- SECTION HEADER STYLING --- */
    .section-header {
        font-size: 1.8rem;
        background: linear-gradient(45deg, #1565C0, #009688);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* --- KPI CARD STYLING --- */
    .kpi-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        box-shadow: 0 8px 24px rgba(13, 71, 161, 0.08);
        height: 140px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
        overflow: hidden;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(13, 71, 161, 0.15);
        background: rgba(255, 255, 255, 0.8);
    }
    .kpi-content { z-index: 2; display: flex; flex-direction: column; justify-content: center; }
    .kpi-icon-box { opacity: 0.15; transform: scale(1.4); }
    .kpi-title { color: #1976D2; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; }
    .kpi-value { color: #0D47A1; font-size: 2.2rem; font-weight: 900; line-height: 1; }
    .kpi-subtitle { color: #0097A7; font-size: 0.8rem; font-weight: 600; margin-top: 5px; }

    /* --- HIGHLIGHT CARD --- */
    .highlight-link { text-decoration: none !important; color: inherit; display: block; height: 100%; }
    .highlight-card {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        height: 500px;
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .highlight-card:hover { transform: scale(1.01); box-shadow: 0 20px 40px rgba(0,0,0,0.15); background: rgba(255, 255, 255, 0.85); }
    .highlight-header { display: flex; gap: 25px; align-items: flex-start; margin-bottom: 20px; }
    .highlight-img-placeholder {
        width: 130px; height: 180px; 
        background: linear-gradient(135deg, #ddd, #f0f0f0);
        border-radius: 16px; flex-shrink: 0; display: flex; align-items: center; justify-content: center;
        color: #aaa; font-size: 0.9rem; border: 2px solid white; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        overflow: hidden; padding: 0 !important;
    }
    .highlight-meta h2 { margin: 0 0 10px 0; font-size: 2rem; color: #0D47A1; font-weight: 900; line-height: 1.1; }
    .highlight-badge { background: #0D47A1; color: white; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 1rem; display: inline-block; box-shadow: 0 4px 10px rgba(13, 71, 161, 0.3); }
    .highlight-desc { font-size: 0.95rem; color: #455A64; line-height: 1.6; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 8; -webkit-box-orient: vertical; }
    .click-hint { position: absolute; bottom: 25px; right: 30px; font-size: 0.9rem; color: #1976D2; font-weight: bold; opacity: 0.8; }
    .js-plotly-plot .plotly .modebar { display: none !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('Data/AnimeFiltered.csv')
    def safe_eval(x):
        try: return ast.literal_eval(x)
        except: return []
    df['Genres_List'] = df['Genres'].apply(safe_eval)
    df['Themes_List'] = df['Themes'].apply(safe_eval)
    df['Demographics_List'] = df['Demographics'].apply(safe_eval)
    return df

try:
    anime_filtered = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

@st.cache_data(show_spinner=False)
def get_img_url(url):
    return image_scrap.get_anime_cover(url)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### MALFinder Analytics")
    st.markdown("---")
    page_selection = st.radio("Navigation", ["Overview", "Semantic Search"])
    st.markdown("---")
    st.caption("Dataset: Summer 2024 |  By: Montefalcon")

# =============================================================================
# DASHBOARD PAGE
# =============================================================================
if page_selection == "Overview":

    # --- RESET LOGIC ---
    if "g_rad" not in st.session_state: st.session_state.g_rad = "All Genres"
    if "d_rad" not in st.session_state: st.session_state.d_rad = "All Demographics"
    # --- SNAPSHOT STATE ---
    if "snapshot_mode" not in st.session_state: st.session_state.snapshot_mode = False

    def reset_filters():
        st.session_state.g_rad = "All Genres"
        st.session_state.d_rad = "All Demographics"

    # --- INJECT SNAPSHOT CSS IF ACTIVE ---
    if st.session_state.snapshot_mode:
        st.markdown("""
        <style>
            .stApp {
                /* Force background to cover at least 2000px vertically */
                background: linear-gradient(0deg, #E3F2FD 0%, #BBDEFB 50%, #90CAF9 100%) !important;
                background-attachment: initial !important; /* Not fixed, effectively 'scroll' but allows height stretching */
                min-height: 2000px !important; 
                background-size: 100% 100% !important; /* Stretch gradient to fill the forced height */
                background-repeat: no-repeat !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # --- HEADER SECTION (40:60 SPLIT) ---
    c_head_title, c_head_filters = st.columns([0.8, 1.2], gap="medium", vertical_alignment="center")
    
    with c_head_title:
        st.markdown("""
        <div class="title-glass">
            <h1>MyAnimeList Overview</h1>
        </div>
        """, unsafe_allow_html=True)
        
    with c_head_filters:
        # Layout: [Genre Text] [Btn] [Demo Text] [Btn] [Reset Btn] [Snapshot Btn]
        f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns([3.5, 1, 4.0, 1, 0.7, 0.7], gap="small", vertical_alignment="center")
        
        # --- Genre Filter ---
        with f_col1:
            st.markdown(f"<div class='filter-label-text'>{st.session_state.g_rad}</div>", unsafe_allow_html=True)
        with f_col2:
            all_genres = sorted(list(set([g for genres in anime_filtered['Genres_List'] for g in genres])))
            all_genres = [g for g in all_genres if "unknown" not in str(g).lower()]
            with st.popover("", icon=":material/filter_list:", use_container_width=True):
                st.markdown("**Select Genre**")
                st.radio("Genre", ["All Genres"] + all_genres, key="g_rad", label_visibility="collapsed")

        # --- Demographic Filter ---
        with f_col3:
            st.markdown(f"<div class='filter-label-text'>{st.session_state.d_rad}</div>", unsafe_allow_html=True)
        with f_col4:
            all_demos = sorted(list(set([d for demos in anime_filtered['Demographics_List'] for d in demos])))
            all_demos = [d for d in all_demos if "unknown" not in str(d).lower()]
            with st.popover("", icon=":material/filter_list:", use_container_width=True):
                st.markdown("**Select Demographic**")
                st.radio("Demographic", ["All Demographics"] + all_demos, key="d_rad", label_visibility="collapsed")
        
        # --- Reset Button ---
        with f_col5:
            if st.button("↺", type="secondary", help="Reset Filters", on_click=reset_filters):
                pass 

        # --- Snapshot Toggle Button ---
        with f_col6:
            # When active: Type=Primary (Filled/Hovered appearance). When inactive: Secondary (Ghost)
            btn_type = "primary" if st.session_state.snapshot_mode else "secondary"
            btn_help = "Exit Snapshot Mode" if st.session_state.snapshot_mode else "Enter Snapshot Mode (Fixes Background)"
            
            if st.button("", icon=":material/save:", type=btn_type, help=btn_help):
                st.session_state.snapshot_mode = not st.session_state.snapshot_mode
                st.rerun()

    # --- DATA FILTERING ---
    dashboard_df = anime_filtered.copy()
    dashboard_df = dashboard_df[(dashboard_df['Score'] >= 3.0) & (dashboard_df['Score'] <= 10.0)]
    
    if st.session_state.g_rad != "All Genres":
        dashboard_df = dashboard_df[dashboard_df['Genres_List'].apply(lambda x: st.session_state.g_rad in x)]
        
    if st.session_state.d_rad != "All Demographics":
        dashboard_df = dashboard_df[dashboard_df['Demographics_List'].apply(lambda x: st.session_state.d_rad in x)]

    st.markdown("###")

    # --- KPI CARDS ---
    k1, k2, k3, k4 = st.columns(4)
    total_titles = len(dashboard_df)
    avg_score = dashboard_df['Score'].mean() if not dashboard_df.empty else 0
    delta_score = avg_score - anime_filtered[(anime_filtered['Score'] >= 3.0)]['Score'].mean()
    total_members_m = dashboard_df['Members'].sum() / 1_000_000
    eps_df = dashboard_df[dashboard_df['Episodes'] != 'Unknown'].copy()
    eps_df['Episodes_Numeric'] = pd.to_numeric(eps_df['Episodes'], errors='coerce')
    avg_eps = eps_df['Episodes_Numeric'].mean() if not eps_df.empty else 0

    icon_mal = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#1976D2" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"></path></svg>"""
    icon_star = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#0097A7" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>"""
    icon_users = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#009688" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>"""
    icon_clock = """<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#00BCD4" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>"""

    with k1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-content"><div class="kpi-title">Total Titles</div><div class="kpi-value">{total_titles:,}</div><div class="kpi-subtitle">Anime in Dataset</div></div><div class="kpi-icon-box">{icon_mal}</div></div>""", unsafe_allow_html=True)
    with k2:
        color_delta = "#00BCD4" if delta_score >= 0 else "#E57373"
        symbol = "↑" if delta_score >= 0 else "↓"
        st.markdown(f"""<div class="kpi-card" style="border-left: 4px solid #00BCD4;"><div class="kpi-content"><div class="kpi-title">Average Score</div><div class="kpi-value">{avg_score:.2f}</div><div class="kpi-subtitle" style="color: {color_delta}; font-weight:600;">{symbol} {abs(delta_score):.3f} vs avg</div></div><div class="kpi-icon-box">{icon_star}</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card" style="border-left: 4px solid #009688;"><div class="kpi-content"><div class="kpi-title">Audience Reach</div><div class="kpi-value">{total_members_m:.1f}M</div><div class="kpi-subtitle">Total Members</div></div><div class="kpi-icon-box">{icon_users}</div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card" style="border-left: 4px solid #4DD0E1;"><div class="kpi-content"><div class="kpi-title">Average Length</div><div class="kpi-value">{avg_eps:.0f}</div><div class="kpi-subtitle">Episodes per Series</div></div><div class="kpi-icon-box">{icon_clock}</div></div>""", unsafe_allow_html=True)

    st.markdown("###")

    # --- ROW 1: TOP 15 + HIGHLIGHT (40:60 RATIO) ---
    c_top_chart, c_highlight = st.columns([4, 6])
    
    # Initialize selection state if not exists
    if "selected_anime" not in st.session_state: st.session_state.selected_anime = None

    with c_top_chart:
        st.markdown('<h3 class="section-header">Top 15 Anime by Score</h3>', unsafe_allow_html=True)
        if not dashboard_df.empty:
            top_15 = dashboard_df.nlargest(15, 'Score')[['Title', 'Score', 'Members']].reset_index(drop=True)
            min_score = top_15['Score'].min()
            max_score = top_15['Score'].max()
            range_min = min_score - 0.05
            range_max = max_score + 0.05

            fig_top15 = go.Figure(go.Bar(
                y=top_15['Title'][::-1], x=top_15['Score'][::-1], orientation='h',
                text=top_15['Score'][::-1].round(2), textposition='inside',
                marker=dict(color=top_15['Score'][::-1], colorscale=[[0, '#B3E5FC'], [0.5, '#4FC3F7'], [1, '#0277BD']], showscale=False),
                textfont=dict(color='white', weight='bold')
            ))
            fig_top15.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#0D47A1', 'size': 14, 'family': 'Roboto'},
                margin=dict(l=10, r=20, t=10, b=10), height=500,
                xaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', range=[range_min, range_max], color='#0D47A1'),
                yaxis=dict(showgrid=False, color='#0D47A1'),
                hoverlabel=dict(bgcolor="rgba(255,255,255,0.9)", font_color="#0D47A1"),
                clickmode='event+select'
            )
            chart_event = st.plotly_chart(
                fig_top15, 
                use_container_width=True, 
                on_select="rerun", 
                selection_mode="points",
                key="top15_chart"
            )

    # --- Highlight Card Logic ---
    with c_highlight:
        st.markdown('<h3 class="section-header">Top Selection</h3>', unsafe_allow_html=True)
        if not dashboard_df.empty:
            top_anime_row = None
            if chart_event and len(chart_event.selection['points']) > 0:
                selected_title = chart_event.selection['points'][0]['y']
                if selected_title in dashboard_df['Title'].values:
                    top_anime_row = dashboard_df[dashboard_df['Title'] == selected_title].iloc[0]
            if top_anime_row is None:
                top_anime_row = dashboard_df.loc[dashboard_df['Score'].idxmax()]
            
            desc = str(top_anime_row['Description'])
            if desc == "nan": desc = "No description available."
            img_url = get_img_url(top_anime_row.get('Url'))
            if img_url:
                img_content = f'<img src="{img_url}" style="width:100%; height:100%; object-fit:cover; display:block;">'
            else:
                img_content = '<span>Image<br>Placeholder</span>'

            st.markdown(f"""
            <a href="{top_anime_row['Url']}" target="_blank" class="highlight-link">
                <div class="highlight-card">
                    <div class="highlight-header">
                        <div class="highlight-img-placeholder">
                            {img_content}
                        </div>
                        <div class="highlight-meta"><h2>{top_anime_row['Title']}</h2><span class="highlight-badge">Score: {top_anime_row['Score']}</span></div>
                    </div>
                    <div class="highlight-desc">{desc}</div>
                    <div class="click-hint">Click to view on MAL ↗</div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # --- ROW 2: DIST & GENRE ---
    c_mid1, c_mid2 = st.columns([1, 1])

    with c_mid1:
        st.markdown('<h3 class="section-header">Score Distribution</h3>', unsafe_allow_html=True)
        fig_hist = go.Figure(go.Histogram(
            x=dashboard_df['Score'], nbinsx=30,
            marker=dict(color='#29B6F6', line=dict(color='rgba(255,255,255,0.5)', width=1)),
            hovertemplate='Score: %{x}<br>Count: %{y}<extra></extra>'
        ))
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'family': 'Roboto', 'size': 13},
            margin=dict(l=20, r=20, t=10, b=20), height=350,
            xaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Score", color='#0D47A1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Frequency", color='#0D47A1')
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with c_mid2:
        st.markdown('<h3 class="section-header">Genre Popularity</h3>', unsafe_allow_html=True)
        genres_expanded = dashboard_df.explode('Genres_List')
        genres_expanded = genres_expanded[~genres_expanded['Genres_List'].astype(str).str.contains('unknown', case=False, na=False)]
        genre_counts = genres_expanded['Genres_List'].value_counts().reset_index().head(12)
        genre_counts.columns = ['Genre', 'Count']
        genre_scores = genres_expanded.groupby('Genres_List')['Score'].mean().reset_index()
        genre_scores.columns = ['Genre', 'AvgScore']
        genre_data = genre_counts.merge(genre_scores, on='Genre')

        fig_bubble = px.scatter(
            genre_data, x='Count', y='AvgScore', size='Count', color='AvgScore',
            text='Genre', color_continuous_scale=['#4DD0E1', '#01579B'], size_max=50
        )
        fig_bubble.update_traces(textposition='top center', textfont=dict(size=12, color='#0D47A1', weight='bold'))
        fig_bubble.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'family': 'Roboto', 'size': 13},
            margin=dict(l=20, r=20, t=10, b=20), height=350,
            xaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Count", color='#0D47A1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', title="Avg Score", color='#0D47A1'),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    # --- ROW 3: THEMES, TYPE, DEMO ---
    c_bot1, c_bot2, c_bot3 = st.columns([1, 1, 1])

    with c_bot1:
        st.markdown('<h3 class="section-header">Top Themes</h3>', unsafe_allow_html=True)
        themes_expanded = dashboard_df.explode('Themes_List')
        themes_expanded = themes_expanded[~themes_expanded['Themes_List'].astype(str).str.contains('unknown', case=False, na=False)]
        theme_counts = themes_expanded['Themes_List'].value_counts().reset_index().head(10)
        theme_counts.columns = ['Theme', 'Count']
        theme_counts = theme_counts.sort_values('Count', ascending=True)

        fig_themes = go.Figure(go.Bar(
            y=theme_counts['Theme'], x=theme_counts['Count'], orientation='h',
            text=theme_counts['Count'], textposition='outside', 
            marker=dict(color=theme_counts['Count'], colorscale=[[0, '#B3E5FC'], [1, '#0277BD']], showscale=False),
            textfont=dict(color='#0D47A1', weight='bold', size=13)
        ))
        fig_themes.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'size': 12}, margin=dict(l=10, r=30, t=10, b=10), height=300,
            xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=False, color='#0D47A1')
        )
        st.plotly_chart(fig_themes, use_container_width=True)

    with c_bot2:
        st.markdown('<h3 class="section-header">Type Split</h3>', unsafe_allow_html=True)
        type_counts = dashboard_df['Type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        type_counts = type_counts[~type_counts['Type'].astype(str).str.contains('unknown', case=False, na=False)]

        fig_donut = go.Figure(go.Pie(
            labels=type_counts['Type'], values=type_counts['Count'], hole=0.6,
            marker=dict(colors=['#0288D1', '#03A9F4', '#29B6F6', '#4FC3F7', '#81D4FA']),
            textfont=dict(color='#0D47A1', weight='bold', size=13)
        ))
        fig_donut.update_traces(textposition='outside', textinfo='label+percent')
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1'}, margin=dict(l=40, r=40, t=40, b=40), height=320, showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with c_bot3:
        st.markdown('<h3 class="section-header">Demographics</h3>', unsafe_allow_html=True)
        demo_expanded = dashboard_df.explode('Demographics_List')
        demo_expanded = demo_expanded[~demo_expanded['Demographics_List'].astype(str).str.contains('unknown', case=False, na=False)]
        demo_counts = demo_expanded['Demographics_List'].value_counts().reset_index()
        demo_counts.columns = ['Demographic', 'Count']
        
        fig_demo = go.Figure(go.Bar(
            x=demo_counts['Demographic'], y=demo_counts['Count'],
            marker=dict(color='#009688', line=dict(width=0)),
            text=demo_counts['Count'], textposition='auto',
            textfont=dict(color='#FFFFFF', weight='bold', size=13)
        ))
        fig_demo.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#0D47A1', 'family': 'Roboto', 'size': 12},
            margin=dict(l=10, r=10, t=10, b=10), height=300,
            xaxis=dict(showgrid=False, color='#0D47A1'),
            yaxis=dict(showgrid=True, gridcolor='rgba(25, 118, 210, 0.1)', color='#0D47A1')
        )
        st.plotly_chart(fig_demo, use_container_width=True)

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