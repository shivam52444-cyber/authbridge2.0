import streamlit as st
from databasesetup import SessionLocal
from schema import User


def login():
    st.title("HireIQ Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        db = SessionLocal()

        try:
            user = db.query(User).filter_by(email=email).first()

            if user and user.password == password:

                st.session_state["user"] = user.email
                st.session_state["role"] = user.role
                st.session_state["user_id"] = user.user_id

                st.success(f"Logged in as {user.role}")
                st.rerun()

            else:
                st.error("Invalid credentials")

        finally:
            db.close()