from argparse import ArgumentParser
from datetime import date
import json
from pathlib import Path


def build_version(major_update: int, minor_update: int) -> str:
    """Build a version number in the format 1.major.minor.yyyymmdd."""
    if major_update < 0:
        raise ValueError("major update number must be 0 or higher")

    if minor_update < 0:
        raise ValueError("minor update number must be 0 or higher")

    local_date = date.today()
    date_section = local_date.strftime("%Y%m%d")

    return f"1.{major_update}.{minor_update}.{date_section}"


def update_package_json(package_json_path: Path, version: str) -> None:
    """Update the version field in package.json."""
    if not package_json_path.exists():
        raise FileNotFoundError(f"Could not find {package_json_path}")

    package_data = json.loads(package_json_path.read_text(encoding="utf-8"))
    package_data["version"] = version

    package_json_path.write_text(
        json.dumps(package_data, indent=2) + "\n",
        encoding="utf-8",
    )


def prompt_for_update_number(label: str) -> int:
    while True:
        raw_value = input(f"{label} update number: ").strip()

        try:
            update_number = int(raw_value)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if update_number < 0:
            print("Please enter a number that is 0 or higher.")
            continue

        return update_number


def main() -> None:
    parser = ArgumentParser(
        description="Generate a version number and save it to package.json."
    )
    parser.add_argument(
        "--package-json",
        default="package.json",
        help="Path to package.json. Defaults to package.json in the current folder.",
    )

    args = parser.parse_args()
    major_update = prompt_for_update_number("Major")
    minor_update = prompt_for_update_number("Minor")
    version = build_version(major_update, minor_update)
    package_json_path = Path(args.package_json)

    update_package_json(package_json_path, version)
    print(f"Updated {package_json_path} to version {version}")


if __name__ == "__main__":
    main()