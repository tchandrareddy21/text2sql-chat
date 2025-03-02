<h1 align="center">Text2Query Chat</h1>

## Problem Overview
- Structured databases require users to write SQL queries to retrieve information. However, many users are not proficient in SQL. This project, Text2Query Chat, allows users to interact with a database using natural language. The system translates text-based queries into SQL commands and fetches relevant results, making database interaction seamless and user-friendly.

## Architecture
![Text2SQl Chat - Project Workflow](flowchart/Text2SQL%20Chat%20Workflow.png)
### Workflow:
1. User inputs a natural language query.
2. The system processes the query using an LLM (Large Language Model).
3. The LLM generates a SQL query based on the user’s input.
4. The SQL query is executed on the selected database (SQLite3/MySQL).
5. The retrieved data is formatted and displayed in a user-friendly manner using Streamlit.

### Components:
1. **Frontend**: Streamlit-based interactive UI
2. **Backend**: LangChain-powered SQL Agent
3. **Database Support**: SQLite3 & MySQL
4. **LLM Integration**: Groq API for text-to-SQL conversion
5. **Security Measures**: Role-based DB access to prevent SQL injection

##  Technologies Used
1. Python
2. Streamlit (Web UI framework)
3. LangChain (For AI-powered query generation)
4. SQLite3 & MySQL (Supported databases)
5. Groq API (LLM-based text processing)

## How to Run Locally

### Prerequisite:
- Create one API key from [GROQ](https://console.groq.com/keys)
#### Step 1: Clone the repository:
```pycon
git clone https://github.com/tchandrareddy21/text2sql-chat.git
```
#### Step 2: Create a virtual environment and activate it:
```pycon
conda create -n [env-name] python=3.11 -y
conda actuvate [env-name]
```
#### Step 3: Install dependencies
```pycon
pip install -r requirements.txt
```

#### Step 4: Run the application:
```pycon
streamlit run app.py
```

## How to Use Streamlit App Published in Streamlit Cloud
1. Open the deployed Streamlit link: Streamlit Cloud App
2. Select the database (SQLite3 or MySQL) from the sidebar.
3. If using MySQL, provide the database connection details.
4. Enter a text-based query (e.g., "Show me the students with marks above 80").

The app will convert the query into SQL and display the results in a tabular format.
- Go to the below URL and follow the Usage Guide below:

[Text to SQL Chat - Live APP](https://text2sql-chat.streamlit.app/)

## Project Screenshots
### Home Page:
![Home Page](Screenshots/Home%20page.png)
### Database Selection:
![Database Selection](Screenshots/DB%20selection.png)
### Query Execution:
![Query Execution](Screenshots/Cloud%20sqllite%20query.png)
![Query Execution](Screenshots/Localdb%20output%20with%20multipe%20tables.png)
