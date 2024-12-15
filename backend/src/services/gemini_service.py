# src/services/gemini_service.py
from langchain_google_genai import GoogleGenerativeAI
import google.generativeai as genai
import os
from dotenv import load_dotenv
from src.model.query_data import query_data

# Load environment variables
load_dotenv()

# Configure Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def clean_sql_response(sql_response: str) -> str:
    # Remove any backticks or extra formatting
    return sql_response.replace("```sql", "").replace("```", "").strip()

class GeminiService:
    def __init__(self):
        self.llm = GoogleGenerativeAI(model="gemini-pro", temperature=0.1)
        
        # System prompt to help Gemini generate SQL queries
        self.system_prompt = """
        You are a SQL expert. Given a question about sales data, generate a SQL query to answer it.
        The database has a orders table with these columns:
        ORDERID, ORDERNUMBER, QUANTITYORDERED, PRICEEACH, ORDERLINENUMBER, SALES, ORDERDATE, 
        STATUS, QTR_ID, MONTH_ID, YEAR_ID, PRODUCTLINE, MSRP, PRODUCTCODE, 
        CUSTOMERNAME, PHONE, ADDRESSLINE1, ADDRESSLINE2, CITY, STATE, POSTALCODE, 
        COUNTRY, TERRITORY, CONTACTLASTNAME, CONTACTFIRSTNAME, DEALSIZE

        Return only the SQL query without any additional explanation.
        Do not include ```sql or any other code formatting.
        Make sure to use proper SQL syntax for SQLite.
        The data is very large, so do not write a query which returns all rows.
        """

    async def query(self, question: str) -> str:
        try:
            # Enhanced parameter check prompt with column information
            parameter_check_prompt = f"""
            The database has a orders table with these columns:
            - ORDERID: Unique identifier for each order
            - ORDERNUMBER: Order number
            - QUANTITYORDERED: Number of items ordered
            - PRICEEACH: Price per item
            - ORDERLINENUMBER: Line number of the order
            - SALES: Total sales amount
            - ORDERDATE: Date of the order
            - STATUS: Order status
            - QTR_ID: Quarter ID
            - MONTH_ID: Month ID
            - YEAR_ID: Year of the order
            - PRODUCTLINE: Category of the product
            - MSRP: Manufacturer's Suggested Retail Price
            - PRODUCTCODE: Unique identifier for each product
            - CUSTOMERNAME: Name of the customer
            - PHONE: Customer's phone number
            - ADDRESSLINE1: Customer's primary address
            - ADDRESSLINE2: Customer's secondary address
            - CITY: Customer's city
            - STATE: Customer's state
            - POSTALCODE: Customer's postal code
            - COUNTRY: Customer's country
            - TERRITORY: Sales territory
            - CONTACTLASTNAME: Customer's contact last name
            - CONTACTFIRSTNAME: Customer's contact first name
            - DEALSIZE: Size of the deal (Small, Medium, Large)

            Analyze this question: "{question}"
            If it needs any specific parameters (like year, product line, country, etc.) that are not explicitly provided,
            list the required parameters and their corresponding table columns.
            Consider the context and what would make a comprehensive analysis.
            
            Format: If parameters needed, respond with:
            NEEDED|column1,column2,...
            If no parameters needed, respond with:
            NONE
            """
            
            params_needed = await self.llm.ainvoke(parameter_check_prompt)
            params_response = params_needed.strip().split('|')
            
            if params_response[0] == 'NEEDED':
                # Get the required columns
                needed_columns = params_response[1].split(',')
                
                # Build a dynamic query to get available values for each needed parameter
                available_params = {}
                for column in needed_columns:
                    param_query = f"SELECT DISTINCT {column.strip()} FROM orders ORDER BY {column.strip()}"
                    param_df = query_data(param_query)
                    available_params[column.strip()] = param_df[column.strip()].tolist()
                
                # Modify the original question to include all available parameter values
                param_context = []
                for column, values in available_params.items():
                    param_context.append(f"Available {column}: {', '.join(map(str, values))}")
                
                modified_question = f"""
                Given the following parameters:
                {'. '.join(param_context)}
                
                {question}
                Please provide a comprehensive analysis breaking down by {', '.join(needed_columns)}.
                """
                
                # Get the SQL query from Gemini for the modified question
                sql_response = await self.llm.ainvoke(
                    f"{self.system_prompt}\n\nQuestion: {modified_question}\nSQL query:"
                )
            else:
                # Process the original question as is
                sql_response = await self.llm.ainvoke(
                    f"{self.system_prompt}\n\nQuestion: {question}\nSQL query:"
                )
            
            # Use the response directly as it's already a string
            sql_query = clean_sql_response(sql_response.strip())
            
            print(f"Executing SQL query: {sql_query}")
            
            # Execute the SQL query
            result_df = query_data(sql_query)
            
            print(result_df)
            
            if result_df is None or result_df.empty:
                result_prompt = f"""
                Based on the given inputs:
                - **Question:** "{question}"
                - **SQL Query:** "{sql_query} (Generated by converting human language to SQL)"
                - **Observation:** The query returned no data.

                Generate a user-friendly response that clearly informs the user that no relevant data was found for their question.
                """
                final_response = await self.llm.ainvoke(result_prompt)
                return final_response.strip()
            
            # Format the results using Gemini
            result_prompt = f"""
            Based on the following:
            Question: {question}
            Data: {result_df.to_string()}
            
            Provide a clear, comprehensive analysis in proper Markdown format following these rules:
            1. Start with a level 2 heading "## Analysis"
            2. Use bullet points for listing key findings
            3. If there are numerical comparisons, present them in a Markdown table
            4. Use bold and italic text where appropriate for emphasis
            5. If there are distinct categories or time periods, use level 3 headings
            6. Include a brief summary at the end under a level 3 heading "### Summary"
            
            Make sure to break down the information appropriately and focus on significant insights and patterns.
            """
            
            final_response = await self.llm.ainvoke(result_prompt)
            return final_response.strip()

        except Exception as e:
            print(f"Error details: {str(e)}")
            return (
                "Sorry, something went wrong while processing your query. "
                "This might be due to an issue with the data or the system. "
                "Please try rephrasing your question or provide more details."
            )

# Initialize the service
gemini_service = GeminiService()