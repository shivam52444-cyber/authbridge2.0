def leader_dashboard():
    import streamlit as st
    from databasesetup import SessionLocal
    from schema import Candidate
    import pandas as pd
    import matplotlib.pyplot as plt

    st.title("📊 Leader Dashboard — Hiring Intelligence")

    db = SessionLocal()

    try:
        candidates = db.query(Candidate).all()

        if not candidates:
            st.warning("No candidate data available")
            return

        # ---------------------------
        # Prepare Data
        # ---------------------------
        data = []
        for c in candidates:
            if c.status == "pending":
                continue

            data.append({
                "hr_id": c.hr_id,
                "score": c.score,
                "status": c.status
            })

        df = pd.DataFrame(data)

        # 🔥 CRITICAL FIX (avoid missing hr_id issues)
        df = df.dropna(subset=["hr_id"])

        if df.empty:
            st.warning("No reviewed candidates yet")
            return

        # ---------------------------
        # Aggregations
        # ---------------------------
        summary = df.groupby("hr_id").agg(
            total_reviewed=("status", "count"),
            shortlisted=("status", lambda x: (x == "shortlisted").sum()),
            rejected=("status", lambda x: (x == "rejected").sum()),
            avg_score_shortlisted=("score", lambda x: x[df.loc[x.index, "status"] == "shortlisted"].mean()),
            avg_score_rejected=("score", lambda x: x[df.loc[x.index, "status"] == "rejected"].mean())
        ).reset_index()

        summary = summary.fillna(0)

        # ---------------------------
        # Derived Metrics
        # ---------------------------
        summary["shortlist_rate"] = summary["shortlisted"] / summary["total_reviewed"]

        summary["quality_score"] = (
            summary["avg_score_shortlisted"] - summary["avg_score_rejected"]
        )

        # ---------------------------
        # TABLE
        # ---------------------------
        st.subheader("📋 HR Performance Table")
        st.dataframe(summary)

        # ---------------------------
        # 📊 Visualization 1
        # ---------------------------
        st.subheader("📊 Shortlisted vs Rejected per HR")

        fig = plt.figure()
        plt.bar(summary["hr_id"], summary["shortlisted"])
        plt.bar(summary["hr_id"], summary["rejected"], bottom=summary["shortlisted"])
        plt.xlabel("HR ID")
        plt.ylabel("Candidates")
        st.pyplot(fig)

        # ---------------------------
        # 📈 Visualization 2
        # ---------------------------
        st.subheader("📈 Avg Score Comparison")

        fig2 = plt.figure()
        plt.plot(summary["hr_id"], summary["avg_score_shortlisted"])
        plt.plot(summary["hr_id"], summary["avg_score_rejected"])
        plt.xlabel("HR ID")
        plt.ylabel("Score")
        st.pyplot(fig2)

        # ---------------------------
        # KPI Metrics
        # ---------------------------
        st.subheader("📊 Key Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Avg Shortlist Score",
            f"{summary['avg_score_shortlisted'].mean():.2f}"
        )

        col2.metric(
            "Avg Reject Score",
            f"{summary['avg_score_rejected'].mean():.2f}"
        )

        col3.metric(
            "Avg Shortlist Rate",
            f"{summary['shortlist_rate'].mean():.2%}"
        )

        # ---------------------------
        # 🏆 Top HR
        # ---------------------------
        best_hr = summary.sort_values("quality_score", ascending=False).iloc[0]

        st.subheader("🏆 Top Performing HR")
        st.success(
            f"HR {best_hr['hr_id']} | Quality Score: {best_hr['quality_score']:.2f}"
        )

        # ---------------------------
        # 🚨 Alerts
        # ---------------------------
        st.subheader("🚨 AI Alerts")

        for _, row in summary.iterrows():

            if row["quality_score"] < 10:
                st.warning(
                    f"⚠️ HR {row['hr_id']} has low decision quality "
                    f"(Score gap: {row['quality_score']:.2f})"
                )

            if row["shortlist_rate"] < 0.2:
                st.warning(
                    f"⚠️ HR {row['hr_id']} is rejecting too many candidates"
                )

            if row["shortlist_rate"] > 0.8:
                st.warning(
                    f"⚠️ HR {row['hr_id']} may be over-shortlisting"
                )

    finally:
        db.close()