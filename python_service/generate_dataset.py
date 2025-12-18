import json
import pandas as pd
import random
import re

# ==========================================
# 1. YOUR RAW DATA (The JSON you provided)
# ==========================================
raw_courses = [
  {
  "course_code": "DEK3023",
  "course_name": "Probability and Statistical Data Analysis",
  "associated_skills": [
    "Statistical Data Analysis", "Probability Modeling", "Hypothesis Testing", "Z-tests", "T-tests",
    "Linear Regression", "Correlation Analysis", "Data Visualization", "Histograms", "Bar Charts", "Scatter Plots",
    "Python Pandas", "SciPy", "Matplotlib", "R Programming", "Excel Data Analysis", "SPSS", "Minitab"
  ],
  "course_content_outline": [
    "Types of Statistics", "Cross-Section vs Time Series Data", "Frequency Distributions",
    "Measures of Central Tendency", "Probability Experiments", "Sample Spaces", "Independent vs Dependent Events",
    "Discrete Random Variables", "Continuous Random Variables", "Sampling Distributions",
    "Point and Interval Estimates", "Inference about Mean Difference"
  ]
 },
 {
  "course_code": "DEK3033",
  "course_name": "Numerical Methods For Computing",
  "associated_skills": [
    "Numerical Analysis", "Algorithm Design", "MATLAB", "Maple", "Root-Finding Algorithms",
    "Bisection Method", "Newton-Raphson", "Linear Algebra Solvers", "LU Factorization", "Gauss Elimination",
    "Numerical Integration", "Curve Fitting", "Error Propagation", "C++ for Numerical Computing"
  ],
  "course_content_outline": [
    "Computational Algorithms", "Iterative Methods for Nonlinear Equations", "Secant Method", "False Position Method",
    "Systems of Linear Equations", "Least Squares Approximation", "Polynomial Regression", "Interpolation",
    "Cubic Spline", "Lagrange Interpolation"
  ]
 },
 {
  "course_code": "DEP3013",
  "course_name": "Instructional Technology and Design In Courseware Development",
  "associated_skills": [
    "Instructional Design Models", "ADDIE", "Dick and Carey", "ASSURE", "Learning Theories",
    "Behaviorism", "Cognitivism", "Constructivism", "Mayer's Cognitive Theory", "UI Design", "Storyboarding",
    "Courseware Development", "Mobile Learning", "Serious Games", "Heuristic Evaluation", "Figma", "Adobe XD", "Unity", "Unreal Engine"
  ],
  "course_content_outline": [
    "Instructional Technology", "Systems Design", "Multimedia Elements", "User Interface Design Principles",
    "Intrinsic and Extrinsic Motivation", "VR and AR Development", "Web-based Learning",
    "Cognitive Walkthrough", "Expert Review"
  ]
 },
 {
  "course_code": "DEP3023",
  "course_name": "Models of Instruction",
  "associated_skills": [
    "Instructional Strategy Integration", "Curriculum Development", "Learning Style Assessment",
    "Blended Learning", "Flipped Classroom", "Formative Assessment", "Summative Assessment",
    "Cooperative Learning", "LMS Navigation", "Educational Delivery Modeling"
  ],
  "course_content_outline": [
    "Educational Concepts", "Multidisciplinary Perspectives", "Teaching and Learning Styles",
    "Instructional Objectives", "Instructional Alignment", "Behavioral Systems", "Information-Processing Families",
    "Inquiry Models", "Synectics", "Socratic Seminar", "Effective Classroom Environments"
  ]
 },
 {
  "course_code": "DEP3063",
  "course_name": "Courseware Engineering",
  "associated_skills": [
    "Agile Methodology", "Scrum", "Prototyping", "Waterfall Model", "Software Quality Assurance",
    "Alpha Testing", "Beta Testing", "Multimedia Authoring", "Digital Ethics", "Intellectual Property Rights",
    "Technical Documentation", "Android App Development", "Pedagogical Systems"
  ],
  "course_content_outline": [
    "Computers in Teaching", "Software Engineering Methodologies", "Courseware Testing",
    "IPR Law and Ethics", "Courseware Evaluation Instruments", "Packaging and Delivery",
    "Technical Report Writing"
  ]
 },
 {
  "course_code": "DEQ3063",
  "course_name": "Software Project Management",
  "associated_skills": [
    "Agile Project Management", "Kanban", "Software Development Plan", "Project Scheduling",
    "Gantt Charts", "CPM", "PERT", "Cost Estimation", "COCOMO", "Function Points",
    "Risk Management", "Resource Allocation", "Jira", "Trello", "Feasibility Analysis", "Project Charter"
  ],
  "course_content_outline": [
    "SPM Lifecycle", "Project Manager Roles", "Feasibility Studies", "Cost-Benefit Analysis",
    "Work Breakdown Structure", "Software Size Estimation", "Critical Path Analysis",
    "Resource Scheduling", "Risk Identification and Control"
  ]
 },
 {
  "course_code": "DEQ3093",
  "course_name": "Software Configuration Management",
  "associated_skills": [
    "Version Control", "Git", "SVN", "Baseline Management", "Change Control Board",
    "Software Auditing", "Branching Strategies", "Merging Strategies", "CI/CD Pipeline",
    "Configuration Status Accounting", "Release Management"
  ],
  "course_content_outline": [
    "SCM Concepts", "Configuration Items", "Project Management Triangle", "Change Requests",
    "Check-in Check-out Procedures", "Configuration Verification", "SCM Tools"
  ]
 },
 {
  "course_code": "DES3013",
  "course_name": "Principle of Software Engineering",
  "associated_skills": [
    "SDLC", "Agile", "Waterfall", "UML Diagrams", "Requirements Engineering",
    "Architectural Design Patterns", "Unit Testing", "User Testing", "TDD",
    "Software Maintenance", "Evolution Processes"
  ],
  "course_content_outline": [
    "Core Process Models", "Coping with Change", "Functional Requirements", "Non-functional Requirements",
    "Context Models", "Interaction Models", "Activity Diagrams", "Sequence Diagrams",
    "Object-oriented Design", "Open Source Development"
  ]
 },
 {
  "course_code": "DES3023",
  "course_name": "Software Requirements and Specifications",
  "associated_skills": [
    "Requirements Elicitation", "Interviews", "Surveys", "UML Use Case", "SRS Documentation",
    "Requirements Validation", "Negotiation", "Change Management", "Jira", "Confluence",
    "Enterprise Architect", "StarUML", "Technical Writing"
  ],
  "course_content_outline": [
    "Business vs User Requirements", "Elicitation Strategies", "Elicitation Pitfalls",
    "Requirements Modeling", "SRS Structure", "Verification vs Validation",
    "Conflict Resolution", "Version Control for Requirements"
  ]
 },
 {
  "course_code": "DES3043",
  "course_name": "Software Design",
  "associated_skills": [
    "Software Architecture", "SPA", "Microservices", "Serverless", "Mobile App Design",
    "RESTful API", "UI/UX Design", "Object-Oriented Design", "Database Schema Design",
    "SDD Authoring", "Figma", "Adobe XD"
  ],
  "course_content_outline": [
    "Architecture Views", "Native vs Hybrid Apps", "Cloud-based Architectures",
    "API Types", "Subsystem Development", "Performance Evaluation", "Navigation Design",
    "Component Behavior", "Design Documentation Standards"
  ]
 },
 {
  "course_code": "DES3053",
  "course_name": "Software Testing and Quality",
  "associated_skills": [
    "SQA", "Black-Box Testing", "Equivalence Partitioning", "Boundary Value Analysis",
    "White-Box Testing", "Control Flow", "UAT", "Regression Testing", "API Testing",
    "Selenium", "Postman", "Static Analysis"
  ],
  "course_content_outline": [
    "Testing Principles", "Testing Lifecycles", "Decision Tables", "Use Case Testing",
    "Data Flow Analysis", "Test Suite Prioritization", "Mobile App Testing",
    "Defect Reporting", "Safety Requirements"
  ]
 },
 {
  "course_code": "DES3073",
  "course_name": "Software Engineering Project",
  "associated_skills": [
    "Full-Stack Development", "Laravel", "MVC Framework", "Defensive Programming",
    "Database Integration", "UI/UX Prototyping", "Agile Tracking", "Software Migration",
    "IoT Integration", "Big Data Basics"
  ],
  "course_content_outline": [
    "Data Analytics Trends", "Cyber Security Trends", "Back-end Logic", "Data Persistence",
    "Front-end Interaction", "System Stability", "Deployment Strategies"
  ]
 },
 {
  "course_code": "DES3083",
  "course_name": "Software Engineering Process",
  "associated_skills": [
    "SPLC", "Scrum", "XP", "DevOps", "RUP", "Spiral Model",
    "Software Process Improvement", "Process Mining", "Process Intelligence", "Azure DevOps"
  ],
  "course_content_outline": [
    "Generic Process Models", "Rapid Application Development", "Concurrent Development",
    "Sprints and Ceremonies", "Process Metrics", "Strategic Importance of Processes"
  ]
 },
 {
  "course_code": "DES3103",
  "course_name": "Software Validation and Verification",
  "associated_skills": [
    "V&V Strategies", "IEEE Standards", "HCI Testing", "CMM", "TMMi",
    "Failure Analysis", "Automated Testing", "Hazard Analysis", "Bugzilla"
  ],
  "course_content_outline": [
    "Quality Metrics", "Peer Code Reviews", "Walkthroughs", "Heuristic Evaluation",
    "Manual vs Automation", "Defect Tracking", "Safety Coding Practices"
  ]
 },
 {
  "course_code": "DES3113",
  "course_name": "Mobile Application Design & Development",
  "associated_skills": [
    "Flutter", "Dart", "Declarative UI", "Widget Lifecycle", "Firebase Firestore",
    "SQLite", "Push Notifications", "Google Play Store Deployment", "Apple App Store"
  ],
  "course_content_outline": [
    "Mobile Platforms", "Dart Syntax", "State Management", "ListViews",
    "Page Routing", "Local Notifications", "Bottom Navigation", "Modal Bottom Sheets",
    "App Signing"
  ]
 },
 {
  "course_code": "DTN3023",
  "course_name": "Computer Networks",
  "associated_skills": [
    "Network Administration", "Cisco Packet Tracer", "TCP/IP", "OSI Model",
    "Router Configuration", "LAN/WAN", "Wireshark", "IPv4 Subnetting"
  ],
  "course_content_outline": [
    "Network Edge", "Packet Switching", "HTTP Protocols", "DNS",
    "UDP vs TCP", "Routing Algorithms", "MAC Addressing"
  ]
 },
 {
  "course_code": "DTN3043",
  "course_name": "Operating Systems",
  "associated_skills": [
    "Process Management", "Threading", "Paging", "Segmentation", "RAID",
    "Deadlock Avoidance", "Linux Bash", "Windows PowerShell", "Virtualization"
  ],
  "course_content_outline": [
    "System Architecture", "Inter-process Communication", "Virtual Memory",
    "Disk Scheduling", "Access Control Matrices", "Kernel I/O"
  ]
 },
 {
  "course_code": "DTS3013",
  "course_name": "Structured Programming",
  "associated_skills": [
    "C++", "Structured Logic", "Algorithms", "Pointers", "File I/O",
    "Arrays", "Visual Studio Code", "Modular Programming"
  ],
  "course_content_outline": [
    "Programming Syntax", "Control Structures", "Loops", "Parameter Passing",
    "Multi-dimensional Arrays", "Sequential File Processing", "Structs"
  ]
 },
 {
  "course_code": "DTS3093",
  "course_name": "Object Oriented Programming",
  "associated_skills": [
    "Java", "OOD", "Encapsulation", "Polymorphism", "UML Class Diagrams",
    "IntelliJ IDEA", "Java Collections", "Clean Code"
  ],
  "course_content_outline": [
    "Procedural vs OOP", "Information Hiding", "Java Variables", "Constructors",
    "Wrapper Classes", "Static Members", "Enhanced For Loops", "Dynamic Method Binding"
  ]
 },
 {
  "course_code": "DER3982",
  "course_name": "Final Year Project 1",
  "associated_skills": [
    "Technical Writing", "Gantt Charts", "Research Methodology", "Literature Review",
    "TPOSS Framework", "Fast Pitching"
  ],
  "course_content_outline": [
    "Research Topic Selection", "Methodology Diagrams", "SRS Finalization",
    "Prototype Development", "Chapter 1-3 Writing"
  ]
 },
 {
  "course_code": "DER3994",
  "course_name": "Final Year Project 2",
  "associated_skills": [
    "SDLC Implementation", "Software Deployment", "Thesis Writing", "Public Speaking",
    "Product Exhibition", "STD Documentation"
  ],
  "course_content_outline": [
    "Coding Core Functions", "Product Evaluation", "User Acceptance",
    "Final Research Report", "Showcase Presentation"
  ]
 }
]

# ==========================================
# 2. TEMPLATES (The Data Augmentation Engine)
# ==========================================
# These templates simulate different ways a student might ask about a topic
templates = [
    # Direct Learning Intent
    "I want to learn {keyword}",
    "How do I use {keyword}?",
    "Teach me about {keyword}",
    "What is {keyword}?",
    "Explain {keyword} to me",
    "I need to understand {keyword}",
    "Best course for {keyword}",
    "Where can I learn {keyword}?",
    "Is {keyword} covered in this syllabus?",
    
    # Career/Job Intent
    "I need {keyword} for my job",
    "Does this course teach {keyword} for interviews?",
    "How to apply {keyword} in real life?",
    "I want to be a developer who knows {keyword}",
    "Is {keyword} important for my career?",
    
    # Academic Intent
    "Does the exam cover {keyword}?",
    "I'm struggling with {keyword}",
    "Help me with my {keyword} assignment",
    "What are the basics of {keyword}?",
    "Advanced topics in {keyword}",
    
    # Short/Direct
    "{keyword}",
    "{keyword} tutorial",
    "{keyword} help",
    "Learning {keyword}"
]

# ==========================================
# 3. GENERATION LOGIC
# ==========================================
print("🚀 Starting Data Generation...")

dataset = []
TARGET_ROWS_PER_COURSE = 2500 # 2500 * ~20 courses = 50,000 rows

def clean_text(text):
    # Remove "Week X:" prefix if it exists in the outline
    return re.sub(r"Week \d+[-]?\d*: ", "", text).strip()

for course in raw_courses:
    code = course['course_code']
    name = course['course_name']
    
    # Combine all possible keywords for this course
    # 1. Skills
    keywords = course['associated_skills']
    # 2. Cleaned Outline Topics
    keywords += [clean_text(t) for t in course['course_content_outline']]
    # 3. The Course Name itself
    keywords.append(name)
    keywords.append(code)
    
    # Generate rows
    for _ in range(TARGET_ROWS_PER_COURSE):
        # Pick a random keyword from this course's bucket
        keyword = random.choice(keywords)
        # Pick a random sentence structure
        template = random.choice(templates)
        
        # Create query
        query = template.format(keyword=keyword)
        
        # Add to dataset
        dataset.append({
            "text": query,
            "label": code
        })

# ==========================================
# 4. SAVE TO CSV
# ==========================================
df = pd.DataFrame(dataset)

# Shuffle the data so the model doesn't learn order
df = df.sample(frac=1).reset_index(drop=True)

filename = "dataset.csv"
df.to_csv(filename, index=False)

print(f"✅ Generated {len(df)} rows of training data.")
print(f"✅ Saved to {filename}")
print("   Now run 'python train_model.py' to create your super-smart model!")