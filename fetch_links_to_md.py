import os
import requests
from bs4 import BeautifulSoup

table_path = "training_list.md"
output_dir = "/training_links_content"
os.makedirs(output_dir, exist_ok=True)

def extract_links_titles(md_path):
    links_titles = []
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("| ") and "[Link](http" in line:
                parts = line.strip().split("|")
                if len(parts) >= 4:
                    title = parts[2].strip()
                    link = parts[3].split("[")[1].split("](")[1].split(")")[0]
                    links_titles.append((title, link))
    return links_titles

def fetch_and_save(title, url, out_dir):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        main = soup.find("main")
        text = main.get_text("\n", strip=True) if main else soup.get_text("\n", strip=True)
        safe_title = "".join(c for c in title if c.isalnum() or c in "-_ ").rstrip()
        out_path = os.path.join(out_dir, f"{safe_title}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(text)
        print(f"Saved: {out_path}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

def main():
    links_titles = extract_links_titles(table_path)
    for title, url in links_titles:
        fetch_and_save(title, url, output_dir)

if __name__ == "__main__":
    main()
