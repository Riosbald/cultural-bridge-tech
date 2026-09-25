"""
Cultural Bridge Tech – Streamlit Dashboard (MVP)
Matches the designed screens: Analysis, Adversarial Tester, Steering notes.
"""

import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Cultural Bridge Tech",
    page_icon="\U0001f309",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Cultural Bridge Tech")
st.caption("MVP \u00b7 Cross-lingual deception detection (Mock SAE layer) \u00b7 African language stress test")

# Sidebar
with st.sidebar:
    st.header("Input")
    language = st.selectbox(
        "Language",
        options=["yoruba", "hausa", "igbo", "english"],
        index=0
    )
    prompt = st.text_area(
        "Prompt",
        height=180,
        placeholder="Enter a query that might trigger translation-layer behaviour..."
    )
    analyze_btn = st.button("Analyze", type="primary", use_container_width=True)
    st.divider()
    st.markdown("**Mode**")
    st.info("Current SAE layer is **MOCK**. Real GemmaScope / SAELens integration is the next step.")
    st.markdown("---")
    st.caption("Protocol: HUMAN\u2013AI MULTI-LANE v2.0 \u00b7 Option B Prototype First")

# Main area
tab1, tab2, tab3 = st.tabs(["Analysis Dashboard", "Adversarial Robustness", "Steering & Notes"])

def call_analyze(prompt: str, language: str):
    try:
        r = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"prompt": prompt, "language": language},
            timeout=15
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"Backend error: {e}")
        return None

if analyze_btn and prompt.strip():
    with st.spinner("Running analysis (mock SAE)..."):
        result = call_analyze(prompt, language)
        if result:
            st.session_state["last_result"] = result
            st.session_state["last_prompt"] = prompt
            st.session_state["last_language"] = language

result = st.session_state.get("last_result")

with tab1:
    if not result:
        st.info("Enter a prompt and click **Analyze** to see D6 / D3 style scores and layer summary.")
    else:
        st.subheader("Deception Scores")
        scores = result["deception_scores"]
        cols = st.columns(4)
        cols[0].metric("D6 Capability", f"{scores['D6_capability']:.3f}")
        cols[1].metric("D3 Context", f"{scores['D3_context']:.3f}")
        cols[2].metric("D2 Confidence", f"{scores['D2_confidence']:.3f}")
        cols[3].metric("D1 False Conf.", f"{scores['D1_false_confidence']:.3f}")

        st.subheader("Layer Summary")
        layer = result["layer_summary"]
        fig = go.Figure(data=[
            go.Bar(
                x=["Bottom (lang identity)", "Middle (English dominance)", "Generation (confidence)"],
                y=[
                    layer["bottom_language_activation"],
                    layer["middle_english_dominance"],
                    layer["generation_confidence"]
                ],
                marker_color=["#2ecc71", "#e74c3c", "#3498db"]
            )
        ])
        fig.update_layout(yaxis_title="Activation / Dominance", height=350, margin=dict(t=20))
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top Features")
        for f in result["top_features"]:
            st.markdown(f"**{f['name']}** (`{f['layer']}`) \u2014 activation {f['activation']}  \n*{f['role']}*")

        st.caption(f"Provenance: {result['provenance']}")
        st.json({"language_detected": result["language_detected"], "is_low_resource": result["is_low_resource"]})

with tab2:
    if not result:
        st.info("Run an analysis first to see adversarial variants and robustness deltas.")
    else:
        st.subheader("Adversarial Variants")
        for v in result.get("adversarial_variants", []):
            with st.expander(f"{v['type']} \u2014 {v['description']}"):
                st.code(v["text"], language=None)

        st.subheader("Robustness (D6 delta)")
        rob = result.get("robustness", {})
        st.metric("Mean D6 delta across variants", f"{rob.get('mean_d6_delta', 0):.3f}")
        if rob.get("details"):
            df = pd.DataFrame(rob["details"])
            st.dataframe(df, use_container_width=True)

with tab3:
    if not result:
        st.info("Run an analysis to see steering recommendation.")
    else:
        rec = result.get("steering_recommendation", {})
        st.subheader("Steering Recommendation")
        st.write(f"**Action:** `{rec.get('action')}`")
        st.write(rec.get("note", ""))
        if rec.get("target_features"):
            st.write("Target features:", ", ".join(rec["target_features"]))

        st.divider()
        st.markdown("""
        ### Design Intent (from prior architecture)
        - **D6**: Low language-specific activation at bottom layers + high output confidence \u2192 capability misrepresentation.
        - **D3**: English-token / English-reasoning dominance in middle layers while user interacts in African language \u2192 context misrepresentation.
        - Real system will clamp or offset the corresponding SAE features and optionally insert explicit uncertainty disclosure before the English-reasoning phase.
        """)

st.divider()
st.caption("Cultural Bridge Tech MVP \u00b7 Mock SAE layer \u00b7 Ready for real GemmaScope / SAELens replacement")
