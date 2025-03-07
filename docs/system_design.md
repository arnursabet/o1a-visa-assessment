# O-1A Visa Qualification Assessment - System Design

## Overview

This document outlines the system design for an AI-powered application that analyzes CVs to assess qualification for an O-1A immigration visa.

## Architecture

The application follows a clean, layered architecture:

```
┌────────────────┐     ┌─────────────────┐     ┌───────────────────┐
│   API Layer    │────▶│  Service Layer  │────▶│ Integration Layer │
│  (FastAPI)     │◀────│ (Business Logic)│◀────│     (OpenAI)      │
└────────────────┘     └─────────────────┘     └───────────────────┘
         │                      │                        │
         │                      │                        │
         ▼                      ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Utility Layer                           │
│             (File Processing, Text Extraction, etc.)            │
└─────────────────────────────────────────────────────────────────┘
```

### Components

1. **API Layer**
   - FastAPI application
   - Handles HTTP requests/responses
   - Input validation and error handling
   - File upload management

2. **Service Layer**
   - Contains business logic
   - CV processing pipeline
   - O-1A criteria matching logic
   - Qualification rating determination

3. **Integration Layer**
   - OpenAI API client
   - Prompt engineering
   - Response parsing

4. **Utility Layer**
   - PDF text extraction
   - Text preprocessing
   - Data structures and models

## Data Flow

1. User uploads a CV through the API
2. The API layer validates the file and passes it to the service layer
3. The service layer:
   - Extracts text from the CV
   - Organizes the text into a structured format
   - Constructs prompts for the OpenAI API
4. The integration layer:
   - Sends prompts to the OpenAI API
   - Receives and parses the responses
5. The service layer:
   - Processes the AI responses
   - Maps responses to O-1A criteria
   - Determines a qualification rating
6. The API layer returns the structured response to the user

## Design Decisions

### 1. Use of GPT-4o for CV Analysis

GPT-4o is chosen for its advanced text understanding capabilities, faster speed andlower cost compared to o1-preview and other advanced reasoning models. The model can:
- Identify achievements in unstructured text
- Understand context in different CV formats
- Make nuanced judgments about qualification criteria

### 2. Prompt Engineering Strategy

The application uses a two-step prompting strategy:
1. **Analysis prompt**: Extracts and categorizes relevant achievements from the CV
2. **Evaluation prompt**: Assesses the extracted achievements against O-1A criteria and determines qualification rating

This approach improves accuracy by separating the extraction and evaluation tasks.

### 3. PDF Processing

PDF documents are processed using the PyPDF library, which:
- Handles various PDF formats
- Extracts text while preserving structure where possible
- Works well with both scanned (OCR'd) and digital PDFs

### 4. Qualification Rating Algorithm

The qualification rating (low, medium, high) is determined by:
1. Counting the number of criteria met
2. Weighting the strength of evidence for each criterion
3. Applying a threshold-based classification algorithm

## Scalability

The current design balances simplicity with functionality. For scaling:

- Implement a task queue for handling multiple requests
- Add caching for common operations
- Implement rate limiting to manage OpenAI API usage
- Add secure document storage with expiration policies

## Security

CVs contain sensitive personal information. The design ensures:
  - No long-term storage of uploaded documents
  - Secure processing pipeline
  - No sharing of personal data outside the application
  - Authentication for API access
  - Input validation to prevent injection attacks
  - Rate limiting to prevent abuse

## Limitations

- Accuracy depends on the quality of the CV and the OpenAI model's interpretation
- May not capture nuanced achievements without proper context
- Requires a well-structured and digitally readable CV for best results

## Future Improvements

- Support for multiple languages
- Advanced document parsing for better structure extraction
- Integration with immigration databases for more accurate assessments
- User dashboard for tracking and comparing assessments
- Detailed explanations and recommendations for improving O-1A qualification 