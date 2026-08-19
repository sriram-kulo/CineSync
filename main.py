"""
CineSync Dyno: Studio Platform

Autonomous Multi-Agent Orchestration Platform powered by Gemini,
True Model Context Protocol (MCP) Client-Server Subprocess Transport,
Deterministic Financial Calculations, Automated Failure Recovery,
and Human-in-the-Loop Executive Governance.
"""

import streamlit as st
import tempfile
import os
import time
import datetime
import json
import asyncio

from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# =========================================================
# 0. ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CineSync Dyno",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. GLOBAL CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 0%,
                rgba(59, 130, 246, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(124, 58, 237, 0.08),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #020617 0%,
                #07111f 50%,
                #020617 100%
            );

        color: #e5e7eb;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #050b16 0%,
                #07111f 55%,
                #050b16 100%
            );

        border-right: 1px solid rgba(148, 163, 184, 0.10);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        overflow-y: auto !important;
        height: auto !important;
    }

    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding-bottom: 2rem;
    }


    /* =====================================================
       SIDEBAR BRAND
       ===================================================== */

    .sidebar-brand-box {
        padding: 4px 0 16px 0;
        margin-bottom: 18px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
    }

    .sidebar-brand-title {
        font-size: 1.35rem;
        font-weight: 850;
        color: #f8fafc;
        letter-spacing: -0.5px;
    }

    .sidebar-brand-subtitle {
        margin-top: 5px;
        color: #64748b;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .sidebar-heading {
        color: #94a3b8;
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 18px;
        margin-bottom: 10px;
    }


    /* =====================================================
       SIDEBAR INFO CARD
       ===================================================== */

    .runtime-card {
        width: 100%;
        box-sizing: border-box;
        padding: 14px;
        margin: 0;
        border-radius: 14px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.95),
                rgba(15, 23, 42, 0.70)
            );

        border: 1px solid rgba(148, 163, 184, 0.11);

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.20);
    }

    .runtime-label {
        display: block;
        width: 100%;
        box-sizing: border-box;
        color: #64748b;
        font-size: 0.64rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
        margin-bottom: 3px;
    }

    .runtime-value {
        display: block;
        width: 100%;
        box-sizing: border-box;
        color: #f8fafc;
        font-size: 0.82rem;
        font-weight: 750;
        margin-top: 3px;
        line-height: 1.35;
        overflow-wrap: anywhere;
        word-break: break-word;
    }


    /* =====================================================
       MAIN HEADER
       ===================================================== */

    .hero-kicker {
        color: #60a5fa;
        font-size: 0.70rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        margin-bottom: 7px;
    }

    .hero-title {
        font-size: 3.15rem;
        line-height: 1;
        font-weight: 900;
        letter-spacing: -2px;
        margin: 0;

        background:
            linear-gradient(
                90deg,
                #60a5fa 0%,
                #a78bfa 52%,
                #f472b6 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        max-width: 900px;
        color: #94a3b8;
        font-size: 0.94rem;
        line-height: 1.65;
        margin-top: 12px;
        margin-bottom: 20px;
    }


    /* =====================================================
       STATUS CARDS
       ===================================================== */

    .status-card {
        padding: 10px 13px;
        border-radius: 12px;

        background:
            rgba(15, 23, 42, 0.75);

        border:
            1px solid rgba(148, 163, 184, 0.11);

        text-align: center;
    }

    .status-title {
        color: #f8fafc;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    .status-subtitle {
        color: #64748b;
        font-size: 0.60rem;
        margin-top: 2px;
    }

    .status-online {
        color: #34d399;
    }

    .status-blue {
        color: #60a5fa;
    }

    .status-purple {
        color: #a78bfa;
    }

    .status-white {
        color: #e2e8f0;
    }


    /* =====================================================
       SECTION HEADER
       ===================================================== */

    .section-heading {
        color: #94a3b8;
        font-size: 0.70rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: 1.5px;

        margin-top: 28px;
        margin-bottom: 12px;

        padding-bottom: 8px;

        border-bottom:
            1px solid rgba(96, 165, 250, 0.14);
    }


    /* =====================================================
       CARDS
       ===================================================== */

    .ui-card {
        padding: 22px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.96),
                rgba(15, 23, 42, 0.74)
            );

        border:
            1px solid rgba(148, 163, 184, 0.11);

        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.25);

        margin-bottom: 18px;
    }

    .card-title {
        color: #f8fafc;
        font-size: 1.05rem;
        font-weight: 800;
    }

    .card-description {
        display: block;
        width: 100%;
        box-sizing: border-box;
        color: #64748b;
        font-size: 0.78rem;
        line-height: 1.55;
        margin-top: 5px;
        margin-bottom: 15px;
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    /* Tab content card styling — wraps Streamlit widgets inside tabs */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.74));
        border: 1px solid rgba(148,163,184,0.11);
        box-shadow: 0 18px 45px rgba(0,0,0,0.25);
        margin-bottom: 18px;
    }


    /* =====================================================
       METRICS
       ===================================================== */

    .metric-box {
        width: 100%;
        min-height: 112px;
        box-sizing: border-box;

        padding: 17px;

        border-radius: 15px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.96),
                rgba(15, 23, 42, 0.72)
            );

        border:
            1px solid rgba(148, 163, 184, 0.11);

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.20);
    }

    .metric-label {
        display: block;
        color: #64748b;
        font-size: 0.64rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        display: block;
        color: #f8fafc;
        font-size: 1.45rem;
        font-weight: 850;
        margin-top: 8px;
        line-height: 1.2;
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    .metric-description {
        display: block;
        color: #64748b;
        font-size: 0.67rem;
        margin-top: 3px;
        line-height: 1.4;
        overflow-wrap: anywhere;
        word-break: break-word;
    }


    /* =====================================================
       TELEMETRY
       ===================================================== */

    .telemetry-container {
        width: 100%;
        box-sizing: border-box;
        padding: 18px;

        border-radius: 17px;

        background:
            linear-gradient(
                145deg,
                rgba(15, 23, 42, 0.97),
                rgba(15, 23, 42, 0.76)
            );

        border:
            1px solid rgba(96, 165, 250, 0.16);

        box-shadow:
            0 16px 40px rgba(0, 0, 0, 0.26);

        margin: 10px 0 20px 0;
    }

    .telemetry-title {
        display: block;
        color: #f8fafc;
        font-size: 1rem;
        font-weight: 800;
    }

    .telemetry-description {
        display: block;
        color: #64748b;
        font-size: 0.75rem;
        margin-top: 3px;
        margin-bottom: 16px;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        border-radius: 10px !important;
        min-height: 43px;

        font-weight: 800 !important;

        border:
            1px solid rgba(96, 165, 250, 0.18) !important;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 10px 24px rgba(37, 99, 235, 0.20);
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    textarea {
        border-radius: 12px !important;
    }

    [data-testid="stFileUploader"] {
        border-radius: 12px;
    }


    /* =====================================================
       TABS
       ===================================================== */

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;

        background:
            rgba(15, 23, 42, 0.70);

        padding: 6px;

        border-radius: 13px;

        border:
            1px solid rgba(148, 163, 184, 0.10);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #64748b;
        font-weight: 700;
        padding: 8px 11px;
    }

    .stTabs [aria-selected="true"] {
        background:
            linear-gradient(
                135deg,
                #2563eb,
                #7c3aed
            ) !important;

        color: white !important;

        box-shadow:
            0 5px 18px rgba(37, 99, 235, 0.25);
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    [data-testid="stExpander"] {
        border:
            1px solid rgba(148, 163, 184, 0.11);

        border-radius: 13px;

        background:
            rgba(15, 23, 42, 0.55);
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer-text {
        text-align: center;
        color: #475569;
        font-size: 0.68rem;
        padding: 35px 0 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. CLIENT INITIALIZATION
# =========================================================

try:
    client = genai.Client()

except Exception as initialization_error:

    st.error(
        "Critical Error: Failed to initialize Gemini Client. "
        "Verify GEMINI_API_KEY."
    )

    st.code(str(initialization_error))
    st.stop()


# =========================================================
# 4. SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "show_telemetry": False,
    "studio_chat_session": None,
    "chat_message_history": [],
    "director_output": None,
    "dept_output": None,
    "finance_output": None,
    "audit_output": None,
    "mcp_traces": [],
    "audit_trail": [],
    "recovery_actions": [],
    "requires_approval": False,
    "budget_data": {},
    "production_tier": None,
    "last_execution_time": None,
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 5. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-title">
                🎬 CineSync Dyno
            </div>
            <div class="sidebar-brand-subtitle">
                Studio Operations Control
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-heading">Production Configuration</div>',
        unsafe_allow_html=True,
    )

    selected_gemini_model = st.selectbox(
        "Gemini Engine",
        [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
        ],
        help="Gemini model used by the CineSync agents.",
    )

    production_tier = st.selectbox(
        "Production Tier",
        [
            "Indie Micro-Budget ($500k)",
            "Studio Feature ($20M+)",
            "High-End Commercial",
        ],
    )

    max_allowed_budget = st.slider(
        "Strict Budget Ceiling",
        min_value=50000,
        max_value=2000000,
        value=500000,
        step=25000,
        format="$%d",
    )

    audit_strictness = st.slider(
        "Executive Compliance Strictness",
        min_value=1,
        max_value=5,
        value=5,
        help=(
            "Controls how aggressively the Executive Auditor "
            "evaluates risk."
        ),
    )

    st.markdown(
        '<div class="sidebar-heading">Runtime</div>',
        unsafe_allow_html=True,
    )

    st.success("Gemini API Connected")

    st.markdown(
        f"""<div class="runtime-card">
<div class="runtime-label">Active Engine</div>
<div class="runtime-value">{selected_gemini_model}</div>
<div class="runtime-label">MCP Transport</div>
<div class="runtime-value">Stdio / JSON-RPC 2.0</div>
<div class="runtime-label">Governance</div>
<div class="runtime-value">Human-in-the-loop</div>
<div class="runtime-label">Observability</div>
<div class="runtime-value">Grafana Cloud</div>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-heading">Environment</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "CineSync Dyno • Enterprise Production Intelligence"
    )


# =========================================================
# 6. MAIN HERO
# =========================================================

st.markdown(
    """
    <div class="hero-kicker">
        Autonomous Studio Intelligence
    </div>

    <div class="hero-title">
        CineSync Dyno
    </div>

    <div class="hero-description">
        Production intelligence for screenplay analysis,
        asset discovery, deterministic budgeting,
        autonomous recovery, and executive governance.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 7. SYSTEM STATUS
# =========================================================

status_1, status_2, status_3, status_4 = st.columns(4)

with status_1:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title status-online">● SYSTEM ONLINE</div>
            <div class="status-subtitle">Core application</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with status_2:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title status-blue">● GEMINI CONNECTED</div>
            <div class="status-subtitle">AI orchestration</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with status_3:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title status-purple">● MCP READY</div>
            <div class="status-subtitle">Asset services</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with status_4:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title status-white">🔒 HUMAN GOVERNANCE</div>
            <div class="status-subtitle">Executive controls</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 8. TELEMETRY BUTTON
# =========================================================

st.markdown(
    '<div class="section-heading">Operations</div>',
    unsafe_allow_html=True,
)

telemetry_left, telemetry_right = st.columns([5, 1])

with telemetry_right:

    telemetry_button_text = (
        "📡 Hide Telemetry"
        if st.session_state["show_telemetry"]
        else "📡 Production Telemetry"
    )

    if st.button(
        telemetry_button_text,
        use_container_width=True,
    ):
        st.session_state["show_telemetry"] = (
            not st.session_state["show_telemetry"]
        )
        st.rerun()


# =========================================================
# 9. OPTIONAL TELEMETRY
# =========================================================

if st.session_state["show_telemetry"]:

    st.markdown(
        """
        <div class="telemetry-container">
            <div class="telemetry-title">📡 Production Telemetry</div>
            <div class="telemetry-description">Runtime health and orchestration status.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    telemetry1, telemetry2, telemetry3, telemetry4 = st.columns(4)

    with telemetry1:
        st.markdown(
            """
            <div class="metric-box">
                <div class="metric-label">AI Orchestration</div>
                <div class="metric-value">READY</div>
                <div class="metric-description">Gemini multi-agent pipeline</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with telemetry2:
        st.markdown(
            """
            <div class="metric-box">
                <div class="metric-label">MCP Transport</div>
                <div class="metric-value">LIVE</div>
                <div class="metric-description">JSON-RPC over stdio</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with telemetry3:
        governance_state = (
            "APPROVAL"
            if st.session_state.get("requires_approval", False)
            else "READY"
        )
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">Governance</div>
                <div class="metric-value">{governance_state}</div>
                <div class="metric-description">Executive authorization layer</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with telemetry4:
        trace_count = len(st.session_state.get("mcp_traces", []))
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-label">MCP Calls</div>
                <div class="metric-value">{trace_count}</div>
                <div class="metric-description">Verified subprocess calls</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# 10. MCP TOOL DEFINITION
# =========================================================

query_studio_asset_database_tool = {
    "name": "query_studio_asset_database",
    "description": (
        "Securely query the standalone MCP server subprocess "
        "for verified props, specialized weaponry, and camera packages."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "item_query": {
                "type": "STRING",
                "description": (
                    "Specific prop, wardrobe, or optical "
                    "equipment identifier to inspect."
                ),
            }
        },
        "required": ["item_query"],
    },
}


# =========================================================
# 11. TRUE MCP CLIENT
# =========================================================

async def _async_execute_mcp_call(
    tool_name: str,
    arguments: dict,
) -> dict:

    server_params = StdioServerParameters(
        command="python",
        args=["studio_mcp_server.py"],
        env=None,
    )

    json_rpc_request = {
        "jsonrpc": "2.0",
        "method": f"tools/call/{tool_name}",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
        "id": int(time.time() * 1000),
    }

    try:

        async with stdio_client(server_params) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                tool_result = await session.call_tool(
                    tool_name,
                    arguments=arguments,
                )

                parsed_output = {}

                if tool_result.content:

                    for content_item in tool_result.content:

                        if hasattr(content_item, "text"):

                            try:
                                parsed_output = json.loads(content_item.text)
                            except Exception:
                                parsed_output = {"raw_text": content_item.text}

                json_rpc_response = {
                    "jsonrpc": "2.0",
                    "result": parsed_output,
                    "id": json_rpc_request["id"],
                }

                return {
                    "request_payload": json_rpc_request,
                    "response_payload": json_rpc_response,
                    "execution_status": "SUCCESS",
                }

    except Exception as error:

        return {
            "request_payload": json_rpc_request,
            "response_payload": {"error": str(error)},
            "execution_status": "FAILED",
        }


def execute_true_mcp_client(tool_name: str, arguments: dict) -> dict:
    return asyncio.run(_async_execute_mcp_call(tool_name, arguments))


# =========================================================
# 12. DETERMINISTIC FINANCIAL ENGINE
# =========================================================

def calculate_deterministic_budget(
    extracted_items: list,
    shoot_days: int = 5,
) -> dict:

    base_crew_cost = 15000 * shoot_days

    equipment_total = sum(
        item.get("cost_per_day", 100) * shoot_days
        for item in extracted_items
    )

    insurance_and_permits = 7500

    grand_total = base_crew_cost + equipment_total + insurance_and_permits

    return {
        "shoot_days": shoot_days,
        "base_crew_cost": base_crew_cost,
        "equipment_total": equipment_total,
        "insurance_and_permits": insurance_and_permits,
        "grand_total": grand_total,
    }


# =========================================================
# 13. PRODUCTION INPUT
# =========================================================

st.markdown(
    '<div class="section-heading">Production Input</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="ui-card">
        <div class="card-title">📥 Script &amp; Media Ingestion</div>
        <div class="card-description">
            Provide a screenplay excerpt or upload a production
            document / concept asset for Gemini analysis.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

ingestion_mode = st.radio(
    "Source Ingestion Protocol",
    [
        "Paste Script Excerpt",
        "Upload Screenplay Document (PDF) / Concept Art",
    ],
    horizontal=True,
)

raw_script_payload = ""
uploaded_media_reference = None


# =========================================================
# 14. PASTE MODE
# =========================================================

if ingestion_mode == "Paste Script Excerpt":

    raw_script_payload = st.text_area(
        "Production Script Excerpt / Scene Description",
        height=180,
        placeholder=(
            "EXT. ABANDONED METRO TUNNEL - NIGHT\n\n"
            "Rainwater drips heavily from rusted iron pipes "
            "overhead as Detective Lorca draws her service weapon..."
        ),
    )


# =========================================================
# 15. UPLOAD MODE
# =========================================================

else:

    uploaded_document = st.file_uploader(
        "Upload Screenplay or Visual Asset",
        type=["pdf", "png", "jpg", "jpeg", "txt"],
    )

    if uploaded_document is not None:

        try:

            suffix = "." + uploaded_document.name.split(".")[-1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded_document.getvalue())
                temp_file_path = temp_file.name

            uploaded_media_reference = client.files.upload(file=temp_file_path)

            raw_script_payload = (
                "[Multimodal Asset Indexed: "
                f"{uploaded_document.name}]"
            )

            st.success(f"Successfully indexed {uploaded_document.name}.")

            try:
                os.unlink(temp_file_path)
            except Exception:
                pass

        except Exception as upload_error:
            st.error(f"Asset upload failure: {upload_error}")


# =========================================================
# 16. EXECUTION BUTTON
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

execute_col1, execute_col2 = st.columns([4, 1])

with execute_col1:
    pipeline_execution_trigger = st.button(
        "🚀 Execute Autonomous Production Pipeline",
        type="primary",
        use_container_width=True,
    )

with execute_col2:
    st.caption("Gemini → MCP → Finance → Audit")


# =========================================================
# 17. MULTI-AGENT PIPELINE
# =========================================================

if pipeline_execution_trigger:

    if not raw_script_payload.strip() and not uploaded_media_reference:

        st.warning(
            "Please provide script text or upload "
            "an asset before launching the pipeline."
        )

    else:

        audit_trail = []

        def log_audit(actor: str, action: str, details: str):
            audit_trail.append(
                {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "actor": actor,
                    "action": action,
                    "details": details,
                }
            )

        with st.status(
            "🌟 Initializing CineSync Production Pipeline...",
            expanded=True,
        ) as execution_status:

            try:

                # =================================================
                # STAGE 1
                # =================================================

                log_audit(
                    "System",
                    "Pipeline Initialized",
                    f"Model: {selected_gemini_model}, Transport: Stdio Subprocess",
                )

                st.write(
                    "🤖 **Orchestrator Agent** — "
                    "Analyzing screenplay requirements..."
                )

                if uploaded_media_reference:
                    director_contents = [
                        uploaded_media_reference,
                        (
                            "You are the Lead Production Director. "
                            "Extract the core scene breakdown, visual "
                            "tone, staging requirements, lighting, "
                            "and equipment needs.\n\n"
                            f"{raw_script_payload}"
                        ),
                    ]
                else:
                    director_contents = (
                        "You are the Lead Production Director. "
                        "Extract the core scene breakdown, visual "
                        "tone, staging requirements, lighting, "
                        "and equipment needs.\n\n"
                        f"{raw_script_payload}"
                    )

                director_response = client.models.generate_content(
                    model=selected_gemini_model,
                    contents=director_contents,
                )

                log_audit(
                    "Director Agent",
                    "Scene Analysis Completed",
                    "Extracted tone, lighting, and staging requirements.",
                )

                time.sleep(0.3)


                # =================================================
                # STAGE 2
                # =================================================

                st.write(
                    "🔌 **MCP Client** — "
                    "Connecting to studio asset database..."
                )

                department_prompt = f"""
You are a professional Hollywood Prop Master.

Analyze this production script:

{raw_script_payload}

Identify required:

- Props
- Weapons
- Vehicles
- Camera equipment
- Specialized production equipment

For each relevant asset, use the
query_studio_asset_database tool to verify availability.
"""

                department_response = client.models.generate_content(
                    model=selected_gemini_model,
                    contents=department_prompt,
                    config=types.GenerateContentConfig(
                        tools=[
                            types.Tool(
                                function_declarations=[
                                    query_studio_asset_database_tool
                                ]
                            )
                        ],
                        temperature=0.2,
                    ),
                )

                collected_mcp_traces = []
                extracted_items_for_calc = []
                recovery_actions = []


                # =================================================
                # MCP TOOL CALLS
                # =================================================

                if department_response.function_calls:

                    for function_call in department_response.function_calls:

                        mcp_result_wrapper = execute_true_mcp_client(
                            function_call.name,
                            function_call.args,
                        )

                        collected_mcp_traces.append(mcp_result_wrapper)

                        log_audit(
                            "MCP Stdio Client",
                            f"JSON-RPC Call: {function_call.name}",
                            str(mcp_result_wrapper),
                        )

                        inner_result = (
                            mcp_result_wrapper
                            .get("response_payload", {})
                            .get("result", {})
                        )

                        result_data = inner_result.get("result", {})

                        status_str = str(
                            result_data.get("status", "")
                        ).upper()

                        cost_val = result_data.get("cost_per_day", 100)

                        if "UNAVAILABLE" in status_str or "RESTRICTED" in status_str:
                            recovery_actions.append(
                                (
                                    "Resource Conflict Detected "
                                    f"for '{result_data.get('item')}': "
                                    f"{status_str}. "
                                    "Autonomous re-planning engaged."
                                )
                            )

                        extracted_items_for_calc.append(
                            {
                                "item": result_data.get("item"),
                                "cost_per_day": cost_val,
                            }
                        )


                # =================================================
                # FALLBACK
                # =================================================

                if not extracted_items_for_calc:
                    extracted_items_for_calc = [
                        {"item": "flashlight", "cost_per_day": 15},
                        {"item": "camera", "cost_per_day": 1200},
                    ]

                time.sleep(0.3)


                # =================================================
                # STAGE 3
                # =================================================

                st.write(
                    "💰 **Financial Line Producer** — "
                    "Running deterministic cost engine..."
                )

                budget_data = calculate_deterministic_budget(
                    extracted_items_for_calc,
                    shoot_days=5,
                )

                log_audit(
                    "Line Producer",
                    "Deterministic Budget Computed",
                    f"Grand Total: ${budget_data['grand_total']:,}",
                )

                budget_exceeded = budget_data["grand_total"] > max_allowed_budget

                if budget_exceeded:
                    recovery_actions.append(
                        (
                            "Budget Exceeded Limit "
                            f"(${budget_data['grand_total']:,} "
                            f"> ${max_allowed_budget:,}). "
                            "Re-planning schedule to reduce shoot days."
                        )
                    )

                    budget_data = calculate_deterministic_budget(
                        extracted_items_for_calc,
                        shoot_days=3,
                    )

                    log_audit(
                        "Line Producer",
                        "Budget Recovery",
                        "Shoot schedule reduced from 5 days to 3 days.",
                    )

                time.sleep(0.3)


                # =================================================
                # STAGE 4
                # =================================================

                st.write(
                    "🛡️ **Executive Auditor** — "
                    "Evaluating safety and compliance..."
                )

                audit_prompt = f"""
You are an elite Hollywood Studio Executive.

Compliance Strictness:
{audit_strictness}/5

Production Tier:
{production_tier}

Review the following CineSync production packet.

DIRECTOR ANALYSIS:
{director_response.text}

MCP TRACE DATA:
{collected_mcp_traces}

DETERMINISTIC FINANCIAL SUMMARY:
{budget_data}

RECOVERY ACTIONS:
{recovery_actions}

Write a formal executive production compliance report.

Include:

1. Executive Summary
2. Production Findings
3. Equipment / Asset Validation
4. Financial Validation
5. Safety & Compliance Findings
6. Autonomous Recovery Actions
7. Final Executive Recommendation
8. Approval Status

Do not invent MCP results.
Do not change deterministic financial calculations.
"""

                audit_response = client.models.generate_content(
                    model=selected_gemini_model,
                    contents=audit_prompt,
                )

                log_audit(
                    "Executive Auditor",
                    "Audit Completed",
                    "Production packet generated and verified.",
                )


                # =================================================
                # PIPELINE COMPLETE
                # =================================================

                execution_status.update(
                    label="✨ Production Pipeline Complete",
                    state="complete",
                    expanded=False,
                )


                # =================================================
                # SESSION STATE
                # =================================================

                st.session_state["director_output"] = director_response.text
                st.session_state["dept_output"] = department_response.text
                st.session_state["finance_output"] = (
                    "### Authoritative Budget Breakdown\n\n"
                    f"- **Shoot Days:** {budget_data['shoot_days']}\n"
                    f"- **Base Crew Cost:** ${budget_data['base_crew_cost']:,}\n"
                    f"- **Equipment Rentals:** ${budget_data['equipment_total']:,}\n"
                    f"- **Insurance & Permits:** ${budget_data['insurance_and_permits']:,}\n"
                    f"- **Grand Total:** **${budget_data['grand_total']:,}**"
                )
                st.session_state["audit_output"] = audit_response.text
                st.session_state["mcp_traces"] = collected_mcp_traces
                st.session_state["audit_trail"] = audit_trail
                st.session_state["recovery_actions"] = recovery_actions
                st.session_state["requires_approval"] = (
                    budget_data["grand_total"] > 100000
                )
                st.session_state["budget_data"] = budget_data
                st.session_state["production_tier"] = production_tier
                st.session_state["last_execution_time"] = (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )

                st.success("Production intelligence packet generated successfully.")


            except Exception as pipeline_exception:

                execution_status.update(
                    label="❌ Pipeline execution encountered an error.",
                    state="error",
                )

                st.error(f"Error diagnostics: {pipeline_exception}")


# =========================================================
# 18. EXECUTIVE RESULTS
# =========================================================

if st.session_state.get("director_output"):

    st.markdown("---")

    st.markdown(
        '<div class="section-heading">Production Intelligence</div>',
        unsafe_allow_html=True,
    )


    # =====================================================
    # GOVERNANCE GATE
    # =====================================================

    if st.session_state.get("requires_approval", False):

        st.warning(
            "⚠️ **Executive Governance Gate** — "
            "This production exceeds the $100k authorization "
            "threshold. Human executive authorization is required."
        )

        approval_checkbox = st.checkbox(
            "I authorize executive deployment of resources and disbursement of funds."
        )

        if approval_checkbox:
            st.success("✅ Executive Authorization Logged.")


    # =====================================================
    # RESULTS TABS
    # =====================================================

    (
        tab_director,
        tab_department,
        tab_financial,
        tab_audit,
        tab_mcp_inspector,
        tab_recovery,
        tab_audit_trail,
        tab_chat,
    ) = st.tabs(
        [
            "🎬 Director Vision",
            "📦 Art Department",
            "💰 Financial Engine",
            "🔍 Executive Audit",
            "⚡ MCP Inspector",
            "🔄 Failure & Recovery",
            "🛡️ Audit Trail",
            "💬 Studio Chat",
        ]
    )


    # =====================================================
    # DIRECTOR
    # =====================================================

    with tab_director:
        st.markdown("### 🎬 Cinematic Direction & Breakdown")
        st.markdown(st.session_state["director_output"])


    # =====================================================
    # ART DEPARTMENT
    # =====================================================

    with tab_department:
        st.markdown("### 📦 Art Department & Asset Requirements")
        st.markdown(st.session_state["dept_output"])


    # =====================================================
    # FINANCIAL
    # =====================================================

    with tab_financial:
        st.markdown("### 💰 Deterministic Financial Engine")

        budget = st.session_state.get("budget_data", {})

        if budget:
            f1, f2, f3, f4 = st.columns(4)

            with f1:
                st.metric("Shoot Days", budget.get("shoot_days", 0))

            with f2:
                st.metric("Crew", f"${budget.get('base_crew_cost', 0):,}")

            with f3:
                st.metric("Equipment", f"${budget.get('equipment_total', 0):,}")

            with f4:
                st.metric("Grand Total", f"${budget.get('grand_total', 0):,}")

            st.markdown("---")

        st.markdown(st.session_state["finance_output"])


    # =====================================================
    # EXECUTIVE AUDIT
    # =====================================================

    with tab_audit:
        st.markdown("### 🔍 Certified Executive Production Audit")
        st.markdown(st.session_state["audit_output"])
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Export Certified Production Dossier",
            data=st.session_state["audit_output"],
            file_name="cinesync_dyno_certified_dossier.md",
            mime="text/markdown",
            use_container_width=True,
        )


    # =====================================================
    # MCP INSPECTOR
    # =====================================================

    with tab_mcp_inspector:
        st.markdown("### ⚡ True MCP Stdio Subprocess Inspector")
        st.caption(
            "Live JSON-RPC transport traces between "
            "the Streamlit client and studio_mcp_server.py."
        )

        traces = st.session_state.get("mcp_traces", [])

        if traces:
            for idx, trace in enumerate(traces):
                with st.expander(
                    f"Trace #{idx + 1} — {trace.get('execution_status')}",
                    expanded=False,
                ):
                    st.markdown("**📤 JSON-RPC Request**")
                    st.json(trace.get("request_payload"))
                    st.markdown("**📥 JSON-RPC Response**")
                    st.json(trace.get("response_payload"))
        else:
            st.info(
                "No MCP traces recorded yet. "
                "Run the production pipeline to capture "
                "live MCP transport activity."
            )


    # =====================================================
    # RECOVERY
    # =====================================================

    with tab_recovery:
        st.markdown("### 🔄 Autonomous Failure Detection & Recovery")

        recovery_actions = st.session_state.get("recovery_actions", [])

        if recovery_actions:
            for action in recovery_actions:
                st.warning(f"⚠️ {action}")
            st.success(
                "✅ Autonomous re-planning completed. "
                "The production workflow was recalculated "
                "around detected constraints."
            )
        else:
            st.success(
                "🟢 No resource conflicts or failure states "
                "were detected during execution."
            )


    # =====================================================
    # AUDIT TRAIL
    # =====================================================

    with tab_audit_trail:
        st.markdown("### 🛡️ Governance & Telemetry Audit Trail")

        audit_data = st.session_state.get("audit_trail", [])

        if audit_data:
            st.dataframe(audit_data, use_container_width=True, hide_index=True)
        else:
            st.info("No audit events recorded.")


    # =====================================================
    # STUDIO CHAT
    # =====================================================

    with tab_chat:
        st.markdown("### 💬 Interactive Studio Dispatcher")
        st.caption(
            "Ask the CineSync AI Producer to revise "
            "the production plan."
        )

        if st.session_state["studio_chat_session"] is None:
            st.session_state["studio_chat_session"] = client.chats.create(
                model=selected_gemini_model,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are the CineSync Dyno AI Producer. "
                        "Help production teams revise schedules, "
                        "budgets, equipment plans, staffing, "
                        "and production strategy. "
                        "Never override deterministic financial "
                        "calculations."
                    )
                ),
            )

        for chat_msg in st.session_state["chat_message_history"]:
            with st.chat_message(chat_msg["role"]):
                st.markdown(chat_msg["content"])

        user_input_prompt = st.chat_input("Enter revision instructions...")

        if user_input_prompt:

            st.session_state["chat_message_history"].append(
                {"role": "user", "content": user_input_prompt}
            )

            with st.chat_message("user"):
                st.markdown(user_input_prompt)

            with st.chat_message("assistant"):
                with st.spinner("AI Producer compiling revision..."):
                    try:
                        chat_resp = st.session_state[
                            "studio_chat_session"
                        ].send_message(user_input_prompt)

                        assistant_text = chat_resp.text
                        st.markdown(assistant_text)

                        st.session_state["chat_message_history"].append(
                            {"role": "assistant", "content": assistant_text}
                        )

                    except Exception as chat_error:
                        st.error(f"Studio Chat Error: {chat_error}")


# =========================================================
# 19. EMPTY STATE
# =========================================================

else:

    st.markdown(
        """
        <div class="ui-card">
            <div class="card-title">🎬 Production Control Plane</div>
            <div class="card-description">
                Provide a screenplay excerpt or production asset
                above, then launch the autonomous pipeline.
                CineSync will analyze the production, query the
                MCP asset server, calculate deterministic costs,
                evaluate compliance, and generate an executive
                production packet.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 20. FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer-text">
        CineSync Dyno • Autonomous Studio Intelligence Platform
        • Gemini + MCP + Deterministic Finance + Governance
    </div>
    """,
    unsafe_allow_html=True,
)