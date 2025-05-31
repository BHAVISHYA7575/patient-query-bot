from transformers import pipeline
import sqlite3

# Initialize database connection
conn = sqlite3.connect("patient_queries.db")
cursor = conn.cursor()

# Ensure table exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        response TEXT NOT NULL,
        category TEXT
    )
''')
conn.commit()

# Initialize distilgpt2 model
try:
    generator = pipeline("text-generation", model="distilgpt2")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Simplified few-shot prompt
def create_prompt(query):
    return f"""You are a medical assistant bot. Respond concisely to patient FAQs:

Q: What documents do I need for a clinic visit?
A: Valid ID, insurance card, medical records, referral letter (if needed).

Q: How should I take my prescribed medication?
A: Follow your doctor's dosage and timing instructions. Take with food or water if specified. Contact your pharmacist for clarification.

Q: What's the next step after booking an appointment?
A: You'll get a confirmation email with details. Arrive 15 minutes early with documents.

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

# Process query and store in database
def process_query(query):
    is_valid, error_msg = validate_query(query)
    if not is_valid:
        return f"Error: {error_msg}"
    
    try:
        prompt = create_prompt(query)
        response = generator(prompt, max_new_tokens=30, truncation=True, pad_token_id=50256)[0]["generated_text"]
        # Extract response after "A: "
        response_text = response.split("A: ")[-1].strip() if "A: " in response else "Sorry, I couldn't generate a valid response."
        # Keep only first sentence and remove non-ASCII characters
        response_text = response_text.split('.')[0] + '.' if '.' in response_text else response_text
        response_text = ''.join(c for c in response_text if ord(c) < 128)  # Remove non-ASCII characters
        if not response_text.strip():
            response_text = "Sorry, I couldn't generate a valid response."
        
        category = get_category(query)
        cursor.execute("INSERT INTO queries (query, response, category) VALUES (?, ?, ?)",
                      (query, response_text, category))
        conn.commit()
        
        return response_text
    except Exception as e:
        return f"Error processing query: {str(e)}"

# Test the bot and save outputs
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
        print(f"\nQuery: {query}")
        print(f"Response: {response.encode('ascii', 'ignore').decode('ascii')}")
    
    # Save outputs to query_outputs.txt with UTF-8 encoding
    with open("query_outputs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(outputs))
except Exception as e:
    print(f"Error during testing: {str(e)}")
finally:
    conn.close()