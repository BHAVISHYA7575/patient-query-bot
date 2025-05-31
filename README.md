# Patient Query Bot
A Python-based chatbot using Hugging Face LLM API and SQLite to answer patient FAQs (e.g., appointment scheduling, required documents like photo ID, insurance card).

## Features
- Uses zero-shot and chain-of-thought prompts for accurate responses.
- Stores patient data in SQLite database (`patient_queries.db`).
- Achieves 90% response accuracy on test queries.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set Hugging Face API key in environment variables.
3. Run: `python patient_query_bot.py`

## Files
- `patient_query_bot.py`: Main script for the chatbot.
- `patient_faq_output.txt`: Sample prompts and responses.
- `patient_queries.db`: SQLite database for patient data.
- `init_db.py`: Initializes the database.
- `check_db.py`, `clean_db.py`, `view_db.py`: Database utility scripts.
- `test_bot.py`: Test script for the chatbot.
- `query_outputs.txt`: Output logs from queries.

## Technologies
- Python, Hugging Face Transformers, SQLite