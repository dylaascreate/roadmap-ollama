import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import pickle
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. CONFIGURATION & RESOURCES
# ==========================================
# Update this with your actual DB password
DB_CONFIG = {
    'dbname': 'devnexus_db', 
    'user': 'postgres', 
    'password': 'postgres', 
    'host': 'localhost', 
    'port': '5432'
}

MODEL_PATH = 'devnexus.pkl'
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'gpt-oss:120b-cloud' # Or 'mistral', 'llama3'

print("⏳ Loading Machine Learning Model...")
try:
    with open('devnexus.pkl', 'rb') as f:
        model = pickle.load(f)
        print("✅ Model Loaded!")
except Exception as e:
    print(f"❌ Error loading .pkl model: {e}")
    model = None

# ==========================================
# 2. DB HELPER FUNCTIONS (The "R" in RAG)
# ==========================================
def get_db_connection():
    try: 
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e: 
        print(f"❌ DB Connection Error: {e}")
        return None

def get_course_details_from_db(course_code):
    """
    Fetches Course Content (Outline, Skills) directly from PostgreSQL.
    This replaces the old JSON lookup.
    """
    conn = get_db_connection()
    if not conn: return None

    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # We fetch the outline and skills which are likely stored as JSON/Text in DB
    query = """
        SELECT 
            code, 
            name as course_name, 
            next_course_code,
            learning_outline,   
            associated_skills   
        FROM courses 
        WHERE code = %s
    """
    cur.execute(query, (course_code,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        # DATA CLEANING: Convert DB text fields back to Python Lists
        # 1. Handle Outline
        if isinstance(row['learning_outline'], str):
            try:
                row['course_content_outline'] = json.loads(row['learning_outline'])
            except:
                row['course_content_outline'] = row['learning_outline'].split('\n')
        else:
            row['course_content_outline'] = row['learning_outline'] if row['learning_outline'] else []

        # 2. Handle Skills
        if isinstance(row['associated_skills'], str):
            try:
                row['associated_skills'] = json.loads(row['associated_skills'])
            except:
                row['associated_skills'] = row['associated_skills'].split(',')
        else:
             row['associated_skills'] = row['associated_skills'] if row['associated_skills'] else []
             
        return row
    return None

def get_user_profile(user_id):
    """Fetches Skills, Completed Courses, and Career Goal."""
    conn = get_db_connection()
    if not conn: 
        return [], [], "Technology Professional"
    
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # 1. Fetch User Skills (Pivot Table)
    cur.execute("""
        SELECT s.name 
        FROM skills s 
        JOIN skill_user su ON s.id = su.skill_id 
        WHERE su.user_id = %s
    """, (user_id,))
    user_skills = {row['name'].lower() for row in cur.fetchall()}
    
    # 2. Fetch Completed Courses
    cur.execute("""
        SELECT course_code 
        FROM course_user 
        WHERE user_id = %s AND status = 'completed'
    """, (user_id,))
    completed = [row['course_code'] for row in cur.fetchall()]
    
    # 3. Fetch Career Name
    cur.execute("""
        SELECT c.name as career_title 
        FROM users u
        JOIN careers c ON u.career_id = c.id
        WHERE u.id = %s
    """, (user_id,))
    career_row = cur.fetchone()
    career_goal = career_row['career_title'] if career_row else "Software Engineer"
    
    conn.close()
    return list(user_skills), completed, career_goal

# ==========================================
# 3. AI ENGINE
# ==========================================
def call_ollama(prompt, is_json=False):
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    if is_json:
        payload["format"] = "json"

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        if not response.text: return None
        result = response.json().get('response', '').strip()
        if is_json: return json.loads(result)
        return result
    except Exception as e:
        print(f"⚠️ AI Error: {e}")
        return None

def generate_ollama_message(user_query, course_name, skills, outline, career_goal, context=""):
    prompt = f"""
    [INST]
    Context: You are a Career Mentor for a student wanting to be a {career_goal}.
    Student Query: "{user_query}"
    Course: "{course_name}"
    System Note: {context}
    
    Syllabus Topics: {', '.join(outline[:6])}
    
    Task:
    1. Explain why this course is essential for a {career_goal}.
    2. Pick one topic from the syllabus and link it to a real-world job task.
    3. Be encouraging and concise.
    [/INST]
    """
    return call_ollama(prompt)

def get_industry_bridge_skills(course_name, syllabus_skills):
    prompt = f"For the course '{course_name}', suggest 3 specific modern industry software tools (2025). Return ONLY comma-separated names."
    raw = call_ollama(prompt)
    if raw:
        tools = [s.strip() for s in raw.split(',')]
        return [f"{t} (Industry Choice)" for t in tools[:3]]
    return []

def analyze_skill_synergy(user_skills, course_name, syllabus_skills):
    """
    Sends all skills to AI, but commands it to return ONLY the Top 3 strongest matches.
    """
    prompt = f"""
    [INST]
    You are an Academic Synergy Analyst.
    
    DATA:
    1. Student Skills: {', '.join(user_skills)}
    2. Course: "{course_name}"
    3. Syllabus Keywords: {', '.join(syllabus_skills[:20])}
    
    TASK:
    1. Compare the Student Skills against the Syllabus.
    2. Rank them by relevance.
    3. Select ONLY the TOP 3 skills that provide the biggest advantage.
    4. Ignore low-relevance skills.
    
    OUTPUT:
    Return a JSON array with exactly 3 objects (or fewer if no skills match). 
    Do not add introduction text. Use this format:
    
    [
      {{
        "rank": 1,
        "skill": "The most relevant skill",
        "match_reason": "One clear sentence explaining the specific advantage."
      }},
      {{
        "rank": 2,
        "skill": "The second most relevant skill",
        "match_reason": "..."
      }}
    ]
    [/INST]
    """
    # Force JSON mode
    return call_ollama(prompt, is_json=True) or []

def get_all_courses_summary():
    """Fetches a lightweight summary of ALL courses for scanning."""
    conn = get_db_connection()
    if not conn: return []
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT code, name, associated_skills FROM courses")
    rows = cur.fetchall()
    conn.close()
    return rows

# ==========================================
# 4. API ROUTES
# ==========================================
@app.route('/generate-path', methods=['POST'])
def generate_path():
    data = request.json
    career_goal = data.get('career_goal', '')
    user_skills = data.get('user_skills', []) 
    
    # 1. Fetch ALL available courses (The RAG "Library")
    all_courses = get_all_courses_summary()
    
    # Format list for AI: "- CODE: Name (Skills)"
    courses_str = "\n".join([f"- {c['code']}: {c['name']}" for c in all_courses])
    
    # 2. Strict Prompt
    prompt = f"""
    [INST]
    Context: You are a University Advisor.
    Available Courses Database:
    {courses_str}
    
    Student Goal: "{career_goal}"
    Student Skills: {', '.join(user_skills)}
    
    Task: Select exactly 3 to 5 courses from the Database that form a learning path for this goal.
    Constraint: Use ONLY the course codes provided. Do not invent courses.
    
    Return a JSON array:
    [
      {{ "step": 1, "course_code": "CODE", "reason": "Brief reason" }},
      {{ "step": 2, "course_code": "CODE", "reason": "Brief reason" }}
    ]
    [/INST]
    """
    
    # 3. Call AI
    recommendations = call_ollama(prompt, is_json=True)
    
    if not recommendations:
        return jsonify({"error": "AI failed to generate path"}), 500

    # 4. Hydrate with Real DB Data
    final_roadmap = []
    for step in recommendations:
        # Fetch full details (Description, Topics) from DB for each selected course
        details = get_course_details_from_db(step['course_code'])
        if details:
            final_roadmap.append({
                "step": step['step'],
                "course_code": details['code'],
                "course_name": details['course_name'],
                "reason": step['reason'],
                "content": details['course_content_outline'] # Real Syllabus!
            })
            
    return jsonify({
        "career_goal": career_goal,
        "academic_path": final_roadmap
    })
    
@app.route('/sync-courses', methods=['GET'])
def sync_courses():
    """
    Reads directly from the JSON file to bootstrap the Laravel Database.
    """
    try:
        print("📂 Reading from courses_db.json...")
        # Ensure this filename matches exactly what is in your folder
        with open('courses_db.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"✅ Loaded {len(data)} courses from file.")
        return jsonify(data)
        
    except FileNotFoundError:
        print("❌ Error: courses_db.json not found!")
        return jsonify({"error": "courses_db.json not found"}), 404
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    query = data.get('query', '')
    u_id = data.get('user_id')
    
    # 1. Prediction (Using ML Model)
    if not model: return jsonify({"error": "Model not loaded"}), 500
    prediction = model.predict([query])[0]
    p_code = prediction.split(' ')[0]
    
    # 2. Fetch Initial Details from DB
    final_details = get_course_details_from_db(p_code)
    if not final_details:
        return jsonify({"error": f"Course {p_code} not found in DB"}), 404

    final_code = p_code
    
    # 3. Profile & Redirection Logic
    u_skills = []
    completed = []
    career_goal = "Software Engineer"
    context = "User exploration."

    if u_id:
        u_skills, completed, career_goal = get_user_profile(u_id)
        
        # Normalize
        completed_clean = [c.strip().upper() for c in completed]
        
        # REDIRECTION CHECK
        if p_code.strip().upper() in completed_clean:
            next_c = final_details.get('next_course_code')
            
            if next_c:
                # Fetch NEXT course details from DB
                next_details = get_course_details_from_db(next_c)
                if next_details:
                    final_code = next_c
                    final_details = next_details
                    context = f"User mastered {p_code}. Advancing to {final_code}."
            else:
                return jsonify({
                    "message": f"You have mastered {p_code}!", 
                    "status": "completed"
                })

    # 4. RAG & Enrichment
    outline = final_details.get('course_content_outline', [])
    syllabus_skills = final_details.get('associated_skills', [])
    course_name = final_details.get('course_name')
    
    ai_msg = generate_ollama_message(query, course_name, syllabus_skills, outline, career_goal, context)
    industry_extras = get_industry_bridge_skills(course_name, syllabus_skills)
    
    learned = [s for s in syllabus_skills if any(u.lower() in s.lower() for u in u_skills)]
    to_learn = [s for s in syllabus_skills if s not in learned]

    return jsonify({
        "course_code": final_code,
        "course_name": course_name,
        "target_career": career_goal,
        "message": ai_msg,
        "course_content": outline,
        "industry_recommendations": industry_extras,
        "skills_to_learn": to_learn,
        "skills_you_know": learned
    })

@app.route('/synergy', methods=['POST'])
def synergy():
    data = request.json
    u_id = data.get('user_id')
    course_code = data.get('course_code') # Frontend must send this!
    
    # 1. Fetch User Skills from DB
    user_skills, _, _ = get_user_profile(u_id)
    
    # Safety: If user has no skills, return empty immediately
    if not user_skills:
        return jsonify({
            "synergy_analysis": [], 
            "foundation_skills": [],
            "message": "Add skills to your profile to see how they help you in this course!"
        })

    # 2. Fetch Course Details from DB (The "R" in RAG)
    course = get_course_details_from_db(course_code)
    
    if not course:
        return jsonify({"error": f"Course {course_code} not found"}), 404

    # 3. Perform AI Analysis
    # We pass the cleaned list of skills we fetched from Postgres
    analysis = analyze_skill_synergy(
        user_skills, 
        course['course_name'], 
        course.get('associated_skills', [])
    )
    
    return jsonify({
        "course_name": course['course_name'],
        "synergy_analysis": analysis, 
        "foundation_skills": user_skills
    })
    
if __name__ == '__main__':
    print("🚀 DevNexus AI (DB-Connected) running on Port 5001") 
    app.run(port=5001, debug=True)