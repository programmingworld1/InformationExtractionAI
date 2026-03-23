import sys
import json
from pathlib import Path

from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput, AnalysisResult
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential

SCRIPT_DIR = Path(__file__).parent


def analyze_file(client: ContentUnderstandingClient, analyzer_id: str, file_path: Path) -> None:
    print(f"Analyzing: {file_path.name}")

    file_bytes = file_path.read_bytes()

    try:
        poller = client.begin_analyze_binary(
            analyzer_id=analyzer_id,
            binary_input=file_bytes,
            content_type="application/pdf",
        )
        result: AnalysisResult = poller.result()
    except AzureError as err:
        print(f"[Azure Error] {file_path.name}: {err.message}")
        return
    except Exception as ex:
        print(f"[Unexpected Error] {file_path.name}: {ex}")
        return

    print("=" * 50)
    print(f"Analysis result for: {file_path.name}")
    print("=" * 50 + "\n")

    max_display_lines = 50
    result_str = json.dumps(result.as_dict(), indent=2)
    ret_lines = result_str.splitlines()

    if len(ret_lines) > max_display_lines:
        print("\n".join(ret_lines[:max_display_lines]))
        print(f"\n  {len(ret_lines) - max_display_lines} more lines not displayed...\n")
    else:
        print(result_str)

    print()


def main() -> None:
    endpoint = ""
    key = ""
    analyzer_id = "myfirstanalyzer"
    api_version = "2025-11-01"

    # Local files to analyze — add more filenames here as needed.
    local_files = [
        SCRIPT_DIR / "CV Murat Yilmaz recent.pdf",
    ]

    credential = AzureKeyCredential(key)
    client = ContentUnderstandingClient(endpoint=endpoint, credential=credential, api_version=api_version)

    print(f"Analyzing with '{analyzer_id}' analyzer...\n")

    for file_path in local_files:
        if not file_path.exists():
            print(f"[Skipped] File not found: {file_path.name}")
            continue
        analyze_file(client, analyzer_id, file_path)


if __name__ == "__main__":
    main()
