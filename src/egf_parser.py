"""
parser.py

This module provides functionality to extract bitmap images from .egf files,
specifically targeting resources within PE (Portable Executable) files.
"""

import pefile
import struct

def extract_bitmaps_from_pe(file_path):
    """
    Extract BMP resources from a given PE file.
    
    Args:
        file_path (str): Path to the PE file.

    Returns:
        dict: Dictionary mapping resource IDs to BMP data.
    """
    # Initialize PE file object
    pe = pefile.PE(file_path)
    
    # Dictionary to hold the extracted bitmap data
    extracted_data = {}
    
    # Loop through the resource directory entries
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            if hasattr(resource_type, 'directory'):
                for resource_id_entry in resource_type.directory.entries:
                    # Check for valid resource ID and directory
                    if hasattr(resource_id_entry, 'id') and hasattr(resource_id_entry, 'directory'):
                        resource_id = resource_id_entry.id
                        data_entry = resource_id_entry.directory.entries[0]
                        # Extract the offset and size of the resource data
                        data_rva = data_entry.data.struct.OffsetToData
                        size = data_entry.data.struct.Size
                        raw_data = pe.get_memory_mapped_image()[data_rva:data_rva+size]

                        # Save
                        extracted_data[resource_id] = raw_data

    # Return the dictionary of extracted bitmap data
    return extracted_data