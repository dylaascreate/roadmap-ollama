import mysql.connector
import joblib
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. CONFIGURATION
# ==========================================
# ⚠️ UPDATE THIS WITH YOUR ACTUAL LARAVEL DB CREDENTIALS
DB_CONFIG = {
    'host': '127.0.0.1',      # or 'localhost'
    'user': 'root',           # Default XAMPP/Laragon user
    'password': 'root123',           # Default is often empty
    'database': 'devnexus_db' # CHANGE THIS to your actual Laravel DB name
}

MODEL_PATH = 'devnexus_recommender.pkl'
COURSES_DB_PATH = 'courses_db.json'

# ==========================================
# 2. LOAD RESOURCES
# ==========================================
# A. Load the "Brain" (AI Model)
try:
    model = joblib.load(MODEL_PATH)
    print("🧠 AI Model Loaded.")
except:
    print("❌ Model missing. Please run train_pkl_from_jsonl.py first.")
    model = None

# B. Load the "Book" (Course Details)
course_lookup = {}
try:
    with open(COURSES_DB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for c in data:
            course_lookup[c['course_code']] = c
    print(f"📚 Indexed {len(course_lookup)} courses from JSON.")
except:
    print("❌ courses_db.json missing. Detailed info won't be available.")

# ==========================================
# 3. DATABASE HELPER
# ==========================================
def get_user_skills_from_db(user_id):
    """
    Connects directly to the Laravel Database to find what the user knows.
    Assumes standard Laravel pivot table: skill_user (user_id, skill_id)
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # 1. We join 'skills' and 'skill_user' to get the actual names
        # Adjust table names if yours are different (e.g. 'user_skills')
        query = """
            SELECT s.name 
            FROM skills s
            JOIN skill_user su ON s.id = su.skill_id
            WHERE su.user_id = %s
        """
        
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        conn.close()
        
        # Returns simple list: ['php', 'laravel', 'sql']
        return [row['name'].lower() for row in results]

    except mysql.connector.Error as err:
        print(f"⚠️ Database Error: {err}")
        return []

# ==========================================
# 4. RECOMMENDATION LOGIC
# ==========================================
def get_recommendation(user_query, user_id=None):
    if not model: return {"error": "AI Model not active."}

    # STEP A: Predict the Course
    try:
        prediction = model.predict([user_query])[0]
        # Prediction string is "DES3043 Software Design". Split to get code.
        course_code = prediction.split(' ')[0]
    except:
        return {"message": "I'm not sure about that topic."}

    # STEP B: Get Course Details from JSON
    course_details = course_lookup.get(course_code)
    if not course_details:
        return {
            "course_code": course_code,
            "message": f"AI recommended {course_code}, but I have no details for it."
        }
        
    course_name = course_details['course_name']
    required_skills = course_details.get('associated_skills', [])

    response = {
        "course_code": course_code,
        "course_name": course_name,
        "message": f"Based on your goal, the best course is: <b>{course_name}</b>"
    }

    # STEP C: Personalization (Compare with DB)
    if user_id:
        print(f"🔍 Checking DB for User ID: {user_id}")
        user_known_skills = get_user_skills_from_db(user_id)
        
        learned = []
        to_learn = []
        
        # Compare requirements vs known skills
        for req in required_skills:
            # Clean skill string (e.g. "Laravel (Framework)" -> "laravel")
            clean_req = req.split('(')[0].strip().lower()
            
            # Fuzzy match: "laravel" matches "laravel framework"
            match = any(u_skill in clean_req or clean_req in u_skill for u_skill in user_known_skills)
            
            if match:
                learned.append(req)
            else:
                to_learn.append(req)

        response['skills_you_know'] = learned
        response['skills_to_learn'] = to_learn
        
        if len(learned) > 0:
            response['message'] += f"<br>You're ahead! You already have <b>{len(learned)}</b> skills for this course."
    else:
        # No user logged in
        response['skills_to_learn'] = required_skills

    return response

# ==========================================
# 5. API ROUTE
# ==========================================
@app.route('/recommend', methods=['POST'])
def recommend():
    # Vue.js sends { "query": "...", "user_id": 12 }
    data = request.json
    user_query = data.get('query', '')
    user_id = data.get('user_id') 
    
    result = get_recommendation(user_query, user_id)
    return jsonify(result)

if __name__ == '__main__':
    print("🚀 DevNexus AI Server Running on Port 5001...")
    app.run(debug=True, port=5001)