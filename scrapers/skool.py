import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SkoolScraper:
    def __init__(self):
        self.base_url = "https://www.skool.com"
        self.api_url = "https://api.skool.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.data = {
            "communities": [],
            "categories": {},
            "growth_metrics": {}
        }

    def scrape_featured_communities(self) -> List[Dict]:
        """Scrape featured communities from Skool homepage"""
        try:
            response = requests.get(f"{self.base_url}/explore", headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            communities = []
            community_cards = soup.find_all('div', class_=['community-card', 'card'])

            for card in community_cards:
                try:
                    name_elem = card.find('h2') or card.find('h3')
                    name = name_elem.text.strip() if name_elem else None

                    desc_elem = card.find('p')
                    description = desc_elem.text.strip() if desc_elem else None

                    members_elem = card.find('span', class_=['members', 'count'])
                    members = members_elem.text.strip() if members_elem else "0"

                    category_elem = card.find('span', class_=['category', 'tag'])
                    category = category_elem.text.strip() if category_elem else "Uncategorized"

                    if name:
                        communities.append({
                            "platform": "skool",
                            "name": name,
                            "description": description,
                            "members": self._parse_number(members),
                            "category": category,
                            "url": f"{self.base_url}/explore",
                            "scraped_at": datetime.now().isoformat()
                        })
                except Exception as e:
                    logger.warning(f"Error parsing community card: {e}")
                    continue

            return communities
        except Exception as e:
            logger.error(f"Error scraping Skool communities: {e}")
            return []

    def scrape_category_data(self) -> Dict:
        """Scrape category-specific growth data"""
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

                    categories[cat_name] = {
                        "name": cat_name,
                        "growth_rate": self._parse_percentage(growth_text),
                        "community_count": count,
                        "platform": "skool"
                    }
                except Exception as e:
                    logger.warning(f"Error parsing category: {e}")
                    continue

            return categories
        except Exception as e:
            logger.error(f"Error scraping Skool categories: {e}")
            return {}

    def estimate_revenue(self, communities: List[Dict]) -> Dict:
        """Estimate monthly revenue based on visible metrics"""
        revenue_estimates = {}

        for community in communities:
            members = community.get("members", 0)

            # Estimation model: assume 10-30% conversion to paid, $10-50/month avg
            estimated_subscribers = members * 0.15  # 15% average conversion
            estimated_monthly = estimated_subscribers * 25  # $25 average

            revenue_estimates[community["name"]] = {
                "estimated_monthly_revenue": estimated_monthly,
                "estimated_annual_revenue": estimated_monthly * 12,
                "members": members,
                "conversion_assumption": "15%",
                "avg_price_assumption": "$25/month",
                "confidence": 0.4
            }

        return revenue_estimates

    def _parse_number(self, text: str) -> int:
        """Parse numbers from text (e.g., '1.2K' -> 1200)"""
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

    def get_all_data(self) -> Dict:
        """Get all scraped data"""
        logger.info("Scraping Skool...")
        self.data["communities"] = self.scrape_featured_communities()
        self.data["categories"] = self.scrape_category_data()
        self.data["revenue_estimates"] = self.estimate_revenue(self.data["communities"])
        return self.data
