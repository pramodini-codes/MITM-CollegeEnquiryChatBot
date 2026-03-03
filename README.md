MITM College Enquiry Chatbot

An AI-powered College Enquiry Chatbot built using **FastAPI (Backend)** and **GitHub Pages (Frontend)**.

This chatbot provides information about:

- College Overview
- Principal Details
- Courses Offered
- Fee Structure
- Admission Process
- Placement Details
- Transport Facilities
- Contact Information
- Image-based Smart Replies

---

Live Demo

🔹 Frontend:  
👉 https://pramodini-codes.github.io/mitm-college-enquiry-chatbot/

🔹 Backend API:  
👉 https://mitm-collegeenquirychatbot.onrender.com/

---

Tech Stack

Backend
- FastAPI
- Python 3.10+
- Uvicorn
- filetype (for image validation)

Frontend
- HTML
- CSS
- JavaScript (Fetch API)
- Hosted on GitHub Pages

Deployment
- Backend → Render
- Frontend → GitHub Pages

---

Project Structure

```
mitm-college-enquiry-chatbot/
│
├── backend.py
├── requirements.txt
├── README.md
│
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

---

Backend Setup (Local Development)

1. Clone Repository

```bash
git clone https://github.com/pramodini-codes/mitm-college-enquiry-chatbot.git
cd mitm-college-enquiry-chatbot
```

2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Run Server

```bash
python -m uvicorn backend:app --reload
```

The server will run at:

```
http://127.0.0.1:8000
```

---

Deployment (Render)

1. Push project to GitHub
2. Go to https://render.com
3. Create New Web Service
4. Connect GitHub repo
5. Set:

- Build Command:
  ```
  pip install -r requirements.txt
  ```

- Start Command:
  ```
  uvicorn backend:app --host 0.0.0.0 --port 10000
  ```

6. Deploy

---

CORS Configuration (Important)

Since the frontend is hosted on GitHub Pages and the backend on Render, CORS must allow:

```python
allow_origins = [
    "https://pramodini-codes.github.io"
]
```

---

API Endpoints

1. Health Check

```
GET /
```

Response:
```json
{
  "status": "MITM Belwadi Chatbot API Running!"
}
```

---

2. Chat API

```
POST /chat
```

Request:
```json
{
  "message": "What courses are available?"
}
```

Response:
```json
{
  "reply": "Courses Offered..."
}
```

---

3. Image Upload

```
POST /upload-image
```

Form Data:
```
file: image.jpg
```

Response:
```json
{
  "reply": "Image uploaded successfully..."
}
```

---

Features

- Rule-based smart response system  
- Dynamic reply selection  
- Image-based keyword detection  
- Structured JSON API  
- Fully deployable cloud backend  
- Responsive frontend UI  

---

Future Improvements

- Add AI NLP integration (OpenAI / LLM)
- Add Database support (MongoDB / PostgreSQL)
- Admin dashboard
- Live admission form submission
- Voice chatbot support

---

Author

Pramodini 

## License

This project is developed for academic and educational purposes.

---

## Support

If you like this project, give it a star on GitHub!
