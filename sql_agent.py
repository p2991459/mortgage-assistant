import os

from langchain.prompts.prompt import PromptTemplate
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from dotenv import load_dotenv
load_dotenv()
_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.  If you find SQL syntax is incorrect than reply "Sytax error"
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"  
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

In case the empty query returned you should reply "Got empty result", if the question is not related to the database query than you should reply "It is general question"
Only use the following tables:

{table_info}

Always give the best answer from the query

For ex:
If the user question is question: I want to buy a property in Barbados. What are the terms and conditions?
Than you should answer:
To buy a property in Barbados you need a deposit of at least 30% (70% LTV)
The minimum loan size is $250,000
They are available for Residential, Holiday homes, Land Purchase, Self Build, Bridging Loans, Purchase and renovation
The lowest interest rate available, is currently 3.921%. It is a tracker mortgage a 1% fee, and no Early Redemption Charge (ERC).

Always follow the above question and answer format, don't just give the result of query, You should be able to generate the best answer out of it.

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)
DB_USER = os.getenv("DATABASE_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST_NAME")
db = SQLDatabase.from_uri(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/mortgage_db")

llm = OpenAI(temperature=0, verbose=True,model_name="gpt-3.5-turbo")
db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=PROMPT, verbose=True)

# print(db_chain.run("What is cricket match"))

