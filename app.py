# app.py

import streamlit as st
import plotly.express as px
from knowledge_base import *
from evaluator import evaluate_all

st.set_page_config(layout="wide")

if "educations" not in st.session_state:
    st.session_state.educations = [
        {"highest_degree": HIGHEST_DEGREE_OPTIONS[3], "degree_field": "Computer Science"}
    ]

if "facts" not in st.session_state:
    st.session_state.facts = {}

st.title("Expert System Job Matcher")

left, right = st.columns([1.1, 1.4])

with left:
    st.subheader("Application")

    st.markdown("### Name")
    first = st.text_input("First name")
    last = st.text_input("Last name")

    st.markdown("### Education")

    for i, edu in enumerate(st.session_state.educations):
        with st.container(border=True):
            edu["highest_degree"] = st.selectbox(
                f"Degree {i+1}",
                HIGHEST_DEGREE_OPTIONS,
                key=f"deg_{i}"
            )

            edu["degree_field"] = st.selectbox(
                f"Field {i+1}",
                DEGREE_FIELD_OPTIONS,
                key=f"field_{i}"
            )

    if st.button("Add Degree"):
        if len(st.session_state.educations) < 5:
            st.session_state.educations.append(
                {"highest_degree": HIGHEST_DEGREE_OPTIONS[3], "degree_field": "Other"}
            )
            st.rerun()

    st.markdown("### Courses")
    courses = st.multiselect("STEM Courses", STEM_COURSE_OPTIONS)
    courses_other = ""
    if "Other" in courses:
        courses_other = st.text_input("Other Courses")

    st.markdown("### Experience")
    python_years = st.slider("Python Years", 0, 20, 0)
    data_years = st.slider("Data Years", 0, 20, 0)
    has_git = st.toggle("Used Git")

    certs = st.multiselect("Certifications", CERT_OPTIONS)

    if st.button("Evaluate", type="primary"):
        facts = {}
        facts["first_name"] = first
        facts["last_name"] = last

        facts.update(normalize_educations(st.session_state.educations))
        facts.update(normalize_courses(courses, courses_other))
        facts.update(normalize_certs(certs, ""))

        facts.update({
            "python_years": python_years,
            "data_years": data_years,
            "has_git": has_git,
        })

        st.session_state.facts = facts
        st.session_state.results = evaluate_all(facts, POSITIONS)

with right:
    st.subheader("Results")

    if "results" not in st.session_state:
        st.info("Complete application and evaluate.")
    else:
        results = st.session_state.results

        df = {
            "Position": [r.name for r in results],
            "Match %": [r.required_match_pct for r in results],
        }

        fig = px.bar(df, x="Position", y="Match %", text="Match %")
        st.plotly_chart(fig, use_container_width=True)

        for r in results:
            if r.qualified:
                st.success(r.name)
            else:
                st.error(r.name)

            with st.expander("Reasoning"):
                if r.qualified:
                    for item in r.required_passed:
                        st.write("✅", item["message"])
                else:
                    for item in r.required_failed:
                        st.write("❌", item["message"])
                        st.write("Expected:", item["expected"], "| Actual:", item["actual"])