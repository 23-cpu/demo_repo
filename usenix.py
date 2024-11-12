import requests
import csv
from bs4 import BeautifulSoup

def get_paper_title(search_url):
    papers = {}
    try:
        response = requests.get(search_url, headers={'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', {"class": "field-item"})

        if items:
            for item in items:
                paper = item.find('article')
                paper_title_link = ''
                paper_author = ''
                paper_attr = []

                if paper:
                    paper_title_heading = paper.find('h2', {"class": "node-title"})
                    paper_title_link = paper_title_heading.find('a') if paper_title_heading else None
                    paper_author = paper.find('p')

                if paper_title_link and paper_author:
                    # Debug output to verify parsing
                    print(f"[DEBUG] Found paper: {paper_title_link.text.strip()} by {paper_author.text.strip()}")

                    # Get authors
                    paper_attr.append(paper_author.text.strip())

                    # Get paper link from details
                    final_paper_link = get_paper_link('https://www.usenix.org' + paper_title_link.get('href'))
                    paper_attr.append(final_paper_link)

                    # Add paper and its attributes to dict
                    papers[paper_title_link.text.strip()] = paper_attr
            return papers
        else:
            print("[-] No item found or structure mismatch.")
            return {}
    except requests.RequestException as e:
        print(f"Error fetching the item: {e}")
        return {}

def get_paper_link(usenix_url):
    try:
        response = requests.get(usenix_url, headers={'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        final_paper = soup.find('div', {"class": "field-name-field-final-paper-pdf"})

        if final_paper and final_paper.find('a'):
            return final_paper.find('a').get('href')
        else:
            print("[-] No final paper link found.")
            return 'No Link Available'
    except requests.RequestException as e:
        print(f"Error fetching the paper link: {e}")
        return 'Error fetching link'

# List of conference URLs to scrape
data_urls = [
"https://www.usenix.org/conference/usenixsecurity19/fall-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity20/spring-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity20/summer-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity20/fall-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity21/summer-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity21/fall-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity22/summer-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity22/fall-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity22/winter-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity23/summer-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity23/fall-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity24/summer-accepted-papers",
"https://www.usenix.org/conference/usenixsecurity24/fall-accepted-papers"  
]

# Open CSV file for writing
with open('usenix.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    header = ['Num', 'Paper Title', 'Author', 'Affiliation', 'Conference', 'Year', 'Link to Paper', 'Link for Code', 
              'Available', 'ReadMe', 'RepoGoal', 'TrainedModel', 'Out-of-box', 'Runs', 'Output', 'Data_Available', 
              'Train/test', 'Reason', 'Model Used', 'Hyperparameters', 'Training Described']
    writer.writerow(header)

    for url in data_urls:
        print(f"[+] Getting papers for URL: {url}")
        papers = get_paper_title(url)
        
        if not papers:
            print(f"[-] No papers found for {url}")
            continue

        i = 0
        print("[+] Writing papers to CSV")
        for paper, attributes in papers.items():
            print(f"[INFO] Writing paper: {paper}")
            data = [i, paper, attributes[0], '', 'Usenix', '2023', attributes[1], '', '', '', '', '', '', '', '', '', '', '', '', '', '']
            writer.writerow(data)
            i += 1

print("[INFO] Data extraction completed.")
