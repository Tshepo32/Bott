# app.py
from flask import Flask, request, jsonify
import PyPDF2
import os
import re

app = Flask(__name__)

# --- Configuration ---
# Define a list of PDF files to read
# Make sure these files are in the same directory as app.py
PDF_FILE_NAMES = [
    'resume.pdf',
    'resume2.pdf'
]

# --- Global Variable for Combined Knowledge Base ---
full_combined_text = "" # Stores the combined text from all PDFs

# --- Functions ---

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF '{pdf_path}': {e}")
        return None

def load_knowledge_base():
    global full_combined_text
    full_combined_text = "" # Reset in case of reload or multiple calls

    print("Loading knowledge base from multiple PDFs...")
    for pdf_name in PDF_FILE_NAMES:
        pdf_path = os.path.join(os.path.dirname(__file__), pdf_name)
        if os.path.exists(pdf_path):
            extracted_text = extract_text_from_pdf(pdf_path)
            if extracted_text:
                full_combined_text += extracted_text + "\n\n--- Document Boundary ---\n\n"
                print(f"Text from '{pdf_name}' loaded successfully!")
            else:
                print(f"Failed to extract text from '{pdf_name}'. It might be empty or corrupted.")
        else:
            print(f"Warning: PDF file '{pdf_name}' not found at '{pdf_path}'. Skipping this document.")

    if not full_combined_text.strip(): # Check if combined text is effectively empty
        print("No PDF content loaded. Chatbot will be unable to answer document-specific questions.")
    else:
        print("All specified PDFs processed and combined into knowledge base.")


def simple_keyword_search(query, combined_content):
    """
    Performs a simple keyword/substring search within the combined content.
    Returns sentences or sections containing the keywords.
    """
    query_lower = query.lower()

    # Split combined content into lines/paragraphs. Using sentence tokenization
    # would be better, but requires more libraries (e.g., NLTK), so we'll stick
    # to splitting by lines or approximate sentences.
    # For better results, you might want to split into sentences using a simple regex
    # or just iterate through lines and clean them.
    sentences = re.split(r'(?<=[.!?])\s+', combined_content) # Attempt to split by sentences

    # Extract words from query, excluding very common words or single letters
    # This regex matches words with 2 or more letters/numbers.
    keywords = re.findall(r'\b\w{2,}\b', query_lower)

    relevant_snippets = []
    max_snippets = 5 # Limit the number of snippets to return

    if not keywords: # If no significant keywords, use the whole query as a phrase
        keywords = [query_lower]

    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(keyword in sentence_lower for keyword in keywords) or query_lower in sentence_lower:
            stripped_sentence = sentence.strip()
            if stripped_sentence:
                relevant_snippets.append(stripped_sentence)
                if len(relevant_snippets) >= max_snippets:
                    break # Stop after finding enough snippets

    if relevant_snippets:
        # Join snippets. You might want to add ellipses or similar for flow
        return "Based on the provided documents: " + " ".join(relevant_snippets) + "."

    return "I couldn't find specific information in the documents related to that. Can you rephrase or ask about specific details?"

# --- Flask Routes ---

@app.route('/')
def health_check():
    return "OK", 200


@app.route('/ask_from_resume', methods=['POST'])
def ask_from_resume():
    try:
        data = request.get_json()
        user_question = data.get('question')

        if not user_question:
            return jsonify({"answer": "Please provide a question."}), 400

        print(f"Received question for document-based answer: {user_question}")

        if not full_combined_text.strip():
            # If knowledge base is empty, try to reload it just in case
            load_knowledge_base()
            if not full_combined_text.strip():
                return jsonify({"answer": "Lorens's documents are not available or are empty at the moment. Please ensure the PDF files exist and contain text."}), 500


        # Use simple keyword search on the combined text
        answer = simple_keyword_search(user_question, full_combined_text)

        return jsonify({"answer": answer})

    except Exception as e:
        print(f"Error in /ask_from_resume endpoint: {e}")
        # Return a more generic error for the user, log full error for debugging
        return jsonify({"answer": "An internal error occurred in the Python chatbot service. Please try again later."}), 500

# --- App Initialization ---
if __name__ == '__main__':
    # Load the knowledge base when the application starts
    load_knowledge_base()

    # Get port from environment variable, default to 5000 for local dev
    port = int(os.environ.get("PORT", 5000))
    # In production (Render), Gunicorn will manage the server.
    # For local testing, app.run() is fine.
    app.run(debug=False, host='0.0.0.0', port=port)