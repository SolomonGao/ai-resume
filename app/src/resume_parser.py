import fitz  # PyMuPDF
import docx
import io

def parse_resume(file_bytes, file_type):
    """
    Parse resume content from PDF or DOCX file bytes.
    Args:
        file_bytes (bytes): The content of the resume file in bytes.
        file_type (str): The type of the file, either 'pdf' or 'docx'.
        Returns:
        str: Extracted text content from the resume.
    """
    text = ""
    if file_type == 'pdf':
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            text = "".join(page.get_text() for page in doc)

    elif file_type == 'docx':
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join(para.text for para in doc.paragraphs)

    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
    
    if not text.strip():
        return {"error": "The uploaded resume is empty or could not be parsed."}
    

    resume_data = {
        "personal_info": [],
        "summary": [],
        "work_experience": [],
        "education": [],
        "skills": [],
        "unknown": []  
    }

    SECTION_KEYWORDS = {
        "personal_info": ["contact", "email", "phone", "address", "linkedin", "github"],
        "summary": ["summary", "objective", "profile"],
        "work_experience": ["experience", "employment", "work history", "professional experience"],
        "education": ["education", "academic background", "qualifications"],
        "skills": ["skills", "technical skills", "competencies"]
    }

    current_section = "unknown"

    for line in text.splitlines():
        line_lower = line.strip().lower()
        if not line_lower:
            continue  

        matched_section = None
        for section, keywords in SECTION_KEYWORDS.items():
            if any(keyword in line_lower for keyword in keywords):
                matched_section = section
                break

        if matched_section:
            current_section = matched_section
            continue  

        resume_data[current_section].append(line.strip())

    return text