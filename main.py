from curl_cffi import requests
from curl_cffi.requests.websockets import T
from lxml import etree, html

import config
from log import Log

class Discovery:
    def __init__(self):
        self._logger = Log.get_logger(config.LOG_PATH)
        self._records = set()

    def _get_product_urls(self, sitemap):
        try:
            self._logger.info(f"Starting the get product urls for sitemap: {sitemap}")
            
            res = requests.get(
                url = sitemap,
                headers = config.DISCOVERY_HEADERS,
                timeout = config.TIMEOUT,
                proxies = config.PROXIES
            )
            res.raise_for_status()

            tree = etree.fromstring(res.content)

            product_urls = tree.xpath(
                "//sm:loc/text()",
                namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            )

            for url in product_urls:
                self._records.add(url)
            
            self._logger(f"Completed the get product urls process successfully. Total matches: {len(product_urls)}")

        except Exception as e:
            self._logger.error(f"There was an error while getting the product urls. Error: {e}")

    def _get_product_sitemaps(self):
        try:
            self._logger.info("Starting the get product sitemaps process")
            
            res = requests.get(
                url = f"{config.BASE_URL}/sitemaps/productos.xml",
                headers = config.DISCOVERY_HEADERS,
                timeout = config.TIMEOUT,
                prooxies = config.PROXIES
            )
            res.raise_for_status()

            tree = etree.fromstring(res.content)

            urls = tree.xpath(
                "//sm:loc/text()",
                namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            )

            self._logger.info("Completed get product sitemaps process successfully.")

            return urls

        except Exception as e:
            self._logger.error(f"There was an error while getting the product sitemaps. Error: {e}")
            raise

    def run(self):
        try:
            self._logger.info("Starting the discovery process")

            product_sitemaps = self._get_product_sitemaps()
            for sitemap in product_sitemaps:
                self._get_product_urls(sitemap)

            self._logger.info(f"Completed the discovery process. Total product urls: {len(self._records)}")

            return self._records

        except Exception as e:
            self._logger.error(f"There was an error in the discovery process. Error: {e}")

class PDP:
    def __init__(self):
        self._logger = Log.get_logger(config.LOG_PATH)

    def _parse_product_data(self, url, raw_data, real_price):
        try:
            '''
            data structure:

            

            '''
        except Exception as e:
            self._logger.error(f"There was an error while parsing the data for product: {url}. Error: {e}")
            raise

    def _get_product_data(self, url):
        try:
            self._logger.info(f"Starting the data extraction for product: {url}")

            res = requests.get(
                url = url,
                headers = config.PDP_HEADERS,
                timeout = config.TIMEOUT,
                proxies = config.PROXIES
            )
            res.raise_for_status()

            tree = html.formstring(res.text)

            real_price = tree.xpath("//span[contains(@class, 'pvp')]")
            raw_data = tree.xpath("//script[@type='application/ld+json']")[1]
            parsed_data = self._parse_product_data(url, raw_data, real_price)

            return parsed_data

        except Exception as e:
            self._logger.error(f"There was an error while getting the data for product: {url}. Error: {e}")
            raise

    def run(self, products):
        try:
            self._logger.info(f"Starting the PDP process")
            for url in products:
                self._get_product_data(url)

        except Exception as e:
            self._logger.error(f"There was an error in the PDP process. Error: {e}")

if __name__ == "__main__":
    urls = Discovery().run()
    products = PDP().run()

    print(products)