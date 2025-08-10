# PowerPoint Inspector - Step-by-Step Guide After Completion

## 🎯 What You Have Now

Congratulations! You now have a complete, AI-powered PowerPoint inconsistency detection tool. This guide will walk you through getting it up and running step by step.

## 📋 Prerequisites Checklist

Before you start, ensure you have:

- [ ] **Python 3.8 or higher** installed on your system
- [ ] **Git** installed (for cloning the repository)
- [ ] **Internet connection** (for installing dependencies and API access)
- [ ] **Google Gemini API key** (free from [AI Studio](https://aistudio.google.com/app/apikey))

## 🚀 Step 1: Get Your Gemini API Key

1. **Visit Google AI Studio**: Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. **Sign in** with your Google account
3. **Create a new API key**:
   - Click "Create API Key"
   - Give it a name (e.g., "PowerPoint Inspector")
   - Copy the generated key (you'll need this in Step 3)

## 🚀 Step 2: Clone and Setup the Repository

### Option A: Using Git (Recommended)
```bash
# Clone the repository
git clone <your-repository-url>
cd ppt-inspector

# Or if you already have the files locally, navigate to the directory
cd path/to/ppt-inspector
```

### Option B: Download and Extract
1. Download the project files as a ZIP archive
2. Extract to a folder of your choice
3. Open terminal/command prompt in that folder

## 🚀 Step 3: Set Up Your Environment

### 3.1 Create Environment File
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file and add your API key
# On Windows: notepad .env
# On Mac/Linux: nano .env or code .env
```

### 3.2 Add Your API Key
Edit the `.env` file and replace `your_gemini_api_key_here` with your actual API key:
```env
GEMINI_API_KEY=AIzaSyC...your_actual_key_here...
```

## 🚀 Step 4: Install Dependencies

### 4.1 Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 4.2 Install Required Packages
```bash
# Install all dependencies
pip install -r requirements.txt
```

## 🚀 Step 5: Test the Installation

### 5.1 Run the Demo
```bash
# Run the interactive demo
python demo.py
```

This will:
- Show you what the tool can detect
- Run analysis on sample slides
- Generate sample reports
- Demonstrate the tool's capabilities

### 5.2 Run Basic Tests
```bash
# Run basic functionality tests
python test_inspector.py
```

## 🚀 Step 6: Analyze Your First Presentation

### 6.1 Using the Command Line
```bash
# Analyze a PowerPoint file
python ppt_inspector.py --file your_presentation.pptx

# Analyze images directory
python ppt_inspector.py --images slides/

# Generate JSON report
python ppt_inspector.py --file presentation.pptx --output json --output-file report.json

# Generate CSV report
python ppt_inspector.py --file presentation.pptx --output csv --output-file report.csv
```

### 6.2 Using the Launcher Scripts

**Windows Users**:
```cmd
run_inspector.bat --file your_presentation.pptx
```

**Mac/Linux Users**:
```bash
./run_inspector.sh --file your_presentation.pptx
```

## 🚀 Step 7: Understand the Output

### 7.1 Console Output
The tool will display:
- Number of inconsistencies found
- Type and severity of each issue
- Slides involved in each inconsistency
- Confidence level for each detection
- Detailed descriptions

### 7.2 File Outputs
- **JSON**: Structured data for programmatic use
- **CSV**: Spreadsheet-compatible format for analysis

## 🚀 Step 8: Customize and Configure

### 8.1 Adjust Analysis Parameters
Edit `config.py` to customize:
- Confidence thresholds
- AI model parameters
- Analysis rules
- Output settings

### 8.2 Environment Variables
Add to your `.env` file:
```env
# Customize AI analysis
MAX_TOKENS=8192
TEMPERATURE=0.1

# Set default output format
DEFAULT_OUTPUT_FORMAT=json

# Adjust logging level
LOG_LEVEL=DEBUG
```

## 🚀 Step 9: Advanced Usage

### 9.1 Programmatic Integration
```python
from ppt_inspector import PowerPointInspector

# Initialize the tool
inspector = PowerPointInspector()

# Analyze a presentation
inconsistencies = inspector.analyze_presentation(file_path="presentation.pptx")

# Process results programmatically
for inc in inconsistencies:
    print(f"Found {inc.type} on slides {inc.slides_involved}")
```

### 9.2 Batch Processing
```bash
# Process multiple files (create a script)
for file in *.pptx; do
    python ppt_inspector.py --file "$file" --output json --output-file "${file%.pptx}_report.json"
done
```

## 🚀 Step 10: Troubleshooting Common Issues

### 10.1 API Key Issues
**Problem**: "Invalid API key" error
**Solution**: 
- Verify your API key is correct in `.env`
- Check that the `.env` file is in the project root
- Ensure the API key has proper permissions

### 10.2 Import Errors
**Problem**: "ModuleNotFoundError"
**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### 10.3 File Processing Issues
**Problem**: PPTX files not loading
**Solution**:
- Verify file format is valid `.pptx`
- Check file permissions
- Ensure `python-pptx` is installed

## 🚀 Step 11: Run Comprehensive Tests

### 11.1 Full Test Suite
```bash
# Run all tests
python test_suite.py
```

### 11.2 Individual Test Categories
```bash
# Test specific components
python -m unittest test_suite.TestSlideContent
python -m unittest test_suite.TestAIAnalyzer
python -m unittest test_suite.TestReportGenerator
```

## 🚀 Step 12: Explore Examples

### 12.1 Run Examples
```bash
# Run usage examples
python example.py
```

### 12.2 Study the Code
- **`ppt_inspector.py`**: Main application logic
- **`config.py`**: Configuration management
- **`demo.py`**: Interactive demonstration
- **`example.py`**: Usage examples

## 🚀 Step 13: Customize for Your Needs

### 13.1 Add New Inconsistency Types
1. Edit `config.py` to add new types
2. Implement detection logic in `AIAnalyzer`
3. Add tests in `test_suite.py`

### 13.2 Enhance Content Extraction
1. Modify `ContentExtractor` for new file formats
2. Integrate OCR for image processing
3. Add support for charts and graphs

### 13.3 Create New Output Formats
1. Extend `ReportGenerator` with new formats
2. Add custom formatting options
3. Implement export to other systems

## 🚀 Step 14: Deploy and Share

### 14.1 Package Installation
```bash
# Install as a package
pip install -e .

# Now you can run from anywhere
ppt-inspector --file presentation.pptx
```

### 14.2 Distribution
- Share the repository with colleagues
- Create Docker containers for deployment
- Set up CI/CD pipelines for automated testing

## 🚀 Step 15: Monitor and Improve

### 15.1 Performance Monitoring
- Track analysis time for different file sizes
- Monitor API usage and costs
- Identify bottlenecks and optimize

### 15.2 Quality Assurance
- Collect feedback from users
- Track false positive/negative rates
- Continuously improve detection algorithms

## 📚 Additional Resources

### Documentation
- **`DOCUMENTATION.md`**: Complete technical documentation
- **`PROJECT_SUMMARY.md`**: Project overview and features
- **Inline code comments**: Detailed explanations in the source code

### Examples and Tests
- **`demo.py`**: Interactive demonstration
- **`example.py`**: Usage examples
- **`test_suite.py`**: Comprehensive testing

### Support
- Check the troubleshooting section above
- Review error messages and logs
- Examine test cases for usage patterns

## 🎉 Congratulations!

You now have a fully functional, AI-powered PowerPoint inconsistency detection tool! 

### What You Can Do Next:
1. **Analyze your presentations** for inconsistencies
2. **Customize the tool** for your specific needs
3. **Extend functionality** with new detection types
4. **Share with colleagues** to improve presentation quality
5. **Contribute back** to the project with improvements

### Remember:
- Keep your API key secure
- Monitor API usage to manage costs
- Test thoroughly before using in production
- Back up your presentations before analysis

---

**Happy analyzing!** 🎯✨

If you encounter any issues or have questions, refer to the documentation files or create an issue in the repository.
