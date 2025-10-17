"""
Unit tests for CSV Parser
"""
import pytest
import pandas as pd
from io import BytesIO
from src.parser import CSVParser


@pytest.fixture
def sample_csv_content():
    """Sample CSV content for testing"""
    csv_data = """name,age,email,salary
John Doe,30,john@example.com,50000
Jane Smith,25,jane@example.com,55000
Bob Johnson,35,bob@example.com,60000
Alice Brown,28,alice@example.com,52000"""
    return csv_data.encode('utf-8')


@pytest.fixture
def sample_csv_with_missing():
    """CSV with missing values"""
    csv_data = """name,age,email,salary
John Doe,30,john@example.com,50000
Jane Smith,,jane@example.com,55000
Bob Johnson,35,,60000
Alice Brown,28,alice@example.com,"""
    return csv_data.encode('utf-8')


@pytest.fixture
def parser():
    """Create a CSVParser instance"""
    return CSVParser()


class TestCSVParser:
    
    def test_parse_basic_csv(self, parser, sample_csv_content):
        """Test basic CSV parsing"""
        df = parser.parse_file(sample_csv_content, auto_detect=True)
        
        assert len(df) == 4
        assert len(df.columns) == 4
        assert list(df.columns) == ['name', 'age', 'email', 'salary']
    
    def test_detect_encoding(self, parser, sample_csv_content):
        """Test encoding detection"""
        encoding = parser.detect_encoding(sample_csv_content)
        assert encoding in ['utf-8', 'UTF-8', 'ascii']
    
    def test_detect_delimiter(self, parser):
        """Test delimiter detection"""
        # Test comma delimiter
        sample_comma = "name,age,email\nJohn,30,john@test.com"
        assert parser.detect_delimiter(sample_comma) == ','
        
        # Test semicolon delimiter
        sample_semicolon = "name;age;email\nJohn;30;john@test.com"
        assert parser.detect_delimiter(sample_semicolon) == ';'
        
        # Test tab delimiter
        sample_tab = "name\tage\temail\nJohn\t30\tjohn@test.com"
        assert parser.detect_delimiter(sample_tab) == '\t'
    
    def test_validate_structure(self, parser, sample_csv_content):
        """Test CSV structure validation"""
        df = parser.parse_file(sample_csv_content)
        validation = parser.validate_structure(df)
        
        assert validation['is_valid'] is True
        assert validation['row_count'] == 4
        assert validation['column_count'] == 4
        assert len(validation['columns']) == 4
    
    def test_validate_with_missing_values(self, parser, sample_csv_with_missing):
        """Test validation with missing values"""
        df = parser.parse_file(sample_csv_with_missing)
        validation = parser.validate_structure(df)
        
        assert 'age' in validation['missing_values']
        assert 'email' in validation['missing_values']
        assert 'salary' in validation['missing_values']
    
    def test_get_schema(self, parser, sample_csv_content):
        """Test schema extraction"""
        df = parser.parse_file(sample_csv_content)
        schema = parser.get_schema(df)
        
        assert 'columns' in schema
        assert 'row_count' in schema
        assert schema['row_count'] == 4
        assert len(schema['columns']) == 4
        
        # Check column info
        name_col = next(col for col in schema['columns'] if col['name'] == 'name')
        assert 'dtype' in name_col
        assert 'nullable' in name_col
        assert 'sample_values' in name_col
    
    def test_transform_to_json(self, parser, sample_csv_content):
        """Test transformation to JSON"""
        df = parser.parse_file(sample_csv_content)
        json_data = parser.transform_to_json(df, orient='records')
        
        assert isinstance(json_data, list)
        assert len(json_data) == 4
        assert 'name' in json_data[0]
        assert json_data[0]['name'] == 'John Doe'
    
    def test_clean_data_remove_duplicates(self, parser):
        """Test removing duplicate rows"""
        csv_with_dupes = """name,age
John,30
Jane,25
John,30
Bob,35"""
        df = parser.parse_file(csv_with_dupes.encode('utf-8'))
        
        cleaned = parser.clean_data(df, {'remove_duplicates': True})
        assert len(cleaned) == 3
    
    def test_clean_data_trim_whitespace(self, parser):
        """Test trimming whitespace"""
        csv_with_spaces = """name,age
  John  ,30
  Jane  ,25"""
        df = parser.parse_file(csv_with_spaces.encode('utf-8'))
        
        cleaned = parser.clean_data(df, {'trim_whitespace': True})
        assert cleaned['name'].iloc[0] == 'John'
        assert cleaned['name'].iloc[1] == 'Jane'
    
    def test_clean_data_lowercase_columns(self, parser):
        """Test converting column names to lowercase"""
        csv_upper = """Name,Age,Email
John,30,john@test.com"""
        df = parser.parse_file(csv_upper.encode('utf-8'))
        
        cleaned = parser.clean_data(df, {'lowercase_columns': True})
        assert 'name' in cleaned.columns
        assert 'age' in cleaned.columns
        assert 'email' in cleaned.columns
    
    def test_clean_data_remove_empty_rows(self, parser):
        """Test removing empty rows"""
        csv_with_empty = """name,age,email
John,30,john@test.com
,,
Jane,25,jane@test.com"""
        df = parser.parse_file(csv_with_empty.encode('utf-8'))
        
        cleaned = parser.clean_data(df, {'remove_empty_rows': True})
        assert len(cleaned) == 2
    
    def test_parse_with_different_delimiter(self, parser):
        """Test parsing with semicolon delimiter"""
        csv_semicolon = """name;age;email
John Doe;30;john@example.com
Jane Smith;25;jane@example.com"""
        
        df = parser.parse_file(csv_semicolon.encode('utf-8'), auto_detect=True)
        assert len(df) == 2
        assert len(df.columns) == 3
