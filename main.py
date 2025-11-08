from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time
import asyncio
from pathlib import Path

# Import our custom modules
from models import ResumeAnalyzer, PlagiarismChecker, ResumeImprover
from utils import (
    FileHandler, TextProcessor, ResponseFormatter, 
    CompanyMatcher, Logger, clean_filename
)

# Initialize FastAPI app
app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume analysis, improvement suggestions, and company matching",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000", "http://localhost:5173"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
resume_analyzer = ResumeAnalyzer()
plagiarism_checker = PlagiarismChecker()
resume_improver = ResumeImprover()
company_matcher = CompanyMatcher()

# Pydantic models for request/response
class AnalysisResponse(BaseModel):
    domain: str
    confidence: float
    skills: List[str]
    contact_info: Optional[Dict[str, str]] = None
    readability: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None

class ImprovementResponse(BaseModel):
    overall_score: int
    suggestions: List[Dict[str, Any]]
    categories_analyzed: List[str]

class PlagiarismResponse(BaseModel):
    overall_score: float
    matches: List[Dict[str, Any]]
    total_matches: int
    recommendations: List[str]

class CompanyResponse(BaseModel):
    companies: List[Dict[str, Any]]
    total_count: int
    domain: str

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Resume Analyzer API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "analyze": "/api/analyze-resume",
            "improve": "/api/improve-resume", 
            "plagiarism": "/api/check-plagiarism",
            "companies": "/api/companies/{domain}"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "models_loaded": {
            "resume_analyzer": resume_analyzer.model is not None,
            "plagiarism_checker": True,
            "resume_improver": True
        }
    }

@app.post("/api/analyze-resume", response_model=AnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """
    Analyze uploaded resume and classify domain with skills extraction
    """
    start_time = time.time()
    
    try:
        # Validate file
        file_content = await file.read()
        validation_result = FileHandler.validate_file(file.filename, file_content)
        
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["error"])
        
        Logger.log_analysis(
            filename=file.filename,
            domain="processing",
            confidence=0,
            processing_time=0
        )
        
        # Analyze resume
        analysis_result = resume_analyzer.predict_domain(file_content, file.filename)
        
        if "error" in analysis_result:
            raise HTTPException(status_code=422, detail=analysis_result["error"])
        
        # Extract additional information
        if "extracted_text_length" in analysis_result and analysis_result["extracted_text_length"] > 0:
            # For demo, we'll simulate text extraction for additional features
            # In production, you'd extract the actual text here
            sample_text = "Sample resume text for demonstration"
            contact_info = TextProcessor.extract_contact_info(sample_text)
            readability = TextProcessor.calculate_readability_score(sample_text)
        else:
            contact_info = None
            readability = None
        
        processing_time = time.time() - start_time
        
        # Log successful analysis
        Logger.log_analysis(
            filename=file.filename,
            domain=analysis_result["domain"],
            confidence=analysis_result["confidence"],
            processing_time=processing_time
        )
        
        return AnalysisResponse(
            domain=analysis_result["domain"],
            confidence=analysis_result["confidence"],
            skills=analysis_result["skills"],
            contact_info=contact_info,
            readability=readability,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        Logger.log_error(f"Analysis failed: {str(e)}", {"filename": file.filename})
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/improve-resume", response_model=ImprovementResponse)
async def improve_resume(file: UploadFile = File(...), domain: Optional[str] = None):
    """
    Analyze resume and provide improvement suggestions
    """
    try:
        # Validate file
        file_content = await file.read()
        validation_result = FileHandler.validate_file(file.filename, file_content)
        
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["error"])
        
        # For demo purposes, we'll use sample text
        # In production, extract actual text from the file
        sample_text = """
        John Doe
        Software Developer
        I am a results-driven professional with excellent communication skills.
        I work well under pressure and am a team player.
        """
        
        if domain is None:
            # Get domain from previous analysis or use default
            domain = "Software Engineering"
        
        # Analyze and get improvement suggestions
        improvement_result = resume_improver.analyze_resume(sample_text, domain)
        
        if "error" in improvement_result:
            raise HTTPException(status_code=422, detail=improvement_result["error"])
        
        return ImprovementResponse(
            overall_score=improvement_result["overall_score"],
            suggestions=improvement_result["suggestions"],
            categories_analyzed=improvement_result["categories_analyzed"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        Logger.log_error(f"Improvement analysis failed: {str(e)}", {"filename": file.filename})
        raise HTTPException(status_code=500, detail=f"Improvement analysis failed: {str(e)}")

@app.post("/api/check-plagiarism", response_model=PlagiarismResponse)
async def check_plagiarism(file: UploadFile = File(...)):
    """
    Check resume for plagiarism and overused phrases
    """
    try:
        # Validate file
        file_content = await file.read()
        validation_result = FileHandler.validate_file(file.filename, file_content)
        
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["error"])
        
        # For demo purposes, we'll use sample text
        # In production, extract actual text from the file
        sample_text = """
        I am a results-driven professional with excellent communication skills.
        I have a proven track record and am detail-oriented individual.
        I work well under pressure and am self-motivated team player.
        """
        
        # Check for plagiarism
        plagiarism_result = plagiarism_checker.check_plagiarism(sample_text)
        
        if "error" in plagiarism_result:
            raise HTTPException(status_code=422, detail=plagiarism_result["error"])
        
        return PlagiarismResponse(
            overall_score=plagiarism_result["overall_score"],
            matches=plagiarism_result["matches"],
            total_matches=plagiarism_result["total_matches"],
            recommendations=plagiarism_result["recommendations"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        Logger.log_error(f"Plagiarism check failed: {str(e)}", {"filename": file.filename})
        raise HTTPException(status_code=500, detail=f"Plagiarism check failed: {str(e)}")

@app.get("/api/companies/{domain}", response_model=CompanyResponse)
async def get_companies_by_domain(domain: str, limit: Optional[int] = 10):
    """
    Get companies that hire for specific domain
    """
    try:
        # Get matching companies
        companies = company_matcher.get_matching_companies(domain)
        
        # Apply limit
        if limit:
            companies = companies[:limit]
        
        return CompanyResponse(
            companies=companies,
            total_count=len(companies),
            domain=domain
        )
        
    except Exception as e:
        Logger.log_error(f"Company matching failed: {str(e)}", {"domain": domain})
        raise HTTPException(status_code=500, detail=f"Company matching failed: {str(e)}")

@app.get("/api/domains")
async def get_available_domains():
    """
    Get list of available domains for classification
    """
    return {
        "domains": [
            "Software Engineering",
            "Data Science", 
            "Marketing",
            "Finance",
            "Healthcare",
            "Education"
        ]
    }

# Background task for logging (example)
async def log_usage_stats(endpoint: str, processing_time: float):
    """Background task to log usage statistics"""
    # In production, this would write to a database or analytics service
    print(f"Usage: {endpoint} took {processing_time:.2f}s")

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseFormatter.format_error_response(exc.detail, "HTTP_ERROR")
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    Logger.log_error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ResponseFormatter.format_error_response("Internal server error", "INTERNAL_ERROR")
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    print("🚀 Resume Analyzer API started successfully!")
    print("📊 Models loaded:", {
        "resume_analyzer": resume_analyzer.model is not None,
        "plagiarism_checker": True,
        "resume_improver": True
    })

# Shutdown event  
@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 Resume Analyzer API shutting down...")

if __name__ == "__main__":
    import uvicorn
    
    # Create uploads directory if it doesn't exist
    Path("uploads").mkdir(exist_ok=True)
    
    print("🔥 Starting Resume Analyzer API...")
    print("📝 Available endpoints:")
    print("  - POST /api/analyze-resume")
    print("  - POST /api/improve-resume") 
    print("  - POST /api/check-plagiarism")
    print("  - GET /api/companies/{domain}")
    print("  - GET /api/domains")
    print("  - GET /health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )