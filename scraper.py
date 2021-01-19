import threading

import requests
import re
from urllib.parse import urlparse


#
# This is crawler to find all links
#
# @author: Filip Werra s19375
#



class PyCrawler(object):
    def __init__(self, starting_url):
        starting_url = "https://www.marketviewliquor.com/blog/2018/08/how-to-choose-a-good-wine/"
        self.starting_url = starting_url
        self.visited = set()

    def get_html(self, url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('latin-1')

    # deflinks leci po wszystkich linkach
    def get_links(self, url):
        html = self.get_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)  # z tego trzeba wyciągnąć 10 linków
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base

        return set(filter(lambda x: 'mailto' not in x, links))

    def extract_info(self, url):
        html = self.get_html(url)
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)
        return dict(meta)

    def print_link(self, info, link):
        if "wine" in info.get('description'):
            print(f"""Link: {link}
            Description: {info.get('description')} 
            Keywords: {info.get('keywords')}
                    """)

    def crawl(self, url):
        count = 0
        for link in self.get_links(url):
            if link in self.visited:
                continue
            self.visited.add(link)
            info = self.extract_info(link)
            threads = []
            for counter in range(10):
                t = threading.Thread(target=self.print_link(info, link))
                threads.append(t)
                t.start()
                t.join()
            break

    def start(self):
        self.crawl(self.starting_url)


if __name__ == "__main__":
    crawler = PyCrawler("https://www.marketviewliquor.com/blog/2018/08/how-to-choose-a-good-wine/")
    crawler.start()
