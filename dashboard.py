from datetime import timedelta

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.agent import WaterIntakeAgent
from src.database import get_intake_history, log_water_intake

st.set_page_config(page_title="Hydration", page_icon="💧", layout="centered")

DEFAULT_GOAL_ML = 2000
RING_COLOR = "#1D9E75"
TRACK_COLOR = "#EEECE4"
FEEDBACK_BG = "#E6F1FB"
FEEDBACK_TEXT = "#0C447C"


@st.cache_resource
def get_agent():
    return WaterIntakeAgent()


def load_history_df(user_id: str) -> pd.DataFrame:
    history = get_intake_history(user_id)
    if not history:
        return pd.DataFrame(columns=["intake_ml", "timestamp"])
    df = pd.DataFrame(history, columns=["intake_ml", "timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    df["date"] = df["timestamp"].dt.date
    return df


def compute_stats(df: pd.DataFrame):
    if df.empty:
        return 0, 0, 0.0, 0

    daily_totals = df.groupby("date")["intake_ml"].sum()
    today = pd.Timestamp.now().date()

    today_total = int(daily_totals.get(today, 0))
    avg_ml = float(daily_totals.mean())
    best_ml = int(daily_totals.max())

    streak = 0
    day = today
    while day in daily_totals.index and daily_totals[day] > 0:
        streak += 1
        day = day - timedelta(days=1)

    return today_total, streak, avg_ml, best_ml


def ring_chart(today_total: int, goal_ml: int):
    remaining = max(goal_ml - today_total, 0)
    pct = int(min(today_total / goal_ml, 1) * 100) if goal_ml else 0

    fig = go.Figure(
        go.Pie(
            values=[today_total, remaining] if goal_ml else [1],
            hole=0.75,
            marker_colors=[RING_COLOR, TRACK_COLOR],
            textinfo="none",
            sort=False,
            direction="clockwise",
        )
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=200,
        annotations=[dict(text=f"{pct}%", x=0.5, y=0.5, font_size=28, showarrow=False)],
    )
    return fig


agent = get_agent()

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

st.markdown("### 💧 Hydration")

with st.expander("Settings", expanded=not st.session_state.user_id):
    user_id_input = st.text_input("User ID", value=st.session_state.user_id)
    goal_ml = st.number_input(
        "Daily goal (ml)", min_value=500, max_value=6000, value=DEFAULT_GOAL_ML, step=100
    )
    if user_id_input:
        st.session_state.user_id = user_id_input

user_id = st.session_state.user_id

if not user_id:
    st.info("Enter a user ID in settings above to get started.")
    st.stop()

df = load_history_df(user_id)
today_total, streak, avg_ml, best_ml = compute_stats(df)

ring_col, summary_col = st.columns([1, 1.3])
with ring_col:
    st.plotly_chart(ring_chart(today_total, goal_ml), use_container_width=True)
with summary_col:
    st.markdown(
        f"<p style='font-size:28px;font-weight:600;margin-bottom:0'>{today_total:,} ml</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='color:gray;margin-top:0'>of {goal_ml:,} ml daily goal</p>",
        unsafe_allow_html=True,
    )

st.write("")
c1, c2, c3 = st.columns(3)
for col, amount in ((c1, 100), (c2, 250), (c3, 500)):
    if col.button(f"+{amount} ml", use_container_width=True):
        log_water_intake(user_id, amount)
        st.rerun()

with st.expander("Log a custom amount"):
    custom_ml = st.number_input("Amount (ml)", min_value=0, step=50, key="custom_ml")
    if st.button("Log custom amount"):
        if custom_ml > 0:
            log_water_intake(user_id, custom_ml)
            st.rerun()
        else:
            st.warning("Enter an amount greater than 0.")

st.write("")
m1, m2, m3 = st.columns(3)
m1.metric("Streak", f"{streak} days")
m2.metric("Avg per day", f"{avg_ml:,.0f} ml")
m3.metric("Best day", f"{best_ml:,.0f} ml")

if today_total > 0:
    st.write("")
    with st.spinner("Getting AI feedback..."):
        analysis = agent.analyze_intake(today_total)
    st.markdown(
        f"""<div style='background:{FEEDBACK_BG};border-radius:8px;padding:16px'>
        <span style='color:{FEEDBACK_TEXT}'>{analysis}</span></div>""",
        unsafe_allow_html=True,
    )

st.write("")
st.markdown("#### History")
if df.empty:
    st.info("No intake logged yet. Log a glass above to start tracking.")
else:
    daily = df.groupby("date")["intake_ml"].sum().reset_index()
    daily.columns = ["Date", "Intake (ml)"]

    fig = go.Figure(go.Bar(x=daily["Date"], y=daily["Intake (ml)"], marker_color=RING_COLOR))
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=250)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("View raw data"):
        st.dataframe(daily, use_container_width=True, hide_index=True)