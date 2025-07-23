# 🏠 Real Estate Listing Analyzer & Fake Detection System

## Overview

This project is a full-stack Python-based web application designed to analyze property listings from **Zameen.com** using **Selenium**, and detect potentially fake or overly promotional listings using **NLP models via Hugging Face Transformers**. It also features a **Gemini-powered chatbot assistant**, history tracking via **PostgreSQL**, and a modern frontend interface for input, analysis, and user engagement.

> 📹 A working video demo of the project is available here: [Watch Demo](https://your-link-here.com)

---

## 📂 Project Structure

realestate-analyzer/
│
├── app.py                  # Flask backend server and routing logic
├── config.py               # Environment-based configuration and API keys
├── database.py             # PostgreSQL ORM and transaction logic
├── fake_detection.py       # NLP-based fake listing detection using HuggingFace
├── zameen_scraper.py       # Selenium and BeautifulSoup-based scraper for Zameen.com
│
├── chatbot.js              # Real estate chatbot frontend logic
├── script.js               # General frontend scripts (scrolling, validation, gallery)
│
├── app.log                 # Backend logging output
├── .env                    # API tokens and DB credentials (excluded in production)
│
└── templates/
    ├── index.html          # Main input interface for URL submission
    ├── output.html         # Results page displaying scraped and analyzed data
    └── history.html        # User history of analyzed properties


```

---

## 🚀 Features

* **Zameen Scraper**
  Extracts title, price, location, property features, and images from Zameen property URLs using headless Chrome and BeautifulSoup.

* **Fake Detection Engine**
  Uses HuggingFace models:

  * `distilbert-base-uncased-finetuned-sst-2-english` for **sentiment**
  * `hello-simpleai/roberta-base-fake-news` for **fake news detection**

* **Database Integration**

  * Stores listing info and NLP results in PostgreSQL
  * Auto-creates tables with indexes and relations
  * History tracking with timestamped analysis

* **Flask Web App**

  * Form-based URL input and analysis trigger
  * Bootstrap-style layout with live gallery view
  * Chatbot interface for user engagement

* **Chatbot Assistant**

  * Uses Google Gemini API for domain-specific responses
  * Integrated via `/chatbot` Flask route

---

## 💾 Environment Variables (`.env`)

```bash
HF_API_TOKEN="your_huggingface_token"
DB_PASSWORD="your_postgres_password"
SECRET_KEY="your_flask_secret"
GEMINI_API_KEY="your_google_gemini_key"
```

---

## 🛠 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/realestate-analyzer.git
   cd realestate-analyzer
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup PostgreSQL Database**

   * Ensure PostgreSQL is running
   * Update `.env` with your credentials
   * Tables will be auto-created on first run

5. **Run the App**

   ```bash
   python app.py
   ```

6. **Visit App**

   ```
   http://127.0.0.1:5000/
   ```

---

## 🧠 Technologies Used

* **Backend:** Python, Flask, PostgreSQL
* **Scraping:** Selenium, BeautifulSoup
* **NLP:** HuggingFace Transformers
* **Frontend:** HTML, CSS, JavaScript
* **AI Assistant:** Google Gemini API

---

## 📈 Future Improvements

* Add user authentication system
* Deploy to Heroku/Docker with production-ready configurations
* Improve UI/UX with animations and responsiveness
* Expand to support other property websites (OLX, Lamudi)

---

## 📸 Video Demonstration

Watch the project in action:
👉 [Click to View the Working Demo](https://your-link-here.com)

---

## 📬 Contact

For questions, suggestions, or contributions:
**Ali Warraich**
📧 [ali@example.com](mailto:ali@example.com)
🌐 GitHub: [@aliwarraich](https://github.com/aliwarraich)

---

Would you like me to export this as a `.md` file too? Or update the file with your video link once it's ready?
