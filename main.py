from curl_cffi import requests
from lxml import etree, html

import config
from log import Log

class Discovery:
    def __init__(self):
        self._logger = Log.get_logger(config.LOG_PATH)
        self._records = set()

    def _make_request(self, *args):
        try:
            self._logger.info(f"Starting the request process")

            retries = 0
            max_retries = 3

            while retries < max_retries:
                try:
                    res = requests.get(*args)

                    res.raise_for_status()

                    return res

                except Exception:
                    self._logger.error(f"Request atempted, status code: {res.status_code}. Attempt n: {retries}")
                    
                    retries += 1

        except Exception as e:
            self._logger.critical(f"Max ammount of retries attempted. Error: {e}")

    def _get_product_urls(self, sitemap):
        try:
            self._logger.info(f"Starting the get product urls for sitemap: {sitemap}")
            
            res = self._make_request(
                url = sitemap,
                headers = config.HEADERS,
                timeout = config.TIMEOUT,
                proxies = config.PROXIES,
            )

            tree = etree.fromstring(res.content)

            product_urls = tree.xpath(
                "//sm:loc/text()",
                namespaces={"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            )

            for url in product_urls:
                self._records.add(url)
            
            self._logger.info(f"Completed the get product urls process successfully for sitemap: {sitemap}. Total matches: {len(product_urls)}")

        except Exception as e:
            self._logger.critical(f"There was an error while getting the product urls. Error: {e}")

    def _get_sitemaps(self):
        try:
            self._logger.info("Starting the get sitemaps process")
            res = self._make_request(
                url = f"{config.BASE_URL}",
                headers = config.HEADERS,
                timeout = config.TIMEOUT,
                proxies = config.PROXIES
            )

            tree = html.fromstring(res.text)

            raw = tree.xpath("//div[contains(@class, 'listapaises')]//ul//li//a/@href")

            sitemaps = set()

            for url in raw:
                sitemaps.add(f"{url}/sitemaps/productos.xml")

            return sitemaps

        except Exception as e:
            self._logger.critical(f"There was an error getting the sitemaps. Error: {e}")
    
    def run(self):
        try:
            self._logger.info("Starting the discovery process")

            country_sitemaps = self._get_sitemaps()

            for sitemap in country_sitemaps:
                self._get_product_urls(sitemap)

            self._logger.info(f"Completed the discovery process. Total product urls: {len(self._records)}")

            return self._records

        except Exception as e:
            self._logger.error(f"There was an error in the discovery process. Error: {e}")

class PDP:
    def __init__(self):
        self._logger = Log.get_logger(config.LOG_PATH)

    def _make_request(self, *args):
        try:
            self._logger.info(f"Starting the request process")

            retries = 0
            max_retries = 3

            while retries < max_retries:
                try:
                    res = requests.get(*args)

                    res.raise_for_status()

                    return res

                except Exception:
                    self._logger.error(f"Request atempted, status code: {res.status_code}. Attempt n: {retries}")
                    
                    retries += 1

        except Exception as e:
            self._logger.critical(f"Max ammount of retries attempted. Error: {e}")

    def _parse_text(self, raw):
        try:
            pass
        except Exception as e:
            pass
    
    def _parse_number(self, raw):
        try:
            pass
        except Exception as e:
            pass

    def _parse_description(self, index, description):
        try:
            self._logger.info(f"Parsing description for product: {index}")
            if description is None:
                return None

            parsed = description.replace("\n", "")
            
            return parsed

        except Exception as e:
            self._logger.error(f"There was an error parsing the description for the product: {index}. Error: {e}")

    def _parse_author(self, index, author):
        try:
            self._logger.info(f"Parsing author for product: {index}")
            if author is None:
                return None

            author_url = author.get("url", None)
            author_name = author.get("name", None)

            return author_url, author_name

        except Exception as e:
            self._logger.error(f"There was an error parsing the author for the product {index}. Error: {e}")

    def _parse_publisher(self, index, publisher):
        try:
            pass
        except Exception as e:
            self._logger.error(f"There was an error parsing the publisher for the product {index}. Error {e}")

    def _search_nodes(self, index, tree, xpath):
        try:
            self._logger(f"Searching a node for product: {index}")

            nodes = tree.xpath(xpath)
            if not nodes:
                return None

            if nodes is list:
                return
            
            return nodes[0]
            
        except Exception as e:
            self._logger.error(f"There was an error parsing the translator for the product {index}. Error: {e}")
    
    def _parse_product_data(self, index, tree):
        '''
        data to extract:

        # contenido
        description
        author
        translator
        publisher
        collection
        language

        # edición / formato
        format              # Libro Físico
        binding             # Tapa Blanda
        pages
        year
        edition
        published_in        # Editado en (España)
        dimensions
        weight

        # comercialización
        currency
        base_price
        offer_price
        availability
        categories

        # opcional
        rating
        review_count
        '''
        try:
            self._logger.info(f"Starting the data parsing for product: {index}")

            script = tree.xpath("//script[@type='application/ld+json']")

            # Content
            description = self._parse_description(index, script.get("description", None))
            author_url, author_name = self._parse_author(index, script.get("author", None))
            translator_url = self._search_nodes(index, "//div[@id='metadata-Traducido por']//a[contains(@class, 'primary')]/@href")
            translator_name = self._search_nodes(index, "//div[@id='metadata-Traducido por']//a[contains(@class, 'primary')]/text()")

            return {
                # Identity
                "url": script.get("url", None),
                "sku": script.get("url", None),
                "isbn": script.get("isbn", None),
                "isbn13": script.get("gtin13", None),
                "name": script.get("name", None),
                "image": script.get("image", None),

                # Content
                "description": description,
                "author_url": author_url,
                "author_name": author_name,
                "translator_url": translator_url,
                "translator_name": translator_name,
                "publisher_url": 

                


            }
        except Exception as e:
            self._logger.error(f"There was an error parsing data for product {index}. Error: {e}")

    def _get_product_data(self, index, url):
        try:
            self._logger.info(f"Starting the data extraction for product: {index}")

            product = {}

            res = requests.get(
                url = url,
                headers = config.HEADERS,
                timeout = config.TIMEOUT,
                proxies = config.PROXIES
            )
            res.raise_for_status()

            tree = html.formstring(res.text)

            product = self._parse_product_data(index, tree)

            return product

        except Exception as e:
            self._logger.error(f"There was an error while getting the data for product: {url}. Error: {e}")
            raise

    def run(self, products):
        try:
            self._logger.info(f"Starting the PDP process")
            for index, url in enumerate(products, start=1):
                self._get_product_data(index, url)

        except Exception as e:
            self._logger.error(f"There was an error in the PDP process. Error: {e}")

if __name__ == "__main__":
    urls = Discovery().run()
    products = PDP().run()

    print(products)