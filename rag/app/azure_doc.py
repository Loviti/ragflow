#
#  Copyright 2025 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import io
import logging
from io import BytesIO
from PIL import Image

from api.db import LLMType, ParserType
from api.db.services.llm_service import LLMBundle
from rag.nlp import tokenize

def chunk(filename, binary, tenant_id, lang, callback=None, **kwargs):
    """Process a document using Azure Document Intelligence API.
    
    This function processes documents (images or PDFs) using the Azure
    Document Intelligence API for OCR and document understanding.
    
    Args:
        filename (str): Name of the file being processed
        binary (bytes): Binary content of the file
        tenant_id (str): ID of the tenant
        lang (str): Language code (e.g., "English")
        callback (function, optional): Progress callback function
        **kwargs: Additional keyword arguments
    
    Returns:
        list: List of document chunks with processed content
    """
    try:
        if callback:
            callback(0.2, "Starting Azure Document Intelligence processing...")
        
        # Create the document object to store results
        doc = {
            "docnm_kwd": filename
        }
        
        # Initialize Azure Document Intelligence client
        azure_doc_intel = LLMBundle(tenant_id, LLMType.IMAGE2TEXT, lang=lang, 
                                  llm_name="prebuilt-document")
        
        if callback:
            callback(0.4, "Analyzing document with Azure Document Intelligence...")
        
        # Process the document
        extracted_text, _ = azure_doc_intel.describe(binary)
        
        if callback:
            callback(0.7, f"Document processed successfully. Extracted {len(extracted_text.split())} words.")
        
        # Check if we got any text
        if not extracted_text or len(extracted_text.split()) < 5:
            if callback:
                callback(prog=-1, msg="Azure Document Intelligence couldn't extract text from the document.")
            return []
        
        # Process the extracted text
        eng = lang.lower() == "english"
        tokenize(doc, extracted_text, eng)
        
        if callback:
            callback(0.9, "Document processing completed successfully.")
        
        return [doc]
        
    except Exception as e:
        logging.exception(f"Azure Document Intelligence processing error: {str(e)}")
        if callback:
            callback(prog=-1, msg=f"Error processing document: {str(e)}")
        return [] 