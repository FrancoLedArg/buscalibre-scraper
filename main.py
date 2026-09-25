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
            self._logger.info(f"Parsing publisher for product: {index}")
            if publisher is None:
                return None

            publisher_url = publisher.get("url", None)
            publisher_name = publisher.get("name", None)

            return publisher_url, publisher_name

        except Exception as e:
            self._logger.error(f"There was an error parsing the publisher for the product {index}. Error {e}")

    def _parse_reviews(self, index, reviews):
        try:
            self._logger.info(f"Parsing reviews for product: {index}")
            parsed = []

            for r in reviews:
                language = r.get("inLanguage", None)
                date_published = r.get("datePublished", None)
                rating = r.get("reviewRating", None).get("ratingValue", None)
                review_body = r.get("reviewBody", None)
                author = r.get("author", None).get("name", None)

                parsed.append({
                    "language": language,
                    "date_published": date_published,
                    "rating": rating,
                    "review_body": review_body,
                    "author": author,
                })

            return parsed

        except Exception as e:
            self._logger.error(f"There was an error parsing the reviews for the product {index}. Error {e}")

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
        try:
            self._logger.info(f"Starting the data parsing for product: {index}")

            script = tree.xpath("//script[@type='application/ld+json']")

            # Content
            description = self._parse_description(index, script.get("description", None))
            author_url, author_name = self._parse_author(index, script.get("author", None))
            translator_url = self._search_nodes(index, "//div[@id='metadata-Traducido por']//a[contains(@class, 'primary')]/@href")
            translator_name = self._search_nodes(index, "//div[@id='metadata-Traducido por']//a[contains(@class, 'primary')]/text()")
            publisher_url, publisher_name = self._parse_publisher(index, script.get("publisher", None))
            collection = self._search_nodes(index, "//div[@id='metadata-colección']/text()")
            language = self._search_nodes(index, "//div[@id='metadata-idioma']/text()")

            # Edition / Format
            format = self._search_nodes(index, "//div[contains(@class, 'ficha')]//div[contains(@class, 'row')][.//div[normalize-space()='Formato']]//div[contains(@class, 'col-xs-7')]/div/text()")
            binding = self._search_nodes(index, "//div[@id='metadata-encuadernación']/text()")
            pages = self._search_nodes(index, "//div[contains(@class, 'metadata-número páginas')]/text()")
            year = self._search_nodes(index, "//div[contains(@class, 'metadata-ano')]/text()")
            published_at = self._search_nodes(index, "//div[contains(@class, 'metadata-isbn-pais')]/text()")
            dimensions = self._search_nodes(index, "//div[contains(@class, 'metadata-dimensiones')]/text()")
            weight = self._search_nodes(index, "//div[contains(@class, 'metadata-peso')]/text()")

            # Commercialization
            currency = script.get("offers", None)[0].get("priceCurrency", None)
            base_price = self._search_nodes(index, "//span[contains(@class, 'pvp')]/text()")
            offer_price = script.get("offers", None)[0].get("price", None)
            categories = self._search_nodes(index, "//div[@id='metadata-categorías']//a/text()")

            # Reviews
            rating = script.get("aggregateRating", None).get("ratingValue", None)
            review_count = script.get("aggregateRating", None).get("reviewCount", None)
            reviews = self._parse_reviews(index, script.get("review", None))


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
                "publisher_url": publisher_url,
                "publisher_name": publisher_name,
                "collection": collection,
                "language": language,

                # Edition / Format
                "format": format,
                "binding": binding,
                "pages": pages,
                "year": year,
                "published_at": published_at,
                "dimensions": dimensions,
                "weight": weight,

                # Commercialization
                "currency": currency,
                "base_price": base_price,
                "offer_price": offer_price,
                "categories": categories,

                # Reviews
                "rating": rating,
                "review_count": review_count,
                "reviews": reviews,
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