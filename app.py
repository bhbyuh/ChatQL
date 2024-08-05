import streamlit as st
import os
from langchain_community.llms import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
import pandas as pd
import regex as re
from DataBase import *

# Initialize session state variables if they don't exist
if 'extracted_query' not in st.session_state:
    st.session_state.extracted_query = None

if 'sample' not in st.session_state:
    st.session_state.sample = None

if 'query_file' not in st.session_state:
    st.session_state.query_file = []

databasename = 'Queryteste'
Dbpassword = '123'

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "123" #use generated API token
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

conn, cur = session_creation(databasename, Dbpassword)

st.title("Welcome to ChatQL")
st.sidebar.text("Welcome to talk with DataBase")
uploaded_file = st.sidebar.file_uploader("Choose a csv file")

query = st.text_area("Input text")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.session_state.sample = df.head(2)  # Save sample to session state

    st.sidebar.write(df)

    template = """Generate an SQL query to create a table based on the schema described below. 

    - Use `VARCHAR(size)` for all `VARCHAR` columns, including those intended for dates.
    - Use `INT`, `BIGINT`, and `FLOAT` data types only where absolutely necessary.
    - Avoid using `AUTO_INCREMENT` and `TINYINT`.
    - Name the columns exactly as specified in the schema description.
    - Use varchar(size) for date also
    - Generate an SQL query to insert data into the database based on this schema.
    - Don't make primary key

    Schema Description: {question}"""

    # Create prompt template
    prompt = PromptTemplate.from_template(template)

    repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        max_length=128,
        temperature=0.5,
        token=HUGGINGFACEHUB_API_TOKEN
    )

    # Use RunnableSequence for running prompt and llm
    llm_chain = prompt | llm

    # Run the LLM chain with inputs as a dictionary
    try:
        result = llm_chain.invoke({"question": df.columns})

        # regex pattern to extract the Create table query
        sql_pattern = re.compile(r"(?i)CREATE\s+TABLE\s+\w+\s*\((?:[^()]*|\([^()]*\))*\);", re.DOTALL | re.IGNORECASE)
        
        match = sql_pattern.search(result)
        if match:
            st.session_state.extracted_query = match.group(0)  # Save to session state
            table_creation(conn, cur, st.session_state.extracted_query)
        
        # Regex pattern to find the table name
        pattern = r"INSERT\s+INTO\s+(\w+)"
        match = re.search(pattern, result)

        if match:
            table_name = match.group(1)

        insert_data(cur, conn, df, result, table_name)

    except Exception as e:
        st.error(f"Error: {str(e)}")

if st.button("Press"):
    if query.strip() == "":
        st.error("Please enter a question.")
    else:
        if st.session_state.extracted_query is None:
            st.error("No extracted query found. Please upload a file first.")
        else:
            if st.session_state.sample is None:
                st.error("No sample data available. Please upload a file first.")
            else:
                # Define prompt template with placeholders for inputs
                template = """Generate an SQL query for the following request: "{question}". Use the specified table and column names exactly as given in the schema: "{schema}" sample records are like {record} . Provide only the SQL query without additional instructions."""

                prompt = PromptTemplate.from_template(template)

                repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

                
                llm = HuggingFaceEndpoint(
                    repo_id=repo_id,
                    max_length=128,  
                    temperature=0.5, 
                    token=HUGGINGFACEHUB_API_TOKEN
                )

                llm_chain = prompt | llm

                try:
                    result = llm_chain.invoke({"question": query, "schema": st.session_state.extracted_query, "record": st.session_state.sample})

                    pattern = r"SELECT\b.*?;"

                    # Extract the query
                    query_match = re.search(pattern, result, re.IGNORECASE | re.DOTALL)
                    if query_match:
                        query = query_match.group()
                        st.session_state.query_file.append(query)  # Use session state
                        rows = get_data(cur, query)
                        if rows:
                            columns = [desc[0] for desc in cur.description]  # Get column names
                            df = pd.DataFrame(rows, columns=columns)
                            st.write(df)
                        else:
                            st.write("No data returned for the query.")
                    else:
                        st.error("No valid SELECT query found in the generated result.")

                except Exception as e:
                    st.error(f"Error: {str(e)}")

if st.button("Generate Query File"):
    file_path = 'Queries.txt'

    # Writing the list data to a text file
    with open(file_path, 'w') as file:
        for item in st.session_state.query_file:
            file.write(item + '\n\n\n')

    st.success(f"Query file '{file_path}' generated successfully.")
