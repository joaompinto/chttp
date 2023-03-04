import concurrent.futures
from dataclasses import dataclass

import requests

# https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor


@dataclass
class Fetcher:
    urls: list[str]  # List of urls to be downloaded
    max_workers: int | None = None

    def get_all(self):
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {
                executor.submit(self.fetch_url, url): url for url in self.urls
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                except Exception as exc:
                    print("%r generated an exception: %s" % (url, exc))
                else:
                    yield result

    def fetch_url(self, url):
        return requests.get(url)
