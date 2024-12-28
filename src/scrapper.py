import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from ratelimiter import RateLimiterWithQueue
import time

class Scrapper:
    """
    A web scrapper class to fetch and parse HTML content from a given URL.
    """

    def __init__(self, timeout : int = 10, max_workers : int = 10):
        """
        Initializes the Scrapper instance.
        """
        self.timeout = timeout
        self.max_workers = max_workers
        self.ratelimiter = RateLimiterWithQueue()

    def __scrap_one_link__(self, url: str, ip = 'localhost'):
        """
        Fetches and parses the HTML content of a given URL.

        Args:
            url (str): The URL of the webpage to scrape.

        Returns:
            BeautifulSoup: A BeautifulSoup object containing the parsed HTML of the webpage.

        Raises:
            ValueError: If the provided URL is invalid or empty.
            requests.RequestException: If there's an issue with the HTTP request.
        """
        # Validate the URL
        if not url or not isinstance(url, str):
            raise ValueError("The URL must be a non-empty string.")

        try:
            # checking the ratelimiter for this ip
            if self.ratelimiter.is_allowed(ip = ip):
                # Make an HTTP GET request to the URL
                response = requests.get(url, timeout=self.timeout)

                # Raise an exception for HTTP errors (4xx or 5xx responses)
                response.raise_for_status()

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                return soup

        except requests.exceptions.RequestException as e:
            # Handle network-related errors gracefully
            print(f"An error occurred while fetching the URL: {e}")
            raise e  # Re-raise the exception for further handling

        except Exception as e:
            # Handle any other unexpected errors
            print(f"An unexpected error occurred: {e}")
            raise e  # Re-raise the exception for further handling
        
    def __scrap_links__(self, urls: list,  ip = 'localhost'):
        """
        Scrapes multiple URLs concurrently, using threads to fetch and parse their HTML content.

        Args:
            urls (list): A list of URLs to scrape.

        Returns:
            list: A list of BeautifulSoup objects in the same order as the input URLs.

        Raises:
            ValueError: If the input is not a list of URLs.
        """
        # Validate the input
        if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
            raise ValueError("The input must be a list of non-empty string URLs.")

        # List to store the results in the same order as the input
        results = [None] * len(urls)

        # Function to wrap the private scrapping method for threading
        def fetch_url(index, url):
            try:
                soup = self.__scrap_one_link__(url)
                return index, soup
            except Exception as e:
                print(f"Error processing URL at index {index}: {e}")
                return index, None

        # Use ThreadPoolExecutor with a maximum of the max number of threads
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks for each URL
            future_to_index = {executor.submit(fetch_url, i, url): i for i, url in enumerate(urls)}

            # Collect results as they are completed
            for future in as_completed(future_to_index):
                index, soup = future.result()
                results[index] = soup

        return results

if __name__ == '__main__':
    
    urls = [
        "https://pypi.org/project/strings/",
        "https://pypi.org/project/beautifulsoup4/",
        "https://gpmegypt.com/ar/real-estate/artea-mall-new-cairo",
    ]

    # # test of __scrap_one_link__():
    # scrapper = Scrapper()
    # soup = scrapper.__scrap_one_link__(urls[0])
    # print(soup.prettify())
    # print(type(soup))



    # # test of __scrap_links__:
    scrapper = Scrapper()
    time_start = time.time()
    soups = scrapper.__scrap_links__(urls)
    print(f"\n ==> Scrapping no. of {len(urls)} urls took {time.time()-time_start}sec. \n")

    # Directory to save the soup files
    output_dir = "scraped_soups"
    os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

    # Write each soup to a separate file
    for index, soup in enumerate(soups):
        file_path = os.path.join(output_dir, f"soup_{index + 1}.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(soup.prettify())
            print(f"Soup {index +1} have been saved in the '{file_path}' file.")


    print(f"\n## All soups have been saved in the '{output_dir}' directory.")
