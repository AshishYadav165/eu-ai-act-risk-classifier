# EU AI Act Risk Classifier — Life Sciences & Digital Health Edition

**Dual-model AI use case classification against the EU AI Act 2024/1689 risk framework — running Anthropic Claude and OpenAI GPT-4o-mini independently and comparing results. Built specifically for life sciences, pharma, medical devices, CDx, and digital health contexts.**

---

## Overview

This tool classifies AI use cases against the EU AI Act 2024/1689 risk tiers using two independent LLM models simultaneously. Where models agree, classification confidence is high. Where they disagree, the tool flags the divergence and recommends expert review — demonstrating that AI classification of regulatory risk should never rely on a single model.

The dual-model comparison approach is the key technical differentiator of this tool. It is also a governance principle: regulatory classifications with direct compliance implications require independent verification.

---

## Four EU AI Act Risk Tiers

| Tier | EU AI Act Reference | Life Sciences Examples |
|------|-------------------|----------------------|
| Unacceptable Risk | Article 5 | Prohibited — cannot be placed on market |
| High Risk | Article 6 + Annex III | AI in MDR/IVDR devices, CDx, clinical decision support |
| Limited Risk | Articles 13–14 | Patient-facing chatbots, synthetic medical content |
| Minimal Risk | General safety requirements | Administrative AI, scheduling tools |

---

## What the Tool Produces

- **Dual classification** — Anthropic Claude Haiku + OpenAI GPT-4o-mini run independently
- **Agreement indicator** — flags where models diverge, triggering expert review recommendation
- **Annex III category mapping** — specific category from EU AI Act Annex III
- **Applicable Articles** — exact EU AI Act Articles triggered by the use case
- **Life Sciences flags** — FDA SaMD, EU MDR/IVDR, ISO 13485, IMDRF considerations
- **Jurisdiction comparison** — EU vs US FDA regulatory differences for the same use case
- **ISO 42001 control requirements** — mandatory controls for the classified risk tier
- **Key compliance obligations** — top 3 board-level actions required
- **Exportable classification report** — plain text for regulatory documentation

---

## Architecture
```
User Input (use case description + sector + jurisdiction)
→ Streamlit interface
→ classifier_engine.py (prompt construction + classification logic)
→ Anthropic Claude Haiku (classification 1)
→ OpenAI GPT-4o-mini (classification 2)
→ Agreement analysis
→ ISO 42001 control mapping
→ audit_log.py (JSONL audit trail)
→ Results: dual classification + regulatory detail + controls
```

---

## Technology Stack

- **LLM 1:** Anthropic Claude Haiku — regulatory comprehension and Article citation
- **LLM 2:** OpenAI GPT-4o-mini — independent classification for comparison
- **Interface:** Streamlit
- **Audit logging:** JSON Lines with SHA-256 use case hashing
- **Frameworks:** EU AI Act 2024/1689 · EU MDR/IVDR · FDA SaMD · ISO 42001:2023 · ISO 13485 · IMDRF AI/ML SaMD

---

## Setup

**1. Clone and set up environment**
```bash
git clone https://github.com/AshishYadav165/eu-ai-act-risk-classifier.git
cd eu-ai-act-risk-classifier
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

**2. Configure API keys**
```bash
cp .env.example .env
# Add your Anthropic and OpenAI API keys
```

**3. Run**
```bash
python -m streamlit run app.py
```

---

## Example Classification

**Input:** AI algorithm embedded in a CE-marked IVD device analysing blood biomarkers to predict oncology treatment response, used by oncologists to guide treatment selection.

**Result:** Both models classify as **HIGH RISK** (HIGH confidence) — Article 6(2), Annex III Point 5(a), concurrent EU MDR/IVDR and EU AI Act obligations, parallel FDA SaMD pathway analysis.

---

## Governance Design

Every classification includes a mandatory human review notice. The dual-model architecture is itself a governance control — disagreement between models is surfaced explicitly rather than hidden. All classifications are logged with timestamps and SHA-256 hashed use case descriptions for audit trail purposes.

---

## Regulatory Context

- **EU AI Act:** Tool itself is limited-risk — transparency obligations apply
- **FDA:** Does not meet the definition of a medical device
- **HIPAA:** No patient data processed — use case descriptions only
- **ISO 42001:** Audit logging and human review requirements aligned to AI management system principles

---

## Related Portfolio Projects

- **[Regulatory Intelligence RAG Assistant](https://github.com/AshishYadav165/regulatory-intelligence-assistant)** — AI-powered Q&A over FDA guidance, EU AI Act, ISO 42001, NIST AI RMF
- **[AI Governance Readiness Assessment Tool](https://github.com/AshishYadav165/ai-governance-readiness-tool)** — Executive-level governance maturity diagnostic (production version powers SIGFOC™)

---

## Author

**Ashish Yadav** | Senior Life Sciences Executive | AI Strategy & Governance
Dual ISO Lead Auditor: ISO 42001 (AI Management Systems) · ISO 13485 (Medical Devices QMS)
Founder, PrecisionPulse Consulting LLC
[precisionpulseconsulting.com](https://precisionpulseconsulting.com) · [ashish-yadav.com](https://ashish-yadav.com)
