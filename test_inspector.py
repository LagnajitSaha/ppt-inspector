#!/usr/bin/env python3
"""
Test script for PowerPoint Inconsistency Detector

This script demonstrates the tool's capabilities using the sample slides provided.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ppt_inspector import PowerPointInspector, ContentExtractor, AIAnalyzer, ReportGenerator

def test_with_sample_slides():
    """Test the inspector with the sample slides provided."""
    print("🧪 Testing PowerPoint Inconsistency Detector with Sample Slides")
    print("=" * 60)
    
    # Check for API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("Please set your Gemini API key in the .env file")
        print("Get your free API key from: https://aistudio.google.com/app/apikey")
        return False
    
    try:
        # Initialize inspector
        inspector = PowerPointInspector(api_key)
        
        # Test with sample slides (images)
        print("\n📊 Analyzing sample slides for inconsistencies...")
        inconsistencies = inspector.analyze_presentation(images_dir="sample_slides")
        
        # Generate detailed report
        print("\n📋 Generating detailed report...")
        inspector.report_generator.generate_report(
            inconsistencies,
            output_format="console"
        )
        
        # Save JSON report
        print("\n💾 Saving JSON report...")
        inspector.report_generator.generate_report(
            inconsistencies,
            output_format="json",
            output_file="sample_analysis_report.json"
        )
        
        # Save CSV report
        print("\n📊 Saving CSV report...")
        inspector.report_generator.generate_report(
            inconsistencies,
            output_format="csv",
            output_file="sample_analysis_report.csv"
        )
        
        print(f"\n✅ Analysis complete! Found {len(inconsistencies)} inconsistencies.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_components():
    """Test individual components of the system."""
    print("\n🔧 Testing Individual Components")
    print("=" * 40)
    
    # Test content extractor
    print("\n1. Testing Content Extractor...")
    extractor = ContentExtractor()
    sample_content = extractor.extract_from_images("sample_slides")
    print(f"   ✅ Extracted content from {len(sample_content)} slides")
    
    # Test numerical data extraction
    print("\n2. Testing Numerical Data Extraction...")
    for slide in sample_content:
        print(f"   Slide {slide.slide_number}: {len(slide.numerical_data)} numerical items")
        for data in slide.numerical_data:
            print(f"     - {data['value']}{data['unit']} ({data['context']})")
    
    # Test key claims extraction
    print("\n3. Testing Key Claims Extraction...")
    for slide in sample_content:
        print(f"   Slide {slide.slide_number}: {len(slide.key_claims)} key claims")
        for claim in slide.key_claims[:2]:  # Show first 2 claims
            print(f"     - {claim[:60]}...")
    
    print("\n✅ Component testing complete!")

def main():
    """Main test function."""
    print("🚀 PowerPoint Inconsistency Detector - Test Suite")
    print("=" * 60)
    
    # Test individual components first
    test_individual_components()
    
    # Test full system
    success = test_with_sample_slides()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print("\n📁 Generated files:")
        print("   - sample_analysis_report.json")
        print("   - sample_analysis_report.csv")
    else:
        print("\n💥 Some tests failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
