import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DEEP RESEARCH · AI Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@500;700&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #cfd0d2;
}

.stApp {
    background: #050505;
    background-image: 
        radial-gradient(circle at 50% -20%, #1a1a2e 0%, transparent 70%),
        radial-gradient(circle at 0% 100%, #0d0d12 0%, transparent 50%);
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 5rem; max-width: 1400px; }

/* ── Hero header ── */
.hero {
    text-align: left;
    padding: 2rem 0 3rem;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #4f46e5;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -0.04em;
    color: #ffffff;
    margin: 0;
}
.hero h1 span {
    color: #4f46e5;
}

/* ── Layout Elements ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, #4f46e5 0%, rgba(79, 70, 229, 0) 100%);
    margin: 1rem 0 3rem;
    opacity: 0.3;
}

.input-container {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 1.5rem;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: all 0.3s ease;
}
.step-card.active {
    border-color: #4f46e5;
    background: rgba(79, 70, 229, 0.05);
}
.step-card.done {
    border-color: #10b981;
}

.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #6366f1;
}
.step-title {
    font-weight: 600;
    font-size: 0.9rem;
    color: #e5e7eb;
}

/* ── Buttons & Inputs ── */
.stButton > button {
    background: #4f46e5 !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    height: 3rem !important;
}

.stTextInput > div > div > input {
    background: #0f0f13 !important;
    border: 1px solid #27272a !important;
    color: white !important;
}

/* ── Result panels ── */
.report-panel {
    background: #0a0a0c;
    border: 1px solid #18181b;
    border-radius: 12px;
    padding: 3rem;
    line-height: 1.7;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}
</style>
""", unsafe_allow_html=True)

# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str):
    status_map = {
        "waiting": "○",
        "running": "◈",
        "done": "✓",
    }
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="step-num">PHASE {num}</div>
                <div class="step-title">{title}</div>
            </div>
            <div style="font-family: 'JetBrains Mono'; color: {'#4f46e5' if state=='running' else '#10b981' if state=='done' else '#3f3f46'}">
                {status_map.get(state)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "results" not in st.session_state: st.session_state.results = {}
if "running" not in st.session_state: st.session_state.running = False
if "done" not in st.session_state: st.session_state.done = False

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">NEURAL ENGINE v3.0</div>
    <h1>DEEP <span>RESEARCH</span></h1>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Layout ──────────────────────────────────────────────────────────────────
col_main, col_side = st.columns([7, 3], gap="large")

with col_side:
    st.markdown('<p style="font-family:JetBrains Mono; font-size:0.7rem; color:#4f46e5;">PIPELINE STATUS</p>', unsafe_allow_html=True)
    
    r = st.session_state.results
    
    def get_state(step_key):
        steps = ["search", "reader", "writer", "critic"]
        if step_key in r: return "done"
        if st.session_state.running:
            for s in steps:
                if s not in r: return "running" if s == step_key else "waiting"
        return "waiting"

    step_card("01", "Web Discovery", get_state("search"))
    step_card("02", "Deep Extraction", get_state("reader"))
    step_card("03", "Synthesis", get_state("writer"))
    step_card("04", "Verification", get_state("critic"))

with col_main:
    topic = st.text_input("RESEARCH QUERY", placeholder="Enter complex topic or technical hypothesis...", label_visibility="collapsed")
    run_btn = st.button("EXECUTE ANALYSIS", use_container_width=True)

    if run_btn and topic:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

    # ── Logic ──────────────────────────────────────────────────────────────
    if st.session_state.running and not st.session_state.done:
        curr_results = {}
        
        # 1. Search
        with st.status("Accessing Global Indices...", expanded=False) as status:
            search_agent = build_search_agent()
            sr = search_agent.invoke({"messages": [("user", f"Deep search: {topic}")]})
            curr_results["search"] = sr["messages"][-1].content
            st.session_state.results = dict(curr_results)
            status.update(label="Discovery Complete", state="complete")
        
        # 2. Reader
        with st.status("Analyzing Source Authority...", expanded=False) as status:
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({"messages": [("user", f"Extract core technical data for {topic} from: {curr_results['search'][:1000]}")]})
            curr_results["reader"] = rr["messages"][-1].content
            st.session_state.results = dict(curr_results)
            status.update(label="Extraction Complete", state="complete")

        # 3. Writer
        with st.status("Synthesizing Report...", expanded=False) as status:
            curr_results["writer"] = writer_chain.invoke({"topic": topic, "research": f"{curr_results['search']}\n{curr_results['reader']}"})
            st.session_state.results = dict(curr_results)
            status.update(label="Synthesis Complete", state="complete")

        # 4. Critic
        with st.status("Final Verification...", expanded=False) as status:
            curr_results["critic"] = critic_chain.invoke({"report": curr_results["writer"]})
            st.session_state.results = dict(curr_results)
            status.update(label="Verification Complete", state="complete")

        st.session_state.running = False
        st.session_state.done = True
        st.rerun()

# ── Display Results ───────────────────────────────────────────────────────────
if st.session_state.done:
    st.markdown('<div class="report-panel">', unsafe_allow_html=True)
    st.markdown(st.session_state.results.get("writer", ""))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    with st.expander("CRITIC REVIEW & LOGS"):
        st.markdown(st.session_state.results.get("critic", ""))
        st.code(st.session_state.results.get("search", ""), language="text")

    st.download_button("EXPORT RESEARCH", st.session_state.results.get("writer", ""), f"deep_research_{int(time.time())}.md")