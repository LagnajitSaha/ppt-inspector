import json
from .models import Inconsistency

class ReportGenerator:
    def __init__(self, output_format="json"):
        self.output_format = output_format

    def save(self, issues, output_file):
        if self.output_format == "json":
            data = [issue.__dict__ for issue in issues]
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                for issue in issues:
                    f.write(f"[{issue.type}] Slides {issue.slides} → {issue.description}\n")
