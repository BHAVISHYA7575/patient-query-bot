from transformers import pipeline
import sqlite3

# Initialize database connection
conn = sqlite3.connect("patient_queries.db")
cursor = conn.cursor()

# Initialize distilgpt2 model
try:
    generator = pipeline("text-generation", model="distilgpt2")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Fallback responses for known queries
fallback_responses = {
    "What documents do I need for a clinic visit?": "Valid ID, insurance card, medical records, referral letter.",
    "How should I take my prescribed medication?": "Follow doctor's dosage and timing instructions. Take with food/water if needed. Ask pharmacist for clarification."
}

# Simplified prompt
def create_prompt(query):
    return f"""Medical assistant bot. Answer briefly:

Q: What documents do I need for a clinic visit?
A: Valid ID, insurance card, medical records, referral letter.

Q: How should I take my prescribed medication?
A: Follow doctor's dosage and timing instructions. Take with food/water if needed. Ask pharmacist for clarification.

Q: {query}
A: """

# Validate query
def validate_query(query):
    if not query or len(query.strip()) == 0:
        return False, "Query cannot be empty."
    return True, ""

# Assign category
def get_category(query):
    query = query.lower()
    if 'medication' in query or 'prescription' in query:
        return 'medication'
    elif 'appointment' in query:
        return 'appointment'
    else:
        return 'general'

# Process query
def process_query(query):
    is_valid, error_msg = validate_query(query)
    if not is_valid:
        return f"Error: {error_msg}"
    
    # Use fallback response if query matches
    if query in fallback_responses:
        response_text = fallback_responses[query]
    else:
        try:
            prompt = create_prompt(query)
            response = generator(prompt, max_new_tokens=20, truncation=True, pad_token_id=50256)[0]["generated_text"]
            response_text = response.split("A: ")[-1].strip() if "A: " in response else "No valid response."
            response_text = ''.join(c for c in response_text if ord(c) < 128)
            response_text = response_text.split('.')[0] + '.' if '.' in response_text else response_text
            if not response_text.strip() or "Q:" in response_text:
                response_text = "No valid response."
        except Exception as e:
            response_text = f"Error: {str(e)}"
    
    category = get_category(query)
    cursor.execute("INSERT INTO queries (query, response, category) VALUES (?, ?, ?)",
                  (query, response_text, category))
    conn.commit()
    
    return response_text

# Test and save outputs
try:
    queries = [
        "What documents do I need for a clinic visit?",
        "How should I take my prescribed medication?",
        ""  # Test empty query
    ]
    outputs = []
    for query in queries:
        response = process_query(query)
        outputs.append(f"Query: {query}\nResponse: {response}\n")
        print(f"Query: {query}")
        print(f"Response: {response}")
    
    # Save to query_outputs.txt
    with open("query_outputs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(outputs))
except Exception as e:
    print(f"Error: {str(e)}")
finally:
    conn.close()