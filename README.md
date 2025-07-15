# PII-detector-tr

A Python-based PII detection and anonymization tool for Turkish, featuring a Streamlit UI and Microsoft Presidio Analyzer & Anonymizer.

<img width="1909" height="873" alt="Untitled5" src="https://github.com/user-attachments/assets/cdc01c47-d7be-46ae-bf00-5831e968deef" />

## Features

- Detects Turkish PII (e.g., T.C. Kimlik No, Phone numbers, Emails, Credit Card number, Address, Names and Surnames) with custom Presidio recognizers
- Supports anonymization via Presidio Anonymizer  
- Interactive Streamlit web app with real-time masking/redacting
- Displays analysis for findings and condifence scores

## Installation

```bash
git clone https://github.com/delos0/PII-detector-tr.git
cd PII-detector-tr
pip install -r requirements.txt

## Usage

```bash
streamlit run src/main.py
```

Open http://localhost:8501 to start detecting and redacting PII in Turkish text.  
