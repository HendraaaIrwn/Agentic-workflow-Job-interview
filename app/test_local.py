from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.modules.research.methods import run_interview_prep_workflow

if __name__ == "__main__":
    result = run_interview_prep_workflow("Backend Developer")
    print("Report saved at:", result["report_path"])
    print("Report format:", result["report_format"])
