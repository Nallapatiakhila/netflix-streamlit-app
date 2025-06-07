import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Netflix Titles Explorer", layout="wide")

# Title
st.title("🎬 Netflix Titles Data Explorer")

# Load data
@st.cache_data
def load_data():
    file_path = "netflix_titles.csv"  # ✅ Correct filename here
    return pd.read_csv(file_path)

df = load_data()

# Show raw data
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(df)

# Basic info
st.subheader("Dataset Info")
st.write(f"🔢 Rows: {df.shape[0]}, 🧬 Columns: {df.shape[1]}")
st.write("📌 Column Names:", list(df.columns))

# Summary statistics
if st.checkbox("Show summary statistics (numeric only)"):
    st.subheader("Summary Statistics")
    st.write(df.describe())

# Column selection
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

if numeric_cols:
    st.subheader("📈 Plotting")
    col1 = st.selectbox("Select X-axis (numeric)", numeric_cols)
    col2 = st.selectbox("Select Y-axis (numeric)", numeric_cols)

    plot_type = st.radio("Choose plot type:", ["Scatter", "Line", "Histogram", "Boxplot"])

    fig, ax = plt.subplots()
    if plot_type == "Scatter":
        sns.scatterplot(data=df, x=col1, y=col2, ax=ax)
    elif plot_type == "Line":
        sns.lineplot(data=df, x=col1, y=col2, ax=ax)
    elif plot_type == "Histogram":
        sns.histplot(data=df, x=col1, bins=30, kde=True, ax=ax)
    elif plot_type == "Boxplot":
        sns.boxplot(data=df, x=col1, y=col2, ax=ax)

    st.pyplot(fig)
else:
    st.warning("No numeric columns available for plotting.")

# Footer
st.markdown("---")
st.markdown("👨‍💻 Built with Streamlit")
