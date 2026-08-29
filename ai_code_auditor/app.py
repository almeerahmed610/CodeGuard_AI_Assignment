# from __future__ import annotations
# import streamlit as st
# from dotenv import load_dotenv
# from services.pipeline import run_pipeline

# load_dotenv()
# st.set_page_config(page_title="CodeGuard AI", page_icon="🛡️", layout="wide")

# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
# html,body,[class*="css"]{font-family:Inter,sans-serif}
# .stApp{background:radial-gradient(circle at 10% 0%,rgba(99,102,241,.14),transparent 30%),radial-gradient(circle at 90% 10%,rgba(14,165,233,.10),transparent 28%),#08111f;color:#e8eef8}
# .block-container{max-width:1450px;padding-top:2rem;padding-bottom:3rem}
# .hero{padding:30px 34px;border:1px solid rgba(148,163,184,.16);border-radius:24px;background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(17,30,52,.82));box-shadow:0 20px 70px rgba(0,0,0,.25);margin-bottom:22px}
# .badge{display:inline-block;padding:7px 12px;border-radius:999px;background:rgba(99,102,241,.15);color:#a5b4fc;border:1px solid rgba(129,140,248,.25);font-size:12px;font-weight:700;text-transform:uppercase}
# .hero h1{font-size:42px;margin:14px 0 10px}.hero p{color:#9fb0c7;font-size:16px;max-width:900px}
# .card{background:rgba(15,23,42,.72);border:1px solid rgba(148,163,184,.14);border-radius:18px;padding:20px;height:100%}
# .section-title{font-size:18px;font-weight:750;margin:5px 0 15px}
# .metric{padding:16px;border-radius:15px;background:rgba(30,41,59,.55);border:1px solid rgba(148,163,184,.12)}
# .metric .label{color:#8fa2bb;font-size:12px}.metric .value{font-size:25px;font-weight:800;margin-top:3px}
# .agent{display:flex;gap:13px;align-items:center;padding:14px;border-radius:14px;background:rgba(30,41,59,.48);border:1px solid rgba(148,163,184,.11);margin-bottom:10px}
# .agent .icon{font-size:24px}.agent b{font-size:14px}.agent span{display:block;color:#8fa2bb;font-size:12px;margin-top:2px}
# .stButton>button{border-radius:12px;min-height:44px;font-weight:700}
# div[data-testid="stTextArea"] textarea{background:#0b1729!important;border:1px solid #253650!important;border-radius:12px!important;color:#e8eef8!important}
# [data-testid="stSidebar"]{background:#07101d;border-right:1px solid rgba(148,163,184,.12)}
# .small-note{color:#7f93ad;font-size:12px}
# </style>
# """, unsafe_allow_html=True)

# if "result" not in st.session_state:
#     st.session_state.result = None

# st.markdown("""
# <div class="hero">
# <span class="badge">AI Development Intelligence</span>
# <h1>🛡️ CodeGuard AI</h1>
# <p>Sequential Multi-Agent Code Auditor — scan code, refactor it, and generate production-ready documentation.</p>
# </div>
# """, unsafe_allow_html=True)

# with st.sidebar:
#     st.markdown("## ⚙️ Configuration")
#     st.caption("Scanner → Refactor → Docs")
#     model = st.selectbox("Gemini Model", ["gemini-2.5-flash", "gemini-2.5-flash-lite"])
#     temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
#     st.divider()
#     st.markdown("### Agent roles")
#     st.markdown("🔎 **Scanner** — audit & findings")
#     st.markdown("🧹 **Refactor** — clean & optimize")
#     st.markdown("📚 **Docs** — README & docstrings")

# left,right=st.columns([1.18,.82],gap="large")
# with left:
#     st.markdown('<div class="card">',unsafe_allow_html=True)
#     st.markdown('<div class="section-title">💻 Source Code</div>',unsafe_allow_html=True)
#     uploaded=st.file_uploader("Upload Python file (optional)",type=["py","txt"])
#     default_code="""import sqlite3

# def get_user(user_id):
#     conn = sqlite3.connect("app.db")
#     query = "SELECT * FROM users WHERE id = " + str(user_id)
#     return conn.execute(query).fetchone()

# def greet(name):
#     print("Hello " + name)
# """
#     if uploaded:
#         code=uploaded.read().decode("utf-8",errors="replace")
#         st.caption(f"Loaded: {uploaded.name}")
#     else:
#         code=st.text_area("Paste code",value=default_code,height=380,label_visibility="collapsed")
#     run=st.button("🚀 Run Full Audit",type="primary",use_container_width=True)
#     st.markdown("</div>",unsafe_allow_html=True)

# with right:
#     st.markdown('<div class="card">',unsafe_allow_html=True)
#     st.markdown('<div class="section-title">🔄 Sequential Agent Pipeline</div>',unsafe_allow_html=True)
#     for icon,name,desc in [
#         ("🔎","Scanner Agent","Security, bugs, quality & PEP8 audit"),
#         ("🧹","Refactor Agent","Fix findings and improve maintainability"),
#         ("📚","Docs Agent","Generate README and function documentation")]:
#         st.markdown(f'<div class="agent"><div class="icon">{icon}</div><div><b>{name}</b><span>{desc}</span></div></div>',unsafe_allow_html=True)
#     st.info("Typed LangGraph state safely carries results from one agent to the next.")
#     st.markdown("</div>",unsafe_allow_html=True)

# if run:
#     with st.status("Running CodeGuard AI pipeline…",expanded=True) as status:
#         try:
#             st.write("🔎 Scanner Agent: auditing code…")
#             result=run_pipeline(code,model,temperature)
#             st.write("🧹 Refactor Agent: improving code…")
#             st.write("📚 Docs Agent: generating documentation…")
#             st.session_state.result=result
#             status.update(label="Audit completed successfully",state="complete")
#         except Exception as exc:
#             status.update(label="Pipeline failed",state="error")
#             st.error(f"{type(exc).__name__}: {exc}")
#             st.stop()

# result=st.session_state.result
# if result:
#     st.markdown("## 📊 Audit Dashboard")
#     findings=result.get("findings",[])
#     sev={"High":0,"Medium":0,"Low":0}
#     for f in findings:
#         s=str(f.get("severity","Low")).title()
#         if s in sev: sev[s]+=1
#     cols=st.columns(4)
#     for col,(label,value) in zip(cols,[("Total Findings",len(findings)),("High Risk",sev["High"]),("Medium Risk",sev["Medium"]),("Low Risk",sev["Low"])]):
#         with col: st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div></div>',unsafe_allow_html=True)

#     st.markdown("## 🔎 Scanner Report")
#     for i,item in enumerate(findings,1):
#         with st.expander(f"{i}. {item.get('title','Finding')} · {item.get('severity','Low')}"):
#             st.write(item.get("description",""))
#             st.markdown("**Recommendation:** "+item.get("recommendation",""))
#     if not findings: st.success("No findings were returned.")

#     tab1,tab2,tab3=st.tabs(["🧹 Refactored Code","📚 Documentation","🧠 Pipeline State"])
#     with tab1:
#         fixed=result.get("refactored_code","")
#         st.code(fixed or "No refactored code returned.",language="python")
#         if fixed: st.download_button("⬇️ Download cleaned code",fixed,"refactored_code.py","text/x-python")
#     with tab2:
#         docs=result.get("documentation","")
#         st.markdown(docs or "No documentation returned.")
#         if docs: st.download_button("⬇️ Download README",docs,"README.md","text/markdown")
#     with tab3:
#         st.json({"scanner":"completed","refactor":"completed","docs":"completed"})
# else:
#     st.markdown("## ✨ Assignment Features")
#     for col,title,text in zip(st.columns(3),
#         ["Automated Scanning","Automatic Refactoring","Auto Documentation"],
#         ["Detect bugs, security risks and quality issues.","Fix findings and improve maintainability.","Generate README content and documentation."]):
#         with col:
#             st.markdown(f'<div class="card"><div class="section-title">{title}</div><div class="small-note">{text}</div></div>',unsafe_allow_html=True)

from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from services.pipeline import run_pipeline


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CodeGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(59, 130, 246, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(139, 92, 246, 0.10),
            transparent 30%
        ),
        #07111f;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Header */

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 4px;
}

.main-subtitle {
    font-size: 16px;
    color: #94a3b8;
    margin-bottom: 28px;
}

/* Section headings */

.section-heading {
    font-size: 21px;
    font-weight: 750;
    margin-top: 10px;
    margin-bottom: 15px;
}

/* Agent cards */

.agent-card {
    background: rgba(15, 30, 50, 0.72);
    border: 1px solid rgba(100, 116, 139, 0.20);
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
}

.agent-title {
    font-size: 16px;
    font-weight: 700;
}

.agent-description {
    color: #8da1ba;
    font-size: 13px;
    margin-top: 5px;
}

/* Metrics */

.metric-card {
    background: rgba(15, 30, 50, 0.72);
    border: 1px solid rgba(100, 116, 139, 0.18);
    border-radius: 16px;
    padding: 18px;
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    margin-top: 4px;
}

/* Text editor */

textarea {
    font-family:
        Consolas,
        "Courier New",
        monospace !important;
}

/* Buttons */

.stButton > button {
    border-radius: 11px;
    min-height: 46px;
    font-weight: 700;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #06101c;
}

/* File uploader */

section[data-testid="stFileUploaderDropzone"] {
    background: rgba(15, 30, 50, 0.60);
    border-radius: 14px;
}

/* Tabs */

button[data-baseweb="tab"] {
    font-weight: 650;
}

/* Alerts */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Code */

pre {
    border-radius: 12px !important;
}

/* Pipeline status */

.pipeline-status {
    background: rgba(15, 30, 50, 0.55);
    border: 1px solid rgba(100, 116, 139, 0.20);
    border-radius: 14px;
    padding: 14px;
    margin-top: 10px;
}

</style>""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "audit_error" not in st.session_state:
    st.session_state.audit_error = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ CodeGuard AI")

    st.caption(
        "Sequential Multi-Agent Code Auditor"
    )

    st.divider()

    st.subheader("⚙️ AI Configuration")

    model = st.selectbox(
        "Gemini Model",
        [
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-3.1-flash-lite",
        ],
        index=0,
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
    )

    st.divider()

    st.subheader("🤖 Agent Pipeline")

    st.write("🔎 **Scanner Agent**")

    st.caption(
        "Security, bugs, quality and PEP8 analysis."
    )

    st.write("🧹 **Refactor Agent**")

    st.caption(
        "Fix findings and improve maintainability."
    )

    st.write("📚 **Docs Agent**")

    st.caption(
        "Generate README and function documentation."
    )

    st.divider()

    st.caption(
        "Built with Streamlit • LangGraph • LangChain • Gemini"
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ CodeGuard AI</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-subtitle">'
    "AI-powered sequential code auditing, refactoring "
    "and automatic documentation."
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# TOP INFORMATION
# ============================================================

info1, info2, info3 = st.columns(3)

with info1:

    st.info(
        "🔎 **Scanner**\n\n"
        "Find vulnerabilities, bugs and code-quality issues."
    )

with info2:

    st.info(
        "🧹 **Refactor**\n\n"
        "Improve security, readability and maintainability."
    )

with info3:

    st.info(
        "📚 **Documentation**\n\n"
        "Automatically generate professional documentation."
    )


st.divider()


# ============================================================
# MAIN INPUT AREA
# ============================================================

left, right = st.columns(
    [1.25, 0.75],
    gap="large",
)


# ============================================================
# LEFT: SOURCE CODE
# ============================================================

with left:

    st.markdown(
        '<div class="section-heading">💻 Source Code</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload Python file",
        type=["py", "txt"],
        help="Upload a Python source file for auditing.",
    )

    default_code = """import sqlite3


def get_user(user_id):
    conn = sqlite3.connect("app.db")

    query = (
        "SELECT * FROM users WHERE id = "
        + str(user_id)
    )

    return conn.execute(query).fetchone()


def greet(name):
    print("Hello " + name)
"""

    if uploaded_file is not None:

        try:

            source_code = uploaded_file.read().decode(
                "utf-8",
                errors="replace",
            )

            st.success(
                f"Loaded: {uploaded_file.name}"
            )

        except Exception as exc:

            st.error(
                f"Unable to read uploaded file: {exc}"
            )

            source_code = ""

    else:

        source_code = st.text_area(
            "Python Source Code",
            value=default_code,
            height=390,
            label_visibility="collapsed",
        )

    run_audit = st.button(
        "🚀 Run Full Audit",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# RIGHT: AGENTS
# ============================================================

with right:

    st.markdown(
        '<div class="section-heading">'
        "🔄 Sequential Agent Pipeline"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-title">
                🔎 Scanner Agent
            </div>
            <div class="agent-description">
                Security, bugs, code quality and PEP8 audit
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-title">
                🧹 Refactor Agent
            </div>
            <div class="agent-description">
                Fix findings and improve maintainability
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="agent-card">
            <div class="agent-title">
                📚 Docs Agent
            </div>
            <div class="agent-description">
                Generate README and function documentation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.success(
        "Scanner → Refactor → Documentation"
    )

    st.caption(
        "Typed pipeline state carries the output of "
        "each agent to the next agent."
    )


# ============================================================
# RUN AUDIT
# ============================================================

if run_audit:

    if not source_code.strip():

        st.warning(
            "Please enter Python code or upload a Python file."
        )

        st.stop()

    st.session_state.audit_error = None

    with st.status(
        "🚀 Running CodeGuard AI...",
        expanded=True,
    ) as status:

        try:

            st.write(
                "🔎 Scanner Agent — analyzing source code..."
            )

            result = run_pipeline(
                source_code=source_code,
                model=model,
                temperature=temperature,
            )

            st.write(
                "🧹 Refactor Agent — improving source code..."
            )

            st.write(
                "📚 Docs Agent — generating documentation..."
            )

            st.session_state.result = result

            status.update(
                label="✅ Audit completed successfully",
                state="complete",
            )

        except Exception as exc:

            st.session_state.audit_error = (
                f"{type(exc).__name__}: {exc}"
            )

            status.update(
                label="❌ Pipeline failed",
                state="error",
            )


# ============================================================
# ERROR DISPLAY
# ============================================================

if st.session_state.audit_error:

    st.error(
        st.session_state.audit_error
    )

    st.info(
        "Please verify GEMINI_API_KEY in your .env file "
        "and make sure the Google GenAI package is installed."
    )


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.result


if result:

    st.divider()

    st.markdown(
        '<div class="section-heading">'
        "📊 Audit Dashboard"
        "</div>",
        unsafe_allow_html=True,
    )

    findings = result.get(
        "findings",
        [],
    )

    if not isinstance(findings, list):
        findings = []


    # ========================================================
    # SEVERITY COUNTS
    # ========================================================

    high_count = 0
    medium_count = 0
    low_count = 0

    for finding in findings:

        if not isinstance(finding, dict):
            continue

        severity = str(
            finding.get(
                "severity",
                "Low",
            )
        ).lower()

        if severity == "high":
            high_count += 1

        elif severity == "medium":
            medium_count += 1

        else:
            low_count += 1


    # ========================================================
    # METRICS
    # ========================================================

    m1, m2, m3, m4 = st.columns(4)

    with m1:

        st.metric(
            "Total Findings",
            len(findings),
        )

    with m2:

        st.metric(
            "🔴 High Risk",
            high_count,
        )

    with m3:

        st.metric(
            "🟠 Medium Risk",
            medium_count,
        )

    with m4:

        st.metric(
            "🟢 Low Risk",
            low_count,
        )


    st.divider()


    # ========================================================
    # FINDINGS
    # ========================================================

    st.markdown(
        '<div class="section-heading">'
        "🔎 Scanner Findings"
        "</div>",
        unsafe_allow_html=True,
    )

    if not findings:

        st.success(
            "🎉 No findings were returned by the Scanner Agent."
        )

    else:

        for index, finding in enumerate(
            findings,
            start=1,
        ):

            if not isinstance(finding, dict):
                continue

            title = finding.get(
                "title",
                f"Finding {index}",
            )

            severity = finding.get(
                "severity",
                "Low",
            )

            description = finding.get(
                "description",
                "No description provided.",
            )

            recommendation = finding.get(
                "recommendation",
                "No recommendation provided.",
            )

            with st.expander(
                f"{index}. {title} — {severity}"
            ):

                st.write(description)

                st.markdown(
                    "**Recommendation**"
                )

                st.info(
                    recommendation
                )


    # ========================================================
    # OUTPUT TABS
    # ========================================================

    st.divider()

    code_tab, docs_tab, state_tab = st.tabs(
        [
            "🧹 Refactored Code",
            "📚 Documentation",
            "🧠 Pipeline State",
        ]
    )


    # ========================================================
    # REFACTORED CODE
    # ========================================================

    with code_tab:

        refactored_code = result.get(
            "refactored_code",
            "",
        )

        if refactored_code:

            st.code(
                refactored_code,
                language="python",
            )

            st.download_button(
                "⬇️ Download Refactored Code",
                data=refactored_code,
                file_name="refactored_code.py",
                mime="text/x-python",
                use_container_width=True,
            )

        else:

            st.warning(
                "No refactored code was returned."
            )


    # ========================================================
    # DOCUMENTATION
    # ========================================================

    with docs_tab:

        documentation = result.get(
            "documentation",
            "",
        )

        if documentation:

            st.markdown(
                documentation
            )

            st.download_button(
                "⬇️ Download README",
                data=documentation,
                file_name="README.md",
                mime="text/markdown",
                use_container_width=True,
            )

        else:

            st.warning(
                "No documentation was returned."
            )


    # ========================================================
    # STATE
    # ========================================================

    with state_tab:

        st.json(
            {
                "scanner": "completed",
                "refactor": "completed",
                "docs": "completed",
                "model": result.get(
                    "model",
                    model,
                ),
            }
        )


# ============================================================
# INITIAL EMPTY STATE
# ============================================================

else:

    st.divider()

    st.markdown(
        '<div class="section-heading">'
        "✨ How CodeGuard AI Works"
        "</div>",
        unsafe_allow_html=True,
    )

    step1, step2, step3 = st.columns(3)

    with step1:

        st.markdown("### 01 🔎 Scan")

        st.write(
            "Analyze Python source code for security "
            "vulnerabilities, bugs, bad practices and PEP8 issues."
        )

    with step2:

        st.markdown("### 02 🧹 Refactor")

        st.write(
            "Use the audit findings to produce cleaner, "
            "safer and more maintainable code."
        )

    with step3:

        st.markdown("### 03 📚 Document")

        st.write(
            "Generate professional README and function "
            "documentation automatically."
        )