# Real Estate Chatbot 🏠💬

A smart chatbot that helps users find real estate properties using natural language queries, powered by Gemini AI and web scraping.

## Features ✨

- **Natural Language Processing**: Understands user queries like "Find 2-bedroom villas in Dubai under 2 million"
- **Property Database**: Scrapes and stores property data from Zameen.com
- **Smart Search**: Converts natural language to database queries
- **Chat Interface**: Interactive UI with conversation history
- **Automatic Updates**: Periodic web scraping to keep property data fresh

## Technologies Used 🛠️

- **Python** (Flask backend)
- **Gemini AI** (Natural language processing)
- **SQLite** (Database)
- **Bootstrap 5** (Frontend UI)
- **BeautifulSoup** (Web scraping)

## Project Structure 📂

realestate-chatbot/
├── app/
│ ├── init.py # Flask application factory
│ ├── models.py # Database models
│ ├── routes.py # API routes
│ ├── scraper.py # Property data scraper
│ ├── utils/
│ │ ├── ai_helper.py # Gemini AI integration
│ │ └── db_helper.py # Database operations
│ └── templates/
│ └── index.html # Chat interface
├── static/ # CSS/JS files
├── config.py # Configuration settings
├── requirements.txt # Python dependencies
└── run.py # Application entry point

text

## Installation 💻

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/realestate-chatbot.git
   cd realestate-chatbot
Set up virtual environment

bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Set up environment variables
Create a .env file with your Gemini API key:

text
GEMINI_API_KEY=your_api_key_here
Running the Application 🚀
bash
python run.py
The application will be available at http://localhost:5000

Configuration ⚙️
Modify config.py to change:

Database settings

Scraping frequency

Gemini model configuration

How It Works 🔍
User enters natural language query

Gemini AI converts query to database filters

System searches property database

Results are displayed in chat interface

Background scraper periodically updates property data

Contributing 🤝
Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

License 📜
This project is licensed under the MIT License - see the LICENSE file for details.

Screenshots 🖼️
https://screenshots/chat-interface.png
https://screenshots/property-results.png

Contact 📧
For questions or support, contact: your.email@example.com

text

### Additional recommendations:

1. Create a `screenshots` folder and add actual screenshots of your application
2. Add a `LICENSE` file if you want to open-source the project
3. Include a `.gitignore` file with:
.venv/
pycache/
*.pyc
.env
*.sqlite

text

This README provides:
- Clear project description
- Installation instructions
- Usage guide
- Technical documentation
- Contribution guidelines
- Visual examples

You can customize the contact information, license, and screenshots as needed for your specific project.
