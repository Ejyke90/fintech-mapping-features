import { Router, Request, Response } from 'express';

const router = Router();

router.get('/', (req: Request, res: Response) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    services: {
      csvParser: process.env.CSV_PARSER_URL || 'http://localhost:8000',
      xmlSanitizer: process.env.XML_SANITIZER_URL || 'http://localhost:8080',
      mappingGenerator: process.env.MAPPING_GENERATOR_URL || 'http://localhost:8081',
    },
  });
});

export default router;
