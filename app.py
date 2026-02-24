# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from knowledge_base import *
from evaluator import InferenceEngine

st.set_page_config(page_title="Job Matcher", page_icon="🎯", layout="wide")

# Initialize Engine
if "engine" not in st.session_state:
    st.session_state.engine = InferenceEngine()
if "educations" not in st.session_state:
    st.session_state.educations = [{"highest_degree": "Bachelor’s Degree (B.A., B.S., B.F.A.)", "degree_field": "Computer Science"}]

st.title("🎯 Job Matcher Expert System")

left_col, right_col = st.columns([1, 1.5])

with left_col:
    with st.expander("👤 Personal & Education", expanded=True):
        f_name = st.text_input("First Name")
        l_name = st.text_input("Last Name")
        
        for i, edu in enumerate(st.session_state.educations):
            st.divider()
            edu["highest_degree"] = st.selectbox("Degree Level", HIGHEST_DEGREE_OPTIONS, key=f"lvl_{i}")
            edu["degree_field"] = st.selectbox("Field", DEGREE_FIELD_OPTIONS, key=f"fld_{i}")

    with st.expander("💼 Experience & Skills", expanded=True):
        py_yrs = st.slider("Python Years", 0, 15, 0)
        data_yrs = st.slider("Data Years", 0, 15, 0)
        pm_yrs = st.slider("PM Years", 0, 15, 0)
        agile_yrs = st.slider("Agile Years", 0, 15, 0)
        courses = st.multiselect("Courses", STEM_COURSE_OPTIONS)
        git = st.toggle("Git Experience")

    evaluate = st.button("Evaluate Match", type="primary", use_container_width=True)

with right_col:
    if evaluate:
        facts = {
            "python_years": py_yrs, "data_years": data_yrs, "project_mgmt_years": pm_yrs,
            "agile_years": agile_yrs, "has_git": git, **normalize_educations(st.session_state.educations),
            **normalize_courses(courses, "")
        }
        
        results = st.session_state.engine.evaluate_with_trace(facts, POSITIONS)
        
        # Charting
        fig = go.Figure([
            go.Bar(name='Required %', x=[r.name for r in results], y=[r.required_match_pct for r in results]),
            go.Bar(name='Desired %', x=[r.name for r in results], y=[r.desired_match_pct for r in results])
        ])
        st.plotly_chart(fig, use_container_width=True)

        for res in results:
            with st.container(border=True):
                color = "green" if res.qualified else "red"
                st.markdown(f"### :{color}[{res.name}]")
                if not res.qualified:
                    for fail in res.required_failed:
                        st.write(f"❌ {fail.message}")
                else:
                    st.write("✅ All requirements met!")