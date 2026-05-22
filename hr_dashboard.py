def hr_dashboard():
    import streamlit as st
    from databasesetup import SessionLocal
    from schema import Job, Candidate
    from jd_analysis_chain import analyze_jd
    from resume_scoringchain import score_resume
    from resumeparser import extract_text
    from parser import parse_llm_output
    from typing import Optional
    from datetime import datetime
    import re

    from extract_detail import extract_contact_info
    from detail import normalize_contact
    from email_service import send_confirmation_email, send_rejection_email

    st.sidebar.title("HR Panel")

    menu = st.sidebar.radio("Menu", [
        "Active Jobs",
        "Post JD",
        "Pipeline"
    ])

    db = SessionLocal()

    try:

        # =========================
        # ACTIVE JOBS
        # =========================
        if menu == "Active Jobs":
            st.header("Active Job Openings")

            jobs = db.query(Job).all()

            if not jobs:
                st.info("No jobs posted yet")
            else:
                for job in jobs:
                    st.subheader(job.title)
                    st.write(f"📍 {job.location}")
                    st.write(f"🏢 {job.department}")
                    st.write(f"👤 Manager ID: {job.reporting_to}")
                    st.write(f"🕒 {job.posted_at}")
                    st.write(f"🆔 Job ID: {job.jobid}")
                    st.markdown("---")

        # =========================
        # POST JD
        # =========================
        elif menu == "Post JD":
            st.header("Create Job")

            title = st.text_input("Job Title")
            department = st.selectbox(
                "Department",
                ["Engineering", "Product", "Analytics", "HR"]
            )
            location = st.selectbox(
                "Location",
                ["Remote", "Bangalore", "Mumbai", "Delhi"]
            )
            reporting_to = st.number_input("Manager ID", min_value=1)
            jd = st.text_area("Job Description")

            if st.button("Analyze JD"):
                if not jd.strip():
                    st.warning("Enter JD")
                else:
                    result = analyze_jd(jd)
                    st.text_area("AI Output", result, height=200)

            if st.button("Save Job"):
                if not title or not jd:
                    st.error("Fill all fields")
                else:
                    job = Job(
                        title=title,
                        description=jd,
                        department=department,
                        location=location,
                        reporting_to=int(reporting_to),
                        posted_at=datetime.utcnow()
                    )

                    db.add(job)
                    db.commit()
                    db.refresh(job)

                    st.success(f"Job Created | ID: {job.jobid}")

        # =========================
        # PIPELINE
        # =========================
        elif menu == "Pipeline":
            st.header("Resume Pipeline")

            jobs = db.query(Job).all()

            if not jobs:
                st.warning("No jobs available")
                return

            job_map = {
                f"{j.title} (ID:{j.jobid})": j.jobid for j in jobs
            }

            selected = st.selectbox("Select Job", list(job_map.keys()))
            job_id = job_map[selected]

            job: Optional[Job] = db.get(Job, job_id)

            st.text_area("JD", job.description, height=150)

            files = st.file_uploader(
                "Upload Resumes",
                accept_multiple_files=True,
                type=["pdf"]
            )

            # =========================
            # PROCESS RESUMES
            # =========================
            if st.button("Process Resumes"):

                if not files:
                    st.warning("Upload resumes first")
                    return

                progress = st.progress(0)

                for i, file in enumerate(files):
                    try:
                        st.write(f"Processing: {file.name}")

                        text = extract_text(file)

                        # DEBUG
                        print("\n==== DEBUG ====")
                        print("FILE:", file.name)
                        print("TEXT LENGTH:", len(text))
                        print(text[:300])

                        if len(text.strip()) < 100:
                            st.error(f"{file.name}: Bad resume text")
                            continue

                        # 🔥 RULE-BASED NAME FIX
                        def extract_name(text):
                            lines = text.split("\n")
                            for line in lines[:5]:
                                if 2 <= len(line.split()) <= 4:
                                    return line.strip()
                            return file.name

                        name = extract_name(text)

                        # CONTACT
                        contact_raw = extract_contact_info(text)
                        contact_clean = normalize_contact(contact_raw)

                        email = contact_clean.get("email") or f"{file.name}_{i}"
                        mobile = contact_clean.get("mobile")

                        # SCORING
                        ai_output = score_resume(job.description, text)

                        print("AI OUTPUT:", ai_output)

                        if not ai_output:
                            score = 0
                            parsed = {}
                        else:
                            score, parsed = parse_llm_output(ai_output)

                            ai_recommendation = None
                            if parsed:
                                ai_recommendation = parsed.get("recommendation")

                            if score is None:
                                score = 0
                                parsed = {}

                        print("FINAL SCORE:", score)

                        # CHECK EXISTING
                        existing = (
                            db.query(Candidate)
                            .filter_by(email=email, job_id=job_id)
                            .first()
                        )

                        if existing:
                            # 🔥 FIX: UPDATE INSTEAD OF SKIP
                            existing.name = name
                            existing.contact = mobile
                            existing.resume_text = text
                            existing.score = score
                            existing.summary = str(parsed)

                            db.commit()
                            st.info(f"{name} updated")
                            continue

                        # NEW CANDIDATE
                        candidate = Candidate(
                            name=name,
                            email=email,
                            contact=mobile,
                            resume_text=text,
                            job_id=job_id,
                            score=score,
                            summary=str(parsed),
                            status="pending",
                            email_sent=False,
                            ai_recommendation=ai_recommendation
                        )

                        db.add(candidate)

                        send_confirmation_email(email, name)
                        candidate.email_sent = True

                    except Exception as e:
                        st.error(f"{file.name}: {e}")

                    progress.progress((i + 1) / len(files))

                db.commit()
                st.success("Resumes processed successfully")

            # =========================
            # CANDIDATE REVIEW
            # =========================
            st.header("Candidate Review")

            candidates = (
                db.query(Candidate)
                .filter_by(job_id=job_id)
                .order_by(Candidate.id.desc())
                .all()
            )

            for c in candidates:
                st.subheader(c.name)
                st.metric("AI Score", f"{c.score:.1f}/100")

                if c.score >= 80:
                    st.success("🔥 Strong Match")
                elif c.score >= 60:
                    st.warning("⚠️ Moderate Match")
                else:
                    st.error("❌ Weak Match")

                st.write(f"Status: {c.status}")

                with st.expander("AI Summary"):
                    st.write(c.summary)

                if c.status != "pending":
                    st.info(f"{c.status} | {c.hr_reason}")
                    continue

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"Shortlist {c.id}", key=f"s_{c.id}"):
                        st.session_state[f"a_{c.id}"] = "shortlisted"

                with col2:
                    if st.button(f"Reject {c.id}", key=f"r_{c.id}"):
                        st.session_state[f"a_{c.id}"] = "rejected"

                action = st.session_state.get(f"a_{c.id}")

                if action:
                    reason = st.text_input("Reason", key=f"reason_{c.id}")

                    if st.button(f"Confirm {c.id}", key=f"c_{c.id}"):

                        if not reason.strip():
                            st.error("Enter reason")
                        else:
                            c.status = action
                            c.hr_reason = reason
                            c.hr_id = st.session_state["user_id"]

                            if action == "rejected":
                                send_rejection_email(c.email, c.name)

                            db.commit()
                            del st.session_state[f"a_{c.id}"]

                            st.success("Updated")
                            st.rerun()

    finally:
        db.close()