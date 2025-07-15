```markdown
# PII-detector-tr

A Python-based PII detection and anonymization tool for Turkish, featuring a Streamlit UI and Microsoft Presidio Analyzer & Anonymizer. ([GitHub](https://github.com/delos0/PII-detector-tr), [GitHub](https://github.com/delos0/PII-detector-tr/raw/main/requirements.txt))

## Features

- Detects Turkish PII (e.g., T.C. Kimlik No, phone numbers, emails) with custom Presidio recognizers  
- Supports anonymization via Presidio Anonymizer  
- Interactive Streamlit web app with real-time highlighting  

## Installation

```bash
git clone https://github.com/delos0/PII-detector-tr.git
cd PII-detector-tr
pip install -r requirements.txt
``` ([GitHub](https://github.com/delos0/PII-detector-tr/raw/main/requirements.txt))

## Usage

```bash
streamlit run src/app.py
```

Open http://localhost:8501 to start detecting and redacting PII in Turkish text.  
```
