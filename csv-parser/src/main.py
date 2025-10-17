"""
FastAPI REST API for CSV Parser Microservice
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path
import os
from dotenv import load_dotenv

from parser import CSVParser

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("API_TITLE", "CSV Parser Microservice"),
    version=os.getenv("API_VERSION", "1.0.0"),
    description="Microservice for parsing, validating, and transforming CSV files"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MAX_FILE_SIZE = int(os.getenv("CSV_MAX_FILE_SIZE", 10485760))  # 10MB default
UPLOAD_DIR = Path(os.getenv("CSV_UPLOAD_DIR", "./uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)


# Pydantic models
class ParseOptions(BaseModel):
    auto_detect: bool = Field(True, description="Auto-detect encoding and delimiter")
    encoding: Optional[str] = Field(None, description="Character encoding")
    delimiter: Optional[str] = Field(None, description="CSV delimiter")
    chunk_size: Optional[int] = Field(None, description="Chunk size for large files")


class CleaningOptions(BaseModel):
    remove_empty_rows: bool = Field(False, description="Remove completely empty rows")
    remove_duplicates: bool = Field(False, description="Remove duplicate rows")
    trim_whitespace: bool = Field(True, description="Trim whitespace from strings")
    lowercase_columns: bool = Field(False, description="Convert column names to lowercase")
    fill_missing_value: Optional[Any] = Field(None, description="Value to fill missing data")


class ParseResponse(BaseModel):
    status: str
    message: str
    data: Optional[List[Dict[str, Any]]] = None
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    columns: Optional[List[str]] = None


class ValidationResponse(BaseModel):
    is_valid: bool
    row_count: int
    column_count: int
    columns: List[str]
    missing_values: Dict[str, int]
    data_types: Dict[str, str]
    errors: List[str]


class SchemaResponse(BaseModel):
    columns: List[Dict[str, Any]]
    row_count: int
    estimated_size_mb: float


@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "CSV Parser Microservice",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "parse": "/api/csv/parse",
            "validate": "/api/csv/validate",
            "schema": "/api/csv/schema",
            "transform": "/api/csv/transform"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/csv/parse", response_model=ParseResponse)
async def parse_csv(
    file: UploadFile = File(...),
    auto_detect: bool = Query(True, description="Auto-detect encoding and delimiter"),
    encoding: Optional[str] = Query(None, description="Character encoding"),
    delimiter: Optional[str] = Query(None, description="CSV delimiter"),
    chunk_size: Optional[int] = Query(None, description="Chunk size for large files")
):
    """
    Parse a CSV file and return its contents as JSON
    """
    try:
        # Validate file extension
        if not file.filename.endswith(('.csv', '.txt', '.tsv')):
            raise HTTPException(status_code=400, detail="Invalid file type. Only CSV, TXT, and TSV files are allowed.")
        
        # Read file content
        content = await file.read()
        
        # Check file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Initialize parser
        parser = CSVParser(
            encoding=encoding or 'utf-8',
            delimiter=delimiter or ','
        )
        
        # Parse the file
        df = parser.parse_file(content, auto_detect=auto_detect, chunk_size=chunk_size)
        
        # Transform to JSON
        data = parser.transform_to_json(df)
        
        return ParseResponse(
            status="success",
            message="CSV file parsed successfully",
            data=data,
            row_count=len(df),
            column_count=len(df.columns),
            columns=list(df.columns)
        )
        
    except ValueError as e:
        logger.error(f"Parsing error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/api/csv/validate", response_model=ValidationResponse)
async def validate_csv(
    file: UploadFile = File(...),
    auto_detect: bool = Query(True, description="Auto-detect encoding and delimiter")
):
    """
    Validate CSV file structure without returning full data
    """
    try:
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        parser = CSVParser()
        df = parser.parse_file(content, auto_detect=auto_detect)
        
        validation_result = parser.validate_structure(df)
        
        return ValidationResponse(**validation_result)
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/csv/schema", response_model=SchemaResponse)
async def get_schema(
    file: UploadFile = File(...),
    auto_detect: bool = Query(True, description="Auto-detect encoding and delimiter")
):
    """
    Get schema information from CSV file
    """
    try:
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        parser = CSVParser()
        df = parser.parse_file(content, auto_detect=auto_detect)
        
        schema = parser.get_schema(df)
        
        return SchemaResponse(**schema)
        
    except Exception as e:
        logger.error(f"Schema extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/csv/transform")
async def transform_csv(
    file: UploadFile = File(...),
    auto_detect: bool = Query(True),
    remove_empty_rows: bool = Query(False),
    remove_duplicates: bool = Query(False),
    trim_whitespace: bool = Query(True),
    lowercase_columns: bool = Query(False)
):
    """
    Transform and clean CSV data
    """
    try:
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        parser = CSVParser()
        df = parser.parse_file(content, auto_detect=auto_detect)
        
        # Clean data
        cleaning_options = {
            'remove_empty_rows': remove_empty_rows,
            'remove_duplicates': remove_duplicates,
            'trim_whitespace': trim_whitespace,
            'lowercase_columns': lowercase_columns
        }
        
        df_cleaned = parser.clean_data(df, cleaning_options)
        data = parser.transform_to_json(df_cleaned)
        
        return {
            "status": "success",
            "message": "CSV transformed successfully",
            "original_row_count": len(df),
            "cleaned_row_count": len(df_cleaned),
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Transformation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/csv/prepare-for-xml")
async def prepare_for_xml(
    file: UploadFile = File(...),
    auto_detect: bool = Query(True)
):
    """
    Prepare CSV data for XML transformation
    Returns structured data ready for XML conversion
    """
    try:
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        parser = CSVParser()
        df = parser.parse_file(content, auto_detect=auto_detect)
        
        # Get schema and data
        schema = parser.get_schema(df)
        data = parser.transform_to_json(df)
        
        return {
            "status": "success",
            "message": "CSV prepared for XML transformation",
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": list(df.columns),
            "schema": schema,
            "data": data,
            "xml_ready": True
        }
        
    except Exception as e:
        logger.error(f"XML preparation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/csv/prepare-for-mapping")
async def prepare_for_mapping(
    file: UploadFile = File(...),
    target_format: str = Query("ISO20022", description="Target format for mapping"),
    auto_detect: bool = Query(True)
):
    """
    Prepare CSV schema for intelligent mapping generation
    Returns schema information suitable for mapping analysis
    """
    try:
        content = await file.read()
        
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        parser = CSVParser()
        df = parser.parse_file(content, auto_detect=auto_detect)
        
        # Get comprehensive schema
        schema = parser.get_schema(df)
        
        # Get sample data for mapping context
        sample_data = parser.transform_to_json(df.head(10))
        
        # Perform validation
        validation = parser.validate_structure(df)
        
        return {
            "status": "success",
            "message": "CSV schema prepared for mapping generation",
            "target_format": target_format,
            "source_schema": schema,
            "sample_data": sample_data,
            "validation": validation,
            "mapping_ready": True
        }
        
    except Exception as e:
        logger.error(f"Mapping preparation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    logger.info(f"Starting CSV Parser Microservice on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
