# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from knowledge_base import *
from evaluator import evaluate_all, InferenceEngine

# Page configuration
st.set_page_config(
    page_title="Expert System Job Matcher",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state
if "educations" not in st.session_state:
    st.session_state.educations = [
        {"highest_degree": HIGHEST_DEGREE_OPTIONS[3], "degree_field": "Computer Science"}
    ]

if "facts" not in st.session_state:
    st.session_state.facts = {}

if "results" not in st.session_state:
    st.session_state.results = None

if "inference_engine" not in st.session_state:
    st.session_state.inference_engine = InferenceEngine()

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .qualified-badge {
        background-color: #00C853;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .not-qualified-badge {
        background-color: #D32F2F;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .skill-chip {
        background-color: #f0f2f6;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎯 Expert System Job Matcher</h1>', unsafe_allow_html=True)

# Main layout
left_col, right_col = st.columns([1.1, 1.4])

with left_col:
    st.markdown("## 📋 Application Form")
    
    with st.container(border=True):
        st.markdown("### 👤 Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", key="first_name")
        with col2:
            last_name = st.text_input("Last Name", key="last_name")
    
    with st.container(border=True):
        st.markdown("### 🎓 Education")
        
        # Display education entries
        for i, edu in enumerate(st.session_state.educations):
            with st.container(border=True):
                st.markdown(f"**Degree {i+1}**")
                edu["highest_degree"] = st.selectbox(
                    "Degree Level",
                    HIGHEST_DEGREE_OPTIONS,
                    key=f"deg_level_{i}",
                    index=HIGHEST_DEGREE_OPTIONS.index(edu["highest_degree"]) 
                    if edu["highest_degree"] in HIGHEST_DEGREE_OPTIONS else 3
                )
                
                edu["degree_field"] = st.selectbox(
                    "Field of Study",
                    DEGREE_FIELD_OPTIONS,
                    key=f"deg_field_{i}",
                    index=DEGREE_FIELD_OPTIONS.index(edu["degree_field"])
                    if edu["degree_field"] in DEGREE_FIELD_OPTIONS else 0
                )
        
        # Add degree button
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("➕ Add Another Degree", use_container_width=True):
                if len(st.session_state.educations) < 5:
                    st.session_state.educations.append(
                        {"highest_degree": HIGHEST_DEGREE_OPTIONS[3], "degree_field": "Other"}
                    )
                    st.rerun()
        with col2:
            if len(st.session_state.educations) > 1 and st.button("🗑️ Remove Last", use_container_width=True):
                st.session_state.educations.pop()
                st.rerun()
    
    with st.container(border=True):
        st.markdown("### 📚 Courses & Certifications")
        
        # Course selection
        courses = st.multiselect(
            "STEM Courses Completed",
            STEM_COURSE_OPTIONS,
            help="Select all relevant courses you have completed"
        )
        
        courses_other = ""
        if "Other" in courses:
            courses_other = st.text_input("Please specify other courses", key="other_courses")
        
        # Certifications
        certs = st.multiselect(
            "Professional Certifications",
            CERT_OPTIONS,
            help="Select any certifications you hold"
        )
        
        certs_other = ""
        if "Other" in certs:
            certs_other = st.text_input("Please specify other certifications", key="other_certs")
    
    with st.container(border=True):
        st.markdown("### 💼 Work Experience")
        
        # Experience inputs in columns
        exp_col1, exp_col2 = st.columns(2)
        
        with exp_col1:
            python_years = st.slider(
                "🐍 Python Development (years)",
                0, 20, 0,
                help="Years of professional Python development experience"
            )
            
            data_years = st.slider(
                "📊 Data Development (years)",
                min_value=0, max_value=20, value=0,
                help="Years of data development/engineering experience"
            )
            
            expert_systems_years = st.slider(
                "🤖 Expert Systems (years)",
                0, 20, 0,
                help="Years of expert systems development experience"
            )
        
        with exp_col2:
            project_mgmt_years = st.slider(
                "📋 Project Management (years)",
                0, 20, 0,
                help="Years of software project management experience"
            )
            
            agile_years = st.slider(
                "🔄 Agile Experience (years)",
                0, 20, 0,
                help="Years of experience working in Agile teams"
            )
            
            data_architecture_years = st.slider(
                "🏗️ Data Architecture (years)",
                0, 20, 0,
                help="Years of data architecture experience"
            )
        
        # Git experience toggle
        has_git = st.toggle("🔧 Git Experience", value=False, help="Have you used Git for version control?")
    
    # Evaluate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        evaluate_button = st.button(
            "🎯 Evaluate Qualifications",
            type="primary",
            use_container_width=True
        )

with right_col:
    st.markdown("## 📊 Evaluation Results")
    
    if evaluate_button:
        # Collect all facts
        facts = {}
        facts["first_name"] = first_name
        facts["last_name"] = last_name
        
        # Normalize and add all data
        facts.update(normalize_educations(st.session_state.educations))
        facts.update(normalize_courses(courses, courses_other))
        facts.update(normalize_certs(certs, certs_other))
        
        # Add experience facts
        facts.update({
            "python_years": python_years,
            "data_years": data_years,
            "expert_systems_years": expert_systems_years,
            "project_mgmt_years": project_mgmt_years,
            "agile_years": agile_years,
            "data_architecture_years": data_architecture_years,
            "has_git": has_git,
        })
        
        # Store facts and evaluate
        st.session_state.facts = facts
        
        # Evaluate with trace
        results = st.session_state.inference_engine.evaluate_with_trace(facts, POSITIONS)
        st.session_state.results = results
        
        # Store trace in session state for display
        st.session_state.trace = st.session_state.inference_engine.trace
    
    # Display results if available
    if st.session_state.results:
        results = st.session_state.results
        
        # Summary metrics
        qualified_count = sum(1 for r in results if r.qualified)
        
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(
                "✅ Qualified For",
                f"{qualified_count}/{len(results)} positions",
                delta=f"{qualified_count} matches"
            )
        with metric_col2:
            avg_required = sum(r.required_match_pct for r in results) / len(results)
            st.metric(
                "📊 Avg Required Match",
                f"{avg_required:.1f}%"
            )
        with metric_col3:
            avg_desired = sum(r.desired_match_pct for r in results) / len(results)
            st.metric(
                "⭐ Avg Desired Match",
                f"{avg_desired:.1f}%"
            )
        
        # Visualization
        st.markdown("### 📈 Qualification Overview")
        
        # Create comparison chart
        df = pd.DataFrame({
            'Position': [r.name for r in results],
            'Required Match %': [r.required_match_pct for r in results],
            'Desired Match %': [r.desired_match_pct for r in results],
            'Status': ['✅ Qualified' if r.qualified else '❌ Not Qualified' for r in results]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Required Skills',
            x=df['Position'],
            y=df['Required Match %'],
            marker_color='#1E88E5',
            text=df['Required Match %'].round(1),
            textposition='outside',
        ))
        fig.add_trace(go.Bar(
            name='Desired Skills',
            x=df['Position'],
            y=df['Desired Match %'],
            marker_color='#FFC107',
            text=df['Desired Match %'].round(1),
            textposition='outside',
        ))
        
        fig.update_layout(
            title="Skills Match by Position",
            xaxis_title="Position",
            yaxis_title="Match Percentage",
            barmode='group',
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed results
        st.markdown("### 📋 Detailed Position Analysis")
        
        tabs = st.tabs([r.name for r in results])
        
        for tab, result in zip(tabs, results):
            with tab:
                # Header with qualification status
                if result.qualified:
                    st.success(f"✅ **QUALIFIED** for {result.name}")
                else:
                    st.error(f"❌ **NOT QUALIFIED** for {result.name}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🔴 Required Skills")
                    if result.required_passed:
                        st.markdown("**Met Requirements:**")
                        for req in result.required_passed:
                            st.markdown(f"✅ {req.message}")
                    
                    if result.required_failed:
                        st.markdown("**Missing Requirements:**")
                        for req in result.required_failed:
                            st.markdown(f"❌ {req.message}")
                            st.caption(f"Expected: {req.expected}, Actual: {req.actual or 'Not provided'}")
                    
                    # Required skills progress
                    st.progress(result.required_match_pct / 100, 
                              text=f"Required Skills: {result.required_match_pct:.1f}%")
                
                with col2:
                    st.markdown("#### ⭐ Desired Skills")
                    if result.desired_met:
                        st.markdown("**Desired Skills Met:**")
                        for des in result.desired_met:
                            st.markdown(f"✅ {des.message}")
                    
                    if result.desired_missing:
                        st.markdown("**Desired Skills Not Met:**")
                        for des in result.desired_missing:
                            st.markdown(f"⭐ {des.message}")
                            st.caption(f"Expected: {des.expected}, Actual: {des.actual or 'Not provided'}")
                    
                    if not result.desired_met and not result.desired_missing:
                        st.info("No desired skills specified for this position.")
                    else:
                        st.progress(result.desired_match_pct / 100,
                                  text=f"Desired Skills: {result.desired_match_pct:.1f}%")
        
        # Inference trace expander
        with st.expander("🔍 View Inference Engine Trace"):
            if "trace" in st.session_state:
                for line in st.session_state.trace:
                    st.text(line)
        
        # Export results
        st.markdown("### 💾 Export Results")
        
        # Create export data
        export_text = f"""EXPERT SYSTEM JOB MATCHER RESULTS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Candidate: {first_name} {last_name}

{'='*60}

SUMMARY
Qualified for: {qualified_count}/{len(results)} positions

"""
        
        for result in results:
            export_text += f"""
{'-'*40}
POSITION: {result.name}
STATUS: {'QUALIFIED' if result.qualified else 'NOT QUALIFIED'}
Required Skills Match: {result.required_match_pct:.1f}%
Desired Skills Match: {result.desired_match_pct:.1f}%

Required Skills:
"""
            for req in result.required_passed:
                export_text += f"  ✅ {req.message}\n"
            for req in result.required_failed:
                export_text += f"  ❌ {req.message} (Expected: {req.expected}, Actual: {req.actual})\n"
            
            if result.desired_met or result.desired_missing:
                export_text += "\nDesired Skills:\n"
                for des in result.desired_met:
                    export_text += f"  ✅ {des.message}\n"
                for des in result.desired_missing:
                    export_text += f"  ⭐ {des.message} (Expected: {des.expected}, Actual: {des.actual})\n"
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download Results (TXT)",
                export_text,
                file_name=f"job_matcher_results_{first_name}_{last_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                use_container_width=True
            )
        
        with col2:
            # Create JSON export
            import json
            export_json = {
                "candidate": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "timestamp": datetime.now().isoformat()
                },
                "results": [
                    {
                        "position": r.name,
                        "qualified": r.qualified,
                        "required_match_pct": r.required_match_pct,
                        "desired_match_pct": r.desired_match_pct,
                        "required_passed": [{"message": req.message, "actual": req.actual} for req in r.required_passed],
                        "required_failed": [{"message": req.message, "expected": req.expected, "actual": req.actual} for req in r.required_failed],
                        "desired_met": [{"message": des.message, "actual": des.actual} for des in r.desired_met],
                        "desired_missing": [{"message": des.message, "expected": des.expected, "actual": des.actual} for des in r.desired_missing]
                    }
                    for r in results
                ]
            }
            
            st.download_button(
                "📥 Download Results (JSON)",
                json.dumps(export_json, indent=2),
                file_name=f"job_matcher_results_{first_name}_{last_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                use_container_width=True
            )
    
    else:
        # Placeholder when no results yet
        st.info("👈 Complete the application form and click 'Evaluate Qualifications' to see results")
        
        # Show example data
        with st.expander("📖 About This Expert System"):
            st.markdown("""
            This expert system evaluates job applicants against four positions:
            
            **Entry-Level Python Engineer**
            - Python coursework
            - Software Engineering coursework  
            - Agile course
            - Bachelor's in CS
            
            **Python Engineer**
            - 3+ years Python development
            - 1+ year data development
            - Bachelor's in CS
            - *Desired: Agile experience, Git*
            
            **Project Manager**
            - 3+ years managing software projects
            - 2+ years Agile experience
            - *Desired: PMI Lean Certification*
            
            **Senior Knowledge Engineer**
            - 4+ years Python development
            - 2+ years Expert Systems development
            - 2+ years data architecture
            - Master's in CS
            """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; padding: 1rem;'>"
    "🎯 Expert System Job Matcher | Built with Streamlit | "
    f"Session ID: {st.session_state.get('session_id', 'N/A')}"
    "</div>",
    unsafe_allow_html=True
)