#!/usr/bin/env python3
"""
Simple Example Script for PowerPoint Inspector

This script demonstrates how to use the PowerPoint Inspector tool
to analyze presentations and detect inconsistencies.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path to import our modules
sys.path.append(str(Path(__file__).parent))

from ppt_inspector import PowerPointInspector
from config import get_config

def example_basic_usage():
    """Demonstrate basic usage of the PowerPoint Inspector."""
    print("🔍 PowerPoint Inspector - Basic Usage Example")
    print("=" * 50)
    
    # Initialize the inspector
    inspector = PowerPointInspector()
    
    # Example 1: Analyze a PowerPoint file (if available)
    pptx_file = "sample_presentation.pptx"
    if os.path.exists(pptx_file):
        print(f"\n📊 Analyzing PowerPoint file: {pptx_file}")
        try:
            inconsistencies = inspector.analyze_presentation(file_path=pptx_file)
            print(f"Found {len(inconsistencies)} inconsistencies")
            
            # Generate different output formats
            inspector.report_generator.generate_report(
                inconsistencies, 
                output_format="console"
            )
            
            # Save as JSON
            inspector.report_generator.generate_report(
                inconsistencies, 
                output_format="json", 
                output_file="inconsistencies.json"
            )
            
        except Exception as e:
            print(f"Error analyzing PowerPoint file: {e}")
    else:
        print(f"\n⚠️  PowerPoint file '{pptx_file}' not found")
    
    # Example 2: Analyze sample slides (built-in demo)
    print(f"\n📊 Analyzing sample slides (built-in demo)")
    try:
        inconsistencies = inspector.analyze_presentation()
        print(f"Found {len(inconsistencies)} inconsistencies in sample slides")
        
        # Show first few inconsistencies
        for i, inc in enumerate(inconsistencies[:3]):
            print(f"\n{i+1}. {inc.type}: {inc.description}")
            print(f"   Slides: {inc.slides_involved}")
            print(f"   Confidence: {inc.confidence}")
            
    except Exception as e:
        print(f"Error analyzing sample slides: {e}")

def example_custom_analysis():
    """Demonstrate custom analysis configuration."""
    print("\n🔧 Custom Analysis Configuration Example")
    print("=" * 50)
    
    # Get configuration
    config = get_config()
    
    # Show current AI configuration
    ai_config = config.get('AI_CONFIG', {})
    print(f"Current AI Model: {ai_config.get('MODEL_NAME', 'Not set')}")
    print(f"Max Tokens: {ai_config.get('MAX_TOKENS', 'Not set')}")
    print(f"Temperature: {ai_config.get('TEMPERATURE', 'Not set')}")
    
    # Show analysis configuration
    analysis_config = config.get('ANALYSIS_CONFIG', {})
    print(f"Confidence Threshold: {analysis_config.get('CONFIDENCE_THRESHOLD', 'Not set')}")
    print(f"Enable AI Analysis: {analysis_config.get('ENABLE_AI_ANALYSIS', 'Not set')}")
    print(f"Enable Rule-based Checks: {analysis_config.get('ENABLE_RULE_BASED_CHECKS', 'Not set')}")

def example_output_formats():
    """Demonstrate different output formats."""
    print("\n📤 Output Format Examples")
    print("=" * 50)
    
    inspector = PowerPointInspector()
    
    # Analyze sample slides
    inconsistencies = inspector.analyze_presentation()
    
    if inconsistencies:
        # Console output
        print("\n1. Console Output:")
        inspector.report_generator.generate_report(
            inconsistencies, 
            output_format="console"
        )
        
        # JSON output
        print("\n2. JSON Output (saved to file):")
        inspector.report_generator.generate_report(
            inconsistencies, 
            output_format="json", 
            output_file="example_output.json"
        )
        print("   Saved to: example_output.json")
        
        # CSV output
        print("\n3. CSV Output (saved to file):")
        inspector.report_generator.generate_report(
            inconsistencies, 
            output_format="csv", 
            output_file="example_output.csv"
        )
        print("   Saved to: example_output.csv")
    else:
        print("No inconsistencies found to demonstrate output formats.")

def main():
    """Run all examples."""
    print("🚀 PowerPoint Inspector - Examples")
    print("=" * 60)
    
    try:
        # Check if API key is set
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️  Warning: GEMINI_API_KEY not set in environment variables")
            print("   Some features may not work properly")
            print("   Set it using: export GEMINI_API_KEY='your_key_here'")
            print()
        
        # Run examples
        example_basic_usage()
        example_custom_analysis()
        example_output_formats()
        
        print("\n✅ Examples completed successfully!")
        print("\n📁 Generated files:")
        print("   - example_output.json")
        print("   - example_output.csv")
        print("   - inconsistencies.json (if PowerPoint file was analyzed)")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
