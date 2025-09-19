import pytest
import sys
import json

def get_metadata_args():
    """
    Reads metadata from a JSON file and formats it for pytest-html.
    """
    try:
        with open('metadata.json', 'r') as f:
            metadata = json.load(f)
    except FileNotFoundError:
        return [] # Return an empty list if file not found

    metadata_args = []
    for key, value in metadata.items():
        metadata_args.append("--metadata")
        metadata_args.append(f"{key}")
        metadata_args.append(f"{value}")
    return metadata_args

def main():
    """
    Main function to run tests with a dynamic HTML report.
    """
    # Base pytest arguments
    args = [
        "-v",
        "-m", "sim",
        "--html=reports/automation_report.html",
        "tests/"
    ]

    # Add metadata arguments
    metadata_args = get_metadata_args()
    args.extend(metadata_args)

    # Run pytest
    sys.exit(pytest.main(args))

if __name__ == "__main__":
    main()