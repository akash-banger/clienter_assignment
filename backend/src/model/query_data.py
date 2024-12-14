from sqlalchemy import create_engine, text
import pandas as pd
import sqlparse

def get_db_connection():
    """Create and return database connection"""
    engine = create_engine('sqlite:///src/model/sales_data.db')
    return engine

def validate_query(query):
    """Validate SQL query"""
    try:
        # Check if query is empty or None
        if not query or not query.strip():
            return False, "Query is empty"
            
        # Parse the SQL query
        parsed = sqlparse.parse(query)
        if not parsed:
            return False, "Invalid SQL syntax"
            
        # Check for dangerous keywords (basic SQL injection prevention)
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'MODIFY']
        upper_query = query.upper()
        for keyword in dangerous_keywords:
            if keyword in upper_query:
                return False, f"Dangerous operation '{keyword}' not allowed"
                
        return True, "Query is valid"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def query_data(query):
    """Execute SQL query and return results as pandas DataFrame"""
    try:
        # Validate query first
        is_valid, message = validate_query(query)
        if not is_valid:
            print(f"Query validation failed: {message}")
            return f"Query validation failed: {message}"

        # Create engine and connect
        engine = get_db_connection()
        with engine.connect() as connection:
            # Execute query using pandas with SQLAlchemy text clause
            result = pd.read_sql(text(query), connection)
            return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None