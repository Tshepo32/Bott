import os
from flask import Flask, request, jsonify # Assuming you are using Flask
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- Resume Data Dictionary ---
resume_data = {
    "personal_info": {
        "name": "Lorens Tshepo Maleo",
        "location": "Woodstock, Cape Town",
        "linkedin": "https://www.linkedin.com/in/lorens-tshepo-m-2533b04a",
        "website": "https://tshepo32.github.io/personal-website/"
    },

    "stack": {
        "programming_languages": ["Java", "Python", "C", "SQL"],
        "frameworks_tools": ["Spring Boot", "Flask", "React", "Jinja", "Gunicorn", "RESTful APIs", "Git", "Maven", "npm", "Web Speech API"],
        "databases": ["MySQL", "PostgreSQL"],
        "cloud": ["Render"]
    },

    "school": [
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

    # Skills-related queries
    if any(keyword in query for keyword in ["framework", "tool", "tools", "stack", "technology", "tech"]):
        frameworks = ", ".join(resume_data["stack"]["frameworks_tools"])
        return f"I am skilled with frameworks and tools like: {frameworks}."

    elif any(keyword in query for keyword in ["programming language", "code in", "language", "coding"]):
        languages = ", ".join(resume_data["skills"]["programming_languages"])
        return f"My programming languages include: {languages}."

    elif any(keyword in query for keyword in ["database", "db", "data storage"]):
        databases = ", ".join(resume_data["skills"]["databases"])
        return f"I have experience with databases such as: {databases}."

    elif any(keyword in query for keyword in ["cloud", "deployment", "hosting"]):
        cloud_platforms = ", ".join(resume_data["skills"]["cloud"])
        return f"My cloud platform experience includes: {cloud_platforms}."

    # Experience/Internship-related queries
    elif any(keyword in query for keyword in ["internship", "experience", "work", "job", "vacancy"]):
        internship_info = resume_data["internship"]
        achievements = "; ".join(internship_info["achievements"])
        return (f"I completed an internship at {internship_info['company']} from {internship_info['duration']}. "
                f"Key achievements include: {achievements}.")

    # Project-related queries
    elif any(keyword in query for keyword in ["project", "developed", "built", "website", "chatbot", "system"]):
        projects = resume_data["projects"]
        response = "Here are details on my key projects:\n"
        response += f"1. **Student Enrolment System**: {projects['student_enrolment_system']['summary']} (Tech used: {', '.join(projects['student_enrolment_system']['tech'])})\n"
        response += f"2. **Personal Website with AI Chatbot**: {projects['personal_website_ai_chatbot']['summary']} (Tech used: {', '.join(projects['personal_website_ai_chatbot']['tech'])})"
        return response

    # Education-related queries
    elif any(keyword in query for keyword in ["education", "study", "studies", "diploma", "certificate", "school", "university"]):
        education_details = []
        for edu in resume_data["school"]:
            highlights = "; ".join(edu['highlights'])
            education_details.append(f"- {edu['title']} ({edu['year']}): {highlights}")
        return "My education includes:\n" + "\n".join(education_details)

    # Certification-related queries
    elif any(keyword in query for keyword in ["certification", "certified", "cs50x", "harvard"]):
        cert = resume_data["certifications"][0]
        return f"I am certified in {cert['title']} by {cert['issuer']} (completed in {cert['year']})."

    # Contact information queries
    elif any(keyword in query for keyword in ["contact", "email", "phone", "reach out", "linkedin", "website", "get in touch"]):
        info = resume_data["personal_info"]
        # Format as clickable Markdown links
        linkedin_link = f"[LinkedIn Profile]({info['linkedin']})"
        website_link = f"[Personal Website]({info['website']})"

        return (f"Check out my {linkedin_link} or my {website_link}.")

    # Summary/General profile queries
    elif any(keyword in query for keyword in ["summary", "profile", "about you", "who are you", "tell me about yourself", "lorens", "tshepo", "maleo"]):
        personal_info = resume_data["personal_info"]
        summary_text = resume_data["summary"]
        linkedin_link = f"[LinkedIn Profile]({personal_info['linkedin']})"
        website_link = f"[Personal Website]({personal_info['website']})"
        return (f"{summary_text} My full name is {personal_info['name']} and I am based in {personal_info['location']}."
                f"you may also check out my {linkedin_link} or my {website_link}.")

    else:
        return "I'm still learning to answer more general questions. Could you try asking more specifically about my skills, projects, education, or experience?"


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