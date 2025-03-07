import os
import logging
from typing import Union
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile, HTTPException
from pypdf import PdfReader

from app.core.config import settings

logger = logging.getLogger(__name__)


def validate_file_extension(filename: str) -> bool:
    """
    Validate if the file has an allowed extension.
    
    Args:
        filename: The name of the file to validate
        
    Returns:
        bool: True if the file extension is allowed, False otherwise
    """
    return filename.lower().endswith(tuple(f".{ext}" for ext in settings.ALLOWED_EXTENSIONS))


def validate_file_size(file_size: int) -> bool:
    """
    Validate if the file size is within the allowed limit.
    
    Args:
        file_size: The size of the file in bytes
        
    Returns:
        bool: True if the file size is within limits, False otherwise
    """
    return file_size <= settings.MAX_UPLOAD_SIZE


async def save_upload_file_tmp(upload_file: UploadFile) -> Path:
    """
    Save an upload file temporarily and return the path.
    
    Args:
        upload_file: The uploaded file
        
    Returns:
        Path: Path to the saved temporary file
        
    Raises:
        HTTPException: If there's an error saving the file
    """
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await upload_file.read()
            tmp.write(content)
            tmp_path = Path(tmp.name)
        return tmp_path
    except Exception as e:
        logger.error(f"Error saving upload file: {e}")
        raise HTTPException(status_code=500, detail="Error saving upload file")


def extract_text_from_pdf(file_path: Union[str, Path]) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
        
    Raises:
        HTTPException: If there's an error reading the PDF
    """
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=422, detail="Error extracting text from PDF file")
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.unlink(file_path)


async def process_cv_file(upload_file: UploadFile) -> str:
    """
    Process an uploaded CV file, validating and extracting text.
    
    Args:
        upload_file: The uploaded CV file
        
    Returns:
        str: Extracted text content from the CV
        
    Raises:
        HTTPException: If the file is invalid or processing fails
    """
    if not validate_file_extension(upload_file.filename):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file format. Allowed formats: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    file_size = 0
    file_content = await upload_file.read()
    file_size = len(file_content)
    await upload_file.seek(0)  # Reset file pointer
    
    if not validate_file_size(file_size):
        max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        raise HTTPException(
            status_code=400, 
            detail=f"File too large. Maximum size allowed: {max_size_mb} MB"
        )
    
    tmp_path = await save_upload_file_tmp(upload_file)
    
    text_content = extract_text_from_pdf(tmp_path)
    
    if not text_content.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from the PDF file")
    
    return text_content 