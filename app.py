import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Variety Show Strategy Lab", layout="wide")

# 🎬 Title
st.title("🎬 Variety Show Strategy Lab")
st.markdown("Plan, simulate, and analyze TV variety shows like a pro 🔥")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("📊 Create New Show")

title = st.sidebar.text_input("Show Title", "New Show")
genre = st.sidebar.selectbox("Genre", ["Reality", "Survival", "Talk", "Dating", "Game"])
cast = st.sidebar.slider("Number of Cast Members", 2, 20, 6)
budget = st.sidebar.number_input("Estimated Budget ($M)", 1, 500, 50)
platform = st.sidebar.selectbox("Platform", ["TV", "YouTube", "OTT"])

# -----------------------------
# Scoring Logic
# -----------------------------
genre_weight = {
    "Reality": 1.2,
    "Survival": 1.5,
    "Talk": 0.8,
    "Dating": 1.3,
    "Game": 1.1
}

popularity_score = genre_weight[genre] * cast * 10
engagement_rate = popularity_score / (cast + 5)
roi = (popularity_score * 1000) / (budget * 100)

# -----------------------------
# Sample Data
# -----------------------------
data = [
    ["Running Man", "Reality", 8, 100, "TV"],
    ["Produce 101", "Survival", 11, 200, "OTT"],
    ["Single's Inferno", "Dating", 10, 80, "OTT"],
    ["Knowing Bros", "Talk", 7, 60, "TV"],
    ["Physical 100", "Survival", 12, 150, "OTT"]
]

df = pd.DataFrame(data, columns=["Title", "Genre", "Cast", "Budget", "Platform"])

# Compute metrics for dataset
df["Popularity"] = df.apply(lambda x: genre_weight[x["Genre"]] * x["Cast"] * 10, axis=1)
df["Engagement"] = df["Popularity"] / (df["Cast"] + 5)
df["ROI"] = (df["Popularity"] * 1000) / (df["Budget"] * 100)

# Add new show
new_row = pd.DataFrame([[title, genre, cast, budget, platform,
                         popularity_score, engagement_rate, roi]],
                       columns=df.columns)
df = pd.concat([df, new_row], ignore_index=True)

# -----------------------------
# Filters
# -----------------------------
platform_filter = st.selectbox("Filter by Platform", ["All"] + list(df["Platform"].unique()))

if platform_filter != "All":
    df = df[df["Platform"] == platform_filter]

# -----------------------------
# Ranking
# -----------------------------
df = df.sort_values(by="Popularity", ascending=False).reset_index(drop=True)

top_show = df.iloc[0]

# -----------------------------
# Metrics Row
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("🔥 Top Popularity", f"{top_show['Popularity']:.1f}", top_show["Title"])
col2.metric("📊 Avg Engagement", f"{df['Engagement'].mean():.2f}")
col3.metric("💰 Avg ROI", f"{df['ROI'].mean():.2f}")

st.markdown("---")

# -----------------------------
# Table with Styling
# -----------------------------
def highlight_performance(val):
    if val > df["Popularity"].mean():
        return "background-color: #d4edda"
    else:
        return "background-color: #f8d7da"

st.subheader("📋 Show Database")

styled_df = df.style.applymap(highlight_performance, subset=["Popularity"])
st.dataframe(styled_df, use_container_width=True)

# -----------------------------
# Charts
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Budget vs Popularity")
    st.bar_chart(df.set_index("Title")[["Budget", "Popularity"]])

with col2:
    st.subheader("🥧 Genre Distribution")
    st.write(df["Genre"].value_counts().plot.pie(autopct='%1.1f%%'))

# -----------------------------
# Line Chart
# -----------------------------
st.subheader("📈 Engagement Trends")
st.line_chart(df.set_index("Title")["Engagement"])

# -----------------------------
# Top Performer Highlight
# -----------------------------
st.markdown("---")
st.subheader("🏆 Top Performing Show")

st.success(f"""
🎬 **{top_show['Title']}** dominates the rankings!

🔥 Popularity Score: {top_show['Popularity']:.1f}
📊 Engagement Rate: {top_show['Engagement']:.2f}
💰 ROI: {top_show['ROI']:.2f}
""")
