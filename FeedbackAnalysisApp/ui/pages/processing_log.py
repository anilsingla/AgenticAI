"""
FE-07: Processing Log — View the CSV processing log.
"""

import streamlit as st
import pandas as pd

from config.settings import OUTPUT_LOG_PATH


def render():
    st.header("Processing Log")

    if not OUTPUT_LOG_PATH.exists():
        st.info("No processing log yet. Run the pipeline first.")
        return

    df = pd.read_csv(OUTPUT_LOG_PATH, dtype=str).fillna("")
    if df.empty:
        st.info("Processing log is empty.")
        return

    st.caption(f"**{len(df)} log entries**")

    # ── Filters ─────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    if "agent_name" in df.columns:
        agents = sorted(df["agent_name"].unique())
        agent_filter = col1.multiselect("Filter by agent", agents, default=agents)
        df = df[df["agent_name"].isin(agent_filter)]

    if "source_id" in df.columns:
        source_ids = sorted(df["source_id"].unique())
        source_filter = col2.multiselect("Filter by source", source_ids, default=source_ids)
        df = df[df["source_id"].isin(source_filter)]

    # ── Table ───────────────────────────────────────────────────────
    st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Download ────────────────────────────────────────────────────
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Filtered Log",
        data=csv_bytes,
        file_name="processing_log_filtered.csv",
        mime="text/csv",
    )
