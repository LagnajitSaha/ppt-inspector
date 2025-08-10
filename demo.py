#!/usr/bin/env python3
"""
Demo script for PowerPoint Inconsistency Detector

This script demonstrates the tool's capabilities by analyzing the sample slides
and showing the inconsistencies found.
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ppt_inspector import PowerPointInspector, ContentExtractor, AIAnalyzer, ReportGenerator

def run_demo():
    """Run the main demo."""
    print("🎯 PowerPoint Inconsistency Detector - Live Demo")
    print("=" * 60)
    print("This demo will analyze the sample slides and show inconsistencies found.")
    print()
    
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
        print("🔧 Initializing PowerPoint Inspector...")
        inspector = PowerPointInspector(api_key)
        
        # Analyze sample slides
        print("\n📊 Analyzing sample slides for inconsistencies...")
        print("   (This may take a few moments as we analyze with AI)")
        print()
        
        inconsistencies = inspector.analyze_presentation(images_dir="sample_slides")
        
        # Show results
        print("\n" + "="*60)
        print("🔍 ANALYSIS RESULTS")
        print("="*60)
        
        if not inconsistencies:
            print("✅ No inconsistencies detected in the sample slides!")
        else:
            print(f"⚠️  Found {len(inconsistencies)} inconsistencies across the slides:")
            print()
            
            # Group by type for better organization
            by_type = {}
            for inc in inconsistencies:
                inc_type = inc.inconsistency_type
                if inc_type not in by_type:
                    by_type[inc_type] = []
                by_type[inc_type].append(inc)
            
            # Display findings
            for inc_type, incs in by_type.items():
                print(f"📋 {inc_type.upper()} ({len(incs)} issues):")
                print("-" * 40)
                
                for i, inc in enumerate(incs, 1):
                    print(f"\n{i}. {inc.description}")
                    print(f"   📍 Slides: {', '.join(map(str, inc.slide_numbers))}")
                    print(f"   🎯 Confidence: {inc.confidence:.1%}")
                    print(f"   📝 Evidence:")
                    for evidence in inc.evidence:
                        print(f"      • {evidence}")
                    print(f"   💡 Recommendation: {inc.recommendation}")
                    print()
        
        # Generate reports
        print("\n📊 Generating detailed reports...")
        
        # JSON report
        inspector.report_generator.generate_report(
            inconsistencies,
            output_format="json",
            output_file="demo_analysis_report.json"
        )
        
        # CSV report
        inspector.report_generator.generate_report(
            inconsistencies,
            output_format="csv",
            output_file="demo_analysis_report.csv"
        )
        
        print("\n✅ Demo completed successfully!")
        print("\n📁 Generated files:")
        print("   - demo_analysis_report.json")
        print("   - demo_analysis_report.csv")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_sample_slides_summary():
    """Show a summary of what the sample slides contain."""
    print("\n📋 SAMPLE SLIDES SUMMARY")
    print("=" * 40)
    print("The demo will analyze these sample slides:")
    print()
    print("Slide 1: Case Study - Noogat helps consultants make decks 2x faster using AI")
    print("   • Claims: 2x faster, $2M saved, 15 mins per slide")
    print()
    print("Slide 2: Noogat Helps Consultants Make Decks Faster Using AI")
    print("   • Claims: 3x faster, $3M saved, 20 mins per slide")
    print()
    print("Slide 3: Noogat: 50 Hours Saved Per Consultant Monthly")
    print("   • Claims: 50 hours total, but breakdown shows 40 hours (10+12+8+6+4)")
    print()
    print("Expected inconsistencies:")
    print("   • Performance claims: 2x vs 3x faster")
    print("   • Financial data: $2M vs $3M saved")
    print("   • Time savings: 15 mins vs 20 mins per slide")
    print("   • Mathematical error: 50 hours claimed vs 40 hours calculated")
    print()

def main():
    """Main demo function."""
    print("🚀 PowerPoint Inconsistency Detector - Interactive Demo")
    print("=" * 60)
    
    # Show sample slides summary
    show_sample_slides_summary()
    
    # Ask user if they want to proceed
    response = input("Do you want to run the demo? (y/n): ").lower().strip()
    if response not in ['y', 'yes']:
        print("Demo cancelled. You can run it later with: python demo.py")
        return
    
    # Run the demo
    success = run_demo()
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Review the generated reports")
        print("   2. Try with your own PowerPoint files")
        print("   3. Customize the analysis parameters")
    else:
        print("\n💥 Demo failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
