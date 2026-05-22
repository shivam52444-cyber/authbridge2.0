import streamlit as st
from databasesetup import SessionLocal
from schema import Candidate
from email_service import send_manager_approval_email
from email_service import send_rejection_email

def manager_dashboard():
    st.title("Manager Review")

    db = SessionLocal()

    try:
        candidates = db.query(Candidate).filter_by(status="shortlisted").all()

        if not candidates:
            st.info("No shortlisted candidates yet")
            return

        for c in candidates:
            st.subheader(c.name)
            st.write(c.summary)

            col1, col2 = st.columns(2)

            # -------------------------
            # APPROVE
            # -------------------------
            with col1:
                if st.button(f"Approve {c.id}"):
                    c.status = "approved"
                    c.manager_decision = "approved"

                    # 🔥 SEND EMAIL ONLY ONCE
                    if not getattr(c, "manager_email_sent", False):
                        sent=send_manager_approval_email(c.email, c.name)
                        if sent:
                            c.manager_email_sent = True

                    db.commit()
                    st.success(f"{c.name} approved & email sent")
                    st.rerun()

            # -------------------------
            # REJECT
            # -------------------------
            with col2:
                if st.button(f"Reject {c.id}"):
                    c.status = "rejected"
                    c.manager_decision = "rejected"

                    # 🔥 send email only once
                    if not getattr(c, "rejection_email_sent", False):
                        sent = send_rejection_email(c.email, c.name)
                        if sent:
                            c.rejection_email_sent = True

                    db.commit()
                    st.warning(f"{c.name} rejected & email sent")
                    st.rerun()

    finally:
        db.close()