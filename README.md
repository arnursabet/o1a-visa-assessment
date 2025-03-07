# O-1A Visa Qualification Assessment

An AI-powered application that analyzes CVs to assess qualification for an O-1A immigration visa.

## Features

- Analyzes CV/resume documents to identify elements matching O-1A visa criteria
- Evaluates qualification based on 8 official O-1A criteria
- Provides a qualification rating (low, medium, high)
- Extracts and categorizes achievements from uploaded documents
- REST API built with FastAPI

## O-1A Criteria

The application evaluates CVs based on the following 8 O-1A visa criteria:

1. **Awards** - Receipt of nationally or internationally recognized prizes/awards for excellence
2. **Membership** - Membership in associations requiring outstanding achievement
3. **Press** - Published material about the applicant in professional publications or major media
4. **Judging** - Participation as a judge of others in the same or related field
5. **Original Contribution** - Original scientific, scholarly, or business-related contributions of significance
6. **Scholarly Articles** - Authorship of scholarly articles in the field
7. **Critical Employment** - Employment in a critical or essential capacity at distinguished organizations
8. **High Remuneration** - Command of a high salary or remuneration

## Documentation

- [System Design Documentation](docs/system_design.md) - Detailed explanation of the application architecture
- [API Documentation](docs/api_documentation.md) - Complete API reference

## Repository Structure

```
.
├── app/
│   ├── api/                # API endpoints
│   ├── core/               # Core configuration 
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   └── utils/              # Utility functions
├── docs/                   # Documentation
├── examples/               # Example scripts
├── tests/                  # Test suite
├── .env.example            # Environment variables template
├── Dockerfile              # Docker configuration
├── Makefile                # Common tasks
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation Options

#### Option 1: Using Make (Recommended)

```bash
# Clone the repository
git clone https://github.com/arnursabet/o1a-visa-assessment.git
cd o1a-visa-assessment

# Setup virtual environment and install dependencies
make setup

# Add your OpenAI API key to .env file
# Edit the .env file and replace the placeholder with your API key
```

#### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/arnursabet/o1a-visa-assessment.git
cd o1a-visa-assessment

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env file to add your OpenAI API key
```

#### Option 3: Using Docker

```bash
# Clone the repository
git clone https://github.com/arnursabet/o1a-visa-assessment.git
cd o1a-visa-assessment

# Create .env file and add your OpenAI API key
cp .env.example .env
# Edit .env file to add your OpenAI API key

# Build and run with Docker
docker build -t o1a-visa-assessment .
docker run -p 8000:8000 --env-file .env o1a-visa-assessment
```

### Running the Application

#### Using Make

```bash
make run
```

#### Using Python directly

```bash
# With virtual environment activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Using the run script

```bash
# Make the script executable
chmod +x run.sh
# Run the script
./run.sh
```

The API will be available at http://localhost:8000

## API Usage

### Using the Swagger UI

You can explore and test the API using the Swagger UI at http://localhost:8000/docs

### Using the API Client (Recommended for better user experience)

The repository includes a convenient Python client for making API requests:

```bash
# Make the client executable
chmod +x examples/api_client.py

# Run the client with the path to your CV file (absolute or relative path)
python examples/api_client.py /path/to/your/cv.pdf
```

### Direct API Calls

You can also make direct API calls using curl or any HTTP client:

```bash
curl -X POST http://localhost:8000/api/v1/assess \
  -F "file=@/path/to/your/cv.pdf"
```

### Example Response

```json
{
  "criteria_matches": {
    "awards": [
      {
        "text": "String describing the award from the CV",
        "explanation": "Explanation of why this is considered an award"
      }
    ],
    "membership": [],
    "press": [],
    "judging": [],
    "original_contribution": [],
    "scholarly_articles": [],
    "critical_employment": [],
    "high_remuneration": []
  },
  "qualification_rating": "medium",
  "analysis": "Detailed explanation of the qualification assessment"
}
```

## Testing

Run the test suite with:

```bash
# Using Make
make test

# Manual execution
pytest
```

## Architecture

The application follows a clean, layered architecture:
- **API Layer** - FastAPI routes handling HTTP requests/responses
- **Service Layer** - Business logic for CV processing and assessment
- **Integration Layer** - OpenAI API interaction
- **Utility Layer** - Helpers for file processing, etc.

See the [System Design Documentation](docs/system_design.md) for details.

## Notes

- For best results, use digital PDF files rather than scanned documents
- The OpenAI model (GPT-4o) requires a valid API key with appropriate permissions
- You can use any absolute or relative path to your CV file when using the API client