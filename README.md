# CSV to PostgreSQL with LLM-Powered Query Interaction

This repository demonstrates a **Streamlit-based application** that allows users to upload a CSV file, store it in a PostgreSQL database, and interact with the data using natural language queries. The app uses **Gemini LLM** to convert user queries into SQL statements, which are then executed on the database. Results are displayed directly within the Streamlit interface.

## Tools Used
- **Streamlit**: For creating an interactive web application.
- **PostgreSQL**: To store and query the uploaded CSV data.
- **Gemini LLM**: To interpret user queries and convert them into SQL commands.
- **Regex**: For query validation and preprocessing.
- **Pandas**: For CSV file handling and preprocessing before storage.

## Features
1. **CSV Upload**:
   - Users can upload a CSV file via the Streamlit interface.
   - The data is processed and stored in a PostgreSQL database.
   
2. **Natural Language Querying**:
   - Users can type natural language queries like:
     - "Show me the maximum value in column X."
     - "Retrieve the first 300 rows of data."
   - These queries are processed by **Gemini LLM**, converted into SQL, and executed against the database.

3. **Query Results**:
   - The results of the SQL query are displayed in a tabular format on the Streamlit interface.

## Workflow
1. **CSV File Upload**:
   - The user uploads a CSV file through the Streamlit app.
   - The file is read using **Pandas** and the schema is generated dynamically for PostgreSQL.
   - The data is inserted into a PostgreSQL table.

2. **Natural Language Query to SQL**:
   - The user enters a natural language query.
   - **Gemini LLM** interprets the query and generates an SQL statement.
   - The SQL query is validated using **regex** to ensure security and accuracy.

3. **Execute and Display Results**:
   - The validated SQL query is executed on the PostgreSQL database.
   - The results are retrieved and displayed in the Streamlit app.
