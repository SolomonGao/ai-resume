import streamlit as st
import resume_parser

def stage1_ui():


    st.set_page_config(
        page_title="AI-Powered Resume Customization",
        page_icon="🚀", 
        layout="wide"     
    )

    # title
    st.title("🚀 AI-Powered Resume Customization")
    st.markdown("""
    Welcome to the AI-Powered Resume Customization tool! This application leverages advanced AI technologies to help you tailor your resume to specific job descriptions, enhancing your chances of landing your dream job. Please follow the steps below to get started:
    1. Paste the complete job description (JD) into the text area on the left.
    2. Upload your current resume in PDF or DOCX format on the right.
    """)
    st.divider() # add a horizontal divider for better visual separation

    # two columns layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("Paste the Job Description (JD)")

        jd_text = st.text_area(
            "Please paste the full job description here:",
            height=400, 
            placeholder="We are looking for a skilled software engineer with experience in Python and machine learning..." ,
        )


    with col2:
        st.header("Upload Your Resume")
        resume_file = st.file_uploader(
            "Upload Resume(PDF or DOCX)",
            type=['pdf', 'docx'],
            help="Accepted formats: PDF, DOCX",
            label_visibility="visible"
        )

    st.divider()

    start_button = st.button(
        "Start Intelligent Optimization",
        type="primary",        
        use_container_width=True #
    )
    
    return jd_text, resume_file, start_button


if __name__ == "__main__":

    jd_text, resume_file, start_button = stage1_ui()

    if start_button:
        # Input validation
        if not jd_text or resume_file is None:
            st.warning("⚠️ Please provide both the job description and upload your resume to proceed.")
        else:
            st.success("✅ Inputs received! Processing your resume...")

            resume_bytes = resume_file.getvalue()
            # Call the backend processing functions
            st.info("Next step: Calling Resume Parsing Module...")
            resume_text = resume_parser.resume_to_text(resume_bytes, resume_file.type)
            if "error" in resume_text:
                st.error(f"❌ Resume read failed: {resume_text['error']}")
                st.stop()
            structured_resume = resume_parser.parse_resume_with_gemini(resume_text, jd_text)

            if "error" in structured_resume:
                st.error(f"❌ Resume parsing with Gemini failed: {structured_resume['error']}")
                st.stop()
            
            pdf_bytes = resume_parser.create_pdf_from_data(structured_resume)
            
            if isinstance(pdf_bytes, dict) and "error" in pdf_bytes:
                st.error(f"❌ PDF generation failed: {pdf_bytes['error']}")
                st.stop()
            if pdf_bytes:
                st.success("✅ Resume optimized successfully!")
                st.download_button(
                    label="Download Optimized Resume (PDF)",
                    data=pdf_bytes,
                    file_name="optimized_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )



