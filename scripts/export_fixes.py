import json
import csv

def main():
    try:
        with open('outputs/report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)
    except FileNotFoundError:
        print("Error: outputs/report.json not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode outputs/report.json.")
        return

    fixes = report.get("fixes", {})

    # Titles Fixes
    titles_fixes = fixes.get("titles", [])
    with open('outputs/titles_fixes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["url", "old", "new"])
        writer.writeheader()
        writer.writerows(titles_fixes)

    # Redirect Map
    redirect_map = fixes.get("redirect_map", [])
    with open('outputs/redirect_map.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["from", "to", "reason"])
        writer.writeheader()
        writer.writerows(redirect_map)

if __name__ == "__main__":
    main()
