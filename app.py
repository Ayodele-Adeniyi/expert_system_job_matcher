# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from knowledge_base import (
    HIGHEST_DEGREE_OPTIONS,
    DEGREE_FIELD_OPTIONS,
    STEM_COURSE_OPTIONS,
    CERT_OPTIONS,
    POSITIONS,
    COURSE_WORK_EXAMPLES,
    normalize_educations,
    normalize_courses,
    normalize_certs,
)
from evaluator import InferenceEngine


st.set_page_config(page_title="Expert System Job Matcher", page_icon="🎯", layout="wide")

# -------------------------
# Session State
# -------------------------

if "educations" not in st.session_state:
    st.session_state.educations = [
        {"highest_degree": HIGHEST_DEGREE_OPTIONS[3], "degree_field": "Computer Science"}
    ]

if "results" not in st.session_state:
    st.session_state.results = None

if "trace" not in st.session_state:
    st.session_state.trace = []

if "engine" not in st.session_state:
    st.session_state.engine = InferenceEngine()

# -------------------------
# Header
# -------------------------

st.markdown(
    """
    <style>
    .main-header {font-size: 2.5rem; color: #1E88E5; text-align: center; margin-bottom: 1.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<h1 class="main-header">🎯 Expert System Job Matcher</h1>', unsafe_allow_html=True)

left_col, right_col = st.columns([1.1, 1.4])

# ============================================================
# LEFT COLUMN – FORM
# ============================================================

with left_col:

    st.markdown("## 📋 Application Form")

    # -------------------------
    # Personal Info
    # -------------------------

    with st.container(border=True):
        st.markdown("### 👤 Personal Information")
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First Name")
        with c2:
            last_name = st.text_input("Last Name")

    # -------------------------
    # Education
    # -------------------------

    with st.container(border=True):
        st.markdown("### 🎓 Education (up to 5)")

        for i, edu in enumerate(st.session_state.educations):
            with st.container(border=True):
                st.markdown(f"**Degree {i+1}**")

                edu["highest_degree"] = st.selectbox(
                    "Degree Level",
                    HIGHEST_DEGREE_OPTIONS,
                    key=f"deg_level_{i}",
                    index=HIGHEST_DEGREE_OPTIONS.index(edu["highest_degree"])
                    if edu["highest_degree"] in HIGHEST_DEGREE_OPTIONS
                    else 3,
                )

                edu["degree_field"] = st.selectbox(
                    "Field of Study",
                    DEGREE_FIELD_OPTIONS,
                    key=f"deg_field_{i}",
                    index=DEGREE_FIELD_OPTIONS.index(edu["degree_field"])
                    if edu["degree_field"] in DEGREE_FIELD_OPTIONS
                    else 0,
                )

        b1, b2 = st.columns([3, 1])

        with b1:
            if st.button("Add Another Degree", use_container_width=True):
                if len(st.session_state.educations) < 5:
                    st.session_state.educations.append(
                        {"highest_degree": HIGHEST_DEGREE_OPTIONS[3], "degree_field": "Other"}
                    )
                    st.rerun()
                else:
                    st.warning("Maximum of 5 education entries reached.")

        with b2:
            if len(st.session_state.educations) > 1:
                if st.button("Remove Last", use_container_width=True):
                    st.session_state.educations.pop()
                    st.rerun()

    # -------------------------
    # Courses & Certifications
    # -------------------------

    with st.container(border=True):
        st.markdown("### 📚 Courses and Certifications")

        courses = st.multiselect("STEM Courses Completed", STEM_COURSE_OPTIONS)

        courses_other = ""
        if "Other" in courses:
            courses_other = st.text_input("Other courses (comma separated)")

        certs = st.multiselect("Professional Certifications", CERT_OPTIONS)

        certs_other = ""
        if "Other" in certs:
            certs_other = st.text_input("Other certifications (comma separated)")

    # -------------------------
    # Work Experience
    # -------------------------

    with st.container(border=True):
        st.markdown("### 💼 Work Experience")

        exp1, exp2 = st.columns(2)

        with exp1:
            python_years = st.slider("Python Development (years)", 0, 20, 0)
            data_years = st.slider("Data Development (years)", 0, 20, 0)
            expert_systems_years = st.slider("Expert Systems Development (years)", 0, 20, 0)

        with exp2:
            project_mgmt_years = st.slider("Managing Software Projects (years)", 0, 20, 0)
            agile_years = st.slider("Agile Projects Experience (years)", 0, 20, 0)
            data_architecture_years = st.slider("Data Architecture and Development (years)", 0, 20, 0)

        has_git = st.toggle("Used Git", value=False)
        agile_projects = st.toggle("Experience in Agile projects", value=False)

    evaluate_button = st.button("Evaluate Qualifications", type="primary", use_container_width=True)

# ============================================================
# RIGHT COLUMN – RESULTS
# ============================================================

with right_col:

    st.markdown("## 📊 Evaluation Results")

    if evaluate_button:

        if not first_name.strip() or not last_name.strip():
            st.error("Please enter first name and last name.")
        else:
            facts = {
                "first_name": first_name.strip(),
                "last_name": last_name.strip(),
            }

            facts.update(normalize_educations(st.session_state.educations))
            facts.update(normalize_courses(courses, courses_other))
            facts.update(normalize_certs(certs, certs_other))

            facts.update(
                {
                    "python_years": python_years,
                    "data_years": data_years,
                    "expert_systems_years": expert_systems_years,
                    "project_mgmt_years": project_mgmt_years,
                    "agile_years": agile_years,
                    "data_architecture_years": data_architecture_years,
                    "has_git": has_git,
                    "agile_projects": agile_projects,
                }
            )

            results = st.session_state.engine.evaluate_with_trace(facts, POSITIONS)
            st.session_state.results = results
            st.session_state.trace = st.session_state.engine.trace
            st.success("Evaluation complete.")

    if st.session_state.results is None:
        st.info("Complete the form on the left and click Evaluate Qualifications.")

    else:

        results = st.session_state.results
        qualified_count = sum(1 for r in results if r.qualified)

        m1, m2, m3 = st.columns(3)

        with m1:
            st.metric("Qualified For", f"{qualified_count}/{len(results)}")

        with m2:
            st.metric(
                "Avg Required Match",
                f"{sum(r.required_match_pct for r in results) / len(results):.1f}%",
            )

        with m3:
            st.metric(
                "Avg Total Match",
                f"{sum(r.total_match_pct for r in results) / len(results):.1f}%",
            )

        # -------------------------
        # Detailed Analysis
        # -------------------------

        st.markdown("### 📋 Detailed Analysis")

        tabs = st.tabs([r.name for r in results])

        for tab, r in zip(tabs, results):

            with tab:

                if r.qualified:
                    st.success(f"QUALIFIED for {r.name}")
                else:
                    st.error(f"NOT QUALIFIED for {r.name}")

                c1, c2 = st.columns(2)

                # -------------------------
                # Required
                # -------------------------

                with c1:
                    st.markdown("#### Required")

                    if r.required_passed:
                        st.markdown("Met:")
                        for req in r.required_passed:
                            st.write(f"✅ {req.message}")

                    if r.required_failed:
                        st.markdown("Missing:")
                        for req in r.required_failed:
                            st.write(f"❌ {req.message}")

                            if req.field in COURSE_WORK_EXAMPLES:
                                examples = ", ".join(COURSE_WORK_EXAMPLES[req.field])
                                st.caption(f"Examples that count: {examples}")

                            if req.operator == "bool":
                                st.caption("This requirement was not satisfied.")
                            else:
                                st.caption(
                                    f"Required: {req.expected} | You entered: "
                                    f"{req.actual if req.actual is not None else 'Not provided'}"
                                )

                    st.progress(
                        r.required_match_pct / 100.0,
                        text=f"Required Match: {r.required_match_pct:.1f}%",
                    )

                # -------------------------
                # Desired
                # -------------------------

                with c2:
                    st.markdown("#### Desired")

                    if not r.desired_met and not r.desired_missing:
                        st.info("No desired items for this position.")
                    else:
                        if r.desired_met:
                            st.markdown("Met:")
                            for des in r.desired_met:
                                st.write(f"✅ {des.message}")

                        if r.desired_missing:
                            st.markdown("Not met:")
                            for des in r.desired_missing:
                                st.write(f"⭐ {des.message}")

                                if des.operator != "bool":
                                    st.caption(
                                        f"Required: {des.expected} | You entered: "
                                        f"{des.actual if des.actual is not None else 'Not provided'}"
                                    )

                        st.progress(
                            r.desired_match_pct / 100.0,
                            text=f"Desired Match: {r.desired_match_pct:.1f}%",
                        )

        # -------------------------
        # Trace
        # -------------------------

        with st.expander("View Inference Engine Trace"):
            for line in st.session_state.trace:
                st.text(line)

        # -------------------------
        # Export
        # -------------------------

        st.markdown("### 💾 Export Results")

        export_text = (
            "EXPERT SYSTEM JOB MATCHER RESULTS\n"
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Candidate: {first_name} {last_name}\n\n"
        )

        for r in results:
            export_text += f"POSITION: {r.name}\n"
            export_text += f"STATUS: {'QUALIFIED' if r.qualified else 'NOT QUALIFIED'}\n"
            export_text += f"Required Match: {r.required_match_pct:.1f}%\n"
            export_text += f"Desired Match: {r.desired_match_pct:.1f}%\n"
            export_text += "Missing Required:\n"

            if r.required_failed:
                for req in r.required_failed:
                    export_text += f"  - {req.message}\n"
            else:
                export_text += "  - None\n"

            export_text += "\n"

        st.download_button(
            "Download Results (TXT)",
            export_text,
            file_name=f"job_matcher_results_{first_name}_{last_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            use_container_width=True,
        )