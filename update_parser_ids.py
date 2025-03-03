#!/usr/bin/env python3

"""
Script to update tenant parser_ids to include Azure Document Intelligence parser.
This adds the new parser type to the existing parser_ids list for all tenants.
"""

import os
import sys

# Add the current directory to the path so we can import the app modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from api.db.services.user_service import TenantService
from api.db import DB

def update_parser_ids():
    """Update parser_ids for all tenants to include Azure Document Intelligence."""
    try:
        # Connect to the database
        DB.connect()
        
        # This query will update all tenants
        # It appends ",azure_doc:Azure Document Intelligence" to the existing parser_ids
        result = TenantService.filter_update(
            [1 == 1],  # This is equivalent to "WHERE TRUE" - update all records
            {"parser_ids": DB.fn.CONCAT(
                TenantService.model.parser_ids, 
                ",azure_doc:Azure Document Intelligence"
            )}
        )
        
        print(f"Updated {result} tenant records to include Azure Document Intelligence parser")
        return True
    except Exception as e:
        print(f"Error updating parser_ids: {e}")
        return False
    finally:
        # Close the database connection
        if not DB.is_closed():
            DB.close()

if __name__ == "__main__":
    success = update_parser_ids()
    sys.exit(0 if success else 1) 