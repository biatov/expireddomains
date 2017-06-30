import subprocess

# subprocess.call('scrapy crawl get_title_and_href -o title_and_href.json', shell=True)
subprocess.call('scrapy crawl get_domains -o tetatet.csv', shell=True)
