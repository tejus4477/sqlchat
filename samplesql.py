from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains import create_sql_query_chain
from langchain.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType

import mysql.connector  # Ensure you have this package installed

llms = Ollama(model="llama3")
template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""
prompt_response = ChatPromptTemplate.from_template(template)

# Function to get schema
def get_schema(db):
    schema = db.get_table_info()
    return schema

# Function to run query 
def run_query(query):
    return db.run(query)

db_user = "root"
db_password = "rufalh"
db_host = "localhost:3306"
db_name = "loans"
 
# Create the MySQL connection string
mysql_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
 
# Connect to the MySQL database
db = SQLDatabase.from_uri(mysql_uri) 
#print(db.table_info)

agent_executor = create_sql_agent(llms, db = db, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose = True)
agent_executor.invoke("How many loans have emi amount higher than 60000")