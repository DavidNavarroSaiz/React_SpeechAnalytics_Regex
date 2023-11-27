import re
import spacy
from spacy.matcher import Matcher
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
#uvicorn main:app --reload
app = FastAPI()




origins = [
    "http://127.0.0.1:3000",  #  URL of your front-end
    "http://127.0.0.1:2000",  #  URL of your front-end
    "http://127.0.0.1:1000",  #  URL of your front-end
    "http://localhost:3000",  #  URL of your front-end
    "http://localhost:3001",  #  URL of your front-end
]

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

class TextInput(BaseModel):
    text: str
    language: str

@app.post("/extract_info")
async def extract_info(input_data: TextInput):

    name = None
    age = None
    location = None
    address = None
    emails = None
    areas_of_interest = None
    goals = None
    phone = None
    dates = None
        
    language = input_data.language
    print(language)
    if(language == 'en-US'):
        nlp = spacy.load("en_core_web_lg")
        Person_label = "PERSON"
    elif(language == 'es-ES'):
        nlp = spacy.load("es_core_news_lg")
        Person_label = "PER"

    
    sentence = input_data.text
    doc = nlp(sentence)
    # Extract email using regex
    email_patterns = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
    r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}){2,}\b',
    r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,7})(\.[A-Z|a-z]{2,7})+\b',
    r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}){2,}(?=\s|$)\b',
    r'\b[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Z|a-z]{2,7})(\.[A-Z|a-z]{2,7})+(?=\s|$)\b',
    r'\b(email|e-mail):\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7})\b'
    ]   
    for pattern in email_patterns:
        email_match = re.search(pattern, sentence, re.IGNORECASE)
        if email_match:
            emails = email_match.group(1)
            break


    # Keywords for areas of interest and goals
    areas_of_interest_keywords = ['technology', 'art', 'science', 'design', 'music', 'literature', 'sports', 'health', 'environment', 'business', 'psychology', 'mathematics', 'programming', 'history', 'culture', 'tecnología', 'arte', 'ciencia', 'diseño', 'música', 'literatura', 'deportes', 'salud', 'medio ambiente', 'negocios', 'psicología', 'matemáticas', 'programación', 'historia', 'cultura'];
    goals_keywords = ['learn', 'improve', 'connect', 'achieve', 'innovate', 'succeed', 'grow', 'inspire', 'collaborate', 'challenge', 'contribute', 'explore', 'lead', 'adapt', 'aprender', 'mejorar', 'conectar', 'lograr', 'innovar', 'tener éxito', 'crecer', 'inspirar', 'colaborar', 'desafiar', 'contribuir', 'explorar', 'liderar', 'adaptar'];

    # Extract areas of interest using keyword matching
    areas_of_interest = [keyword for keyword in areas_of_interest_keywords if keyword in sentence.lower()]
    goals = [keyword for keyword in goals_keywords if keyword in sentence.lower()]


    # Telephone Number Patterns
    telephone_number_patterns = [
    r'\b(?:\+\d{1,3}\s?)?(?:\(\d{1,4}\)\s?)?([\d\s\.\-]+)\b',  # General format
    r'\b(?:\+\d{1,3}\s?)?(?:\(\d{1,4}\)\s?)?\d{3}\s?\d{3}\s?\d{4}\b',  # XXX XXX XXXX format
    r'\b(?:\+\d{1,3}\s?)?(?:\(\d{1,4}\)\s?)?[2-9]\d{2}\s?\d{3}\s?\d{4}\b',  # North American area code format
    r'\b(?:\+\d{1,3}\s?)?(?:\(\d{1,4}\)\s?)?[2-9]\d{2}\-\d{3}\-\d{4}\b',  # North American area code format with hyphens
    r'\b(?:\+\d{1,3}\s?)?(?:\(\d{1,4}\)\s?)?[2-9]\d{6,}\b',  # Local number format
    r'\b\d{10}\b'  # 10-digit number format (e.g., 3007741376)
    
    ]


# Date/Time Patterns
    date_time_patterns = [
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',  # MM-DD-YYYY or DD-MM-YYYY format
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\s+\d{1,2}:\d{2}\s*(?:AM|PM)?)\b',  # MM-DD-YYYY HH:MM AM/PM format
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\s+\d{1,2}:\d{2}\:\d{2}\s*(?:AM|PM)?)\b',  # MM-DD-YYYY HH:MM:SS AM/PM format
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\s+\d{1,2}:\d{2}\s*(?:AM|PM)\s*[+-]\d{2}:\d{2})\b',  # MM-DD-YYYY HH:MM AM/PM ±HH:MM format
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\s+\d{1,2}:\d{2}\:\d{2}\s*(?:AM|PM)\s*[+-]\d{2}:\d{2})\b',  # MM-DD-YYYY HH:MM:SS AM/PM ±HH:MM format
        r'\b(\d{1,2}:\d{2}\s*(?:AM|PM))\b',  # HH:MM AM/PM format
        r'\b(\d{1,2}:\d{2}\:\d{2}\s*(?:AM|PM))\b'  # HH:MM:SS AM/PM format
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',  # MM-DD-YYYY or DD-MM-YYYY format
        r'\b(\d{1,2}\s+de\s+\w+\s+de\s+\d{2,4})\b',  # DD de Month de YYYY format (e.g., 14 de agosto de 2023)
    ]
    for pattern in telephone_number_patterns:
        phone_match = re.search(pattern, sentence, re.IGNORECASE)
        if phone_match:
            phone = phone_match.group(1)
            break


    for pattern in date_time_patterns:
        date_match = re.search(pattern, sentence, re.IGNORECASE)
        if date_match:
            dates = date_match.group(1)
            break

    for ent in doc.ents:
        if ent.label_ == Person_label:
            name = ent.text
        elif ent.label_ == "LOC":
            location = ent.text
        elif ent.label_ == "GPE":
            location = ent.text

    # Find age using regex
    age_patterns = [
    r'\bI\s+am\s+(\d+)\s+years\s+old\b',
    r'\bMy\s+age\s+is\s+(\d+)\b',
    r'\b(\d+)\s+years\s+old\b',
    r'(\d+)\s*(years old|y\.o\.|y/o)',
    r'\bage:\s*(\d+)\b',
    r'\baged?\s*(\d+)\b'
    ]

    # Spanish Age Patterns
    age_patterns_spanish = [
        r'\btengo\s+(\d+)\s+años\b',
        r'\bmi\s+edad\s+es\s+(\d+)\b',
        r'\b(\d+)\s+años\b',
        r'(\d+)\s*(años|años de edad|a\.o\.|a/o)',
        r'\bedad:\s*(\d+)\b',
        r'\b(edad\s+)?(\d+)\s+años\b'
    ]

# Combine the patterns
    combined_age_patterns = age_patterns + age_patterns_spanish

    for pattern in combined_age_patterns:
        age_match = re.search(pattern, sentence, re.IGNORECASE)
        if age_match:
            age = age_match.group(1)
            break


    address_patterns = [
    r'\b(?:calle|carrera|avenida|avenue|street|st\.|ave\.)(?:\s+)(\d+\s*(?:[#\-]?\s*\d+)?)(.*)\b',
    r'\b(?:domicilio|address|dirección)\s*:\s*(\d+\s*(?:[#\-]?\s*\d+)?)(.*)\b'
]

    def extract_address(sentence):
        for pattern in address_patterns:
            address_match = re.search(pattern, sentence, re.IGNORECASE)
            if address_match:
                street = re.search(r'\b(?:calle|carrera|avenida|avenue|street|st\.|ave\.)\b', address_match.group(0), re.IGNORECASE)
                if street:
                    street_name = street.group(0)
                    house_and_apartment = f"{address_match.group(1)} {address_match.group(2)}"
                    return f"{street_name} {house_and_apartment}"
        return None


    address = extract_address(sentence)

                
        # Construct the response JSON
    response = {
        "Name": name,
        "Age": age,
        "Location": location,
        "Address": address,
        "date": dates,
        "phone": phone,
        "Email": emails,
        "Areas_of_Interest": areas_of_interest,
        "Goals": goals
    }
    print(response)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000,reload = True)