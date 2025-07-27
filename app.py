import os
from flask import Flask, request, jsonify # Assuming you are using Flask
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Resume Data Dictionary ---
resume_data = {
    "skills": {
        "programming_languages": ["Java", "Python", "C", "SQL"],
        "frameworks_tools": ["Spring Boot", "Flask", "React", "Jinja", "Gunicorn", "RESTful APIs", "Git", "Maven", "npm", "Web Speech API"],
        "databases": ["MySQL", "PostgreSQL"],
        "cloud": ["Render"]
    },

    "education": [
        {
            "title": "Diploma in ICT Applications Development",
            "year": "2022 - Present",
            "highlights": [
                "Built fullstack applications using Java, Spring Boot, and React.",
                "Introduced to Power BI and data science concepts.",
                "Completed Capstone team project using agile methodologies."
            ]
        },
        {
            "title": "Higher Certificate in ICT",
            "year": "2021",
            "highlights": [
                "Gained foundational programming in Java and JavaScript.",
                "Learned basic web development and networking."
            ]
        }
    ],

    "projects": {
        "student_enrolment_system": {
            "tech": ["Java", "Swing", "JDBC", "MySQL", "TCP Sockets", "OOP"],
            "summary": "Client-server application to manage enrolments with responsive GUI and multi-threading."
        },
        "personal_website_ai_chatbot": {
            "tech": ["React", "Spring Boot", "Flask", "Render", "PostgreSQL"],
            "summary": "Fullstack site with AI chatbot answering resume-based queries using NLP."
        }
    },

    "internship": {
        "company": "Condorgreen",
        "duration": "01/07/2024 - 31/12/2024",
        "achievements": [
            "Completed CS50x from Harvard.",
            "Contributed to real-world software design projects.",
            "Gained hands-on technical and professional experience."
        ]
    },

    "certifications": [
        {
            "title": "CS50x: Introduction to Computer Science",
            "issuer": "Harvard University",
            "year": 2024
        }
    ]
}

# --- Resume Query Function ---
def answer_resume_query(query: str):
    query = query.lower()

    if "framework" in query or "tool" in query:
        return ", ".join(resume_data["skills"]["frameworks_tools"])

    elif "programming language" in query or "code in" in query:
        return ", ".join(resume_data["skills"]["programming_languages"])

    elif "database" in query:
        return ", ".join(resume_data["skills"]["databases"])

    elif "cloud" in query:
        return ", ".join(resume_data["skills"]["cloud"])

    elif "internship" in query:
        achievements = "; ".join(resume_data["internship"]["achievements"])
        return f"I interned at {resume_data['internship']['company']} from {resume_data['internship']['duration']}. Key contributions: {achievements}."

    elif "project" in query:
        projects = resume_data["projects"]
        return (
            f"1. Student Enrolment System: {projects['student_enrolment_system']['summary']}\n"
            f"2. Personal Website with AI Chatbot: {projects['personal_website_ai_chatbot']['summary']}"
        )

    elif "education" in query or "studies" in query:
        return "\n".join([
            f"{edu['title']} ({edu['year']})"
            for edu in resume_data["education"]
        ])

    elif "certification" in query:
        cert = resume_data["certifications"][0]
        return f"{cert['title']} by {cert['issuer']} ({cert['year']})"

    elif "contact" in query or "email" in query or "phone" in query:
        info = resume_data["personal_info"]
        return f"You can reach me at {info['email']} or {info['phone']}."

    elif "summary" in query or "profile" in query:
        return resume_data["summary"]

    else:
        return "I'm still learning. Could you try asking about my skills, projects, education, or experience?"


# --- API Endpoint ---
@app.route('/ask_from_resume', methods=['POST'])
def ask_from_resume():
    try:
        data = request.json
        user_question = data.get('question')

        if not user_question:
            return jsonify({"error": "Missing 'question' in request body"}), 400

        logger.info(f"Received question: '{user_question}'")
        answer = answer_resume_query(user_question)

        return jsonify({"answer": answer}), 200

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return jsonify({"status": "error", "message": "An internal server error occurred.", "details": str(e)}), 500

# --- Health Check Endpoint ---
@app.route('/')
def health_check():
    return "Resume Bot Service is running!", 200

# --- Run the Flask App ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)