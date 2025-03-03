#!/usr/bin/env python3

"""
Script to update tenant parser_ids to include Azure Document Intelligence parser.
This script adds 'azure_doc:Azure Document Intelligence' to the existing parser_ids list for all tenants.
Run this script once to update the existing database entries.
"""

import os
import sys

# Add the current directory to the path so we can import the app modules
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from api.db.services.user_service import TenantService
from api.db import DB

def update_tenant_parser_ids():
    """Update parser_ids for all tenants to include Azure Document Intelligence."""
    try:
        # Connect to the database
        if DB.is_closed():
            DB.connect()
        
        # Get all tenants
        tenants = TenantService.filter_query([1 == 1])
        updated_count = 0
        
        for tenant in tenants:
            # Only add azure_doc if it's not already in the parser_ids
            if "azure_doc:Azure Document Intelligence" not in tenant.parser_ids:
                # Update the parser_ids to include Azure Document Intelligence
                new_parser_ids = tenant.parser_ids + ",azure_doc:Azure Document Intelligence"
                TenantService.update_by_id(tenant.id, {"parser_ids": new_parser_ids})
                updated_count += 1
        
        print(f"Updated {updated_count} tenant records to include Azure Document Intelligence parser")
        return True
    except Exception as e:
        print(f"Error updating parser_ids: {e}")
        return False
    finally:
        # Close the database connection
        if not DB.is_closed():
            DB.close()

if __name__ == "__main__":
    success = update_tenant_parser_ids()
    sys.exit(0 if success else 1) 