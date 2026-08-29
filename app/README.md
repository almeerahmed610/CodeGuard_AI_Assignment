# 🛡️ CodeGuard AI — Sequential Multi-Agent Code Auditor

This implementation follows the supplied assignment brief.

## Pipeline
**Scanner Agent → Refactor Agent → Docs Agent**

## Features
- Automated scanning
- Security and bug findings
- PEP8 recommendations
- Automatic refactoring
- Auto-generated documentation
- Streamlit live pipeline tracking
- Typed LangGraph state
- Google Gemini via LangChain

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Run:
```bash
streamlit run app.py
```

## Architecture
User Code → Scanner → Audit Report → Refactor → Clean Code → Docs → README
