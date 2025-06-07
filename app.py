import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['date_added'] = pd.to_datetime(df['date_added'])
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

# Title
st.title("🎬 Netflix Movies & TV Shows Dashboard")

# Sidebar filters
st.sidebar.header("Filter")
selected_type = st.sidebar.multiselect("Type", df['type'].unique(), default=df['type'].unique())
selected_country = st.sidebar.multiselect("Country", df['country'].dropna().unique()[:10], default=None)
selected_year = st.sidebar.slider("Year Added", 2008, 2021, (2015, 2020))

# Apply filters
filtered_df = df[
    (df['type'].isin(selected_type)) &
    (df['year_added'].between(selected_year[0], selected_year[1]))
]

if selected_country:
    filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

# Show data
st.subheader("📄 Filtered Results")
st.write(f"Total entries: {filtered_df.shape[0]}")
st.dataframe(filtered_df[['title', 'type', 'country', 'release_year', 'rating']])

# Plot: Shows per year
st.subheader("📈 Shows Added per Year")
count_by_year = filtered_df['year_added'].value_counts().sort_index()
st.bar_chart(count_by_year)

# Plot: Top 10 Genres
st.subheader("🎭 Top 10 Genres")
genre_data = df['listed_in'].dropna().str.split(', ', expand=True).stack().value_counts().head(10)
st.plotly_chart(px.bar(genre_data, orientation='h', title="Top Genres"))

# Plot: Type Distribution
st.subheader("📊 Type Distribution")
st.plotly_chart(px.pie(df, names='type', title="Movies vs TV Shows"))

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")