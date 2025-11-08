# Use Cases - Resume Analyzer System

## Use Case Diagram Overview

The Resume Analyzer system provides four main use cases for job seekers to optimize their resumes for specific domains and companies.

---

## Use Case 1: Upload Resume

**Actor:** Job Seeker

**Description:** The user uploads their resume in PDF or DOCX format to the system for analysis.

**Preconditions:**
- User has a valid resume file (PDF or DOCX format)
- File size is within acceptable limits (< 10MB)

**Postconditions:**
- Resume file is successfully uploaded and validated
- System extracts text content from the resume
- File is ready for domain classification

**Main Flow:**
1. User navigates to the Resume Analyzer homepage
2. User clicks on the upload area or drags and drops resume file
3. System validates file type and size
4. System displays upload progress indicator
5. System extracts text content from the uploaded file
6. System confirms successful upload with visual feedback
7. Use Case 2 (Classify Domain) is triggered automatically

**Alternative Flow:**
- 3a. If file type is invalid:
  - System displays error message "Only PDF and DOCX files are supported"
  - User returns to step 2
- 3b. If file size exceeds limit:
  - System displays error message "File size must be less than 10MB"
  - User returns to step 2

---

## Use Case 2: Classify Resume Domain

**Actor:** Job Seeker

**Description:** The system analyzes the uploaded resume and classifies it into a specific professional domain using machine learning.

**Preconditions:**
- Resume has been successfully uploaded (Use Case 1 completed)
- Resume text has been extracted and preprocessed

**Postconditions:**
- Domain is identified with confidence score
- Relevant skills for the domain are displayed
- Company suggestions are enabled based on the identified domain

**Main Flow:**
1. System preprocesses the resume text (cleaning, tokenization)
2. System applies TF-IDF vectorization to the text
3. System uses trained Logistic Regression model to predict domain
4. System calculates confidence score for the prediction
5. System retrieves relevant skills from the training dataset
6. System displays domain classification results with:
   - Identified domain name and icon
   - Confidence percentage with visual indicator
   - List of relevant skills as badges
7. Use Case 3 (Get Company Suggestions) is triggered automatically

**Alternative Flow:**
- 4a. If confidence score is below 50%:
  - System displays warning about low confidence
  - System still shows predicted domain but with caution indicator

**Domains Supported:**
- Software Development
- Data Science
- DevOps
- Cybersecurity
- Web Development
- Mobile Development
- Cloud Computing
- AI/ML Engineering

---

## Use Case 3: Get Company Suggestions

**Actor:** Job Seeker

**Description:** Based on the classified domain, the system suggests relevant companies that are actively hiring in that field.

**Preconditions:**
- Domain classification is complete (Use Case 2 completed)
- Domain has been identified with confidence score

**Postconditions:**
- List of relevant companies is displayed
- User can view company details and open roles
- User can navigate to company career pages

**Main Flow:**
1. System queries company database based on identified domain
2. System filters companies with active job openings
3. System retrieves company information including:
   - Company name and logo
   - Location and company size
   - Brief description
   - Number of open roles
4. System displays company cards in a grid layout
5. User can view detailed company information
6. User can click "View Jobs" to open company career page in new tab

**Alternative Flow:**
- 2a. If no companies found for the domain:
  - System displays "No companies found" message
  - System suggests checking back later

**Company Information Displayed:**
- Company logo and branding
- Company name
- Headquarters location
- Company size (employees)
- Brief description
- Number of open positions
- Link to careers page

---

## Use Case 4: Generate Resume Improvement Suggestions

**Actor:** Job Seeker

**Description:** The system analyzes the resume content and provides personalized suggestions to improve it for the identified domain.

**Preconditions:**
- Domain classification is complete (Use Case 2 completed)
- User has clicked "Generate Improvements" button

**Postconditions:**
- Improvement suggestions are displayed
- User can view actionable recommendations
- Suggestions are categorized for easy implementation

**Main Flow:**
1. User clicks "Generate Improvements" button
2. System analyzes resume content against domain requirements
3. System identifies gaps and areas for improvement
4. System generates personalized suggestions including:
   - Missing technical skills
   - Weak action verbs
   - Formatting improvements
   - Content optimization tips
5. System displays suggestions in categorized list
6. User reviews and can implement suggestions

**Improvement Categories:**
- Skills Enhancement: Missing or underrepresented technical skills
- Action Verbs: Stronger verbs to describe achievements
- Formatting: Layout and structure improvements
- Content: Keyword optimization and content suggestions

**Alternative Flow:**
- 3a. If resume is already well-optimized:
  - System displays congratulatory message
  - System shows minor refinement suggestions

---

## Use Case 5: Check Resume Uniqueness

**Actor:** Job Seeker

**Description:** The system checks the uniqueness of the resume content to ensure it stands out and is not similar to common templates or other resumes.

**Preconditions:**
- Domain classification is complete (Use Case 2 completed)
- User has clicked "Check Uniqueness" button

**Postconditions:**
- Uniqueness score is calculated and displayed
- Similar content matches are highlighted (if any)
- Recommendations for improving uniqueness are provided

**Main Flow:**
1. User clicks "Check Uniqueness" button
2. System analyzes resume text for originality
3. System compares content against:
   - Common resume templates
   - Generic phrases database
   - Industry clichés
4. System calculates uniqueness score (0-100%)
5. System identifies similar or generic phrases
6. System displays:
   - Overall uniqueness percentage
   - Visual indicator (color-coded)
   - Highlighted generic phrases
   - Suggestions for improvement
7. User reviews findings and can revise content

**Uniqueness Score Interpretation:**
- 90-100%: Excellent - Highly unique and original
- 70-89%: Good - Some unique elements, minor improvements needed
- 50-69%: Fair - Contains common phrases, needs revision
- Below 50%: Poor - Too generic, significant rewrite needed

**Alternative Flow:**
- 4a. If uniqueness score is below 50%:
  - System highlights all generic phrases in red
  - System provides specific rewrite suggestions
  - System recommends focusing on specific achievements

---

## Actor Description

**Job Seeker:**
- A professional looking to optimize their resume for job applications
- Has basic computer literacy and file management skills
- Seeks to improve resume quality and match it with target companies
- Wants to stand out in the competitive job market
- Interested in domain-specific career opportunities

---

## System Benefits

1. **Time Efficiency**: Automated domain classification saves hours of manual research
2. **Targeted Applications**: Company suggestions help focus job search efforts
3. **Quality Improvement**: AI-powered suggestions enhance resume quality
4. **Competitive Edge**: Uniqueness checker ensures resume stands out
5. **User-Friendly**: Simple interface requires no technical expertise
6. **Fast Processing**: Results delivered in under 3 seconds
7. **Comprehensive Analysis**: Multiple perspectives on resume quality

---

## Technical Requirements

- **Response Time**: < 3 seconds for all operations
- **Accuracy**: 85-92% domain classification accuracy
- **File Support**: PDF and DOCX formats
- **File Size Limit**: Maximum 10MB
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Mobile Responsive**: Works on tablets and smartphones
