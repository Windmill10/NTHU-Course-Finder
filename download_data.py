import requests
import json
from pathlib import Path
import sys

def download_course_data(output_path: str = "course_data.json") -> bool:
    """
    Download course data from NTHU API and save to JSON file
    Returns True if successful, False otherwise
    """
    url = 'https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/OPENDATA/open_course_data.json'
    
    try:
        # Fetch data
        response = requests.get(url)
        response.encoding = 'utf-8'
        courses_data = response.json()
        
        # Save to file
        output_file = Path(output_path)
        with output_file.open('w', encoding='utf-8') as f:
            json.dump(courses_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully downloaded course data to {output_path}")
        return True
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return False
    except IOError as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = download_course_data()
    sys.exit(0 if success else 1)