# 🏠 Real Estate Listing Analyzer & Fake Detection System

## 🔍 Project Description

**Real Estate Listing Analyzer** is a full-stack Python web application that automates the extraction, evaluation, and verification of property listings from **Zameen.com**. It uses **Selenium** and **BeautifulSoup** for scraping, **HuggingFace NLP models** for detecting fake or overly promotional listings, and **PostgreSQL** for structured storage. A Gemini-powered chatbot is integrated to assist users in real-time, while a responsive frontend enables URL input, image gallery viewing, and analysis history.

> 🎥 **Demo:** [Watch Working Video](https://drive.google.com/file/d/1Km0x1OD10ODcBJ5eKXETtQbHFw-sB_aZ/view?usp=sharing)

---

## 📂 Project Structure

<details>
<summary><strong>Click to Expand</strong></summary>

```

realestate-analyzer/
├── app.py                # Flask backend server and routing logic
├── config.py             # Environment-based configuration and API keys
├── database.py           # PostgreSQL ORM and transaction logic
├── fake\_detection.py     # NLP-based fake listing detection using HuggingFace
├── zameen\_scraper.py     # Selenium and BeautifulSoup-based scraper for Zameen.com
├── chatbot.js            # Real estate chatbot frontend logic
├── script.js             # General frontend scripts (scrolling, validation, gallery)
├── app.log               # Backend logging output
├── .env                  # API tokens and DB credentials (excluded in production)
├── templates/
│   ├── index.html        # Main input interface for URL submission
│   ├── output.html       # Results page displaying scraped and analyzed data
│   └── history.html      # User history of analyzed properties

````

</details>

---

## 🚀 Features

- 🧠 **NLP Analysis:** Detects overly promotional or potentially fake listings using HuggingFace transformers.
- 🔍 **Real-Time Scraper:** Extracts title, price, location, description, features, and images using Selenium.
- 🧾 **Database Integration:** PostgreSQL schema with versioned analysis history and indexing.
- 💬 **Gemini Chatbot:** Built-in AI assistant that guides users through queries and actions.
- 📊 **User Interface:** Analyze listings, browse history, and interact with chatbot—all in one UI.

---

## 🛠 Tech Stack

| Category      | Tools Used |
|---------------|-------------|
| **Backend**   | Python, Flask |
| **Scraping**  | Selenium, BeautifulSoup |
| **NLP/AI**    | HuggingFace Transformers, Google Gemini |
| **Database**  | PostgreSQL |
| **Frontend**  | HTML, CSS, JS |
| **Others**    | dotenv, logging, PIL, urllib |

---

## 🧾 Setup Instructions

1. **Clone the Repo**
   ```bash
   git clone https://github.com/your-username/realestate-analyzer.git
   cd realestate-analyzer
````

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Create a `.env` file:

   ```env
   HF_API_TOKEN=your_huggingface_token
   DB_PASSWORD=your_postgres_password
   SECRET_KEY=your_secret_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

5. **Run the App**

   ```bash
   python app.py
   ```

   Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🎯 Future Scope

* Expand scraping support to OLX, Lamudi, and Graana.
* Deploy with Docker or on Heroku.
* Add authentication for users.
* Optimize LLM responses and add feedback loop.

---

