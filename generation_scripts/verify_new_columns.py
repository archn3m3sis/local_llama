#!/usr/bin/env python3
"""Verify the new columns were added to the software catalog table."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, text

load_dotenv()

def verify_columns():
    """Check if the new columns exist in the software catalog table."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("Database URL not found in environment variables")
        return
    
    engine = create_engine(database_url)
    
    with Session(engine) as session:
        # Check column existence
        result = session.exec(text("""
            SELECT 
                COLUMN_NAME,
                DATA_TYPE,
                IS_NULLABLE
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'softwarecatalog' 
            AND COLUMN_NAME IN ('compliance_status', 'army_gold_master')
            ORDER BY COLUMN_NAME
        """)).all()
        
        print("Column check results:")
        print("-" * 50)
        for col_name, data_type, is_nullable in result:
            print(f"{col_name:<20} | Type: {data_type:<15} | Nullable: {is_nullable}")
        
        if len(result) == 2:
            print("\n✓ Both new columns exist in the database!")
        else:
            print("\n✗ Some columns are missing!")
            
        # Test query with new columns
        print("\nTesting query with new columns...")
        try:
            test_result = session.exec(text("""
                SELECT TOP 1 
                    sw_name,
                    compliance_status,
                    army_gold_master
                FROM softwarecatalog
            """)).first()
            
            if test_result:
                print("Query successful!")
                print(f"Sample: {test_result[0]}, compliance_status={test_result[1]}, army_gold_master={test_result[2]}")
            else:
                print("No data found")
                
        except Exception as e:
            print(f"Query failed: {e}")

if __name__ == "__main__":
    verify_columns()