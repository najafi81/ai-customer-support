import os
import pandas as pd
from dotenv import load_dotenv
import openai
from datetime import datetime

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

FAQ_FILE = "data/faq.csv"
LOG_FILE = "logs/conversations.csv"

# Load FAQ
faq_df = pd.read_csv(FAQ_FILE)

def match_faq(user_question):
    """Try to match question in FAQ."""
    for _, row in faq_df.iterrows():
        if row['question'].lower() in user_question.lower():
            return row['response']
    return None

def get_ai_response(user_question):
    """Get AI-generated response or fallback."""
    faq_answer = match_faq(user_question)
    if faq_answer:
        return faq_answer
    # For complex question, refer to human
    if len(user_question.split()) > 20:  # example threshold
        return "Your question is complex. Please contact support@example.com"
    # Mock AI for other
    return f"Mock AI response to: {user_question}"

def save_conversation(user_question, answer):
    """Save conversation to CSV."""
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=["timestamp","question","answer"])
    else:
        df = pd.read_csv(LOG_FILE)
    df = pd.concat([df, pd.DataFrame([{
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "question": user_question,
        "answer": answer
    }])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)

def main():
    print("AI Customer Support Agent started. Type 'exit' to quit.")
    while True:
        question = input("User: ")
        if question.lower() == "exit":
            break
        answer = get_ai_response(question)
        print(f"Agent: {answer}")
        save_conversation(question, answer)

if __name__ == "__main__":
    main()
