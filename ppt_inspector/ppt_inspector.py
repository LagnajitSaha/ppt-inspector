import argparse
from dotenv import load_dotenv
load_dotenv()

from .content_extractor import ContentExtractor
from .ai_analyzer import AIAnalyzer
from .report_generator import ReportGenerator


class PowerPointInspector:
    def __init__(self):
        self.extractor = ContentExtractor()
        self.analyzer = AIAnalyzer()
        self.reporter = ReportGenerator()

    def analyze(self, pptx_path, output_file="report.json"):
        slides = self.extractor.extract(pptx_path)
        issues = self.analyzer.check_consistency(slides)
        self.reporter.save(issues, output_file)
        print(f"Analysis complete. Found {len(issues)} issues. Report saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze PPTX for inconsistencies")
    parser.add_argument("--file", required=True, help="Path to PPTX file")
    parser.add_argument("--out", default="report.json", help="Output report file")
    args = parser.parse_args()

    inspector = PowerPointInspector()
    inspector.analyze(args.file, args.out)
