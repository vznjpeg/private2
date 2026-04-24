import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhopScraper:
    def __init__(self):
        self.base_url = "https://whop.com"
        self.api_url = "https://api.whop.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.data = {
            "products": [],
            "categories": {},
            "growth_metrics": {}
        }

    def scrape_trending_products(self) -> List[Dict]:
        """Scrape trending/featured products from Whop"""
        try:
            response = requests.get(f"{self.base_url}/explore", headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            products = []
            product_cards = soup.find_all('div', class_=['product-card', 'card', 'item'])

            for card in product_cards:
                try:
                    name_elem = card.find('h2') or card.find('h3')
                    name = name_elem.text.strip() if name_elem else None

                    desc_elem = card.find('p')
                    description = desc_elem.text.strip() if desc_elem else None

                    price_elem = card.find('span', class_=['price'])
                    price = price_elem.text.strip() if price_elem else None

                    sales_elem = card.find('span', class_=['sales', 'sold', 'purchases'])
                    sales_count = sales_elem.text.strip() if sales_elem else "0"

                    category_elem = card.find('span', class_=['category', 'tag'])
                    category = category_elem.text.strip() if category_elem else "Uncategorized"

                    rating_elem = card.find('span', class_=['rating', 'stars'])
                    rating = rating_elem.text.strip() if rating_elem else "0"

                    if name:
                        products.append({
                            "platform": "whop",
                            "name": name,
                            "description": description,
                            "price": price,
                            "sales_count": self._parse_number(sales_count),
                            "category": category,
                            "rating": self._parse_rating(rating),
                            "url": f"{self.base_url}/explore",
                            "scraped_at": datetime.now().isoformat()
                        })
                except Exception as e:
                    logger.warning(f"Error parsing product card: {e}")
                    continue

            return products
        except Exception as e:
            logger.error(f"Error scraping Whop products: {e}")
            return []

    def scrape_category_data(self) -> Dict:
        """Scrape category-specific data from Whop"""
        try:
            response = requests.get(f"{self.base_url}/explore/categories", headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            categories = {}
            category_sections = soup.find_all('section', class_=['category', 'category-section'])

            for section in category_sections:
                try:
                    category_name = section.find('h3') or section.find('h2')
                    if not category_name:
                        continue

                    cat_name = category_name.text.strip()

                    growth_elem = section.find('span', class_=['growth', 'trend'])
                    growth_text = growth_elem.text.strip() if growth_elem else "0%"

                    count_elem = section.find('span', class_=['count', 'total'])
                    count = self._parse_number(count_elem.text.strip() if count_elem else "0")

                    revenue_elem = section.find('span', class_=['revenue', 'earnings'])
                    revenue = revenue_elem.text.strip() if revenue_elem else "$0"

                    categories[cat_name] = {
                        "name": cat_name,
                        "growth_rate": self._parse_percentage(growth_text),
                        "product_count": count,
                        "total_revenue": self._parse_currency(revenue),
                        "platform": "whop"
                    }
                except Exception as e:
                    logger.warning(f"Error parsing category: {e}")
                    continue

            return categories
        except Exception as e:
            logger.error(f"Error scraping Whop categories: {e}")
            return {}

    def estimate_revenue(self, products: List[Dict]) -> Dict:
        """Estimate monthly revenue based on visible metrics"""
        revenue_estimates = {}

        for product in products:
            sales_count = product.get("sales_count", 0)
            price_text = product.get("price", "$0")
            price = self._parse_currency(price_text)

            # Estimate assuming sales continue at current rate
            estimated_monthly = sales_count * price  # Conservative: assume all sales happened in ~30 days

            revenue_estimates[product["name"]] = {
                "estimated_monthly_revenue": estimated_monthly,
                "estimated_annual_revenue": estimated_monthly * 12,
                "sales_count": sales_count,
                "unit_price": price,
                "confidence": 0.6
            }

        return revenue_estimates

    def _parse_number(self, text: str) -> int:
        """Parse numbers from text"""
        try:
            text = text.lower().strip()
            multipliers = {'k': 1000, 'm': 1000000}

            for suffix, mult in multipliers.items():
                if suffix in text:
                    num = float(text.replace(suffix, '').strip())
                    return int(num * mult)

            return int(float(text.split()[0]))
        except:
            return 0

    def _parse_percentage(self, text: str) -> float:
        """Parse percentage from text"""
        try:
            return float(text.replace('%', '').strip())
        except:
            return 0.0

    def _parse_currency(self, text: str) -> float:
        """Parse currency from text"""
        try:
            text = text.replace('$', '').replace(',', '').strip()
            return float(text)
        except:
            return 0.0

    def _parse_rating(self, text: str) -> float:
        """Parse rating from text"""
        try:
            return float(text.split()[0])
        except:
            return 0.0

    def get_all_data(self) -> Dict:
        """Get all scraped data"""
        logger.info("Scraping Whop...")
        self.data["products"] = self.scrape_trending_products()
        self.data["categories"] = self.scrape_category_data()
        self.data["revenue_estimates"] = self.estimate_revenue(self.data["products"])
        return self.data
