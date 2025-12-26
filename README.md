# D-Brief: Decentralized Disaster Intelligence and Verification Platform

Status: Operational
License: MIT
Framework: Next.js | FastAPI

D-Brief is a high-fidelity, decentralized disaster response and intelligence platform designed to provide real-time, verified situational awareness during humanitarian crises. By leveraging a multi-layered verification architecture and state-of-the-art NLP models, D-Brief bridges the gap between raw field reports and official government data.

---

## Technical Architecture

The platform utilizes a levelized data acquisition strategy to ensure redundancy and high coverage across four distinct layers:

### Data Ingestion Layer
- Level 1 (Official): Long-polling of the BIPAD Portal API for confirmed government incidents.
- Level 2 (Contextual): Targeted API calls to ReliefWeb for humanitarian situation reports.
- Level 3 (Trigger): High-frequency polling of the USGS API for seismic events.
- Level 4 (Social/News): Integration with NewsData.io to capture real-time media reports.

### AI Verification Pipeline
When a raw report enters the system, it passes through the following asynchronous stages:
1. De-noising: Content extraction and cleaning, including HTML tag removal and whitespace normalization.
2. Zero-Shot Classification: Categorization into disaster domains (Flood, Earthquake, Fire) using DeBERTa-v3-base models.
3. NER (Named Entity Recognition): Extracting locations and dates to map incidents.
4. Verification Scoring: A multi-factor model evaluates spam signatures, cross-references against ground truth, and checks for internal narrative consistency.
5. Summarization: Conditional generation using DistilBART to produce executive summaries.

---

## Key Features

### Intelligent Verification Engine
- Zero-Shot Classification: Automatically categorizes disaster types using fine-tuned models.
- Contextual Summarization: Distills long-form reports into actionable intelligence.
- Entity Extraction: Automatically identifies locations and organizations in field reports.
- Spam Scoring: Advanced logic to protect the platform from misinformation.

### User Interface and Design
- Dynamic Dashboard: Built with Next.js 14 and Tailwind CSS for high performance.
- Obsidian Glass Aesthetic: A bespoke dark mode designed for high-stress operational environments utilizing glassmorphism and deep slate tones.
- Secure Reporting: Support for raw text, external URLs, and PDF document analysis.

---

## Tech Stack

| Layer | Technology |
| :--- | :--- |
| Frontend | Next.js 14, React, Tailwind CSS |
| Animations | Framer Motion, Lucide Icons |
| Backend API | FastAPI (Python 3.12), Uvicorn |
| AI/ML | Hugging Face Transformers, Sentence-Transformers, Spacy |
| Data Fetchers | NewsData.io, BIPAD Portal, ReliefWeb API, USGS API |
| Storage | SQLite3, Local File Caching |

---

## Installation and Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- NewsData.io API Key

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/D-Brief.git
cd D-Brief
```

### 2. AI Service Setup
```bash
cd ai_service
pip install -r requirements.txt
python download_models.py
python -m ai_service.api
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

### 4. Environment Variables
Create a .env file in the root directory:
```env
NEWSDATA_API_KEY=your_key_here
NEXT_PUBLIC_API_URL=http://localhost:8002
```

---

## API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| /api/classify | POST | Categorizes text into disaster types. |
| /api/summarize | POST | Generates a concise summary of reports. |
| /api/verify/report | POST | Checks credibility and filters spam. |
| /api/realtime/news | GET | Returns the latest AI-verified disaster news. |
| /api/process/upload | POST | Processes and analyzes PDF disaster reports. |

---

## Contribution Guidelines

### Standards
- AI Service: Use loguru for logging and maintain type hinting.
- Frontend: Adhere to the Obsidian design language and ensure responsiveness.
- General: New pipelines must be implemented as classes within ai_service/pipelines/.

### Process
1. Fork the repository and create a branch.
2. Include tests for any new functionality.
3. Update documentation for API changes.
4. Submit a pull request for review.

---

## License

This project is licensed under the MIT License.

Copyright (c) 2025 Team Mama-Bhanjas
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files to deal in the Software without restriction, including the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software.
