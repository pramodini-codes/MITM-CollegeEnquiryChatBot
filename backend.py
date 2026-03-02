from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import filetype   # using instead of imghdr

# -------------------------------
# FASTAPI SETUP
# -------------------------------


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# REQUEST MODEL
# -------------------------------

class ChatRequest(BaseModel):
    message: str


# -------------------------------
# CHATBOT CLASS
# -------------------------------

class MITMysoreChatbot:
    def __init__(self):
        self.college_name = "Maharaja Institute of Technology Mysore (MITM Belwadi)"
        self.location = "Belwadi Village, Srirangapatna Taluk, Mandya District, Karnataka"
        self.college_info = self.get_mit_data()
        
        self.responses = {
            "greeting": [
                f"Hello! Welcome to {self.college_name} enquiry chatbot. How can I assist you today?",
                f"Hello! I'm here to provide information about {self.college_name}. What would you like to know?"
            ],
            "farewell": [
                f"Thank you for contacting {self.college_name}. Have a great day!",
                "Dhanyavadagalu! Visit our beautiful 25-acre campus to learn more.",
                "Thank you for your enquiry. Best of luck with your engineering journey!"
            ],
            "default": [
                "I'm couldn't understand. Could you please rephrase your question?"
            ]
        }

    # -------------------------------------
    # MIT DATA
    # -------------------------------------

    def get_mit_data(self):
        return {
            "about": f"""{self.college_name} is a private autonomous engineering college located in Belwadi near Mysore.
Established: 2007 by Maharaja Educational Trust (R).
Affiliation: VTU Belagavi | Approved by AICTE | Accredited with NAAC B++.
Campus: 25-acre green campus with hostels, library, research labs, cafeteria, sports, and transportation.
""",

            "principal": {
                "name": "Dr. Murali S.",
                "position": "Principal, MIT Mysore",
                "education": "Engineering in Electronics (1991) and M.Tech (Gold Medal), Mangalore University.",
                "career": (
                    "Started as a lecturer and grew to the position of Professor. "
                    "Major contributor to the growth of Maharaja Educational Trust. "
                    "Published research in antenna design, VLSI systems, IoT, and wireless communication."
                ),
                "other_roles": "Managing Director — River View Health Care Pvt Ltd"
            },

            "courses": {
                "UG Programs (B.E.)": [
                    "Civil Engineering",
                    "Computer Science Engineering (CSE)",
                    "Electronics & Communication Engineering (ECE)",
                    "Mechanical Engineering",
                    "Information Technology",
                    "Artificial Intelligence & Machine Learning (AI & ML)"
                ],
                "PG Programs": ["M.Tech", "MBA", "MCA"]
            },

            "admission_info": {
                "UG Admission": "Based on KCET rank, COMEDK score, or Management Quota",
                "PG Admission": "Based on PGCET / GATE / KMAT / CMAT",
                "Important Note": "Documents verification required"
            },

            "fees": {
                "Civil Engineering": "₹95,000 per year",
                "CSE": "₹1,25,000 per year",
                "ECE": "₹1,10,000 per year",
                "Mechanical": "₹1,00,000 per year",
                "Information Technology": "₹1,20,000 per year",
                "AI & ML": "₹1,35,000 per year",
                "M.Tech": "₹75,000 per year",
                "MBA": "₹90,000 per year"
            },

            "contact": {
                "phone": ["+91-08236-265200", "+91-08236-265201"],
                "email": ["admissions@mitmysore.in", "principal@mitmysore.in", "info@mitmysore.in"],
                "address": "MIT Mysore, Belwadi, Srirangapatna, Mandya - 571438",
                "website": "www.mitmysore.in",
                "admission_cell": "+91-9742012345"
            },

            "placement": {
                "median_salary": "₹6,00,000 per annum",
                "highest_package": "₹12 LPA",
                "placement_rate": "85%",
                "top_companies": [
                    "Infosys", "TCS", "Wipro", "IBM", "HP", "Capgemini", "Accenture"
                ],
                "internship_partners": ["Bosch", "HAL", "BHEL", "ISRO"]
            },

            "transport": {
                "bus_routes": [
                    "Mysore City → MIT Campus (12+ buses)",
                    "Mandya → MIT Campus",
                    "Srirangapatna Local Route"
                ],
                "highlights": [
                    "Safe travel", "Affordable fees", "Clean buses", "Experienced drivers"
                ]
            }
        }

    # -------------------------------------
    # TEXT RESPONSE
    # -------------------------------------

    def get_response(self, msg):
        msg = msg.lower().strip()

        if any(w in msg for w in ["hi", "hello", "hey"]):
            return random.choice(self.responses["greeting"])

        if any(w in msg for w in ["bye", "thank you", "thanks"]):
            return random.choice(self.responses["farewell"])

        if any(w in msg for w in ["principal", "dr murali", "head of college"]):
            p = self.college_info["principal"]
            return (
                f"👨‍🏫 **Principal Information**\n\n"
                f"• **Name:** {p['name']}\n"
                f"• **Position:** {p['position']}\n"
                f"• **Education:** {p['education']}\n"
                f"• **Career:** {p['career']}\n"
                f"• **Other Roles:** {p['other_roles']}"
            )

        if any(w in msg for w in ["mitm", "mit", "college info", "about"]):
            return self.college_info["about"]

        if "course" in msg or "engineering" in msg:
            return self.handle_courses()

        if "fee" in msg:
            return self.handle_fees()

        if "admission" in msg or "kcet" in msg:
            return self.handle_admission()

        if any(w in msg for w in ["contact", "phone", "email", "address"]):
            return self.handle_contact()

        if "bus" in msg or "transport" in msg:
            return self.handle_bus()

        if "placement" in msg or "package" in msg:
            return self.handle_placement()

        return random.choice(self.responses["default"])

    # -------------------------------------
    # HANDLERS
    # -------------------------------------

    def handle_courses(self):
        text = "🎓 **Courses Offered:**\n\n"
        for cat, items in self.college_info["courses"].items():
            text += f"{cat}:\n"
            for c in items:
                text += f"• {c}\n"
            text += "\n"
        return text

    def handle_fees(self):
        text = "💰 **Fee Structure:**\n"
        for course, fee in self.college_info["fees"].items():
            text += f"• {course}: {fee}\n"
        return text

    def handle_admission(self):
        text = "📅 **Admission Details:**\n\n"
        for k, v in self.college_info["admission_info"].items():
            text += f"• {k}: {v}\n"
        return text

    def handle_contact(self):
        c = self.college_info["contact"]
        return (
            f"📞 **Contact Details:**\n"
            f"Phone: {', '.join(c['phone'])}\n"
            f"Email: {', '.join(c['email'])}\n"
            f"Address: {c['address']}\n"
            f"Website: {c['website']}"
        )

    def handle_bus(self):
        t = self.college_info["transport"]
        text = "🚌 **Transport Facilities:**\n\nBus Routes:\n"
        for r in t["bus_routes"]:
            text += f"• {r}\n"
        text += "\nHighlights:\n"
        for h in t["highlights"]:
            text += f"• {h}\n"
        return text

    def handle_placement(self):
        p = self.college_info["placement"]
        return (
            f"💼 **Placement Details:**\n\n"
            f"• Median Salary: {p['median_salary']}\n"
            f"• Highest Package: {p['highest_package']}\n"
            f"• Placement Rate: {p['placement_rate']}\n\n"
            f"Top Recruiters: {', '.join(p['top_companies'])}\n"
            f"Internship Partners: {', '.join(p['internship_partners'])}"
        )

    # -------------------------------------
    # IMAGE-BASED SMART REPLY
    # -------------------------------------

    def reply_to_image(self, filename, size_bytes, img_type):

        name_lower = filename.lower()

        if "screenshot" in name_lower:
            return (
                "📸 I see you uploaded a screenshot.\n"
                "If this screenshot is related to *fees, admission, or course details*, "
                "feel free to ask—I can help!"
            )

        keywords = {
            "fee": self.handle_fees(),
            "cse": "It looks like your image is related to CSE. Do you want CSE course details or fees?",
            "ece": "Is this related to ECE? I can give you course, faculty, and lab info.",
            "ai": "AI & ML department is one of the most in-demand branches at MIT. Want details?",
            "mechanical": "Mechanical Engineering info? I can help!",
            "civil": "Civil Engineering details available. Want syllabus, fees, or labs info?",
            "bus": self.handle_bus(),
            "placement": self.handle_placement(),
            "admission": self.handle_admission(),
            "hostel": "Hostel details: Separate hostel for boys & girls, WiFi, study rooms, mess facilities."
        }

        for word, response in keywords.items():
            if word in name_lower:
                return f"📄 Your image seems related to **{word.upper()}**:\n\n{response}"

        if size_bytes > 3_000_000:
            return (
                "⚠️ Your image is quite large. If you’re trying to upload a document or form, "
                "please ensure the text is clear."
            )

        return (
            f"📷 Image '{filename}' uploaded successfully.\n"
            f"Type: {img_type.upper()}\n"
            f"Size: {round(size_bytes/1024, 2)} KB\n\n"
            "How can I help you with this image?"
        )


# -------------------------------
# INITIALIZE CHATBOT
# -------------------------------

chatbot = MITMysoreChatbot()

# -------------------------------
# TEXT CHAT
# -------------------------------

@app.post("/chat")
def chat_api(req: ChatRequest):
    return {"reply": chatbot.get_response(req.message)}

# -------------------------------
# IMAGE UPLOAD — SMART REPLY
# -------------------------------

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    size_bytes = len(content)

    # detect image type using filetype
    kind = filetype.guess(content)
    if not kind:
        return {"reply": "❌ This file is not a valid image. Please upload JPG/PNG/WEBP."}

    img_type = kind.extension

    reply = chatbot.reply_to_image(file.filename, size_bytes, img_type)

    return {"reply": reply}


# -------------------------------
# ROOT
# -------------------------------

@app.get("/")
def home():
    return {"status": "MITM Belwadi Chatbot API Running!"}
