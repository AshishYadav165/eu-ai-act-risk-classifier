import streamlit as st
import uuid
from datetime import date
from classifier_engine import (
    classify_use_case, get_tier_info, get_iso_controls,
    RISK_TIERS, ANNEX_III_CATEGORIES
)
from audit_log import log_classification

st.set_page_config(
    page_title='EU AI Act Risk Classifier — Life Sciences',
    page_icon='⚖',
    layout='wide'
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400&family=IBM+Plex+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; font-weight: 300; }
.stApp { background-color: #0d0d0d; color: #e8e4dc; }
h1, h2, h3 { font-family: 'IBM Plex Sans', sans-serif !important; font-weight: 400 !important; }
.risk-badge { display:inline-block; padding:6px 16px; border-radius:3px; font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:0.12em; text-transform:uppercase; font-weight:400; margin-bottom:12px; }
.model-card { background:#1a1a1a; border:1px solid rgba(255,255,255,0.08); border-radius:4px; padding:20px; margin-bottom:12px; }
.agree-badge { background:rgba(74,140,74,0.15); border:1px solid #4a8c4a; color:#4a8c4a; padding:4px 12px; border-radius:2px; font-family:'IBM Plex Mono',monospace; font-size:10px; letter-spacing:0.1em; text-transform:uppercase; }
.disagree-badge { background:rgba(192,80,80,0.15); border:1px solid #c05050; color:#c05050; padding:4px 12px; border-radius:2px; font-family:'IBM Plex Mono',monospace; font-size:10px; letter-spacing:0.1em; text-transform:uppercase; }
.governance-notice { background:rgba(184,115,51,0.08); border:1px solid rgba(184,115,51,0.3); border-radius:4px; padding:12px 16px; font-size:12px; color:rgba(232,228,220,0.6); margin-bottom:24px; }
.iso-control { background:#111; border-left:2px solid #b87333; padding:8px 12px; margin-bottom:6px; font-size:12px; font-family:'IBM Plex Mono',monospace; color:rgba(232,228,220,0.7); }
</style>
""", unsafe_allow_html=True)

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if 'results' not in st.session_state:
    st.session_state.results = None

SECTORS = [
    'Life Sciences / Pharma',
    'Medical Devices / SaMD',
    'In Vitro Diagnostics / CDx',
    'Digital Health / MHealth',
    'Clinical Research / CRO',
    'Hospital / Health System',
    'Insurance / Payer',
    'Other Healthcare',
    'Financial Services',
    'Other'
]

JURISDICTIONS = [
    'European Union (EU AI Act primary)',
    'United States (FDA primary)',
    'Both EU and US',
    'United Kingdom',
    'Global / Multiple'
]

st.markdown("## ⚖ EU AI Act Risk Classifier")
st.markdown("##### Life Sciences & Digital Health Edition · Claude + GPT-4o-mini Dual Classification")

st.markdown("""
<div class="governance-notice">
This tool classifies AI use cases against the EU AI Act 2024/1689 risk framework using two independent 
LLM models — Anthropic Claude and OpenAI GPT-4o-mini. Where models disagree, human expert review 
is strongly recommended. All classifications require verification by a qualified regulatory professional 
before use in any regulatory submission or compliance programme.<br><br>
Built by <strong>Ashish Yadav</strong> · Dual ISO Lead Auditor (ISO 42001 · ISO 13485) · 
<a href="https://precisionpulseconsulting.com" style="color:#b87333;">PrecisionPulse Consulting LLC</a>
</div>
""", unsafe_allow_html=True)

with st.expander("EU AI Act Risk Tier Reference", expanded=False):
    cols = st.columns(4)
    for i, (tier, info) in enumerate(RISK_TIERS.items()):
        with cols[i]:
            st.markdown(f"<span class='risk-badge' style='background:rgba(0,0,0,0.3);border:1px solid {info['color']};color:{info['color']}'>{info['label']}</span>", unsafe_allow_html=True)
            st.caption(info['description'])
            for ex in info['examples']:
                st.markdown(f"- {ex}")

st.divider()
st.markdown("### Describe Your AI Use Case")

col1, col2 = st.columns([2, 1])
with col1:
    use_case = st.text_area(
        'AI use case description',
        height=160,
        placeholder='Describe the AI system in detail — its intended purpose, how it works, who uses it, what decisions it influences, and the clinical or business context. The more detail you provide, the more accurate the classification.',
        label_visibility='collapsed'
    )
with col2:
    sector = st.selectbox('Sector', SECTORS)
    jurisdiction = st.selectbox('Primary Jurisdiction', JURISDICTIONS)
    st.markdown("")
    classify_btn = st.button('Classify Use Case →', type='primary', use_container_width=True)

if classify_btn and use_case.strip():
    with st.spinner('Running dual-model classification — Claude + GPT-4o-mini…'):
        claude_result, openai_result, agreement = classify_use_case(
            use_case, sector, jurisdiction
        )
        log_classification(
            st.session_state.session_id,
            use_case,
            claude_result,
            openai_result,
            agreement
        )
        st.session_state.results = {
            'claude': claude_result,
            'openai': openai_result,
            'agreement': agreement,
            'use_case': use_case,
            'sector': sector,
            'jurisdiction': jurisdiction
        }

elif classify_btn and not use_case.strip():
    st.warning('Please describe your AI use case before classifying.')

if st.session_state.results:
    r = st.session_state.results
    claude = r['claude']
    openai = r['openai']
    agreement = r['agreement']

    st.divider()
    st.markdown("### Classification Results")

    agree_html = "<span class='agree-badge'>✓ Models Agree</span>" if agreement else "<span class='disagree-badge'>⚠ Models Disagree — Expert Review Required</span>"
    st.markdown(agree_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        claude_tier = claude.get('risk_tier', 'MINIMAL')
        claude_info = get_tier_info(claude_tier)
        st.markdown(f"""
<div class="model-card">
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:rgba(232,228,220,0.4);letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px">Anthropic Claude Haiku</div>
  <span class="risk-badge" style="background:rgba(0,0,0,0.3);border:1px solid {claude_info['color']};color:{claude_info['color']}">{claude_info['label']}</span>
  <div style="font-size:11px;color:rgba(232,228,220,0.4);font-family:'IBM Plex Mono',monospace;margin-bottom:10px">Confidence: {claude.get('confidence','—')}</div>
  <div style="font-size:13px;line-height:1.7;color:rgba(232,228,220,0.7)">{claude.get('primary_rationale','—')}</div>
</div>
""", unsafe_allow_html=True)

    with col2:
        openai_tier = openai.get('risk_tier', 'MINIMAL')
        openai_info = get_tier_info(openai_tier)
        st.markdown(f"""
<div class="model-card">
  <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:rgba(232,228,220,0.4);letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px">OpenAI GPT-4o-mini</div>
  <span class="risk-badge" style="background:rgba(0,0,0,0.3);border:1px solid {openai_info['color']};color:{openai_info['color']}">{openai_info['label']}</span>
  <div style="font-size:11px;color:rgba(232,228,220,0.4);font-family:'IBM Plex Mono',monospace;margin-bottom:10px">Confidence: {openai.get('confidence','—')}</div>
  <div style="font-size:13px;line-height:1.7;color:rgba(232,228,220,0.7)">{openai.get('primary_rationale','—')}</div>
</div>
""", unsafe_allow_html=True)

    primary_tier = claude_tier if agreement else claude_tier
    primary_info = get_tier_info(primary_tier)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Regulatory Detail")
        annex = claude.get('annex_iii_category', '—')
        st.markdown(f"**Annex III Category:** {annex}")
        articles = claude.get('article_references', [])
        if articles:
            st.markdown("**Applicable Articles:**")
            for a in articles:
                st.markdown(f"- {a}")
        ls_flags = claude.get('life_sciences_flags', [])
        if ls_flags:
            st.markdown("**Life Sciences Flags:**")
            for f in ls_flags:
                st.markdown(f"- {f}")
        jn = claude.get('jurisdiction_notes', '')
        if jn:
            st.markdown(f"**Jurisdiction Notes:** {jn}")

    with col2:
        st.markdown("#### Key Compliance Obligations")
        obligations = claude.get('key_obligations', [])
        for ob in obligations:
            st.markdown(f"- {ob}")

    st.divider()
    st.markdown("#### ISO 42001 Control Requirements")
    st.caption(f"Required controls for {primary_info['label']} classification")
    controls = get_iso_controls(primary_tier)
    for control in controls:
        st.markdown(f"<div class='iso-control'>{control}</div>", unsafe_allow_html=True)

    if not agreement:
        st.divider()
        st.error("""**Model Disagreement — Expert Review Required**

Claude and GPT-4o-mini have classified this use case differently. This divergence typically indicates:
- The use case sits on a boundary between risk tiers
- Additional context is needed for accurate classification
- The description may be interpreted differently under different regulatory frameworks

**Recommended action:** Submit this use case for review by a qualified EU AI Act regulatory expert before proceeding with any compliance programme or regulatory submission.""")

    st.divider()

    report = f"""EU AI ACT RISK CLASSIFICATION REPORT
Life Sciences & Digital Health Edition
© 2025 Ashish Yadav · PrecisionPulse Consulting LLC
https://precisionpulseconsulting.com

Date: {date.today().strftime('%d %B %Y')}
Session: {st.session_state.session_id}
Sector: {r['sector']}
Jurisdiction: {r['jurisdiction']}

USE CASE DESCRIPTION:
{r['use_case']}

CLASSIFICATION RESULTS
{'─' * 40}
Claude (Anthropic): {claude_tier} — Confidence: {claude.get('confidence','—')}
GPT-4o-mini (OpenAI): {openai_tier} — Confidence: {openai.get('confidence','—')}
Models Agree: {'Yes' if agreement else 'No — Expert Review Required'}

PRIMARY RATIONALE (Claude):
{claude.get('primary_rationale','—')}

ANNEX III CATEGORY: {claude.get('annex_iii_category','—')}
ARTICLE REFERENCES: {', '.join(claude.get('article_references',[]))}

LIFE SCIENCES FLAGS:
{chr(10).join('- ' + f for f in claude.get('life_sciences_flags',[]))}

KEY OBLIGATIONS:
{chr(10).join('- ' + o for o in claude.get('key_obligations',[]))}

ISO 42001 CONTROLS REQUIRED:
{chr(10).join('- ' + c for c in get_iso_controls(primary_tier))}

JURISDICTION NOTES:
{claude.get('jurisdiction_notes','—')}

HUMAN REVIEW REQUIRED before use in any regulatory submission or compliance programme.

GITHUB: https://github.com/AshishYadav165/eu-ai-act-risk-classifier
"""

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            'Export Classification Report',
            data=report,
            file_name=f'EU_AI_Act_Classification_{date.today()}.txt',
            mime='text/plain'
        )
    with col2:
        if st.button('Classify Another Use Case'):
            st.session_state.results = None
            st.rerun()

    st.markdown("""
---
*EU AI Act Risk Classifier · Life Sciences & Digital Health Edition*
*© 2025 Ashish Yadav · [PrecisionPulse Consulting LLC](https://precisionpulseconsulting.com) · [ashish-yadav.com](https://ashish-yadav.com)*
*Dual-model classification: Anthropic Claude + OpenAI GPT-4o-mini*
*[View on GitHub](https://github.com/AshishYadav165/eu-ai-act-risk-classifier)*
""")
