from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file_obj) -> str:
    reader = PdfReader(file_obj)
    return "".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(file_obj) -> str:
    doc = docx.Document(file_obj)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_txt(file_obj) -> str:
    return file_obj.read().decode("utf-8", errors="ignore")

def load_file_text(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    return extract_text_from_txt(uploaded_file)
