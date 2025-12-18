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
# 1. CONFIGURATION & RESOURCES
# ==========================================
DB_CONFIG = {'dbname': 'devnexus_db', 'user': 'postgres', 'password': 'postgres', 'host': 'localhost', 'port': '5432'}
MODEL_PATH = 'devnexus_recommender.pkl'
COURSES_DB_PATH = 'courses_db.json'
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'gpt-oss:120b-cloud' 

print("⏳ Loading AI Model & JSON Resources...")
model = joblib.load(MODEL_PATH)
course_lookup = {}
with open(COURSES_DB_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)
    for c in data:
        course_lookup[c['course_code']] = c

# ==========================================
# 2. THE CENTRALIZED AI ENGINE
# ==========================================
def call_ollama(prompt, is_json=False):
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    if is_json:
        payload["format"] = "json"

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300) # Increased timeout
        
        # Check if response is empty string
        if not response.text:
            print("❌ Ollama returned an empty body.")
            return None
            
        result = response.json().get('response', '').strip()
        
        if is_json:
            return json.loads(result)
        return result
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON Parsing Error: {e}. Raw Response: {response.text[:100]}")
        return None
    except Exception as e:
        print(f"⚠️ Connection Error: {e}")
        return None

# ==========================================
# 3. DB HELPER FUNCTIONS
# ==========================================
def get_db_connection():
    try: return psycopg2.connect(**DB_CONFIG)
    except: return None

def get_user_profile(user_id):
    conn = get_db_connection()
    if not conn: return [], []
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT s.name FROM skills s JOIN skill_user su ON s.id = su.skill_id WHERE su.user_id = %s", (user_id,))
    user_skills = {row['name'].lower() for row in cur.fetchall()}
    cur.execute("SELECT course_code FROM course_user WHERE user_id = %s AND status = 'completed'", (user_id,))
    completed = [row['course_code'] for row in cur.fetchall()]
    conn.close()
    return list(user_skills), completed

def analyze_skill_synergy(user_skills, course_name, syllabus_skills):
    # If Python logic missed it, this is the AI's final instruction
    prompt = f"""
    [INST]
    Analyze these skills: {', '.join(user_skills)}
    Course: {course_name}
    
    IMPORTANT: 
    - If the student skills list is empty, return exactly: []
    - Only analyze the skills provided. DO NOT invent new skills.
    
    Return a JSON array:
    [
      {{
        "foundation_skill": "...",
        "target_concept": "...",
        "deep_analysis": "..."
      }}
    ]
    [/INST]
    """
    return call_ollama(prompt, is_json=True) or []

# ==========================================
# 4. RAG SPECIALIST FUNCTIONS (Restored Logic)
# ==========================================

def generate_ollama_message(user_query, course_name, skills, clos, context=""):
    """Restored: Explains the Syllabus-to-Industry Link."""
    prompt = f"""
    You are an Academic & Career Advisor. 
    User Query: "{user_query}"
    Course: {course_name}
    University Syllabus (CLOs): {', '.join(clos)}
    Industry Tools: {', '.join(skills)}

    Task:
    Explain the bridge between the University Syllabus and Industry Demand in 3 sentences:
    1. Connect a specific University CLO to a real-world project.
    2. Explain how an industry tool (like {skills[0] if skills else 'relevant tools'}) applies that CLO.
    3. Explain why this makes the student more employable.
    """
    return call_ollama(prompt) or f"We recommend {course_name} based on your goals."

def get_industry_bridge_skills(course_name, syllabus_skills):
    """Restored: Suggests 3 modern tools via AI."""
    prompt = f"Given course '{course_name}' teaching {syllabus_skills}, suggest 3 modern 2025 industry tools. Return ONLY tool names separated by commas."
    raw = call_ollama(prompt)
    if raw:
        tools = [s.strip() for s in raw.split(',')]
        return [f"{t} (Industry Choice)" for t in tools[:3]]
    return []

def analyze_skill_synergy(user_skills, course_name, syllabus_skills):
    # Simplified, high-instruction prompt
    prompt = f"""
    [INST]
    Analyze these student skills: {', '.join(user_skills)}
    Target Course: {course_name}
    
    Return ONLY a JSON array with 2 objects. Use this structure:
    [
      {{
        "foundation_skill": "skill name",
        "target_concept": "course concept",
        "deep_analysis": "explanation"
      }}
    ]
    [/INST]
    """
    # Force JSON mode in the call
    return call_ollama(prompt, is_json=True) or []

# ==========================================
# 5. API ROUTES
# ==========================================
@app.route('/health', methods=['GET'])
def health():
    """Checks if the service and the AI model are ready."""
    status = {
        "service": "online",
        "model_loaded": model is not None,
        "ollama_connection": False
    }
    # Check if Ollama is actually reachable
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            status["ollama_connection"] = True
    except:
        pass
        
    return jsonify(status)

@app.route('/sync-courses', methods=['GET'])
def sync_courses():
    """Returns basic info AND roadmap links for all courses."""
    summary = []
    for code, details in course_lookup.items():
        summary.append({
            "code": code,
            "name": details['course_name'],
            "next_course_code": details.get('next_course_code') # <--- Add this!
        })
    return jsonify(summary)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    query = data.get('query', '')
    u_id = data.get('user_id')
    
    # 1. Prediction
    prediction = model.predict([query])[0]
    p_code = prediction.split(' ')[0]
    
    # 2. Safety Check: Does this course exist in our JSON?
    final_code = p_code
    final_details = course_lookup.get(p_code)
    
    if not final_details:
        return jsonify({"error": "Course not found in syllabus mapping"}), 404

    # 3. State Initialization
    u_skills = []
    completed = [] # Define here to avoid NameError for guests
    context = "User exploration."

    # 4. Profile Check & Roadmap Redirection
    if u_id:
        u_skills, completed = get_user_profile(u_id)
        if p_code in completed:
            next_c = get_next_course_from_db(p_code)
            if next_c:
                final_code = next_c
                final_details = course_lookup.get(final_code)
                context = f"User finished {p_code}. Redirecting to next level: {final_code}."
            else:
                return jsonify({"message": f"You've already mastered {p_code}!", "status": "completed"})

    # 5. Enrichment (RAG)
    syllabus_skills = final_details.get('associated_skills', [])
    clos = final_details.get('clos', [])
    
    ai_msg = generate_ollama_message(query, final_details['course_name'], syllabus_skills, clos, context)
    ind_extras = get_industry_bridge_skills(final_details['course_name'], syllabus_skills)
    
    # 6. Gap Analysis
    learned = [s for s in syllabus_skills if any(u.lower() in s.lower() for u in u_skills)]
    to_learn = [s for s in syllabus_skills if s not in learned]

    return jsonify({
        "course_code": final_code,
        "course_name": final_details['course_name'],
        "message": ai_msg,
        "academic_outcomes": clos,
        "industry_recommendations": ind_extras,
        "skills_to_learn": to_learn,
        "skills_you_know": learned
    })

@app.route('/synergy', methods=['POST'])
def synergy():
    data = request.json
    u_id = data.get('user_id')
    
    # 1. Fetch User Skills from DB
    user_skills, _ = get_user_profile(u_id)
    
    # 2. SAFETY CHECK: If the list is empty, stop here!
    if not user_skills:
        return jsonify({
            "synergy_analysis": [],
            "foundation_skills": [],
            "message": "You haven't added any skills to your profile yet! Add skills like Java or SQL to see how they link to this course."
        })

    # 3. If they HAVE skills, proceed with AI analysis
    course = course_lookup.get(data.get('course_code'))
    analysis = analyze_skill_synergy(user_skills, course['course_name'], course.get('associated_skills', []))
    
    return jsonify({
        "synergy_analysis": analysis, 
        "foundation_skills": user_skills
    })
    
# ==========================================
#  START THE SERVER
# ==========================================
if __name__ == '__main__':
    # This is where the message is printed to your terminal
    print("🚀 DevNexus AI running on Port 5001") 
    
    # This is the actual command that opens the port
    app.run(port=5001, debug=True)