# PowerPoint Inspector 🔍

> **AI-Powered PowerPoint Inconsistency Detection Tool**

An intelligent Python tool that automatically analyzes multi-slide PowerPoint presentations to identify factual and logical inconsistencies across slides. Built with Google Gemini 2.5 Flash AI for comprehensive content analysis.

## 🎯 What It Does

PowerPoint Inspector detects various types of inconsistencies that could undermine presentation credibility:

- **📊 Numerical Conflicts**: Revenue figures, percentages, metrics that don't align
- **📝 Textual Contradictions**: Opposing statements about market conditions, product capabilities
- **⏰ Timeline Mismatches**: Conflicting dates, forecasts, and project timelines
- **🔢 Mathematical Errors**: Calculations that don't add up correctly
- **🏷️ Brand Inconsistencies**: Product name variations and feature claim contradictions

## ✨ Key Features

- **🤖 AI-Powered Analysis**: Uses Google Gemini 2.5 Flash for intelligent content comparison
- **📁 Multi-format Support**: Analyzes both `.pptx` files and image-based presentations
- **🔍 Comprehensive Detection**: Combines rule-based checks with AI analysis
- **📊 Multiple Output Formats**: Console, JSON, and CSV reporting options
- **⚡ Scalable Design**: Efficiently handles large presentations
- **🔄 Cross-platform**: Works on Windows, macOS, and Linux

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Content       │    │  AI             │    │  Report         │
│  Extractor     │───▶│  Analyzer       │───▶│  Generator      │
│                 │    │                 │    │                 │
│ • PPTX Parser  │    │ • Rule-based    │    │ • Console       │
│ • Image Proc.  │    │ • AI Analysis   │    │ • JSON          │
│ • Text Extract │    │ • Detection     │    │ • CSV           │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.8+** installed on your system
- **Git** (for cloning the repository)
- **Google Gemini API key** (free from [AI Studio](https://aistudio.google.com/app/apikey))

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd ppt-inspector

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup API Key

```bash
# Copy environment template
cp env_example.txt .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Run Analysis

```bash
# Analyze a PowerPoint file
python -m ppt_inspector.ppt_inspector --file "path/to/presentation.pptx" --out report.json

# Analyze image-based slides
python -m ppt_inspector.ppt_inspector --images "path/to/slides/" --out report.json
```

## 📖 Usage Examples

### Basic Analysis
```bash
# Analyze PowerPoint file and save to JSON
python -m ppt_inspector.ppt_inspector --file presentation.pptx --out analysis.json

# Analyze slides from image directory
python -m ppt_inspector.ppt_inspector --images slides/ --out report.json
```

### Command Line Options
- `--file`: Path to PowerPoint (.pptx) file
- `--images`: Directory containing slide images
- `--out`: Output file path (default: report.json)

## 📊 Output Format

The tool generates structured JSON reports with detailed inconsistency information:

```json
{
  "id": "I01",
  "type": "semantic_conflict",
  "description": "Detailed description of the inconsistency",
  "slides": [1, 2],
  "evidence": ["Slide 1 content", "Slide 2 content"],
  "confidence": 0.8
}
```

### Report Fields
- **id**: Unique identifier for the inconsistency
- **type**: Category of inconsistency detected
- **description**: Detailed explanation of the issue
- **slides**: Affected slide numbers
- **evidence**: Supporting content from the slides
- **confidence**: AI confidence score (0.0-1.0)

## 🔧 What It Detects

### 1. Numerical Data Conflicts
- **Revenue discrepancies**: "$2M" vs "$3M" savings
- **Performance metrics**: "2x faster" vs "3x faster" claims
- **Time measurements**: "15 mins" vs "20 mins" per slide
- **Statistical inconsistencies**: Conflicting percentages and ratios

### 2. Textual Claim Contradictions
- **Market descriptions**: "Highly competitive" vs "Few competitors"
- **Product capabilities**: Inconsistent feature descriptions
- **Company positioning**: Conflicting brand statements

### 3. Timeline Mismatches
- **Date conflicts**: Conflicting forecast dates
- **Time period inconsistencies**: Mismatched time ranges
- **Sequence errors**: Out-of-order chronological information

### 4. Mathematical Errors
- **Calculation mistakes**: Sums that don't add up
- **Unit conversions**: Inconsistent measurement units
- **Statistical errors**: Incorrect percentage calculations

## 🎮 Advanced Usage

### Interactive Demo
```bash
# Run interactive demonstration
python demo.py
```

### Custom Configuration
```bash
# Run with verbose logging
python -m ppt_inspector.ppt_inspector --file presentation.pptx --verbose

# Generate different output formats
python -m ppt_inspector.ppt_inspector --file presentation.pptx --format csv
```

### Batch Processing
```bash
# Process multiple presentations
for file in presentations/*.pptx; do
    python -m ppt_inspector.ppt_inspector --file "$file" --out "reports/$(basename "$file" .pptx).json"
done
```

## 🧪 Testing

### Run Test Suite
```bash
# Basic functionality tests
python test_inspector.py

# Comprehensive test suite
python test_suite.py

# Test Gemini API integration
python test_gemini.py
```

### Sample Data
The project includes sample PowerPoint files in the `sample_slides/` directory for testing and demonstration purposes.

## 📁 Project Structure

```
ppt-inspector/
├── ppt_inspector/           # Core package
│   ├── __init__.py         # Package initialization
│   ├── ppt_inspector.py    # Main inspector class
│   ├── content_extractor.py # Content extraction logic
│   ├── ai_analyzer.py      # AI-powered analysis
│   ├── report_generator.py # Report generation
│   └── models.py           # Data models
├── ppt_inspector.py         # CLI entry point
├── requirements.txt         # Python dependencies
├── setup.py                # Package installation
├── example.py              # Usage examples
├── demo.py                 # Interactive demo
├── test_suite.py           # Comprehensive tests
├── run_inspector.bat       # Windows launcher
├── run_inspector.sh        # Unix launcher
├── .env.example            # Environment template
└── README.md               # This file
```

## 🔒 Limitations & Considerations

### Current Limitations
1. **AI Model Dependencies**: Analysis quality depends on Gemini API availability and performance
2. **Content Recognition**: May miss inconsistencies in complex visual elements or charts
3. **Context Understanding**: Limited to explicit content; may not catch implicit contradictions
4. **File Size**: Very large presentations may require increased processing time
5. **Language Support**: Optimized for English content; other languages may have reduced accuracy

### Performance Considerations
- **API Rate Limits**: Respects Gemini API usage limits
- **Memory Usage**: Efficient processing for presentations up to 100+ slides
- **Processing Time**: Typically 2-5 seconds per slide depending on content complexity

## 🚀 Future Enhancements

- **Visual Analysis**: Enhanced chart and image inconsistency detection
- **Multi-language Support**: Broader language coverage for international presentations
- **Real-time Analysis**: Live presentation monitoring capabilities
- **Integration APIs**: REST API for web application integration
- **Advanced Reporting**: Interactive HTML reports with visualizations

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run code formatting
black ppt_inspector/

# Run linting
flake8 ppt_inspector/

# Run tests
pytest test_suite.py
```

## 📚 Documentation

- **📖 [Complete Documentation](DOCUMENTATION.md)**: Comprehensive technical details
- **📋 [Project Summary](PROJECT_SUMMARY.md)**: High-level overview
- **🚀 [Step-by-Step Guide](STEP_BY_STEP_GUIDE.md)**: Getting started tutorial
- **🧪 [Test Suite](test_suite.py)**: Comprehensive testing examples

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI**: Powered by Gemini 2.5 Flash for intelligent content analysis
- **Python Community**: Built with popular libraries like `python-pptx`, `rich`, and `pandas`
- **Open Source Contributors**: All those who contribute to making this tool better

## 📞 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions for help and ideas
- **Documentation**: Check the comprehensive documentation for detailed guides

---

## 🔗 Connect & Follow

**Built with ❤️ by [Lagnajit Saha](https://github.com/LagnajitSaha)**

- **GitHub**: [@LagnajitSaha](https://github.com/LagnajitSaha)
- **LinkedIn**: [Lagnajit Saha](https://linkedin.com/in/lagnajit-saha-134b48252)

---

*PowerPoint Inspector - Making presentations more credible, one slide at a time.* 🚀
