import express, { Application, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { v4 as uuidv4 } from 'uuid';
import logger from './utils/logger';
import { errorHandler } from './middleware/errorHandler';
import orchestrationRouter from './routes/orchestration';
import healthRouter from './routes/health';

// Load environment variables
dotenv.config();

const app: Application = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  const requestId = uuidv4();
  req.headers['x-request-id'] = requestId;
  
  logger.info({
    requestId,
    method: req.method,
    path: req.path,
    ip: req.ip,
  });
  
  next();
});

// Routes
app.use('/health', healthRouter);
app.use('/api/v1', orchestrationRouter);

// Root endpoint
app.get('/', (req: Request, res: Response) => {
  res.json({
    service: 'Fintech API Gateway & Orchestrator',
    version: '1.0.0',
    status: 'running',
    endpoints: {
      health: '/health',
      orchestration: '/api/v1/orchestrate',
      csvToXml: '/api/v1/csv-to-xml',
      csvToMapping: '/api/v1/csv-to-mapping',
      fullPipeline: '/api/v1/transform-pipeline'
    }
  });
});

// Error handling
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  logger.info(`API Gateway running on port ${PORT}`);
  logger.info(`CSV Parser: ${process.env.CSV_PARSER_URL || 'http://localhost:8000'}`);
  logger.info(`XML Sanitizer: ${process.env.XML_SANITIZER_URL || 'http://localhost:8080'}`);
  logger.info(`Mapping Generator: ${process.env.MAPPING_GENERATOR_URL || 'http://localhost:8081'}`);
});

export default app;
