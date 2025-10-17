"""
CSV Parser Core Module
Handles CSV file parsing, validation, and transformation
"""
import pandas as pd
import chardet
from typing import Dict, List, Any, Optional
from io import StringIO, BytesIO
import logging

logger = logging.getLogger(__name__)


class CSVParser:
    """Main CSV parsing class with validation and transformation capabilities"""
    
    def __init__(self, encoding: str = 'utf-8', delimiter: str = ','):
        """
        Initialize CSV Parser
        
        Args:
            encoding: Character encoding for CSV file
            delimiter: CSV delimiter character
        """
        self.encoding = encoding
        self.delimiter = delimiter
    
    def detect_encoding(self, file_bytes: bytes) -> str:
        """
        Detect the encoding of a CSV file
        
        Args:
            file_bytes: Raw bytes from the file
            
        Returns:
            Detected encoding string
        """
        result = chardet.detect(file_bytes)
        detected_encoding = result['encoding']
        confidence = result['confidence']
        
        logger.info(f"Detected encoding: {detected_encoding} (confidence: {confidence})")
        return detected_encoding if confidence > 0.7 else self.encoding
    
    def detect_delimiter(self, sample: str) -> str:
        """
        Detect the delimiter used in CSV file
        
        Args:
            sample: Sample string from CSV file
            
        Returns:
            Detected delimiter character
        """
        common_delimiters = [',', ';', '\t', '|']
        delimiter_counts = {delim: sample.count(delim) for delim in common_delimiters}
        detected = max(delimiter_counts, key=delimiter_counts.get)
        
        logger.info(f"Detected delimiter: '{detected}'")
        return detected if delimiter_counts[detected] > 0 else self.delimiter
    
    def parse_file(
        self,
        file_content: bytes,
        auto_detect: bool = True,
        chunk_size: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Parse CSV file content into a pandas DataFrame
        
        Args:
            file_content: Raw bytes of the CSV file
            auto_detect: Whether to auto-detect encoding and delimiter
            chunk_size: Size of chunks for reading large files
            
        Returns:
            Parsed pandas DataFrame
        """
        encoding = self.detect_encoding(file_content) if auto_detect else self.encoding
        
        # Read sample to detect delimiter
        sample = file_content[:1024].decode(encoding, errors='ignore')
        delimiter = self.detect_delimiter(sample) if auto_detect else self.delimiter
        
        # Parse the CSV
        try:
            df = pd.read_csv(
                BytesIO(file_content),
                encoding=encoding,
                delimiter=delimiter,
                chunksize=chunk_size
            )
            
            # If chunked, concatenate all chunks
            if chunk_size:
                df = pd.concat(df, ignore_index=True)
            
            logger.info(f"Successfully parsed CSV with {len(df)} rows and {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error parsing CSV: {str(e)}")
            raise ValueError(f"Failed to parse CSV file: {str(e)}")
    
    def validate_structure(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate the structure of the parsed CSV
        
        Args:
            df: Pandas DataFrame to validate
            
        Returns:
            Dictionary containing validation results
        """
        validation_result = {
            'is_valid': True,
            'row_count': len(df),
            'column_count': len(df.columns),
            'columns': list(df.columns),
            'missing_values': {},
            'data_types': {},
            'errors': []
        }
        
        # Check for missing column names
        unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
        if unnamed_cols:
            validation_result['errors'].append(f"Found unnamed columns: {unnamed_cols}")
            validation_result['is_valid'] = False
        
        # Check for missing values
        for col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                validation_result['missing_values'][col] = int(missing_count)
        
        # Get data types
        validation_result['data_types'] = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        return validation_result
    
    def get_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract schema information from DataFrame
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Schema dictionary with column information
        """
        schema = {
            'columns': [],
            'row_count': len(df),
            'estimated_size_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
        }
        
        for col in df.columns:
            col_info = {
                'name': col,
                'dtype': str(df[col].dtype),
                'nullable': bool(df[col].isna().any()),
                'unique_count': int(df[col].nunique()),
                'sample_values': df[col].dropna().head(3).tolist()
            }
            
            # Add statistics for numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                col_info['stats'] = {
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None,
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None
                }
            
            schema['columns'].append(col_info)
        
        return schema
    
    def transform_to_json(
        self,
        df: pd.DataFrame,
        orient: str = 'records',
        date_format: str = 'iso'
    ) -> List[Dict[str, Any]]:
        """
        Transform DataFrame to JSON format
        
        Args:
            df: Pandas DataFrame
            orient: JSON orientation ('records', 'index', 'columns', etc.)
            date_format: Format for date serialization
            
        Returns:
            List of dictionaries representing rows
        """
        return df.to_dict(orient=orient)
    
    def clean_data(self, df: pd.DataFrame, options: Dict[str, Any]) -> pd.DataFrame:
        """
        Clean and transform data based on options
        
        Args:
            df: Pandas DataFrame to clean
            options: Dictionary of cleaning options
            
        Returns:
            Cleaned DataFrame
        """
        df_cleaned = df.copy()
        
        # Remove empty rows
        if options.get('remove_empty_rows', False):
            df_cleaned = df_cleaned.dropna(how='all')
        
        # Remove duplicate rows
        if options.get('remove_duplicates', False):
            df_cleaned = df_cleaned.drop_duplicates()
        
        # Trim whitespace from string columns
        if options.get('trim_whitespace', True):
            string_cols = df_cleaned.select_dtypes(include=['object']).columns
            df_cleaned[string_cols] = df_cleaned[string_cols].apply(lambda x: x.str.strip())
        
        # Convert column names to lowercase
        if options.get('lowercase_columns', False):
            df_cleaned.columns = df_cleaned.columns.str.lower()
        
        # Fill missing values
        fill_value = options.get('fill_missing_value')
        if fill_value is not None:
            df_cleaned = df_cleaned.fillna(fill_value)
        
        logger.info(f"Cleaned data: {len(df)} -> {len(df_cleaned)} rows")
        return df_cleaned
