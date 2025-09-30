# generate_sitemaps.py

import os
from pathlib import Path
from datetime import datetime
import glob

def get_site_url():
    config_path = Path(".github/config/site_url.txt")
    if config_path.exists():
        with open(config_path, 'r') as f:
            url = f.read().strip()
            if url:
                return url.rstrip('/')
    # Fallback to env (in case script runs outside workflow)
    return os.getenv('SITE_BASE_URL', 'https://example.com').rstrip('/')

def find_generated_files():
    """Find all generated .json and .yaml in schema-files/"""
    patterns = [
        "schema-files/**/*.json",
        "schema-files/**/*.yaml"
    ]
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern, recursive=True))
    return sorted(set(files))  # dedupe

def generate_sitemap_xml(site_url, files):
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for file_path in files:
        # Convert file path to URL path
        relative_path = Path(file_path)
        public_path = str(relative_path).replace("\\", "/")  # Windows-safe
        full_url = f"{site_url}/{public_path}"
        
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{full_url}</loc>")
        xml_lines.append(f"    <lastmod>{now}</lastmod>")
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")

    return "\n".join(xml_lines)

def main():
    site_url = get_site_url()
    print(f"🌍 Base URL: {site_url}")

    files = find_generated_files()
    print(f"📄 Found {len(files)} files for sitemap:")

    for f in files:
        print(f"   - {f}")

    sitemap_content = generate_sitemap_xml(site_url, files)

    with open("ai-sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    print("✅ ai-sitemap.xml generated successfully.")

if __name__ == "__main__":
    main()
