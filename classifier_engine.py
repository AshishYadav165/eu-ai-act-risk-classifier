import json
from llm_router import get_claude_response, get_openai_response

RISK_TIERS = {
    'UNACCEPTABLE': {
        'color': '#c05050',
        'label': 'Unacceptable Risk',
        'description': 'Prohibited under EU AI Act Article 5. Cannot be placed on market.',
        'examples': [
            'Social scoring by public authorities',
            'Real-time remote biometric identification in public spaces',
            'AI exploiting vulnerabilities of specific groups',
            'Subliminal manipulation causing harm'
        ]
    },
    'HIGH': {
        'color': '#c87830',
        'label': 'High Risk',
        'description': 'Permitted subject to conformity assessment under EU AI Act Article 6 and Annex III.',
        'examples': [
            'AI as safety component of medical devices (MDR/IVDR)',
            'AI for diagnosis or prognosis of disease',
            'AI in critical infrastructure management',
            'AI for recruitment or employment decisions'
        ]
    },
    'LIMITED': {
        'color': '#c8b830',
        'label': 'Limited Risk',
        'description': 'Subject to transparency obligations under EU AI Act Articles 13-14.',
        'examples': [
            'Chatbots interacting with patients or users',
            'AI generating synthetic medical content',
            'Emotion recognition systems',
            'Deep fake generation systems'
        ]
    },
    'MINIMAL': {
        'color': '#4a8c4a',
        'label': 'Minimal Risk',
        'description': 'No specific obligations beyond general product safety requirements.',
        'examples': [
            'AI-powered administrative tools',
            'Spam filters',
            'AI in video games',
            'Inventory management AI'
        ]
    }
}

ANNEX_III_CATEGORIES = [
    'Biometric identification and categorisation',
    'Critical infrastructure management',
    'Education and vocational training',
    'Employment and worker management',
    'Access to essential services',
    'Law enforcement',
    'Migration and border control',
    'Administration of justice',
    'Medical devices and in vitro diagnostics',
    'Safety components of regulated products',
    'None of the above'
]

ISO_42001_CONTROLS = {
    'UNACCEPTABLE': [
        'ISO 42001 Cl.6.1: Risk assessment must document prohibition rationale',
        'ISO 42001 Cl.5.1: Leadership must formally prohibit deployment',
        'ISO 42001 Cl.8.1: Operational controls must prevent system activation',
        'Legal review required before any development activity'
    ],
    'HIGH': [
        'ISO 42001 Cl.6.1: Mandatory AI risk assessment and treatment plan',
        'ISO 42001 Cl.8.4: Conformity assessment documentation required',
        'ISO 42001 Cl.9.1: Continuous monitoring and performance evaluation',
        'ISO 42001 Cl.7.5: Documented information for full audit trail',
        'ISO 42001 Cl.5.3: Named accountability at C-suite level',
        'Post-market surveillance plan required (EU MDR Art.83 if applicable)',
        'Technical documentation per EU AI Act Annex IV'
    ],
    'LIMITED': [
        'ISO 42001 Cl.7.4: Transparency communication to affected persons',
        'ISO 42001 Cl.6.1: Risk assessment with transparency gap analysis',
        'ISO 42001 Cl.8.1: Operational controls for disclosure obligations',
        'EU AI Act Art.13: Clear disclosure that system is AI-generated',
        'ISO 42001 Cl.9.1: Monitor compliance with transparency obligations'
    ],
    'MINIMAL': [
        'ISO 42001 Cl.6.1: Basic risk assessment still recommended',
        'ISO 42001 Cl.9.1: Periodic review of risk classification',
        'General product safety requirements apply',
        'Document classification rationale for audit readiness'
    ]
}

SYSTEM_PROMPT = """You are an expert EU AI Act regulatory classifier with deep knowledge of:
- EU AI Act 2024/1689 including all Articles, Annexes, and recitals
- EU MDR/IVDR for medical device AI
- FDA SaMD classification framework
- ISO 42001:2023 AI Management Systems
- IMDRF AI/ML SaMD guidance

Classify AI use cases with the precision of a senior regulatory affairs professional 
who has submitted applications to both FDA and EMA. Be specific, cite exact Articles 
and Annex references, and flag jurisdiction-specific differences where relevant."""

def build_classification_prompt(use_case: str, sector: str, jurisdiction: str) -> str:
    return f"""Classify the following AI use case under the EU AI Act 2024/1689.

USE CASE DESCRIPTION:
{use_case}

SECTOR: {sector}
PRIMARY JURISDICTION: {jurisdiction}

Provide your classification in the following JSON format exactly:
{{
  "risk_tier": "UNACCEPTABLE|HIGH|LIMITED|MINIMAL",
  "confidence": "HIGH|MEDIUM|LOW",
  "primary_rationale": "2-3 sentence explanation citing specific EU AI Act Articles",
  "annex_iii_category": "Most relevant Annex III category or None",
  "article_references": ["List of specific EU AI Act Articles that apply"],
  "life_sciences_flags": ["Any specific FDA SaMD, EU MDR/IVDR, or ISO 13485 considerations"],
  "key_obligations": ["Top 3 most critical compliance obligations for this classification"],
  "jurisdiction_notes": "Any differences between EU, US FDA, or other jurisdiction requirements",
  "human_review_required": true
}}

Respond ONLY with valid JSON. No markdown, no preamble."""

def classify_use_case(use_case: str, sector: str, jurisdiction: str) -> tuple:
    prompt = build_classification_prompt(use_case, sector, jurisdiction)

    try:
        claude_raw = get_claude_response(prompt, system=SYSTEM_PROMPT)
        claude_clean = claude_raw.replace('```json', '').replace('```', '').strip()
        claude_result = json.loads(claude_clean)
    except Exception as e:
        claude_result = {
            'risk_tier': 'ERROR',
            'confidence': 'LOW',
            'primary_rationale': f'Claude classification failed: {str(e)}',
            'annex_iii_category': 'Unknown',
            'article_references': [],
            'life_sciences_flags': [],
            'key_obligations': [],
            'jurisdiction_notes': '',
            'human_review_required': True
        }

    try:
        openai_raw = get_openai_response(prompt, system=SYSTEM_PROMPT)
        openai_clean = openai_raw.replace('```json', '').replace('```', '').strip()
        openai_result = json.loads(openai_clean)
    except Exception as e:
        openai_result = {
            'risk_tier': 'ERROR',
            'confidence': 'LOW',
            'primary_rationale': f'GPT-4o-mini classification failed: {str(e)}',
            'annex_iii_category': 'Unknown',
            'article_references': [],
            'life_sciences_flags': [],
            'key_obligations': [],
            'jurisdiction_notes': '',
            'human_review_required': True
        }

    agreement = claude_result.get('risk_tier') == openai_result.get('risk_tier')
    return claude_result, openai_result, agreement

def get_tier_info(tier: str) -> dict:
    return RISK_TIERS.get(tier, RISK_TIERS['MINIMAL'])

def get_iso_controls(tier: str) -> list:
    return ISO_42001_CONTROLS.get(tier, ISO_42001_CONTROLS['MINIMAL'])
