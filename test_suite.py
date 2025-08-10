#!/usr/bin/env python3
"""
Comprehensive Test Suite for PowerPoint Inspector

This test suite thoroughly tests all components of the PowerPoint Inspector tool,
including edge cases, error handling, and various input scenarios.
"""

import unittest
import os
import sys
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from ppt_inspector import (
    PowerPointInspector, 
    ContentExtractor, 
    AIAnalyzer, 
    ReportGenerator,
    Inconsistency,
    SlideContent
)
from config import get_config, update_config

class TestSlideContent(unittest.TestCase):
    """Test the SlideContent dataclass."""
    
    def test_slide_content_creation(self):
        """Test creating SlideContent objects."""
        content = SlideContent(
            slide_number=1,
            text="Sample text",
            numerical_data=[{"type": "currency", "value": 1000, "unit": "USD"}],
            key_claims=["Sample claim"]
        )
        
        self.assertEqual(content.slide_number, 1)
        self.assertEqual(content.text, "Sample text")
        self.assertEqual(len(content.numerical_data), 1)
        self.assertEqual(len(content.key_claims), 1)
    
    def test_slide_content_defaults(self):
        """Test SlideContent with default values."""
        content = SlideContent(slide_number=1, text="Text")
        
        self.assertEqual(content.numerical_data, [])
        self.assertEqual(content.key_claims, [])
    
    def test_slide_content_equality(self):
        """Test SlideContent equality comparison."""
        content1 = SlideContent(slide_number=1, text="Text")
        content2 = SlideContent(slide_number=1, text="Text")
        content3 = SlideContent(slide_number=2, text="Text")
        
        self.assertEqual(content1, content2)
        self.assertNotEqual(content1, content3)

class TestInconsistency(unittest.TestCase):
    """Test the Inconsistency dataclass."""
    
    def test_inconsistency_creation(self):
        """Test creating Inconsistency objects."""
        inc = Inconsistency(
            type="numerical_conflict",
            description="Conflicting values",
            slides_involved=[1, 2],
            confidence=0.95,
            severity="high"
        )
        
        self.assertEqual(inc.type, "numerical_conflict")
        self.assertEqual(inc.description, "Conflicting values")
        self.assertEqual(inc.slides_involved, [1, 2])
        self.assertEqual(inc.confidence, 0.95)
        self.assertEqual(inc.severity, "high")
    
    def test_inconsistency_defaults(self):
        """Test Inconsistency with default values."""
        inc = Inconsistency(
            type="test",
            description="Test description",
            slides_involved=[1]
        )
        
        self.assertEqual(inc.confidence, 1.0)
        self.assertEqual(inc.severity, "medium")
        self.assertEqual(inc.details, "")

class TestContentExtractor(unittest.TestCase):
    """Test the ContentExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = ContentExtractor()
    
    def test_extract_numerical_data_currency(self):
        """Test extraction of currency values."""
        text = "Revenue: $1,000,000 and $2.5M"
        data = self.extractor._extract_numerical_data(text)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["type"], "currency")
        self.assertEqual(data[0]["value"], 1000000)
        self.assertEqual(data[1]["value"], 2500000)
    
    def test_extract_numerical_data_percentage(self):
        """Test extraction of percentage values."""
        text = "Growth: 15% and 25.5%"
        data = self.extractor._extract_numerical_data(text)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["type"], "percentage")
        self.assertEqual(data[0]["value"], 15.0)
        self.assertEqual(data[1]["value"], 25.5)
    
    def test_extract_numerical_data_time(self):
        """Test extraction of time values."""
        text = "Duration: 2 hours and 30 minutes"
        data = self.extractor._extract_numerical_data(text)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["type"], "time")
        self.assertEqual(data[0]["value"], 2)
        self.assertEqual(data[1]["value"], 30)
    
    def test_extract_numerical_data_multiplier(self):
        """Test extraction of multiplier values."""
        text = "Performance: 2x faster and 3.5x improvement"
        data = self.extractor._extract_numerical_data(text)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["type"], "multiplier")
        self.assertEqual(data[0]["value"], 2.0)
        self.assertEqual(data[1]["value"], 3.5)
    
    def test_extract_numerical_data_empty(self):
        """Test extraction from text with no numerical data."""
        text = "This text has no numbers"
        data = self.extractor._extract_numerical_data(text)
        
        self.assertEqual(len(data), 0)
    
    def test_extract_key_claims(self):
        """Test extraction of key claims."""
        text = "Our product saves time. It improves efficiency. The market is growing."
        claims = self.extractor._extract_key_claims(text)
        
        self.assertGreater(len(claims), 0)
        self.assertTrue(any("saves time" in claim for claim in claims))
    
    def test_extract_key_claims_no_keywords(self):
        """Test extraction from text with no key claim keywords."""
        text = "This is just some random text without key claims."
        claims = self.extractor._extract_key_claims(text)
        
        self.assertEqual(len(claims), 0)
    
    @patch('ppt_inspector.Presentation')
    def test_extract_from_pptx_success(self, mock_presentation):
        """Test successful extraction from PPTX file."""
        # Mock the presentation structure
        mock_slide = Mock()
        mock_slide.shapes = []
        
        # Mock text frame
        mock_text_frame = Mock()
        mock_text_frame.text = "Sample slide text"
        mock_shape = Mock()
        mock_shape.has_text_frame = True
        mock_shape.text_frame = mock_text_frame
        mock_slide.shapes = [mock_shape]
        
        mock_presentation.return_value.slides = [mock_slide]
        
        # Test extraction
        result = self.extractor.extract_from_pptx("dummy.pptx")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Sample slide text")
        self.assertEqual(result[0].slide_number, 1)
    
    @patch('ppt_inspector.Presentation')
    def test_extract_from_pptx_file_not_found(self, mock_presentation):
        """Test extraction from non-existent PPTX file."""
        mock_presentation.side_effect = FileNotFoundError("File not found")
        
        with self.assertRaises(FileNotFoundError):
            self.extractor.extract_from_pptx("nonexistent.pptx")
    
    def test_extract_from_images_sample_content(self):
        """Test extraction from sample images (built-in demo)."""
        result = self.extractor.extract_from_images("dummy_dir")
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # Check that all items are SlideContent objects
        for item in result:
            self.assertIsInstance(item, SlideContent)
            self.assertIsInstance(item.slide_number, int)
            self.assertIsInstance(item.text, str)

class TestAIAnalyzer(unittest.TestCase):
    """Test the AIAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = AIAnalyzer("dummy_api_key")
        self.sample_slides = [
            SlideContent(
                slide_number=1,
                text="Revenue: $2M",
                numerical_data=[{"type": "currency", "value": 2000000, "unit": "USD"}],
                key_claims=["Revenue is $2M"]
            ),
            SlideContent(
                slide_number=2,
                text="Revenue: $3M",
                numerical_data=[{"type": "currency", "value": 3000000, "unit": "USD"}],
                key_claims=["Revenue is $3M"]
            )
        ]
    
    def test_rule_based_checks_numerical_conflict(self):
        """Test rule-based numerical consistency checks."""
        inconsistencies = self.analyzer._rule_based_checks(self.sample_slides)
        
        # Should find numerical conflict between $2M and $3M
        self.assertGreater(len(inconsistencies), 0)
        
        numerical_conflicts = [inc for inc in inconsistencies if inc.type == "numerical_conflict"]
        self.assertGreater(len(numerical_conflicts), 0)
    
    def test_check_numerical_consistency(self):
        """Test numerical consistency checking."""
        inconsistencies = self.analyzer._check_numerical_consistency(self.sample_slides)
        
        self.assertGreater(len(inconsistencies), 0)
        
        # Check that the conflict is properly identified
        conflict = inconsistencies[0]
        self.assertEqual(conflict.type, "numerical_conflict")
        self.assertIn(1, conflict.slides_involved)
        self.assertIn(2, conflict.slides_involved)
    
    def test_check_claim_consistency(self):
        """Test claim consistency checking."""
        slides_with_claims = [
            SlideContent(
                slide_number=1,
                text="Performance improved by 2x",
                key_claims=["Performance improved by 2x"]
            ),
            SlideContent(
                slide_number=2,
                text="Performance improved by 3x",
                key_claims=["Performance improved by 3x"]
            )
        ]
        
        inconsistencies = self.analyzer._check_claim_consistency(slides_with_claims)
        
        self.assertGreater(len(inconsistencies), 0)
        self.assertEqual(inconsistencies[0].type, "claim_contradiction")
    
    @patch('ppt_inspector.google.generativeai.GenerativeModel')
    def test_ai_based_analysis(self, mock_genai):
        """Test AI-based analysis."""
        # Mock the Gemini response
        mock_response = Mock()
        mock_response.text = "Found inconsistency: Revenue values differ between slides"
        mock_model = Mock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.return_value = mock_model
        
        # Test AI analysis
        inconsistencies = self.analyzer._ai_based_analysis(self.sample_slides)
        
        # Should call the AI model
        mock_model.generate_content.assert_called_once()
        
        # Should return some inconsistencies
        self.assertIsInstance(inconsistencies, list)
    
    def test_analyze_inconsistencies_full_pipeline(self):
        """Test the full inconsistency analysis pipeline."""
        inconsistencies = self.analyzer.analyze_inconsistencies(self.sample_slides)
        
        self.assertIsInstance(inconsistencies, list)
        # Should find at least the numerical conflict
        self.assertGreater(len(inconsistencies), 0)

class TestReportGenerator(unittest.TestCase):
    """Test the ReportGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = ReportGenerator()
        self.sample_inconsistencies = [
            Inconsistency(
                type="numerical_conflict",
                description="Revenue values differ: $2M vs $3M",
                slides_involved=[1, 2],
                confidence=0.95,
                severity="high"
            ),
            Inconsistency(
                type="claim_contradiction",
                description="Performance claims conflict: 2x vs 3x",
                slides_involved=[3, 4],
                confidence=0.85,
                severity="medium"
            )
        ]
    
    def test_generate_report_console(self):
        """Test console report generation."""
        # This should not raise an exception
        try:
            self.generator.generate_report(
                self.sample_inconsistencies,
                output_format="console"
            )
        except Exception as e:
            self.fail(f"Console report generation failed: {e}")
    
    def test_generate_report_json(self):
        """Test JSON report generation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            self.generator.generate_report(
                self.sample_inconsistencies,
                output_format="json",
                output_file=temp_file
            )
            
            # Check that file was created and contains valid JSON
            self.assertTrue(os.path.exists(temp_file))
            
            with open(temp_file, 'r') as f:
                data = json.load(f)
            
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 2)
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_generate_report_csv(self):
        """Test CSV report generation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            self.generator.generate_report(
                self.sample_inconsistencies,
                output_format="csv",
                output_file=temp_file
            )
            
            # Check that file was created
            self.assertTrue(os.path.exists(temp_file))
            
            # Check that it's a valid CSV (has content)
            with open(temp_file, 'r') as f:
                content = f.read()
            
            self.assertGreater(len(content), 0)
            self.assertIn("numerical_conflict", content)
            
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_generate_report_invalid_format(self):
        """Test report generation with invalid format."""
        with self.assertRaises(ValueError):
            self.generator.generate_report(
                self.sample_inconsistencies,
                output_format="invalid_format"
            )

class TestPowerPointInspector(unittest.TestCase):
    """Test the PowerPointInspector main class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.inspector = PowerPointInspector()
    
    def test_inspector_initialization(self):
        """Test inspector initialization."""
        self.assertIsInstance(self.inspector.content_extractor, ContentExtractor)
        self.assertIsInstance(self.inspector.ai_analyzer, AIAnalyzer)
        self.assertIsInstance(self.inspector.report_generator, ReportGenerator)
    
    def test_analyze_presentation_sample_slides(self):
        """Test analysis of sample slides (built-in demo)."""
        inconsistencies = self.inspector.analyze_presentation()
        
        self.assertIsInstance(inconsistencies, list)
        # Should find some inconsistencies in the sample slides
        self.assertGreater(len(inconsistencies), 0)
    
    def test_analyze_presentation_no_input(self):
        """Test analysis with no input (should use sample slides)."""
        inconsistencies = self.inspector.analyze_presentation()
        
        self.assertIsInstance(inconsistencies, list)
        self.assertGreater(len(inconsistencies), 0)
    
    @patch('ppt_inspector.ContentExtractor.extract_from_pptx')
    def test_analyze_presentation_pptx_file(self, mock_extract):
        """Test analysis of PPTX file."""
        # Mock the content extraction
        mock_slides = [
            SlideContent(slide_number=1, text="Test slide 1"),
            SlideContent(slide_number=2, text="Test slide 2")
        ]
        mock_extract.return_value = mock_slides
        
        # Mock the AI analysis
        with patch.object(self.inspector.ai_analyzer, 'analyze_inconsistencies') as mock_analyze:
            mock_analyze.return_value = []
            
            inconsistencies = self.inspector.analyze_presentation(file_path="test.pptx")
            
            # Should call the extractor
            mock_extract.assert_called_once_with("test.pptx")
            
            # Should call the analyzer
            mock_analyze.assert_called_once_with(mock_slides)
    
    @patch('ppt_inspector.ContentExtractor.extract_from_images')
    def test_analyze_presentation_images(self, mock_extract):
        """Test analysis of images directory."""
        # Mock the content extraction
        mock_slides = [
            SlideContent(slide_number=1, text="Image slide 1"),
            SlideContent(slide_number=2, text="Image slide 2")
        ]
        mock_extract.return_value = mock_slides
        
        # Mock the AI analysis
        with patch.object(self.inspector.ai_analyzer, 'analyze_inconsistencies') as mock_analyze:
            mock_analyze.return_value = []
            
            inconsistencies = self.inspector.analyze_presentation(images_dir="test_images")
            
            # Should call the extractor
            mock_extract.assert_called_once_with("test_images")
            
            # Should call the analyzer
            mock_analyze.assert_called_once_with(mock_slides)

class TestConfiguration(unittest.TestCase):
    """Test the configuration system."""
    
    def test_get_config(self):
        """Test getting the full configuration."""
        config = get_config()
        
        self.assertIsInstance(config, dict)
        self.assertIn('AI_CONFIG', config)
        self.assertIn('ANALYSIS_CONFIG', config)
        self.assertIn('OUTPUT_CONFIG', config)
    
    def test_get_ai_config(self):
        """Test getting AI-specific configuration."""
        ai_config = get_config().get('AI_CONFIG', {})
        
        self.assertIn('MODEL_NAME', ai_config)
        self.assertIn('MAX_TOKENS', ai_config)
        self.assertIn('TEMPERATURE', ai_config)
    
    def test_get_analysis_config(self):
        """Test getting analysis-specific configuration."""
        analysis_config = get_config().get('ANALYSIS_CONFIG', {})
        
        self.assertIn('CONFIDENCE_THRESHOLD', analysis_config)
        self.assertIn('ENABLE_AI_ANALYSIS', analysis_config)
        self.assertIn('ENABLE_RULE_BASED_CHECKS', analysis_config)
    
    def test_update_config(self):
        """Test updating configuration values."""
        # Test updating a value
        update_config('TEST_KEY', 'test_value')
        
        # Verify the update
        config = get_config()
        self.assertEqual(config.get('TEST_KEY'), 'test_value')
        
        # Clean up
        if 'TEST_KEY' in config:
            del config['TEST_KEY']

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_full_pipeline_sample_slides(self):
        """Test the complete pipeline with sample slides."""
        inspector = PowerPointInspector()
        
        # Run the full analysis
        inconsistencies = inspector.analyze_presentation()
        
        # Verify we get results
        self.assertIsInstance(inconsistencies, list)
        self.assertGreater(len(inconsistencies), 0)
        
        # Verify the structure of inconsistencies
        for inc in inconsistencies:
            self.assertIsInstance(inc, Inconsistency)
            self.assertIsInstance(inc.type, str)
            self.assertIsInstance(inc.description, str)
            self.assertIsInstance(inc.slides_involved, list)
            self.assertIsInstance(inc.confidence, (int, float))
            self.assertIsInstance(inc.severity, str)
    
    def test_report_generation_all_formats(self):
        """Test report generation in all supported formats."""
        inspector = PowerPointInspector()
        
        # Get some inconsistencies
        inconsistencies = inspector.analyze_presentation()
        self.assertGreater(len(inconsistencies), 0)
        
        # Test all output formats
        formats = ["console", "json", "csv"]
        
        for fmt in formats:
            with self.subTest(format=fmt):
                try:
                    if fmt == "console":
                        inspector.report_generator.generate_report(
                            inconsistencies, 
                            output_format=fmt
                        )
                    else:
                        # For file outputs, use temporary files
                        with tempfile.NamedTemporaryFile(
                            mode='w', 
                            suffix=f'.{fmt}', 
                            delete=False
                        ) as f:
                            temp_file = f.name
                        
                        try:
                            inspector.report_generator.generate_report(
                                inconsistencies,
                                output_format=fmt,
                                output_file=temp_file
                            )
                            
                            # Verify file was created
                            self.assertTrue(os.path.exists(temp_file))
                            
                        finally:
                            # Clean up
                            if os.path.exists(temp_file):
                                os.unlink(temp_file)
                                
                except Exception as e:
                    self.fail(f"Report generation failed for format {fmt}: {e}")

def run_performance_tests():
    """Run performance tests (not part of unit tests)."""
    print("\n🚀 Running Performance Tests...")
    
    import time
    
    inspector = PowerPointInspector()
    
    # Test analysis performance
    start_time = time.time()
    inconsistencies = inspector.analyze_presentation()
    analysis_time = time.time() - start_time
    
    print(f"Analysis completed in {analysis_time:.2f} seconds")
    print(f"Found {len(inconsistencies)} inconsistencies")
    
    # Test report generation performance
    start_time = time.time()
    inspector.report_generator.generate_report(inconsistencies, "console")
    console_time = time.time() - start_time
    
    start_time = time.time()
    inspector.report_generator.generate_report(inconsistencies, "json", "perf_test.json")
    json_time = time.time() - start_time
    
    start_time = time.time()
    inspector.report_generator.generate_report(inconsistencies, "csv", "perf_test.csv")
    csv_time = time.time() - start_time
    
    print(f"Report generation times:")
    print(f"  Console: {console_time:.3f}s")
    print(f"  JSON: {json_time:.3f}s")
    print(f"  CSV: {csv_time:.3f}s")
    
    # Clean up performance test files
    for file in ["perf_test.json", "perf_test.csv"]:
        if os.path.exists(file):
            os.unlink(file)

def main():
    """Run the test suite."""
    print("🧪 PowerPoint Inspector - Comprehensive Test Suite")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestSlideContent,
        TestInconsistency,
        TestContentExtractor,
        TestAIAnalyzer,
        TestReportGenerator,
        TestPowerPointInspector,
        TestConfiguration,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 Test Results Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print(f"\n💥 Errors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    # Run performance tests if all unit tests pass
    if result.wasSuccessful():
        print(f"\n✅ All tests passed! Running performance tests...")
        run_performance_tests()
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
