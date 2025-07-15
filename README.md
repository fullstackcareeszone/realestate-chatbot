# 🏠 Fake Property Detection System

## 📌 Project Overview

**Fake Property Detection System** is an intelligent, AI-powered web application designed to validate the authenticity of online property listings. Targeted primarily at listings from platforms like **Zameen.com**, this system helps users detect fraudulent or misleading property ads by analyzing their content, images, and metadata using machine learning and large language models (LLMs).

---

## 🔍 Key Features

- ✅ **Fake Listing Detection** – Automatically identifies suspicious or potentially fake property listings using ML algorithms.
- 🧠 **LLM-Powered Analysis** – Utilizes Gemini API and Hugging Face models to evaluate property descriptions, metadata, and other textual cues.
- 🖼️ **Fake Image Detection** – Flags AI-generated or manipulated images to enhance listing credibility.
- 🤖 **AI Chatbot Assistant** – Gemini-based chatbot answers property-related queries and explains listing authenticity.
- 🔗 **URL-Based Input** – Users paste Zameen.com property links for real-time analysis.
- 👥 **Role-Based Access** – Includes Admin and Verified User roles with distinct permissions and dashboards.

---

## 🛠️ Tech Stack

| Component        | Technology                         |
|------------------|-------------------------------------|
| **Backend**      | Python, Flask                       |
| **ML/AI Models** | Gemini API, Hugging Face Transformers |
| **Web Scraping** | BeautifulSoup, Requests (Zameen.com) |
| **Database**     | PostgreSQL                          |
| **Chatbot**      | Gemini API                          |
| **Hosting**      | Render / Heroku / Replit *(optional)* |

---

## ⚙️ System Workflow

1. **User Authentication** – Admin or Verified User logs in to the system.
2. **Paste Property URL** – User submits a property link from Zameen.com.
3. **Web Scraping** – System extracts key data and images from the listing.
4. **ML Model Analysis** – Models evaluate textual content, image metadata, and structure.
5. **Chatbot Interaction** – User can ask questions about the property and get AI-based feedback.
6. **Prediction Output** – System displays whether the listing is *Fake* or *Genuine*.

---

## 🔐 User Roles

- 🛠️ **Admin**:
  - Manage all users.
  - Monitor submitted listings and model activity logs.
  - Maintain and update system settings.

- ✅ **Verified User**:
  - Paste and analyze property links.
  - Access chatbot for property information.
  - View personal submission history.

> ℹ️ *Guest user functionality may be introduced in future versions.*

---

## 📈 Planned Enhancements

- 📝 **Suspicious Listing Reporting** – Allow users to flag or report questionable properties.
- 🧠 **Advanced NLP Models** – Enhance detection accuracy using fraud pattern recognition and deeper context analysis.
- 🔗 **Blockchain Integration** – Verify property documentation authenticity using decentralized systems.
- 📂 **Manual Uploads** – Support file-based data input (e.g., CSV, Excel).
- 🔔 **Real-Time Notifications** – Email or SMS alerts for users when fake properties are detected.

---

## 🚀 How to Run the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/fake-property-detection.git
   cd fake-property-detection
