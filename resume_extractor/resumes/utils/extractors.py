#for extraction of text

import re
import io
from PIL import Image
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from docx import Document


JOB_ROLE_KEYWORDS = [
    'software engineer','developer','full stack','frontend','backend','data scientist','machine learning','UI & UX'
] # keyword for searching the job role in text
QUALIFICATIONS = ['b.tech', 'bsc', 'b.e', 'mtech', 'mca', 'bca', 'bachelor of technology', 'master of computer', 'bachelor'] #qualification keyword for searching
LANGUAGE_KEYWORDS = ['python','java','c++','c','javascript','react','reactjs','node','sql','go','ruby','php','c#'] # keyowrd for langugae


EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_RE = re.compile(r'(\+?\d{1,4}[\s-]?)?(\d{6,15})')  
DOB_RE = re.compile(r'(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b)|(\b\d{4}\b)')  

def extract_text_from_pdf(file_bytes):
    
    text = ''
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ''
            text += page_text + '\n'
    text = text.strip()
    if text:
        return text
    images = convert_from_bytes(file_bytes) #if pdf contains only image 
    ocr_text = ''
    for img in images:
        ocr_text += pytesseract.image_to_string(img) + '\n'
    return ocr_text.strip()

def extract_text_from_docx(file_bytes):
    doc = Document(io.BytesIO(file_bytes))
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def extract_text_from_image(file_bytes):
    img = Image.open(io.BytesIO(file_bytes)).convert('RGB')
    return pytesseract.image_to_string(img)

def extract_all_text(file_obj):
    filename = getattr(file_obj, 'name', 'file')
    ext = filename.lower().split('.')[-1]
    file_bytes = file_obj.read()
    if ext == 'pdf':
        return extract_text_from_pdf(file_bytes)
    elif ext in ('docx', 'doc'):
        return extract_text_from_docx(file_bytes)
    elif ext in ('jpg','jpeg','png','bmp','tiff'):
        return extract_text_from_image(file_bytes)
    else:
        return file_bytes.decode(errors='ignore') if isinstance(file_bytes, (bytes,)) else str(file_bytes)

# Field extraction 
def find_email(text):
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None

def find_phone(text):
    candidates = re.findall(r'\+?\d[\d\-\s\(\)]{5,}\d', text)
    for c in candidates:
        digits = re.sub(r'\D', '', c)
        if 7 <= len(digits) <= 15:
            return digits
    m = PHONE_RE.search(text)
    if m:
        return re.sub(r'\D', '', m.group(0))
    return None

def find_dob_or_age(text):
    m = DOB_RE.search(text)
    if m:
        return m.group(0)
    m2 = re.search(r'Age[:\s]+(\d{1,3})', text, flags=re.IGNORECASE)
    if m2:
        return m2.group(1)
    return None

def find_qualification(text):
    print(text)
    t = text.lower()
    for q in QUALIFICATIONS:
        if q in t:
            return q.upper()
    return None

def find_job_role(text):
    t = text.lower()
    for kw in JOB_ROLE_KEYWORDS:
        if kw in t:
            return kw.title()
    m = re.search(r'([A-Za-z ]+(Engineer|Developer|Consultant|Analyst))', text, flags=re.IGNORECASE) #edge case
    if m:
        return m.group(0).strip()
    return None

def find_languages(text):
    t = text.lower()
    found = []
    for lang in LANGUAGE_KEYWORDS:
        if re.search(r'\b' + re.escape(lang) + r'\b', t):
            found.append(lang.capitalize())
    return ', '.join(sorted(set(found))) if found else None

def find_address(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    address_lines = []
    for i, line in enumerate(lines):
        if re.search(r'\b(street|st\.|road|rd\.|lane|city|state|pin|pincode|addr|address)\b', line, flags=re.IGNORECASE):
            block = ' '.join(lines[max(0, i-1):min(len(lines), i+2)])
            address_lines.append(block)
    return '; '.join(address_lines) if address_lines else None

def extract_structured(text): # returing dict
    return {
        'email': find_email(text),
        'phone': find_phone(text),
        'dob_or_age': find_dob_or_age(text),
        'qualification': find_qualification(text),
        'job_role': find_job_role(text),
        'languages': find_languages(text),
        'address': find_address(text),
        'raw': text
    }
