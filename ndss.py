import requests
import urllib.parse
import re
import csv
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
                current_paper = {}
                paper = item.find('div', {"class": "selected-post-text-area rel-paper-in"})
                paper_title_link = ''
                if paper:
                    paper_title_link = paper.find('a')
                if paper_title_link:
                    current_paper = get_paper_info(paper_title_link.get('href'))
                    papers.update(current_paper)
            return papers
        else:
            print("[-] No item found.")
            return {}
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
        paper_title = soup.find('h1', {"class": "entry-title"}).text

        paper_authors_div = soup.find('div', {"class": "paper-data"})
        paper_authors_raw = paper_authors_div.find('strong').text.strip() if paper_authors_div else 'No Author'
        paper_authors = re.sub(r'\s*\([^)]*\)', '', paper_authors_raw)
        paper_attr.append(paper_authors)

        paper_link = soup.find('a', {"class", "pdf-button"}).get('href') if soup.find('a', {"class", "pdf-button"}) else 'No Link'
        paper_attr.append(paper_link)
        paper[paper_title] = paper_attr

        if paper:
            return paper
        else:
            print("[-] No item found.")
            return {}
    except requests.RequestException as e:
        print(f"Error fetching the item: {e}")
        return {}

# List of conference URLs
data_urls = [
    "https://www.ndss-symposium.org/ndss2023/accepted-papers/",
    "https://www.ndss-symposium.org/ndss2022/accepted-papers/",
    # Add more URLs as needed
]

with open('ndss.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    header = ['Num', 'Paper Title', 'Author', 'Affiliation', 'Conference', 'Year', 'Link to Paper', 'Link for Code',
              'Available', 'ReadMe', 'RepoGoal', 'TrainedModel', 'Out-of-box', 'Runs', 'Output', 'Data_Available',
              'Train/test', 'Reason', 'Model Used', 'Hyperparameters', 'Training Described']
    writer.writerow(header)

    i = 0
    for url in data_urls:
        print(f"[+] Get papers for URL: {url}")
        papers = get_paper(url)
        print("[+] Write papers to csv")
        for paper in papers:
            print(i, paper, papers[paper][0], '', 'NDSS', '2023', papers[paper][1])  # Adjust year if necessary
            data = [i, paper, papers[paper][0], '', 'NDSS', '2023', papers[paper][1], '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            writer.writerow(data)
            i += 1
