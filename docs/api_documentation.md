# O-1A Visa Qualification Assessment API Documentation

## Overview

This document provides detailed information about the API endpoints for the O-1A Visa Qualification Assessment application.

## Base URL

The base URL for all API endpoints is:

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API does not require authentication. In a production environment, you should implement an authentication mechanism.

## Endpoints

### 1. Assess CV for O-1A Visa Qualification

Analyzes a CV and evaluates qualification for an O-1A visa based on the 8 official criteria.

**Endpoint:** `/assess`

**Method:** POST

**Content-Type:** multipart/form-data

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | File | Yes | CV file in PDF format |

**Response:**

```json
{
  "criteria_matches": {
    "awards": [
      {
        "text": "String describing the award from the CV",
        "explanation": "Explanation of why this is considered an award"
      }
    ],
    "membership": [
      {
        "text": "String describing the membership from the CV",
        "explanation": "Explanation of why this qualifies as a membership"
      }
    ],
    "press": [],
    "judging": [],
    "original_contribution": [],
    "scholarly_articles": [],
    "critical_employment": [],
    "high_remuneration": []
  },
  "qualification_rating": "low | medium | high",
  "analysis": "Detailed explanation of the qualification assessment"
}
```

**Status Codes:**

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad request (invalid file format) |
| 422 | Unprocessable entity (cannot extract text from PDF) |
| 500 | Server error |

**Example Request:**

Using cURL:

```bash
curl -X POST http://localhost:8000/api/v1/assess \
  -F "file=@path/to/your/cv.pdf"
```

Using Python requests:

```python
import requests

url = "http://localhost:8000/api/v1/assess"
files = {'file': open('path/to/your/cv.pdf', 'rb')}

response = requests.post(url, files=files)
print(response.json())
```

## Error Responses

Error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## API Limitations

1. Maximum file size is 10 MB
2. Only PDF files are supported
3. No rate limiting is currently implemented

## O-1A Criteria

The API evaluates CVs based on these 8 O-1A visa criteria:

1. **Awards** - Receipt of nationally or internationally recognized prizes/awards
2. **Membership** - Membership in associations requiring outstanding achievement
3. **Press** - Published material about the applicant in professional publications
4. **Judging** - Participation as a judge of others in the same field
5. **Original Contribution** - Original scientific, scholarly, or business contributions
6. **Scholarly Articles** - Authorship of scholarly articles in the field
7. **Critical Employment** - Employment in a critical capacity at distinguished organizations
8. **High Remuneration** - Command of a high salary or remuneration