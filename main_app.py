# main.py
import streamlit as st
from auth import login
from hr_dashboard import hr_dashboard
from managerdashbord import manager_dashboard
from leaderdashbord import leader_dashboard

st.set_page_config(layout="wide")

if "user" not in st.session_state:
    login()
    st.stop()
else:
    role = st.session_state["role"]
    
    st.sidebar.success(f"Role: {role}")
    
    if role == "HR":
        hr_dashboard()
    elif role == "Manager":
        manager_dashboard()
    elif role == "Leader":
        leader_dashboard()