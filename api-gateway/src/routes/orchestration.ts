import { Router } from 'express';
import multer from 'multer';
import { csvToXml, csvToMapping, fullTransformPipeline } from '../controllers/orchestrationController';

const router = Router();
const upload = multer({ dest: 'uploads/' });

/**
 * CSV to XML transformation
 * Parses CSV and converts to sanitized XML
 */
router.post('/csv-to-xml', upload.single('file'), csvToXml);

/**
 * CSV to Mapping generation
 * Analyzes CSV and generates field mappings
 */
router.post('/csv-to-mapping', upload.single('file'), csvToMapping);

/**
 * Full transformation pipeline
 * CSV -> Parse -> Generate Mappings -> Transform to XML -> Sanitize
 */
router.post('/transform-pipeline', upload.single('file'), fullTransformPipeline);

export default router;
