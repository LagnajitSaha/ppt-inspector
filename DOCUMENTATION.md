# PowerPoint Inspector - Complete Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Development](#development)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)
10. [Limitations and Future Work](#limitations-and-future-work)

## Overview

PowerPoint Inspector is an AI-powered tool designed to detect factual and logical inconsistencies across multi-slide PowerPoint presentations. It combines rule-based analysis with AI-powered content understanding to identify conflicts in numerical data, textual claims, and timeline information.

### Key Features

- **Multi-format Support**: Analyzes both `.pptx` files and image-based slides
- **Hybrid Analysis**: Combines rule-based checks with AI-powered analysis
- **Comprehensive Detection**: Identifies numerical conflicts, claim contradictions, and timeline mismatches
- **Multiple Output Formats**: Console, JSON, and CSV reporting
- **Configurable Analysis**: Customizable thresholds and analysis parameters
- **Extensible Architecture**: Modular design for easy enhancement

### Supported Inconsistency Types

1. **Numerical Conflicts**: Conflicting currency values, percentages, time measurements
2. **Claim Contradictions**: Contradictory performance claims, market descriptions
3. **Timeline Mismatches**: Conflicting dates, forecasts, or time-based assertions
4. **Data Inconsistencies**: Mismatched statistics, metrics, or measurements

## Architecture

### System Components

```
PowerPoint Inspector
├── ContentExtractor
│   ├── PPTX Parser (python-pptx)
│   ├── Image Processor (PIL + OCR placeholder)
│   └── Text Analysis Engine
├── AIAnalyzer
│   ├── Rule-based Checks
│   ├── AI-powered Analysis (Gemini 2.5 Flash)
│   └── Inconsistency Detection Logic
├── ReportGenerator
│   ├── Console Output (Rich)
│   ├── JSON Export
│   └── CSV Export (Pandas)
└── PowerPointInspector (Main Orchestrator)
```

### Data Flow

1. **Input Processing**: File/image loading and content extraction
2. **Content Analysis**: Text parsing, numerical data extraction, claim identification
3. **Inconsistency Detection**: Rule-based checks + AI analysis
4. **Result Aggregation**: Inconsistency collection and prioritization
5. **Report Generation**: Multi-format output generation

### Key Classes

#### SlideContent
```python
@dataclass
class SlideContent:
    slide_number: int
    text: str
    numerical_data: List[Dict[str, Any]]
    key_claims: List[str]
```

#### Inconsistency
```python
@dataclass
class Inconsistency:
    type: str
    description: str
    slides_involved: List[int]
    confidence: float
    severity: str
    details: str
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free from [AI Studio](https://aistudio.google.com/app/apikey))

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ppt-inspector.git
   cd ppt-inspector
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Run the tool**:
   ```bash
   python ppt_inspector.py
   ```

### Alternative Installation Methods

#### Using Setup Scripts

**Windows**:
```cmd
run_inspector.bat
```

**Unix/Linux/macOS**:
```bash
./run_inspector.sh
```

#### Using pip (Development)
```bash
pip install -e .
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required: Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Customize analysis parameters
MAX_TOKENS=8192
TEMPERATURE=0.1
MODEL_NAME=gemini-2.0-flash-exp

# Optional: Output configuration
DEFAULT_OUTPUT_FORMAT=json
LOG_LEVEL=INFO
```

### Configuration File

The `config.py` file contains centralized configuration for:

- **AI Settings**: Model parameters, token limits, temperature
- **Analysis Rules**: Confidence thresholds, enabled checks
- **Output Settings**: Default formats, detail levels
- **Performance**: API timeouts, retry settings

### Customizing Analysis

```python
from config import update_config

# Adjust confidence threshold
update_config('ANALYSIS_CONFIG', {'CONFIDENCE_THRESHOLD': 0.8})

# Enable/disable specific checks
update_config('ANALYSIS_CONFIG', {'ENABLE_AI_ANALYSIS': False})
```

## Usage

### Command Line Interface

#### Basic Usage

```bash
# Analyze sample slides (built-in demo)
python ppt_inspector.py

# Analyze PowerPoint file
python ppt_inspector.py --file presentation.pptx

# Analyze images directory
python ppt_inspector.py --images slides/

# Specify output format
python ppt_inspector.py --output json --output-file report.json
```

#### Command Line Options

```bash
python ppt_inspector.py --help
```

Available options:
- `--file, -f`: Path to PowerPoint file
- `--images, -i`: Directory containing slide images
- `--output, -o`: Output format (console, json, csv)
- `--output-file, -of`: Output file path
- `--verbose, -v`: Enable verbose logging
- `--help, -h`: Show help message

### Programmatic Usage

#### Basic Analysis

```python
from ppt_inspector import PowerPointInspector

# Initialize inspector
inspector = PowerPointInspector()

# Analyze presentation
inconsistencies = inspector.analyze_presentation(file_path="presentation.pptx")

# Generate report
inspector.report_generator.generate_report(
    inconsistencies, 
    output_format="json", 
    output_file="report.json"
)
```

#### Component-Level Usage

```python
from ppt_inspector import ContentExtractor, AIAnalyzer, ReportGenerator

# Extract content
extractor = ContentExtractor()
slides_content = extractor.extract_from_pptx("presentation.pptx")

# Analyze inconsistencies
analyzer = AIAnalyzer("your_api_key")
inconsistencies = analyzer.analyze_inconsistencies(slides_content)

# Generate report
generator = ReportGenerator()
generator.generate_report(inconsistencies, "console")
```

### Output Formats

#### Console Output
Rich-formatted console output with color coding and structured display.

#### JSON Output
```json
[
  {
    "type": "numerical_conflict",
    "description": "Revenue values differ: $2M vs $3M",
    "slides_involved": [1, 2],
    "confidence": 0.95,
    "severity": "high",
    "details": "Slide 1 shows $2M revenue, Slide 2 shows $3M"
  }
]
```

#### CSV Output
Comma-separated values suitable for spreadsheet analysis and reporting.

## API Reference

### ContentExtractor

#### Methods

- `extract_from_pptx(file_path: str) -> List[SlideContent]`
- `extract_from_images(images_dir: str) -> List[SlideContent]`
- `_extract_numerical_data(text: str) -> List[Dict[str, Any]]`
- `_extract_key_claims(text: str) -> List[str]`

#### Numerical Data Extraction

Supports extraction of:
- Currency values ($1M, $1,000,000)
- Percentages (15%, 25.5%)
- Time measurements (2 hours, 30 minutes)
- Multipliers (2x, 3.5x)
- Ratios (1:3, 2:1)

### AIAnalyzer

#### Methods

- `analyze_inconsistencies(slides_content: List[SlideContent]) -> List[Inconsistency]`
- `_rule_based_checks(slides_content: List[SlideContent]) -> List[Inconsistency]`
- `_check_numerical_consistency(slides_content: List[SlideContent]) -> List[Inconsistency]`
- `_check_claim_consistency(slides_content: List[SlideContent]) -> List[Inconsistency]`
- `_ai_based_analysis(slides_content: List[SlideContent]) -> List[Inconsistency]`

#### Analysis Types

1. **Rule-based Checks**: Fast, deterministic analysis using predefined rules
2. **AI-powered Analysis**: Contextual understanding using Gemini 2.5 Flash

### ReportGenerator

#### Methods

- `generate_report(inconsistencies: List[Inconsistency], output_format: str, output_file: str = None)`

#### Supported Formats

- `console`: Rich-formatted terminal output
- `json`: Structured JSON export
- `csv`: Spreadsheet-compatible CSV export

## Development

### Project Structure

```
ppt-inspector/
├── ppt_inspector.py      # Main application
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── setup.py             # Package installation
├── example.py           # Usage examples
├── demo.py              # Interactive demonstration
├── test_inspector.py    # Basic tests
├── test_suite.py        # Comprehensive test suite
├── run_inspector.bat    # Windows launcher
├── run_inspector.sh     # Unix launcher
├── .env.example         # Environment template
└── DOCUMENTATION.md     # This file
```

### Development Setup

1. **Clone and setup**:
   ```bash
   git clone https://github.com/yourusername/ppt-inspector.git
   cd ppt-inspector
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   pip install -e .
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt[dev]
   ```

3. **Set up pre-commit hooks** (optional):
   ```bash
   pre-commit install
   ```

### Code Style

- **Formatting**: Black code formatter
- **Linting**: Flake8 for style checking
- **Type Checking**: MyPy for static type analysis
- **Documentation**: Google-style docstrings

### Adding New Features

#### 1. New Inconsistency Types

```python
# In config.py
INCONSISTENCY_TYPES = {
    "new_type": {
        "description": "Description of new inconsistency type",
        "severity": "medium",
        "confidence_threshold": 0.8
    }
}

# In AIAnalyzer
def _check_new_type_consistency(self, slides_content):
    # Implementation here
    pass
```

#### 2. New Content Extractors

```python
# In ContentExtractor
def extract_from_new_format(self, file_path):
    # Implementation here
    return [SlideContent(...)]
```

#### 3. New Output Formats

```python
# In ReportGenerator
def _generate_new_format_report(self, inconsistencies, output_file):
    # Implementation here
    pass
```

## Testing

### Running Tests

#### Basic Tests
```bash
python test_inspector.py
```

#### Comprehensive Test Suite
```bash
python test_suite.py
```

#### Individual Test Classes
```bash
python -m unittest test_suite.TestSlideContent
python -m unittest test_suite.TestAIAnalyzer
```

### Test Coverage

```bash
python -m pytest --cov=ppt_inspector test_suite.py
```

### Test Structure

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end system testing
- **Performance Tests**: Execution time and resource usage
- **Mock Testing**: External API simulation

### Writing Tests

```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_feature_behavior(self):
        """Test the new feature."""
        # Test implementation
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
```

## Troubleshooting

### Common Issues

#### 1. API Key Errors

**Problem**: `Invalid API key` or `Authentication failed`

**Solution**:
- Verify your Gemini API key is correct
- Check that the `.env` file is in the project root
- Ensure the API key has proper permissions

#### 2. Import Errors

**Problem**: `ModuleNotFoundError` or import failures

**Solution**:
- Install all dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)
- Verify virtual environment activation

#### 3. File Processing Errors

**Problem**: PPTX files not loading or processing

**Solution**:
- Verify file format is valid `.pptx`
- Check file permissions and accessibility
- Ensure `python-pptx` is properly installed

#### 4. Performance Issues

**Problem**: Slow processing or timeouts

**Solution**:
- Reduce `MAX_TOKENS` in configuration
- Lower `TEMPERATURE` for faster responses
- Enable caching if available
- Process smaller batches of slides

### Debug Mode

Enable verbose logging:

```bash
python ppt_inspector.py --verbose
```

Or set environment variable:
```bash
export LOG_LEVEL=DEBUG
python ppt_inspector.py
```

### Log Files

Logs are written to console by default. For file logging, modify `config.py`:

```python
LOGGING_CONFIG = {
    'level': 'INFO',
    'file': 'ppt_inspector.log'
}
```

## Limitations and Future Work

### Current Limitations

1. **OCR Integration**: Image-based slides currently use hardcoded sample content
2. **Language Support**: Primarily English language analysis
3. **Complex Layouts**: Limited support for complex slide layouts and charts
4. **Real-time Processing**: No real-time analysis during presentation creation
5. **Batch Processing**: Limited support for processing multiple presentations simultaneously

### Planned Enhancements

#### Short Term (1-3 months)
- [ ] OCR integration for image-based slides
- [ ] Multi-language support
- [ ] Enhanced chart and graph analysis
- [ ] Performance optimization and caching

#### Medium Term (3-6 months)
- [ ] Real-time presentation monitoring
- [ ] Batch processing capabilities
- [ ] Advanced inconsistency classification
- [ ] Integration with presentation software

#### Long Term (6+ months)
- [ ] Machine learning model training on inconsistency patterns
- [ ] Predictive inconsistency detection
- [ ] Collaborative inconsistency resolution
- [ ] Enterprise deployment features

### Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ppt-inspector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ppt-inspector/discussions)
- **Documentation**: This file and inline code documentation

---

**PowerPoint Inspector** - Making presentations more accurate, one slide at a time.
