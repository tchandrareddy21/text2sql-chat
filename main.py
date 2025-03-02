import streamlit as st
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Text to SQL Chat", page_icon="🛢️")
st.title("🛢️ Text to SQL Chat")

INJECTION_WARNING = """ 
🚨 **Warning:** SQL agent can be vulnerable to prompt injection.  
Use a DB role with limited permissions. Read more [here](https://python.langchain.com/docs/security).
"""

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

# Sidebar - Database Selection
radio_opt = ["Use SQLITE3 Database - Student.db", "Connect to your Database"]
selected_opt = st.sidebar.radio(label="Choose the DB which you want to chat with", options=radio_opt)

# Initialize MySQL connection variables as None
mysql_host = mysql_user = mysql_password = mysql_db = None

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide SQL Host Name", placeholder="localhost:3306")
    mysql_user = st.sidebar.text_input("MYSQL username", placeholder="admin")
    mysql_password = st.sidebar.text_input("MYSQL password", type="password", placeholder="password")
    mysql_db = st.sidebar.text_input("MYSQL Database name", placeholder="DB_NAME")
else:
    db_uri = LOCALDB

# Sidebar - Groq API Key
groq_api_key = st.sidebar.text_input("🔑 Please enter GROQ API key:", type="password")

if not groq_api_key:
    st.info("⚠️ Enter your GROQ API key to continue.")
    st.stop()

# Initialize LLM Model
try:
    llm = ChatGroq(
        model="qwen-2.5-coder-32b",
        api_key=groq_api_key,
        streaming=True,
    )
except Exception as e:
    st.error(f"🚨 Error initializing LLM: {e}")
    st.stop()


@st.cache_resource(ttl="2h")
def get_database_connection(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        db_file_path = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{db_file_path}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("❌ Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase.from_uri(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")


# Pass MySQL variables safely
db = get_database_connection(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)

# Initialize SQLDatabaseToolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Initialize chat history
if "messages" not in st.session_state or st.sidebar.button("🧹 Clear Chat History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "👋 How can I help you?"}]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Get user query
user_query = st.chat_input(placeholder="💬 Ask me anything about your database...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    # Create the SQL Agent
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handling_parsing_errors=True
    )

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = agent.invoke(user_query, callbacks=[streamlit_callback])

        # Extract response text
        if isinstance(response, dict):
            response_text = response.get("output", str(response))
        else:
            response_text = str(response)

        st.session_state.messages.append({"role": "assistant", "content": response_text})

        # Display response beautifully
        if response_text.startswith("{") or response_text.startswith("["):
            # JSON output
            st.json(response_text)
        elif "SELECT" in user_query.upper():
            # SQL Query Result - Try to show as a table
            try:
                result_df = pd.DataFrame(eval(response_text))
                st.dataframe(result_df.style.set_properties(**{'background-color': 'black', 'color': 'white'}))
            except Exception:
                st.code(response_text, language="sql")
        else:
            # General text response
            st.markdown(f"💡 **Response:**\n\n{response_text}", unsafe_allow_html=True)
