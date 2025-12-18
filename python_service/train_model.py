import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC  # <--- NEW IMPORTS
from sklearn.calibration import CalibratedClassifierCV # <--- For probability
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import joblib

DATA_FILE = 'dataset.csv'

print(f"📂 Loading dataset from {DATA_FILE}...")
try:
    df = pd.read_csv(DATA_FILE).dropna(subset=['query', 'course_code'])
except FileNotFoundError:
    print("❌ dataset.csv missing.")
    exit()

# USE LINEAR SVC (Better for specific keywords)
# We wrap it in CalibratedClassifierCV so we can still get probabilities if needed later
model = make_pipeline(
    TfidfVectorizer(ngram_range=(1, 2)), # Look at 2-word phrases like "api testing"
    CalibratedClassifierCV(LinearSVC(dual="auto")) 
)

X_train, X_test, y_train, y_test = train_test_split(df['query'], df['course_code'], test_size=0.2, random_state=42)

print("🧠 Training the SVM Model...")
model.fit(X_train, y_train)

print(f"🎯 Model Accuracy: {model.score(X_test, y_test) * 100:.2f}%")

joblib.dump(model, 'devnexus_recommender.pkl')
print("✅ Saved new SVM model.")