
# NLPChatBot



## FAQ

#### Question 1

Answer 1

#### Question 2

Answer 2


## Authors

- [@sharathm2](https://www.github.com/sharathm2)


## Installation

- HOW TO RUN THIS BOT

- Clone Repo
- Create python 3.11 virtual environment
- Run pip install for requirements.txt
- Run "python -m spacy download en_core_web_sm" in the virtual environment
- Run "python scripts/train_transfomers.py"
- Run "python main.py"


- If you want to deploy the API, just run "uvicorn app.main:app --reload"

- In order to run the frontend, run "npm run dev" and navigate to "localhost:5173".

## REMEMBER, THE BACKEND SHOULD BE RUN FROM WITHIN THE ACTIVATED VENV, THE FRONTEND SHOULD BE RUN FROM OUTSIDE THE VENV IN THE FRONTEND DIR

- I have uploaded my changes for implemented DB storage, so I will soon also release my Supabase DB Schema so my RLS policies are also open source
    