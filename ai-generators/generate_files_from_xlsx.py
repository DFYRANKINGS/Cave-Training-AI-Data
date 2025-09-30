# ai-generators/generate_files_from_xlsx.py — DEBUG VERSION

import argparse
import os
import json
import yaml
from pathlib import Path
import pandas as pd

SHEET_CONFIG = {
    'core_info': {
        'output_dir': 'schema-files/organization',
        'filename_base': 'main-data',
        'is_list': False,
        'is_horizontal': True
    },
    # ... keep other sheets if you want, or comment them out for testing
}

def clean_value(key, val):
    if pd.isna(val):
        return None
    val = str(val).strip()
    if val.lower() in ['not specified', 'n/a', '', 'none']:
        return None
    if key == 'sameAs' and isinstance(val, str):
        urls = [url.strip() for url in val.split('<|>') if url.strip()]
        return urls if urls else None
    if val.replace('.', '', 1).isdigit():
        return float(val) if '.' in val else int(val)
    if val.lower() in ['true', 'yes']:
        return True
    elif val.lower() in ['false', 'no']:
        return False
    return val

def parse_sheet_to_dict_or_list(df, is_list=False, is_horizontal=False):
    if is_list:
        if df.shape[0] == 0:
            return []
        headers = df.iloc[0].apply(lambda x: str(x).strip() if pd.notna(x) else "").tolist()
        records = []
        for idx in range(1, len(df)):
            row = df.iloc[idx]
            record = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    val = clean_value(header, row.iloc[i]) if pd.notna(row.iloc[i]) else None
                    if val is not None:
                        record[header] = val
            if record:
                records.append(record)
        return records
    else:
        if is_horizontal and df.shape[0] >= 2:
            headers = df.iloc[0].apply(lambda x: str(x).strip() if pd.notna(x) else "").tolist()
            values = df.iloc[1].tolist()
            data = {}
            for i, key in enumerate(headers):
                if i < len(values):
                    val = clean_value(key, values[i])
                    # EVEN IF NONE, SET TO EMPTY STRING FOR DEBUG
                    data[key] = val if val is not None else ""
            return data
        else:
            data = {}
            for _, row in df.iterrows():
                if len(row) < 2:
                    continue
                key_cell = row.iloc[0]
                if pd.isna(key_cell) or str(key_cell).strip() == '':
                    continue
                key = str(key_cell).strip()
                value = clean_value(key, row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else ""
                data[key] = value
            return data

def write_json_yaml(data, output_path, filename_base):
    output_path.mkdir(parents=True, exist_ok=True)
    json_path = output_path / f"{filename_base}.json"
    yaml_path = output_path / f"{filename_base}.yaml"

    # FORCE WRITE EVEN IF EMPTY
    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ FORCED WRITE: {json_path}")
    except Exception as e:
        print(f"❌ Failed to write JSON: {e}")
        return False

    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
        print(f"✅ FORCED WRITE: {yaml_path}")
    except Exception as e:
        print(f"❌ Failed to write YAML: {e}")
        return False

    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to input .xlsx file')
    args = parser.parse_args()

    print(f"📂 Working dir: {os.getcwd()}")
    if not os.path.exists(args.input):
        print(f"❌ File not found: {args.input}")
        exit(1)

    try:
        xls = pd.ExcelFile(args.input)
        print(f"📄 Sheets found: {xls.sheet_names}")
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        exit(1)

    # FORCE PROCESS core_info ONLY FOR DEBUG
    sheet_name = 'core_info'
    if sheet_name not in xls.sheet_names:
        print(f"❌ FATAL: Sheet '{sheet_name}' not found. Available: {xls.sheet_names}")
        exit(1)

    print(f"\n--- FORCING PROCESS: {sheet_name} ---")
    df = pd.read_excel(xls, sheet_name=sheet_name, header=None)
    print(f"📊 Shape: {df.shape}")

    if df.shape[0] < 2:
        print("❌ Sheet has less than 2 rows — cannot process horizontal layout")
        exit(1)

    data = parse_sheet_to_dict_or_list(df, is_list=False, is_horizontal=True)
    print(f"📦 PARSED DATA: {data}")

    output_dir = Path("schema-files/organization")
    success = write_json_yaml(data, output_dir, "main-data")

    if success:
        print("🎉 SUCCESS: Files written!")
    else:
        print("❌ FAILED: Could not write files")

    # ALWAYS SAVE SITE URL FOR SITEMAP
    site_url = data.get('website', 'https://example.com')
    config_dir = Path(".github/config")
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(config_dir / "site_url.txt", "w") as f:
        f.write(site_url.strip())
    print(f"🌐 Site URL set to: {site_url}")

if __name__ == "__main__":
    main()
