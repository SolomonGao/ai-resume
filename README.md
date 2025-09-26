# AI-Powered Resume Customization Tool
This project implements an AI-driven web application using Streamlit and the Google Gemini API to automatically tailor a user's resume (PDF or DOCX) to a specific job description (JD). The goal is to maximize the resume's effectiveness for Applicant Tracking Systems (ATS) and human recruiters by highlighting relevant keywords and quantifiable achievements.
***
### Features
Intelligent Alignment: Uses the Gemini model to analyze a Job Description and align the resume's professional summary, skills, and experience bullet points.

ATS-Friendly Output: Generates a clean, structured PDF using WeasyPrint and Jinja2 templates, avoiding complex formatting issues (like nested tables) that cause ATS parsing errors.

Multi-Format Input: Accepts resume files in both PDF and DOCX formats.
***
### Setup and Installation
Follow these steps to get the application running locally:

1. Prerequisites
You must have Python 3.8+ installed.

2. Environment Setup
Clone the repository and set up a virtual environment:

```
git clone <your-repo-url>
cd ai-resume
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install Dependencies
Install all required Python packages:

```
pip install -r requirements.txt
```

4. API Key Configuration
The application requires a Gemini API key to function.

* Get your key from Google AI Studio.

* Create a file named .env in the root directory of the project.

* Add your API key to the file:
```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```
5. Run the Application
Navigate to the application directory and run the Streamlit app:
```
streamlit run app/src/app.py
```
The application will open automatically in your web browser (usually at http://localhost:8501).

***

### Project Structure
The codebase is organized as follows:
```
ai-resume/
├── .env                  # Environment file for API Key
├── requirements.txt      # Project dependencies
└── app/
    └── src/
        ├── app.py              # Main Streamlit application file (UI)
        ├── resume_parser.py    # Core logic: file reading, Gemini API calls, PDF generation
        ├── gemini.py           # Placeholder/utility for direct Gemini calls
        ├── templates/
        │   └── resume_template.html # Jinja2 HTML template for PDF output
        └── ...
```
***
### Dependencies
Key dependencies listed in requirements.txt:

streamlit: For creating the interactive web UI.

google-genai: The official Python SDK for calling the Gemini API.

weasyprint: Used to convert the Jinja2 HTML output into a professional PDF file.

jinja2: Templating engine for generating dynamic HTML resume structure.

PyMuPDF (via fitz): For robust PDF file parsing.

python-docx: For reading and extracting text from Word documents.
