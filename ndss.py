import requests
import csv
import re
from bs4 import BeautifulSoup

def get_paper(search_url):
    papers = {}
    try:
        response = requests.get(search_url, headers={'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', {"class": "tag-box rel-paper"})

        if items:
            for item in items:
                paper_title_link = item.find('a')
                if paper_title_link:
                    paper_info = get_paper_info(paper_title_link.get('href'))
                    if paper_info:
                        papers.update(paper_info)
        else:
            print("[-] No paper items found. Check HTML structure.")
            return {}
        return papers
    except requests.RequestException as e:
        print(f"Error fetching the item: {e}")
        return {}

def get_paper_info(ndss_url):
    try:
        paper = {}
        paper_attr = []
        response = requests.get(ndss_url, headers={'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        paper_title = soup.find('h1', {"class": "entry-title"})
        if not paper_title:
            print(f"[-] No title found for {ndss_url}")
            return {}

        paper_title = paper_title.text.strip()

        paper_authors_div = soup.find('div', {"class": "paper-data"})
        paper_authors_raw = paper_authors_div.find('strong').text.strip() if paper_authors_div else 'No Author'
        paper_authors = re.sub(r'\s*\([^)]*\)', '', paper_authors_raw)
        paper_attr.append(paper_authors)

        paper_link = soup.find('a', {"class": "pdf-button"})
        paper_link = paper_link.get('href') if paper_link else 'No Link'
        paper_attr.append(paper_link)

        paper[paper_title] = paper_attr
        return paper
    except requests.RequestException as e:
        print(f"Error fetching paper info: {e}")
        return {}

# List of conference URLs (ensure these URLs are correct and accessible)
data_urls = [
    "https://www.ndss-symposium.org/ndss2023/accepted-papers/",
    "https://www.ndss-symposium.org/ndss2022/accepted-papers/",
    # Add more URLs as needed
]

# Open CSV file for writing
with open('ndss.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    header = ['Num', 'Paper Title', 'Author', 'Affiliation', 'Conference', 'Year', 'Link to Paper', 'Link for Code',
              'Available', 'ReadMe', 'RepoGoal', 'TrainedModel', 'Out-of-box', 'Runs', 'Output', 'Data_Available',
              'Train/test', 'Reason', 'Model Used', 'Hyperparameters', 'Training Described']
    writer.writerow(header)

    i = 0
    for url in data_urls:
        print(f"[+] Getting papers for URL: {url}")
        papers = get_paper(url)
        print("[+] Writing papers to CSV")
        for paper, attributes in papers.items():
            year = re.search(r'ndss(\d{4})', url).group(1) if re.search(r'ndss(\d{4})', url) else 'Unknown Year'
            print(f"[INFO] Writing paper: {paper}")
            data = [i, paper, attributes[0], '', 'NDSS', year, attributes[1], '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            writer.writerow(data)
            i += 1

print("[INFO] Data extraction completed.")
