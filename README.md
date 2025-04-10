# 🤖 NLPChatBot

An end-to-end Natural Language Processing chatbot with intent classification, to-do management, search, math evaluation, and secure user-based storage using Supabase. Built with Python, FastAPI, and a React frontend.

---

## 🚀 Features

- 💬 Intent classification using a custom-trained Transformer
- 🧠 Rule-based and ML-based response handling
- 🗂️ To-do list management with database storage
- 📄 File upload support (PDF, etc.)
- 📡 RESTful API powered by FastAPI
- 🔐 Authenticated user support with Supabase Auth and RLS
- 🧪 Test suite for backend endpoints

---

## 🛠️ Tech Stack

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: Python + FastAPI
- **Model**: Transformers + spaCy
- **Database**: Supabase (PostgreSQL with RLS)
- **Deployment-ready** with `.env` config

---

## 📁 Project Structure

NLPChatBot/ │ ├── app/ # FastAPI routes ├── model/ # ML logic and core chatbot engine ├── data/ # Local data (ignored via .gitignore) ├── frontend/ # React-based frontend ├── scripts/ # Training and setup scripts ├── .env # Secret keys (not included) └── main.py # Entry point for chatbot

===

## 🧪 Installation & Usage

### 🔧 Backend Setup

```bash
# 1. Clone the repository
git clone https://github.com/sharathm2020/NLPChatBot.git
cd NLPChatBot

# 2. Create and activate virtual environment (Python 3.11)
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Train the transformer intent classifier
python scripts/train_transformers.py

# 6. Run the bot (console mode or API)
python main.py
# OR run the API server
uvicorn app.main:app --reload


### FRONTEND SETUP

# In a separate terminal
- cd frontend
- npm install
- npm run dev


### SETTING UP YOUR .ENV CONFIG

- SUPABASE_URL=your_supabase_url
- SUPABASE_KEY=your_supabase_anon_key
- WEATHER_API_KEY=your_weather_api_key (optional)
- NEWS_API_KEY=your_news_api_key (optional)


### NOTES ABOUT SUPABASE
- RLS (Row-Level Security) is enforced

- You will need to set up your own Supabase tables for chat_history, todos, and users

- Full schema + SQL setup script coming soon!

---

## FAQ 

#### How is the chatbot trained?

A: A custom intent classification model using HuggingFace Transformers and labeled intents.

#### Can I use this bot with my own Supabase project?

A: Yes! Just set up the required tables and update your .env file.

## Authors

- [@sharathm2020](https://www.github.com/sharathm2020)