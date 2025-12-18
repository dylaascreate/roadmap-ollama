import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import joblib
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. DATABASE CONFIGURATION
# ==========================================
DB_CONFIG = {
    'dbname': 'devnexus_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

MODEL_PATH = 'devnexus_recommender.pkl'
COURSES_DB_PATH = 'courses_db.json'
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'gpt-oss:120b-cloud' 

# ==========================================
# 2. LOAD RESOURCES
# ==========================================
print("⏳ Loading AI Model...")
try:
    model = joblib.load(MODEL_PATH)
    print("✅ AI Model Loaded.")
except:
    print("❌ Model missing. Run train_model.py first.")
    model = None

course_lookup = {}
try:
    with open(COURSES_DB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for c in data:
            course_lookup[c['course_code']] = c
    print(f"✅ Indexed {len(course_lookup)} courses from JSON.")
except:
    print("❌ Error: courses_db.json missing.")

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"⚠️ DB Connection Error: {e}")
        return None

def get_user_profile(user_id):
    conn = get_db_connection()
    if not conn: return [], []
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # Get Skills
        cur.execute("""
            SELECT s.name FROM skills s
            JOIN skill_user su ON s.id = su.skill_id
            WHERE su.user_id = %s
        """, (user_id,))
        skills = [row['name'].lower() for row in cur.fetchall()]
        # Get Completed Courses
        cur.execute("""
            SELECT course_code FROM course_user 
            WHERE user_id = %s AND status = 'completed'
        """, (user_id,))
        completed = [row['course_code'] for row in cur.fetchall()]
        conn.close()
        return skills, completed
    except Exception as e:
        print(f"⚠️ Profile Query Error: {e}")
        if conn: conn.close()
        return [], []

def get_next_course_from_db(current_code):
    conn = get_db_connection()
    if not conn: return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT next_course_code FROM courses WHERE code = %s", (current_code,))
        result = cur.fetchone()
        conn.close()
        if result and result[0]: return result[0]
        return None
    except Exception as e:
        print(f"⚠️ Roadmap Query Error: {e}")
        return None

# ==========================================
# 4. MAIN LOGIC (RAG IMPLEMENTATION)
# ==========================================
def generate_recommendation(user_query, user_id=None):
    if not model: return {"error": "AI not ready."}

    # STEP 1: PREDICTION (The Classifier)
    try:
        prediction = model.predict([user_query])[0]
        predicted_code = prediction.split(' ')[0]
    except:
        return {"message": "I couldn't understand your request."}

    # STEP 2: RETRIEVAL (The "R" in RAG)
    course_details = course_lookup.get(predicted_code)
    if not course_details:
        return {"message": f"Recommended {predicted_code}, but details are missing."}
    
    response = {
        "course_code": predicted_code,
        "course_name": course_details['course_name'],
        # Default message (will be overwritten by Ollama)
        "message": f"Based on your interest, we recommend: <b>{course_details['course_name']}</b>"
    }
    required_skills = course_details.get('associated_skills', [])

    # STEP 3: LOGIC & GENERATION
    if user_id:
        print(f"🔎 Checking Profile for User ID: {user_id}")
        user_skills, completed_courses = get_user_profile(user_id) # <--- Variable defined here!

        # [SCENARIO A: REDIRECT IF COMPLETED]
        if predicted_code in completed_courses:
            next_course_code = get_next_course_from_db(predicted_code)
            
            if next_course_code:
                # Switch to Next Course
                print(f"🔀 Redirecting: {predicted_code} -> {next_course_code}")
                predicted_code = next_course_code
                course_details = course_lookup.get(predicted_code)
                required_skills = course_details.get('associated_skills', [])

                response['course_code'] = predicted_code
                response['course_name'] = course_details['course_name']

                # 🔥 RAG GENERATION (Redirect Context)
                response['message'] = generate_ollama_message(
                    user_query, 
                    course_details['course_name'], 
                    required_skills,
                    context=f"Student finished the previous course and is leveling up."
                )
            else:
                response['message'] = f"You have already mastered <b>{predicted_code}</b>! No further steps defined."
                response['status'] = 'completed'
                return response

        # [SCENARIO B: NORMAL RECOMMENDATION]
        else:
            # 🔥 RAG GENERATION (Standard Context)
            response['message'] = generate_ollama_message(
                user_query, 
                course_details['course_name'], 
                required_skills,
                context="Student wants to learn this topic."
            )

        # Gap Analysis
        learned = []
        to_learn = []
        for req in required_skills:
            clean_req = req.split('(')[0].strip().lower()
            match = any(u_s in clean_req or clean_req in u_s for u_s in user_skills)
            if match: learned.append(req)
            else: to_learn.append(req)

        response['skills_you_know'] = learned
        response['skills_to_learn'] = to_learn

    else:
        # Guest User - Simple RAG
        response['message'] = generate_ollama_message(
            user_query, 
            course_details['course_name'], 
            required_skills,
            context="Guest user exploring topics."
        )
        response['skills_to_learn'] = required_skills

    return response

# ==========================================
# 5. API ROUTE
# ==========================================
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    return jsonify(generate_recommendation(data.get('query', ''), data.get('user_id')))

def generate_ollama_message(user_query, course_name, skills, context=""):
    """
    DEBUG VERSION: Prints errors to the terminal
    """
    prompt = f"""
    You are a helpful academic advisor.
    Context: User wants "{user_query}". Recommending "{course_name}".
    Task: Write a 2-sentence encouraging recommendation.
    """

    print(f"🤖 CONNECTING TO OLLAMA ({OLLAMA_MODEL})...") # <--- Debug Print

    try:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        
        # 1. Check if we can reach the server
        response = requests.post(OLLAMA_API_URL, json=payload)
        
        # 2. Check the status code
        print(f"📡 OLLAMA STATUS: {response.status_code}") # <--- Debug Print

        if response.status_code == 200:
            print("✅ Success! Message received.")
            return response.json()['response'].strip()
        else:
            print(f"❌ OLLAMA FAILED: {response.text}") # <--- Print the error message from Ollama
            return f"Based on your interest, we recommend: {course_name}"
            
    except Exception as e:
        print(f"⚠️ CRITICAL ERROR: {e}") # <--- This will tell us if it's a connection issue
        return f"Based on your interest, we recommend: {course_name}"

# def expand_skills_with_ollama(course_name, existing_skills):
#     """
#     Asks Ollama to suggest 3 modern, complementary skills.
#     """
#     prompt = f"""
#     Context:
#     Course: "{course_name}"
#     Current Syllabus Skills: {', '.join(existing_skills)}

#     Task:
#     Suggest exactly 3 modern, industry-standard tools or concepts that complement this list.
#     Return ONLY the 3 skills separated by commas. Do not write sentences.
#     Example Output: Docker, Kubernetes, AWS Lambda
#     """

#     try:
#         payload = {
#             "model": "llama3.2", # <--- Ensure this matches your model
#             "prompt": prompt,
#             "stream": False
#         }
        
#         response = requests.post("http://localhost:11434/api/generate", json=payload)
        
#         if response.status_code == 200:
#             text = response.json()['response'].strip()
#             # Clean up the text to get a nice list
#             new_skills = [s.strip() for s in text.split(',')]
#             # Add a tag so the user knows these came from AI
#             return [f"{s} (AI Suggested)" for s in new_skills]
#         return []
            
#     except:
#         return []
        

if __name__ == '__main__':
    print("🚀 DevNexus AI running on Port 5001")
    app.run(port=5001, debug=True)