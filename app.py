"""
Spotify Best of the Best - Data Analytics Dashboard
Main Streamlit application for analyzing playlist data
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    page_icon="🎵",
    layout="wide"
)

# Title and description
st.title("🎵 Spotify Best of the Best Analytics")
st.markdown("---")

@st.cache_data
def load_data(file_path):
    """Load and cache the CSV data"""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    """Main application function"""
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["Overview", "Data Explorer", "Visualizations", "Interesting Findings"]
    )
    
    # Load data
    data_file = Path("playlist-data-fully-enriched.csv")
    
    if not data_file.exists():
        st.error(f"Data file not found: {data_file}")
        st.info("Please ensure 'playlist-data-fully-enriched.csv' is in the project root directory.")
        return
    
    df = load_data(data_file)
    
    if df is None:
        return
    
    # Page routing
    if page == "Overview":
        show_overview(df)
    elif page == "Data Explorer":
        show_data_explorer(df)
    elif page == "Visualizations":
        show_visualizations(df)
    elif page == "Interesting Findings":
        show_findings(df)

def show_overview(df):
    """Display overview page"""
    st.header("📊 Data Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())
    
    st.subheader("Column Information")
    st.dataframe(
        pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str).values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values
        }).reset_index(drop=True),
        use_container_width=True
    )
    
    st.subheader("Sample Data (First 10 Rows)")
    st.dataframe(df.head(10), use_container_width=True)

def show_data_explorer(df):
    """Display data explorer page"""
    st.header("🔍 Data Explorer")
    
    # Filters
    st.subheader("Filters")
    
    # Create filter columns
    filter_col1, filter_col2 = st.columns(2)
    
    # Genre filter
    with filter_col1:
        if 'genre' in df.columns:
            all_genres = sorted(df['genre'].dropna().unique().tolist())
            selected_genres = st.multiselect(
                "Filter by Genre:",
                all_genres,
                default=None,
                placeholder="Select genres (leave empty for all)"
            )
        else:
            selected_genres = []
    
    # Language filter
    with filter_col2:
        if 'language' in df.columns:
            all_languages = sorted(df['language'].dropna().unique().tolist())
            selected_languages = st.multiselect(
                "Filter by Language:",
                all_languages,
                default=None,
                placeholder="Select languages (leave empty for all)"
            )
        else:
            selected_languages = []
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_genres:
        filtered_df = filtered_df[filtered_df['genre'].isin(selected_genres)]
    
    if selected_languages:
        filtered_df = filtered_df[filtered_df['language'].isin(selected_languages)]
    
    # Show filtered count
    if len(filtered_df) != len(df):
        st.info(f"📊 Filtered: {len(filtered_df)} of {len(df)} tracks")
    
    st.markdown("---")
    
    # Column selection
    all_columns = filtered_df.columns.tolist()
    
    # Set specific default columns
    desired_defaults = ['track_name', 'artist', 'language', 'genre', 'duration_minutes']
    default_columns = [col for col in desired_defaults if col in all_columns]
    
    selected_columns = st.multiselect(
        "Select columns to display:",
        all_columns,
        default=default_columns
    )
    
    if selected_columns:
        # Display data
        if len(filtered_df) > 0:
            # Only show slider if there are more than 5 rows
            if len(filtered_df) > 5:
                max_rows = len(filtered_df)
                min_rows = 5
                default_rows = min(20, max_rows)
                
                num_rows = st.slider(
                    "Number of rows to display:", 
                    min_value=min_rows, 
                    max_value=max_rows, 
                    value=default_rows,
                    key=f"num_rows_slider_{len(filtered_df)}"  # Unique key based on filter state
                )
            else:
                # 5 or fewer rows, show all without slider
                num_rows = len(filtered_df)
                if len(filtered_df) == 1:
                    st.info("Showing the only matching track")
                else:
                    st.info(f"Showing all {len(filtered_df)} matching tracks")
            
            st.write(f"Showing **{num_rows}** of **{len(filtered_df)}** rows:")
            st.dataframe(
                filtered_df[selected_columns].head(num_rows), 
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = filtered_df[selected_columns].to_csv(index=False)
            st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name="filtered_data.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data matches the selected filters.")
    else:
        st.warning("Please select at least one column to display.")

def show_visualizations(df):
    """Display visualizations page"""
    st.header("📈 Visualizations")
    
    # Get numeric columns
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    viz_type = st.radio(
        "Select visualization type:",
        ["Pie Chart (Genres)", "Pie Chart (Languages)", "Genres by Language", "Histogram (duration in ms)"],
        horizontal=True
    )
    
    if viz_type == "Pie Chart (Genres)":
        if 'genre' in df.columns:
            # Get genre counts
            genre_counts = df['genre'].value_counts()
            
            # Option to show top N genres
            show_all = st.checkbox("Show all genres", value=False)
            if not show_all:
                top_n = st.slider("Number of top genres to display:", 5, min(20, len(genre_counts)), 10)
                genre_counts = genre_counts.head(top_n)
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = plt.cm.Set3(range(len(genre_counts)))
            wedges, texts, autotexts = ax.pie(
                genre_counts.values, 
                labels=genre_counts.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors
            )
            
            # Make percentage text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Adjust label size
            for text in texts:
                text.set_fontsize(10)
            
            ax.set_title(f"Distribution of Music Genres (Total: {len(df)} tracks)", fontsize=14, fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
            
            # Show statistics
            st.subheader("Genre Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Genres", df['genre'].nunique())
                st.metric("Most Common Genre", genre_counts.index[0])
            with col2:
                st.metric("Tracks in Most Common Genre", genre_counts.values[0])
                st.metric("Percentage", f"{(genre_counts.values[0] / len(df) * 100):.1f}%")
        else:
            st.warning("No 'genre' column found in the dataset.")
    
    elif viz_type == "Pie Chart (Languages)":
        if 'language' in df.columns:
            # Get language counts
            language_counts = df['language'].value_counts()
            
            # Option to show top N languages
            show_all = st.checkbox("Show all languages", value=False)
            if not show_all:
                top_n = st.slider("Number of top languages to display:", 5, min(20, len(language_counts)), 10)
                language_counts = language_counts.head(top_n)
            
            # Create pie chart with legend instead of labels
            fig, ax = plt.subplots(figsize=(12, 7))
            colors = plt.cm.Pastel1(range(len(language_counts)))
            
            # Custom autopct function to show percentages only for slices > 2%
            def make_autopct(values):
                def my_autopct(pct):
                    if pct > 2:
                        return f'{pct:.1f}%'
                    return ''
                return my_autopct
            
            wedges, texts, autotexts = ax.pie(
                language_counts.values, 
                autopct=make_autopct(language_counts.values),
                startangle=90,
                colors=colors,
                pctdistance=0.80,
                textprops={'fontsize': 12, 'weight': 'bold'}
            )
            
            # Make percentage text more readable with white outline
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(13)
                autotext.set_path_effects([
                    path_effects.withStroke(linewidth=3, foreground='white')
                ])
            
            # Add legend with language names, counts, and percentages
            total_tracks = language_counts.sum()
            legend_labels = [f'{lang}: {count} tracks ({count/total_tracks*100:.1f}%)' 
                           for lang, count in zip(language_counts.index, language_counts.values)]
            ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=11)
            
            ax.set_title(f"Distribution of Languages (Total: {len(df)} tracks)", fontsize=15, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig)
            
            # Show statistics
            st.subheader("Language Statistics")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Languages", df['language'].nunique())
                st.metric("Most Common Language", language_counts.index[0])
            with col2:
                st.metric("Tracks in Most Common Language", language_counts.values[0])
                st.metric("Percentage", f"{(language_counts.values[0] / len(df) * 100):.1f}%")
        else:
            st.warning("No 'language' column found in the dataset.")
    
    elif viz_type == "Genres by Language":
        if 'genre' in df.columns and 'language' in df.columns:
            st.subheader("Genre Distribution by Language")
            
            languages = ['English', 'Ukrainian', 'Polish']
            
            # Display charts vertically
            for language in languages:
                # Filter data by language
                lang_df = df[df['language'] == language]
                
                if len(lang_df) > 0:
                    st.markdown(f"### {language}")
                    st.write(f"**Total tracks:** {len(lang_df)}")
                    
                    # Get genre counts for this language
                    genre_counts = lang_df['genre'].value_counts().head(10)
                    
                    # Create pie chart with legend
                    fig, ax = plt.subplots(figsize=(12, 6))
                    colors = plt.cm.Set3(range(len(genre_counts)))
                    
                    wedges, texts, autotexts = ax.pie(
                        genre_counts.values,
                        autopct='%1.1f%%',
                        startangle=90,
                        colors=colors,
                        pctdistance=0.85
                    )
                    
                    # Make percentage text more readable
                    for autotext in autotexts:
                        autotext.set_color('white')
                        autotext.set_fontweight('bold')
                        autotext.set_fontsize(11)
                    
                    # Add legend with genre names and counts
                    legend_labels = [f'{genre}: {count} tracks ({count/len(lang_df)*100:.1f}%)' 
                                   for genre, count in zip(genre_counts.index, genre_counts.values)]
                    ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
                    
                    ax.set_title(f"Genre Distribution - {language}", fontsize=14, fontweight='bold', pad=15)
                    plt.tight_layout()
                    st.pyplot(fig)
                    
                    # Show top genres statistics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Most Common Genre", genre_counts.index[0])
                    with col2:
                        st.metric("Tracks", f"{genre_counts.values[0]} ({genre_counts.values[0]/len(lang_df)*100:.1f}%)")
                    
                    st.markdown("---")
                else:
                    st.info(f"No tracks found for {language}")
                    st.markdown("---")
        else:
            st.warning("Both 'genre' and 'language' columns are required for this visualization.")
    
    elif viz_type == "Histogram (duration in ms)":
        if not numeric_columns:
            st.warning("No numeric columns found for histogram.")
            return
        column = st.selectbox("Select column:", numeric_columns)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(df[column].dropna(), bins=30, edgecolor='black')
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Distribution of {column}")
        st.pyplot(fig)

def show_findings(df):
    """Display interesting findings page"""
    st.header("💡 Interesting Findings")
    
    st.markdown("""
    Discover interesting patterns and insights from the Spotify playlist data.
    """)
    
    # Most Popular Elements
    st.subheader("🏆 Most Popular Elements")
    
    col1, col2, col3 = st.columns(3)
    
    # Most popular genre
    if 'genre' in df.columns:
        top_genre = df['genre'].value_counts().index[0]
        top_genre_count = df['genre'].value_counts().values[0]
        top_genre_pct = (top_genre_count / len(df)) * 100
        
        with col1:
            st.metric(
                "Most Popular Genre", 
                top_genre,
                delta=f"{top_genre_count} tracks ({top_genre_pct:.1f}%)"
            )
    
    # Most popular language
    if 'language' in df.columns:
        top_language = df['language'].value_counts().index[0]
        top_language_count = df['language'].value_counts().values[0]
        top_language_pct = (top_language_count / len(df)) * 100
        
        with col2:
            st.metric(
                "Most Popular Language", 
                top_language,
                delta=f"{top_language_count} tracks ({top_language_pct:.1f}%)"
            )
    
    # Most popular artist
    if 'artist' in df.columns:
        top_artist = df['artist'].value_counts().index[0]
        top_artist_count = df['artist'].value_counts().values[0]
        
        with col3:
            st.metric(
                "Most Popular Artist", 
                top_artist,
                delta=f"{top_artist_count} tracks"
            )
    
    st.markdown("---")
    
    # Correlation Analysis
    st.subheader("🔗 Correlation Analysis")
    
    if all(col in df.columns for col in ['artist', 'genre', 'language']):
        # Get top artist's details
        top_artist_df = df[df['artist'] == top_artist]
        
        if len(top_artist_df) > 0:
            # What genre does the top artist perform?
            artist_genres = top_artist_df['genre'].value_counts()
            artist_top_genre = artist_genres.index[0]
            artist_genre_count = artist_genres.values[0]
            
            # What language does the top artist use?
            artist_languages = top_artist_df['language'].value_counts()
            artist_top_language = artist_languages.index[0]
            artist_language_count = artist_languages.values[0]
            
            st.write(f"### Analysis of Top Artist: **{top_artist}**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Primary Genre:**")
                st.info(f"🎵 {artist_top_genre} ({artist_genre_count}/{top_artist_count} tracks)")
                
                if artist_top_genre == top_genre:
                    st.success(f"✅ **Correlation Found!** The most popular artist performs in the most popular genre ({top_genre}).")
                else:
                    st.warning(f"⚠️ **No Direct Correlation:** Most popular artist's genre ({artist_top_genre}) differs from the overall most popular genre ({top_genre}).")
            
            with col2:
                st.write("**Primary Language:**")
                st.info(f"🗣️ {artist_top_language} ({artist_language_count}/{top_artist_count} tracks)")
                
                if artist_top_language == top_language:
                    st.success(f"✅ **Correlation Found!** The most popular artist performs in the most popular language ({top_language}).")
                else:
                    st.warning(f"⚠️ **No Direct Correlation:** Most popular artist's language ({artist_top_language}) differs from the overall most popular language ({top_language}).")
            
            st.markdown("---")
            
            # Genre-Language correlation
            st.write("### Genre-Language Relationship")
            
            # Get top genre's languages
            top_genre_df = df[df['genre'] == top_genre]
            genre_languages = top_genre_df['language'].value_counts()
            
            if len(genre_languages) > 0:
                top_lang_in_genre = genre_languages.index[0]
                top_lang_in_genre_count = genre_languages.values[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**In {top_genre} genre:**")
                    st.write(f"- Most common language: **{top_lang_in_genre}**")
                    st.write(f"- {top_lang_in_genre_count} out of {len(top_genre_df)} tracks ({top_lang_in_genre_count/len(top_genre_df)*100:.1f}%)")
                
                with col2:
                    if top_lang_in_genre == top_language:
                        st.success(f"✅ **Strong Correlation!** The most popular language ({top_language}) is also the dominant language in the most popular genre ({top_genre}).")
                    else:
                        st.info(f"ℹ️ The most popular genre ({top_genre}) is primarily in {top_lang_in_genre}, while the overall most popular language is {top_language}.")
    else:
        st.warning("Required columns (artist, genre, language) not found for correlation analysis.")
    
    st.markdown("---")
    
    # Longest and Shortest Songs
    st.subheader("⏱️ Duration Extremes")
    
    # Check which duration column exists
    duration_col = None
    if 'duration_minutes' in df.columns:
        duration_col = 'duration_minutes'
        duration_unit = 'minutes'
    elif 'duration_ms' in df.columns:
        duration_col = 'duration_ms'
        duration_unit = 'ms'
    
    if duration_col and all(col in df.columns for col in ['track_name', 'artist', 'language']):
        col1, col2 = st.columns(2)
        
        # Longest song
        longest_idx = df[duration_col].idxmax()
        longest_song = df.loc[longest_idx]
        
        # Convert to minutes if in ms
        longest_duration = longest_song[duration_col]
        if duration_col == 'duration_ms':
            longest_duration_min = longest_duration / 60000
        else:
            longest_duration_min = longest_duration
        
        with col1:
            st.write("### 🔼 Longest Song")
            st.info(f"""
            **Track:** {longest_song['track_name']}  
            **Artist:** {longest_song['artist']}  
            **Language:** {longest_song['language']}  
            **Duration:** {longest_duration_min:.2f} minutes
            """)
        
        # Shortest song
        shortest_idx = df[duration_col].idxmin()
        shortest_song = df.loc[shortest_idx]
        
        # Convert to minutes if in ms
        shortest_duration = shortest_song[duration_col]
        if duration_col == 'duration_ms':
            shortest_duration_min = shortest_duration / 60000
        else:
            shortest_duration_min = shortest_duration
        
        with col2:
            st.write("### 🔽 Shortest Song")
            st.info(f"""
            **Track:** {shortest_song['track_name']}  
            **Artist:** {shortest_song['artist']}  
            **Language:** {shortest_song['language']}  
            **Duration:** {shortest_duration_min:.2f} minutes
            """)
    else:
        st.warning("Required columns (track_name, artist, language, duration) not found for this analysis.")
    
    st.markdown("---")
    
    # Most Common Words in Song Titles
    st.subheader("📝 Most Common Words in Song Titles")
    
    if 'track_name' in df.columns:
        import re
        from collections import Counter
        
        # Define common words to exclude
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'is', 'it', 'as', 'be', 'was', 'are'}
        
        # Extract all words from track names
        all_words = []
        for title in df['track_name'].dropna():
            # Convert to lowercase and extract words (alphanumeric)
            words = re.findall(r'\b[a-zA-Z]{2,}\b', str(title).lower())
            # Filter out stop words
            words = [word for word in words if word not in stop_words]
            all_words.extend(words)
        
        if all_words:
            # Count word frequencies
            word_counts = Counter(all_words)
            top_5_words = word_counts.most_common(5)
            
            # Create a dataframe for display
            words_df = pd.DataFrame({
                'Rank': range(1, len(top_5_words) + 1),
                'Word': [word for word, count in top_5_words],
                'Frequency': [count for word, count in top_5_words],
                'Percentage': [f"{(count/len(df)*100):.2f}%" for word, count in top_5_words]
            })
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.dataframe(
                    words_df,
                    use_container_width=True,
                    hide_index=True
                )
            
            with col2:
                st.metric("Total Unique Words", len(word_counts))
                st.metric("Total Words Analyzed", len(all_words))
                st.metric("Most Common", f'"{top_5_words[0][0]}"')
        else:
            st.info("No words found in track names")
    else:
        st.warning("Column 'track_name' not found for this analysis.")
    
    st.markdown("---")
    
    # Top Artists by Language
    st.write("### 🎤 Top Artists by Language")
    st.write("Discover the most popular artists in each of the top 10 languages")
    
    if 'language' in df.columns and 'artist' in df.columns:
        # Get top 10 languages
        top_10_languages = df['language'].value_counts().head(10)
        
        for idx, (language, count) in enumerate(top_10_languages.items(), 1):
            with st.expander(f"**{idx}. {language}** ({count} tracks)", expanded=(idx <= 3)):
                # Filter by language and get top 5 artists
                lang_artists = df[df['language'] == language]['artist'].value_counts().head(5)
                
                if len(lang_artists) > 0:
                    # Create a dataframe for display
                    artists_df = pd.DataFrame({
                        'Rank': range(1, len(lang_artists) + 1),
                        'Artist': lang_artists.index,
                        'Track Count': lang_artists.values,
                        'Percentage': [f"{(count/len(df[df['language'] == language])*100):.1f}%" 
                                     for count in lang_artists.values]
                    })
                    
                    st.dataframe(
                        artists_df,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info(f"No artist data available for {language}")
    else:
        st.warning("Required columns (artist, language) not found for this analysis.")
    
    st.markdown("---")
    
    # Top Artists by Genre
    st.write("### 🎸 Top Artists by Genre")
    st.write("Discover the most popular artists in each of the top 10 genres")
    
    if 'genre' in df.columns and 'artist' in df.columns:
        # Get top 10 genres
        top_10_genres = df['genre'].value_counts().head(10)
        
        for idx, (genre, count) in enumerate(top_10_genres.items(), 1):
            with st.expander(f"**{idx}. {genre}** ({count} tracks)", expanded=(idx <= 3)):
                # Filter by genre and get top 5 artists
                genre_artists = df[df['genre'] == genre]['artist'].value_counts().head(5)
                
                if len(genre_artists) > 0:
                    # Create a dataframe for display
                    artists_df = pd.DataFrame({
                        'Rank': range(1, len(genre_artists) + 1),
                        'Artist': genre_artists.index,
                        'Track Count': genre_artists.values,
                        'Percentage': [f"{(count/len(df[df['genre'] == genre])*100):.1f}%" 
                                     for count in genre_artists.values]
                    })
                    
                    st.dataframe(
                        artists_df,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info(f"No artist data available for {genre}")
    else:
        st.warning("Required columns (artist, genre) not found for this analysis.")
    
    st.markdown("---")
    
    # Rarest Languages
    st.write("### 🌍 Rarest Languages")
    st.write("Discover unique tracks in the 10 rarest languages")
    
    if all(col in df.columns for col in ['language', 'track_name', 'artist']):
        # Get language counts and find the 10 rarest (smallest counts)
        language_counts = df['language'].value_counts()
        rarest_10_languages = language_counts.tail(10).sort_values()
        
        # Collect all tracks from the rarest languages
        all_rare_tracks = []
        for language in rarest_10_languages.index:
            lang_tracks = df[df['language'] == language][['track_name', 'artist', 'language']].copy()
            all_rare_tracks.append(lang_tracks)
        
        if all_rare_tracks:
            # Combine all into one dataframe
            combined_rare_tracks = pd.concat(all_rare_tracks, ignore_index=True)
            
            # Add row numbers
            combined_rare_tracks.insert(0, '#', range(1, len(combined_rare_tracks) + 1))
            
            # Rename columns for better display
            combined_rare_tracks.columns = ['#', 'Track Title', 'Artist', 'Language']
            
            st.write(f"**Total tracks in rarest languages:** {len(combined_rare_tracks)}")
            
            st.dataframe(
                combined_rare_tracks,
                use_container_width=True,
                hide_index=True,
                height=400
            )
        else:
            st.info("No rare language tracks found")
    else:
        st.warning("Required columns (language, track_name, artist) not found for this analysis.")

if __name__ == "__main__":
    main()
