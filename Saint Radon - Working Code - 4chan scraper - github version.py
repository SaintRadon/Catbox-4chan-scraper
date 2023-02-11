import os
import re
import requests
import time

# THIS CODE WILL SCRAPE 4CHAN
# RUN AT YOUR OWN RISK

# Start off with the basic requests and all that 
board = "" # Enter the letter of the board you wish to scrape
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
response = requests.get("https://a.4cdn.org/{}/catalog.json".format(board), headers=headers)
catalog = response.json()
post_numbers = []

# Iterate over the pages in the catalog to get the desired threads
# Change the search string as desired
for page in catalog:
    for thread in page["threads"]:
        if "sub" in thread and re.search(r"Diffusion ", thread["sub"], re.IGNORECASE):
            post_numbers.append(thread["no"])

print(post_numbers)

# Transform the post_numbers into a list of URLs
urls = ["https://boards.4chan.org/{}/thread/{}".format(board, post_number) for post_number in post_numbers] 
  
# Now we gotta download everything 
def download_files(urls):
    pattern = re.compile(r'https://files\.catbox\.moe/[a-z0-9]{6}\.png')
    save_dir = r'E:\Saint Radon\Feb 2023\4chan scraper\Scraper'
    count = 0
    start_time = time.time()
    # Loop through the thread URLs passed in as an argument
    for url in urls:
        response = requests.get(url, headers=headers)
        matches = re.findall(pattern, response.text)
        for match in matches:
            # The Catbox urls
            print(match) 
        # Now, in a loop, download the catbox urls, download them, save them, and name them
        for match in matches:
            try:
                response = requests.get(match, headers=headers)
                filename = os.path.basename(match)
                with open(os.path.join(save_dir, filename), 'wb') as f:
                    f.write(response.content)
                count += 1
            except Exception as e:
                print(f'Error downloading {match}: {e}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'{count} files downloaded successfully in {elapsed_time:.2f} seconds.')
    print(f'{count / elapsed_time:.2f} images/s')
download_files(urls)


'''
from bs4 import BeautifulSoup
# Alternate version that uses BS4, but it is slower
def download_files(urls):
    pattern = re.compile(r'https://files\.catbox\.moe/[a-z0-9]{6}\.png')
    save_dir = r'E:\Saint Radon\Feb 2023\4chan scraper\Scraper'
    count = 0
    start_time = time.time()
    # Loop through the thread URLs passed in as an argument
    for url in urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        post_messages = soup.find_all('blockquote', {'class': 'postMessage'})
        for post_message in post_messages:
            matches = re.findall(pattern, str(post_message))
            for match in matches:
                print(match)
                try:
                    response = requests.get(match, headers=headers)
                    filename = os.path.basename(match)
                    with open(os.path.join(save_dir, filename), 'wb') as f:
                        f.write(response.content)
                    count += 1
                except Exception as e:
                    print(f'Error downloading {match}: {e}')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'{count} files downloaded successfully in {elapsed_time:.2f} seconds.')
    print(f'{count / elapsed_time:.2f} images/s')
download_files(urls)
'''