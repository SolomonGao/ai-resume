from google import genai
from google.genai import types
import fitz  # PyMuPDF
import docx
import io
import json
import dotenv
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

dotenv.load_dotenv()

def resume_to_text(file_bytes: bytes, file_type: str) -> dict:

    text = ""
    try:
        if "pdf" in file_type:
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                text = "".join(page.get_text() for page in doc)
        elif "docx" in file_type or "word" in file_type:
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join(para.text for para in doc.paragraphs)
        else:
            return {"error": f"Unsupported file type: {file_type}"}
    except Exception as e:
        return {"error": f"Failed to extract text from file: {e}"}

    if not text.strip():
        return {"error": "Extracted text is empty."}

    return {"text": text}


def parse_resume_with_gemini(resume_text: dict, jd_text: str) -> dict:
    try:
        client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY"),
        )


        prompt = f"""
        You are an expert technical recruiter and professional resume writer. Your task is to rewrite a resume to be perfectly tailored for a specific job description (JD) and optimized for Applicant Tracking Systems (ATS).

        **Rules:**
        1.  Analyze the provided Job Description to identify the top 5-8 most important keywords, skills, and qualifications (e.g., "Python," "data analysis," "project management," "AWS").
        2.  Analyze the original Resume to understand the candidate's experience and skills.
        3.  Rewrite the resume's "Summary" section to be a powerful, concise professional summary (3-4 sentences) that directly mirrors the language and key requirements of the JD.
        4.  Rewrite the "Work Experience" bullet points. For each job, rephrase the accomplishments to include keywords from the JD and use the STAR method (Situation, Task, Action, Result). Focus on quantifiable achievements (e.g., "Increased efficiency by 30%" instead of "Made things more efficient").
        5.  If there is a "Projects" section, rewrite the project descriptions to highlight relevant skills and technologies mentioned in the JD, if there is not a Projects section, do not create one.
        6.  Do not invent new experiences or skills. Only rephrase and enhance existing information from the original resume.
        7.  The output MUST be a valid JSON object. Do not include any text before or after the JSON object.

        **JSON Output Structure:**
        {{
        "name": "Full Name",
        "contact": {{
            "email": "email@address.com",
            "phone": "123-456-7890",
            "link": "linkedin.com/in/username"
        }},
        "summary": "The rewritten professional summary.",
        "skills": ["List", "of", "relevant", "skills", "from", "the", "resume"],
        "experience": [
            {{
            "title": "Job Title",
            "company": "Company Name",
            "date_range": "Month Year – Month Year",
            "description_points": [
                "Rewritten bullet point 1 using STAR method and JD keywords.",
                "Rewritten bullet point 2 with quantifiable results."
            ]
            }}
        ],
        "education": [
            {{
            "degree": "Degree Name",
            "institution": "University Name",
            "date_range": "Month Year – Month Year"
            }}
        ],
        "projects": [
            {{
            "name": "Project Name",
            "description": "Rewritten project description highlighting relevant skills."
            }}
        ]
        }}

        **Here is the information to use:**

        ---
        **Job Description:**
        {jd_text}
        ---
        **Original Resume:**
        {resume_text}
        ---
        """


        model = "gemini-flash-lite-latest"

        contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            thinking_config = types.ThinkingConfig(
                thinking_budget=0,
            ),
        )

        # Make a single, non-streaming call
        response = client.models.generate_content(
            model=model,
            contents=contents,
            # config=generate_content_config,
        )
        

        # The full text is available directly
        full_response_text = response.text
        
        # Clean and parse
        if full_response_text.strip().startswith("```json"):
            json_text = full_response_text.strip()[7:-3]
        else:
            json_text = full_response_text.strip()
            
        parsed_json = json.loads(json_text)
        return parsed_json


    except json.JSONDecodeError as e:
            # This error is specific to when the response is not valid JSON
            print(f"\nError: Failed to decode JSON. Raw response was:\n'{response.text}'")
            return {"error": "JSONDecodeError", "details": str(e), "raw_response": response.text}
    except Exception as e:
        # This catches all other errors, like API key issues, network problems, etc.
        print(f"\nAn unexpected error occurred: {e}")
        return {"error": "An unexpected error occurred", "details": str(e)}
    
    
def create_pdf_from_data(data: dict) -> bytes:
    """Renders an HTML template with resume data and converts it to a PDF."""
    try:
        env = Environment(loader=FileSystemLoader("app/src/templates"))
        template = env.get_template("resume_template.html")
        rendered_html = template.render(data)
        pdf_bytes = HTML(string=rendered_html).write_pdf()
        return pdf_bytes
    except Exception as e:
        return {"error": f"Failed to create PDF: {e}"}