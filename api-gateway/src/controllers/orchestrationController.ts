import { Request, Response, NextFunction } from 'express';
import axios from 'axios';
import FormData from 'form-data';
import fs from 'fs';
import { parseString } from 'xml2js';
import { promisify } from 'util';
import logger from '../utils/logger';
import { AppError } from '../middleware/errorHandler';

const parseXml = promisify(parseString);

const CSV_PARSER_URL = process.env.CSV_PARSER_URL || 'http://localhost:8000';
const XML_SANITIZER_URL = process.env.XML_SANITIZER_URL || 'http://localhost:8080';
const MAPPING_GENERATOR_URL = process.env.MAPPING_GENERATOR_URL || 'http://localhost:8081';

/**
 * CSV to XML Transformation
 * Parses CSV and converts to ISO 20022 XML format
 */
export const csvToXml = async (req: Request, res: Response, next: NextFunction) => {
  const requestId = req.headers['x-request-id'] as string;
  
  try {
    if (!req.file) {
      throw new AppError('No file uploaded', 400);
    }

    logger.info(`[${requestId}] Starting CSV to XML transformation`);

    // Step 1: Parse CSV
    const formData = new FormData();
    formData.append('file', fs.createReadStream(req.file.path));

    logger.info(`[${requestId}] Step 1: Parsing CSV file`);
    const parseResponse = await axios.post(
      `${CSV_PARSER_URL}/api/csv/parse`,
      formData,
      { headers: formData.getHeaders() }
    );

    const csvData = parseResponse.data;
    logger.info(`[${requestId}] CSV parsed: ${csvData.row_count} rows, ${csvData.column_count} columns`);

    // Step 2: Transform JSON to XML (simple transformation for now)
    const xmlPayload = transformJsonToXml(csvData.data, csvData.columns);
    logger.info(`[${requestId}] Step 2: Transformed to XML`);

    // Step 3: Sanitize XML
    logger.info(`[${requestId}] Step 3: Sanitizing XML`);
    const sanitizeResponse = await axios.post(
      `${XML_SANITIZER_URL}/sanitize-chars`,
      xmlPayload,
      { headers: { 'Content-Type': 'application/xml' } }
    );

    // Cleanup uploaded file
    fs.unlinkSync(req.file.path);

    logger.info(`[${requestId}] CSV to XML transformation completed successfully`);

    res.json({
      success: true,
      requestId,
      message: 'CSV successfully transformed to XML',
      data: {
        originalRowCount: csvData.row_count,
        originalColumns: csvData.columns,
        xml: sanitizeResponse.data,
      },
    });
  } catch (error: any) {
    logger.error(`[${requestId}] CSV to XML error:`, error.message);
    
    // Cleanup file on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    if (error.response) {
      return next(new AppError(
        `Service error: ${error.response.data.message || error.message}`,
        error.response.status
      ));
    }
    next(error);
  }
};

/**
 * CSV to Mapping Generation
 * Analyzes CSV schema and generates field mappings
 */
export const csvToMapping = async (req: Request, res: Response, next: NextFunction) => {
  const requestId = req.headers['x-request-id'] as string;
  
  try {
    if (!req.file) {
      throw new AppError('No file uploaded', 400);
    }

    const targetSchema = req.body.targetSchema || 'ISO20022_pain.001.001.09';
    logger.info(`[${requestId}] Starting CSV to Mapping for target: ${targetSchema}`);

    // Step 1: Get CSV schema
    const formData = new FormData();
    formData.append('file', fs.createReadStream(req.file.path));

    logger.info(`[${requestId}] Step 1: Extracting CSV schema`);
    const schemaResponse = await axios.post(
      `${CSV_PARSER_URL}/api/csv/schema`,
      formData,
      { headers: formData.getHeaders() }
    );

    const csvSchema = schemaResponse.data;
    logger.info(`[${requestId}] Schema extracted: ${csvSchema.columns.length} columns`);

    // Step 2: Generate mappings
    logger.info(`[${requestId}] Step 2: Generating field mappings`);
    const mappingRequest = {
      sourceSchema: csvSchema,
      targetFormat: targetSchema,
      requestId,
    };

    const mappingResponse = await axios.post(
      `${MAPPING_GENERATOR_URL}/generate-mapping`,
      mappingRequest,
      { headers: { 'Content-Type': 'application/json' } }
    );

    // Cleanup uploaded file
    fs.unlinkSync(req.file.path);

    logger.info(`[${requestId}] Mapping generation completed successfully`);

    res.json({
      success: true,
      requestId,
      message: 'Field mappings generated successfully',
      data: {
        sourceSchema: csvSchema,
        targetFormat: targetSchema,
        mappings: mappingResponse.data,
      },
    });
  } catch (error: any) {
    logger.error(`[${requestId}] CSV to Mapping error:`, error.message);
    
    // Cleanup file on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    if (error.response) {
      return next(new AppError(
        `Service error: ${error.response.data.message || error.message}`,
        error.response.status
      ));
    }
    next(error);
  }
};

/**
 * Full Transformation Pipeline
 * CSV -> Parse -> Generate Mappings -> Transform to XML -> Sanitize
 */
export const fullTransformPipeline = async (req: Request, res: Response, next: NextFunction) => {
  const requestId = req.headers['x-request-id'] as string;
  const startTime = Date.now();
  
  try {
    if (!req.file) {
      throw new AppError('No file uploaded', 400);
    }

    const targetSchema = req.body.targetSchema || 'ISO20022_pain.001.001.09';
    logger.info(`[${requestId}] Starting full transformation pipeline`);

    const formData = new FormData();
    formData.append('file', fs.createReadStream(req.file.path));

    // Step 1: Parse CSV
    logger.info(`[${requestId}] Step 1/4: Parsing CSV`);
    const parseResponse = await axios.post(
      `${CSV_PARSER_URL}/api/csv/parse`,
      formData,
      { headers: formData.getHeaders() }
    );
    const csvData = parseResponse.data;

    // Step 2: Extract schema
    const formData2 = new FormData();
    formData2.append('file', fs.createReadStream(req.file.path));
    
    logger.info(`[${requestId}] Step 2/4: Extracting schema`);
    const schemaResponse = await axios.post(
      `${CSV_PARSER_URL}/api/csv/schema`,
      formData2,
      { headers: formData2.getHeaders() }
    );
    const csvSchema = schemaResponse.data;

    // Step 3: Generate mappings
    logger.info(`[${requestId}] Step 3/4: Generating mappings`);
    const mappingRequest = {
      sourceSchema: csvSchema,
      targetFormat: targetSchema,
      requestId,
    };
    
    const mappingResponse = await axios.post(
      `${MAPPING_GENERATOR_URL}/generate-mapping`,
      mappingRequest,
      { headers: { 'Content-Type': 'application/json' } }
    );

    // Step 4: Transform to XML and sanitize
    logger.info(`[${requestId}] Step 4/4: Transforming to XML and sanitizing`);
    const xmlPayload = transformJsonToXml(csvData.data, csvData.columns);
    
    const sanitizeResponse = await axios.post(
      `${XML_SANITIZER_URL}/sanitize-chars`,
      xmlPayload,
      { headers: { 'Content-Type': 'application/xml' } }
    );

    // Cleanup uploaded file
    fs.unlinkSync(req.file.path);

    const duration = Date.now() - startTime;
    logger.info(`[${requestId}] Full pipeline completed in ${duration}ms`);

    res.json({
      success: true,
      requestId,
      message: 'Full transformation pipeline completed successfully',
      processingTime: `${duration}ms`,
      data: {
        source: {
          rowCount: csvData.row_count,
          columnCount: csvData.column_count,
          columns: csvData.columns,
        },
        mappings: mappingResponse.data,
        xml: sanitizeResponse.data,
      },
    });
  } catch (error: any) {
    logger.error(`[${requestId}] Pipeline error:`, error.message);
    
    // Cleanup file on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    if (error.response) {
      return next(new AppError(
        `Pipeline error: ${error.response.data.message || error.message}`,
        error.response.status
      ));
    }
    next(error);
  }
};

/**
 * Helper function to transform JSON data to XML
 * This is a simple implementation - can be enhanced based on specific ISO 20022 requirements
 */
function transformJsonToXml(data: any[], columns: string[]): string {
  const xmlRows = data.map((row) => {
    const fields = columns
      .map((col) => `    <${col}>${escapeXml(row[col] || '')}</${col}>`)
      .join('\n');
    return `  <Record>\n${fields}\n  </Record>`;
  }).join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>
<Document>
${xmlRows}
</Document>`;
}

/**
 * Escape special XML characters
 */
function escapeXml(unsafe: any): string {
  if (unsafe === null || unsafe === undefined) {
    return '';
  }
  
  return String(unsafe)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
