from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime
import uuid

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Order details
    order_number = Column(Integer, nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    price_each = Column(Float, nullable=False)
    order_line_number = Column(Integer, nullable=False)
    sales = Column(Float, nullable=False)
    order_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    
    # Time dimensions
    qtr_id = Column(Integer, nullable=False)
    month_id = Column(Integer, nullable=False)
    year_id = Column(Integer, nullable=False)
    
    # Product details
    product_line = Column(String(50), nullable=False)
    msrp = Column(Float, nullable=False)
    product_code = Column(String(20), nullable=False)
    
    # Customer details
    customer_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address_line1 = Column(String(100))
    address_line2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    postal_code = Column(String(20))
    country = Column(String(50))
    territory = Column(String(50))
    contact_last_name = Column(String(50))
    contact_first_name = Column(String(50))
    deal_size = Column(String(20))

def create_database():
    # Create SQLite database
    engine = create_engine('sqlite:///src/model/sales_data.db', echo=True)
    Base.metadata.create_all(engine)
    return engine

def save_data_to_db(csv_file_path):
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    
    # Create database and get engine
    engine = create_database()
    
    # Convert date string to datetime
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    
    if 'ORDERID' in df.columns:
        df['ORDERID'] = df['ORDERID'].apply(lambda x: str(uuid.UUID(x)) if not pd.isna(x) else None)
    
    # Convert DataFrame to SQL
    df.to_sql('orders', engine, if_exists='replace', index=False,
              dtype={
                  'ORDERID': String(36),
                  'ORDERNUMBER': Integer,
                  'QUANTITYORDERED': Integer,
                  'PRICEEACH': Float,
                  'ORDERLINENUMBER': Integer,
                  'SALES': Float,
                  'ORDERDATE': Date,
                  'STATUS': String(20),
                  'QTR_ID': Integer,
                  'MONTH_ID': Integer,
                  'YEAR_ID': Integer,
                  'PRODUCTLINE': String(50),
                  'MSRP': Float,
                  'PRODUCTCODE': String(20),
                  'CUSTOMERNAME': String(100),
                  'PHONE': String(20),
                  'ADDRESSLINE1': String(100),
                  'ADDRESSLINE2': String(100),
                  'CITY': String(50),
                  'STATE': String(50),
                  'POSTALCODE': String(20),
                  'COUNTRY': String(50),
                  'TERRITORY': String(50),
                  'CONTACTLASTNAME': String(50),
                  'CONTACTFIRSTNAME': String(50),
                  'DEALSIZE': String(20)
              })

if __name__ == "__main__":
    # Example usage
    save_data_to_db('src/datasets/sales_data_sample_cleaned.csv')