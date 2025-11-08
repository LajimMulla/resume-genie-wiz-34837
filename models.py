import joblib
import pandas as pd
import PyPDF2
import docx
from io import BytesIO
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ResumeAnalyzer:
    def __init__(self, model_path="public/models/domain_classifier.pkl", 
                 vectorizer_path="public/models/tfidf_vectorizer.pkl"):
        """Initialize the Resume Analyzer with trained models"""
        try:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            print("✅ Models loaded successfully!")
        except FileNotFoundError as e:
            print(f"❌ Error loading models: {e}")
            self.model = None
            self.vectorizer = None
    
    def extract_text_from_pdf(self, file_bytes):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + " "
            return text
        except Exception as e:
            print(f"Error extracting PDF text: {e}")
            return ""
    
    def extract_text_from_docx(self, file_bytes):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(BytesIO(file_bytes))
            text = " ".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
            return ""
    
    def clean_text(self, text):
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Keep only alphabetic characters
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove stopwords
        try:
            stop_words = set(stopwords.words('english'))
            words = text.split()
            text = " ".join([word for word in words if word not in stop_words])
        except:
            pass
        
        return text
    
    def predict_domain(self, file_content, filename):
        """Predict domain from resume content"""
        if not self.model or not self.vectorizer:
            return self._fallback_prediction(filename)
        
        # Extract text based on file type
        file_extension = filename.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            text = self.extract_text_from_pdf(file_content)
        elif file_extension in ['docx', 'doc']:
            text = self.extract_text_from_docx(file_content)
        elif file_extension == 'txt':
            text = file_content.decode('utf-8', errors='ignore')
        else:
            return {"error": "Unsupported file format"}
        
        if not text.strip():
            return {"error": "Could not extract text from file"}
        
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        if not cleaned_text.strip():
            return {"error": "No valid text found after processing"}
        
        try:
            # Vectorize the text
            text_vector = self.vectorizer.transform([cleaned_text])
            
            # Predict domain
            predicted_domain = self.model.predict(text_vector)[0]
            
            # Get confidence score
            if hasattr(self.model, 'predict_proba'):
                confidence = self.model.predict_proba(text_vector).max() * 100
            else:
                confidence = 85.0  # Default confidence
            
            # Get relevant skills based on domain
            skills = self._get_skills_for_domain(predicted_domain)
            
            return {
                "domain": predicted_domain,
                "confidence": round(confidence, 2),
                "skills": skills,
                "extracted_text_length": len(text),
                "processed_text_length": len(cleaned_text)
            }
            
        except Exception as e:
            print(f"Error during prediction: {e}")
            return {"error": f"Prediction failed: {str(e)}"}
    
    def _fallback_prediction(self, filename):
        """Fallback prediction when models are not available"""
        filename_lower = filename.lower()
        
        if any(word in filename_lower for word in ['data', 'analyst', 'science']):
            return {
                "domain": "Data Science",
                "confidence": 75.0,
                "skills": ["Python", "Machine Learning", "SQL", "Statistics", "Pandas", "NumPy"]
            }
        elif any(word in filename_lower for word in ['software', 'developer', 'engineer']):
            return {
                "domain": "Software Engineering", 
                "confidence": 75.0,
                "skills": ["Programming", "Software Development", "Algorithms", "Problem Solving"]
            }
        elif any(word in filename_lower for word in ['marketing', 'digital']):
            return {
                "domain": "Marketing",
                "confidence": 75.0,
                "skills": ["Digital Marketing", "SEO", "Content Creation", "Analytics"]
            }
        else:
            return {
                "domain": "General",
                "confidence": 65.0,
                "skills": ["Communication", "Problem Solving", "Team Work", "Leadership"]
            }
    
    def _get_skills_for_domain(self, domain):
        """Get relevant skills for each domain"""
        skills_mapping = {
            "Software Engineering": [
                "Python", "JavaScript", "Java", "C++", "React", "Node.js", 
                "Git", "Docker", "Kubernetes", "AWS", "Algorithms", "Data Structures"
            ],
            "Data Science": [
                "Python", "R", "Machine Learning", "Deep Learning", "SQL", 
                "TensorFlow", "PyTorch", "Pandas", "NumPy", "Statistics", "Matplotlib"
            ],
            "Marketing": [
                "Digital Marketing", "SEO", "Google Analytics", "Content Marketing",
                "Social Media", "PPC", "Email Marketing", "Brand Management"
            ],
            "Finance": [
                "Financial Analysis", "Excel", "Bloomberg Terminal", "Risk Management",
                "Portfolio Management", "Financial Modeling", "Accounting", "Valuation"
            ],
            "Healthcare": [
                "Clinical Research", "Medical Knowledge", "Patient Care", 
                "Healthcare Regulations", "EMR Systems", "Medical Terminology"
            ],
            "Education": [
                "Curriculum Development", "Classroom Management", "Educational Technology",
                "Assessment", "Student Engagement", "Learning Management Systems"
            ]
        }
        
        return skills_mapping.get(domain, [
            "Communication", "Problem Solving", "Team Work", 
            "Leadership", "Project Management", "Critical Thinking"
        ])

class PlagiarismChecker:
    """Simple plagiarism checker for resumes"""
    
    def __init__(self):
        self.common_phrases = [
            "results-driven professional",
            "detail-oriented individual", 
            "proven track record",
            "excellent communication skills",
            "team player",
            "self-motivated",
            "work well under pressure"
        ]
    
    def check_plagiarism(self, text, threshold=0.3):
        """Check for common overused phrases in resumes"""
        if not text:
            return {"error": "No text provided"}
        
        text_lower = text.lower()
        matches = []
        
        for phrase in self.common_phrases:
            if phrase in text_lower:
                matches.append({
                    "phrase": phrase,
                    "category": "overused",
                    "severity": "medium"
                })
        
        similarity_score = min((len(matches) / len(self.common_phrases)) * 100, 100)
        
        return {
            "overall_score": round(similarity_score, 1),
            "matches": matches,
            "total_matches": len(matches),
            "recommendations": self._get_recommendations(similarity_score)
        }
    
    def _get_recommendations(self, score):
        """Get recommendations based on plagiarism score"""
        if score < 20:
            return ["Great! Your resume has unique content.", "Keep using specific achievements and metrics."]
        elif score < 50:
            return [
                "Consider replacing some common phrases with more specific achievements.",
                "Use concrete examples and numbers to stand out."
            ]
        else:
            return [
                "High similarity detected. Rewrite using specific accomplishments.",
                "Replace generic phrases with quantifiable achievements.",
                "Focus on unique experiences and skills."
            ]

class ResumeImprover:
    """AI-powered resume improvement suggestions"""
    
    def __init__(self):
        self.improvement_categories = [
            "formatting", "content", "keywords", "achievements", "skills"
        ]
    
    def analyze_resume(self, text, domain="General"):
        """Analyze resume and provide improvement suggestions"""
        if not text:
            return {"error": "No text provided"}
        
        suggestions = []
        
        # Check for quantifiable achievements
        if not re.search(r'\d+%|\$\d+|\d+\s*(years?|months?)', text):
            suggestions.append({
                "category": "achievements",
                "title": "Add Quantifiable Achievements",
                "description": "Include specific numbers, percentages, or metrics to demonstrate your impact.",
                "example": "Increased sales by 25% over 6 months",
                "priority": "high"
            })
        
        # Check for action verbs
        action_verbs = ["achieved", "developed", "managed", "created", "improved", "led", "implemented"]
        if not any(verb in text.lower() for verb in action_verbs):
            suggestions.append({
                "category": "content",
                "title": "Use Strong Action Verbs",
                "description": "Start bullet points with powerful action verbs to show initiative.",
                "example": "Led a team of 5 developers to deliver project ahead of schedule",
                "priority": "high"
            })
        
        # Domain-specific suggestions
        domain_suggestions = self._get_domain_suggestions(domain, text)
        suggestions.extend(domain_suggestions)
        
        # Calculate overall score
        score = max(100 - (len(suggestions) * 15), 60)
        
        return {
            "overall_score": score,
            "suggestions": suggestions[:5],  # Limit to top 5 suggestions
            "categories_analyzed": self.improvement_categories
        }
    
    def _get_domain_suggestions(self, domain, text):
        """Get domain-specific improvement suggestions"""
        suggestions = []
        text_lower = text.lower()
        
        if domain == "Software Engineering":
            if "github" not in text_lower:
                suggestions.append({
                    "category": "skills",
                    "title": "Add GitHub Profile",
                    "description": "Include your GitHub profile to showcase your coding projects.",
                    "priority": "medium"
                })
        elif domain == "Data Science":
            if "python" not in text_lower and "r" not in text_lower:
                suggestions.append({
                    "category": "skills", 
                    "title": "Highlight Programming Languages",
                    "description": "Mention key programming languages like Python or R for data science roles.",
                    "priority": "high"
                })
        
        return suggestions