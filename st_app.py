# st_app.py
import streamlit as st
from streamlit.column_config import LinkColumn
import pandas as pd
import script
from descriptor import AnimeDescriptor


# Set page title
st.set_page_config(
    page_title="MALFinder",
    page_icon=":mag:",
)

anime_filtered = pd.read_csv('Data/AnimeFiltered.csv')
anime_filtered = anime_filtered[:15000]

# Description
st.header(":rainbow[MALFinder!] :mag:", divider='rainbow')

st.write(
    "MALFinder help you find the anime you want based on given description. \
    It leverages the use of **Vector Embeddings** to turn query and textual information provided by \
    [MyAnimeList](https://myanimelist.net/topanime.php) into vector of numbers. \
    The vector query will be matched to several anime based on the similarity of the encoding."
)

st.divider()


query = st.text_input("Anime Description:", placeholder="E.g. Time travel murder mystery")
top_n = st.slider("Top n-th anime:", 100, anime_filtered.shape[0], 5000, 100)
searched = st.button("Search")

if query or searched:
    df_output = script.find_anime(query, n_rows=top_n)
    cols = ['Title', 'Url', 'Description', 'Type', 'Episodes', 'Score', 'Popularity', 'Genres', 'Themes', 'Demographics']
    df_output = df_output[cols]
    df_output.index += 1

    column_config = {
        'Url': LinkColumn(
            "MyAnimeList Page ",
            help="Click to view the Anime page",
            validate="^https://[a-z]+\.com$",
            display_text="More details"
        )
    }

    try:
        # st.dataframe(df_output, column_config=column_config)
        st.caption("Click the description twice to expand. Also, the results is ordered by similarity")
        st.dataframe(
            df_output,
            column_config=column_config,
            hide_index=False
        )
    except:
        st.dataframe(df_output.astype(str))

    # Add download button for search results
    csv = df_output.to_csv(index=True)
    st.download_button(
        label="Download search results as CSV",
        data=csv,
        file_name="anime_search_results.csv",
        mime="text/csv",
    )

    # Add analytics section
    st.divider()
    st.subheader("📊 Statistical Insights", divider="rainbow")

    # Create tabs for different types of analysis
    tab1, tab2, tab3 = st.tabs(["Basic Stats", "Genre Analysis", "Score Analysis"])

    # Initialize analyzer
    analyzer = AnimeDescriptor()

    with tab1:
        st.write("### Basic Statistics")
        numeric_stats = df_output[['Episodes', 'Score', 'Popularity']].describe()
        st.dataframe(numeric_stats)
        
        # Count of anime types
        type_counts = df_output['Type'].value_counts()
        st.write("### Distribution by Type")
        st.bar_chart(type_counts)

    with tab2:
        st.write("### Genre Distribution")
        # Split genres and count
        genres = df_output['Genres'].str.split(',').explode()
        genre_counts = genres.value_counts().head(10)
        st.bar_chart(genre_counts)

        # Show themes if available
        if 'Themes' in df_output.columns:
            st.write("### Theme Distribution")
            themes = df_output['Themes'].str.split(',').explode()
            theme_counts = themes.value_counts().head(10)
            st.bar_chart(theme_counts)

    with tab3:
        st.write("### Score Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Average Score",
                f"{df_output['Score'].mean():.2f}",
                f"{df_output['Score'].mean() - anime_filtered['Score'].mean():.2f}"
            )
        
        with col2:
            st.metric(
                "Median Score",
                f"{df_output['Score'].median():.2f}",
                f"{df_output['Score'].median() - anime_filtered['Score'].median():.2f}"
            )

        # Score distribution
        st.write("### Score Distribution")
        score_hist = pd.DataFrame(df_output['Score'].value_counts().sort_index())
        st.line_chart(score_hist)

    # Add download options for analytics
    st.divider()
    st.subheader("📥 Download Analytics", divider="rainbow")
    
    # ...existing code...
    
    # Generate analytics report
    if st.button("Generate Full Analytics Report"):
        with st.spinner("Generating report..."):
            report_filename = "anime_analysis.docx"
            if analyzer.export_report(df_output, query, report_filename):
                with open(report_filename, "rb") as file:
                    st.download_button(
                        label="Download Analytics Report (DOCX)",
                        data=file,
                        file_name=report_filename,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                st.success("Report generated successfully!")
            else:
                st.error("Failed to generate report.")