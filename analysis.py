from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import statistics
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GrowthAnalyzer:
    """Analyze growth metrics and trends across platforms"""

    def __init__(self, data: Dict):
        self.data = data
        self.growth_analysis = {}

    def calculate_category_growth(self) -> Dict:
        """Calculate growth rates for each category"""
        growth_data = {}

        # Process Skool categories
        skool_cats = self.data.get("skool", {}).get("categories", {})
        for cat_name, cat_data in skool_cats.items():
            if cat_name not in growth_data:
                growth_data[cat_name] = {"skool": {}, "whop": {}}

            growth_data[cat_name]["skool"] = {
                "growth_rate": cat_data.get("growth_rate", 0),
                "community_count": cat_data.get("community_count", 0),
                "platform": "skool"
            }

        # Process Whop categories
        whop_cats = self.data.get("whop", {}).get("categories", {})
        for cat_name, cat_data in whop_cats.items():
            if cat_name not in growth_data:
                growth_data[cat_name] = {"skool": {}, "whop": {}}

            growth_data[cat_name]["whop"] = {
                "growth_rate": cat_data.get("growth_rate", 0),
                "product_count": cat_data.get("product_count", 0),
                "platform": "whop"
            }

        return growth_data

    def rank_by_growth(self, growth_data: Dict, time_period: str = "all") -> List[Tuple]:
        """Rank categories by growth rate"""
        rankings = []

        for category, platform_data in growth_data.items():
            combined_growth = 0
            count = 0

            for platform, data in platform_data.items():
                if data and "growth_rate" in data:
                    combined_growth += data["growth_rate"]
                    count += 1

            if count > 0:
                avg_growth = combined_growth / count
                rankings.append((category, avg_growth, platform_data))

        rankings.sort(key=lambda x: x[1], reverse=True)
        return rankings

    def get_top_growth_categories(self, limit: int = 10) -> List[Dict]:
        """Get top growing categories"""
        growth_data = self.calculate_category_growth()
        rankings = self.rank_by_growth(growth_data)

        top_categories = []
        for category, growth_rate, platform_data in rankings[:limit]:
            top_categories.append({
                "category": category,
                "growth_rate": round(growth_rate, 2),
                "skool_data": platform_data.get("skool", {}),
                "whop_data": platform_data.get("whop", {})
            })

        return top_categories

    def calculate_revenue_metrics(self) -> Dict:
        """Calculate aggregated revenue metrics"""
        metrics = {
            "skool": {"total_estimated_revenue": 0, "total_items": 0, "avg_revenue": 0},
            "whop": {"total_estimated_revenue": 0, "total_items": 0, "avg_revenue": 0}
        }

        # Skool revenue
        skool_revenue = self.data.get("skool", {}).get("revenue_estimates", {})
        if skool_revenue:
            revenues = [v.get("estimated_monthly_revenue", 0) for v in skool_revenue.values()]
            metrics["skool"]["total_estimated_revenue"] = sum(revenues)
            metrics["skool"]["total_items"] = len(revenues)
            metrics["skool"]["avg_revenue"] = statistics.mean(revenues) if revenues else 0

        # Whop revenue
        whop_revenue = self.data.get("whop", {}).get("revenue_estimates", {})
        if whop_revenue:
            revenues = [v.get("estimated_monthly_revenue", 0) for v in whop_revenue.values()]
            metrics["whop"]["total_estimated_revenue"] = sum(revenues)
            metrics["whop"]["total_items"] = len(revenues)
            metrics["whop"]["avg_revenue"] = statistics.mean(revenues) if revenues else 0

        return metrics

    def get_market_trends(self) -> Dict:
        """Analyze market trends"""
        trends = {
            "emerging_categories": self.get_top_growth_categories(5),
            "declining_categories": self._get_declining_categories(),
            "market_size": self.calculate_revenue_metrics(),
            "platform_comparison": self._compare_platforms(),
            "affiliate_opportunities": self._identify_affiliate_opportunities()
        }
        return trends

    def _get_declining_categories(self) -> List[Dict]:
        """Get categories with negative or low growth"""
        growth_data = self.calculate_category_growth()
        rankings = self.rank_by_growth(growth_data)
        declining = []

        for category, growth_rate, platform_data in rankings[-5:]:
            if growth_rate < 0 or growth_rate < 5:  # Threshold for "declining"
                declining.append({
                    "category": category,
                    "growth_rate": round(growth_rate, 2),
                    "skool_data": platform_data.get("skool", {}),
                    "whop_data": platform_data.get("whop", {})
                })

        return declining

    def _compare_platforms(self) -> Dict:
        """Compare performance across platforms"""
        skool_data = self.data.get("skool", {})
        whop_data = self.data.get("whop", {})

        skool_communities = len(skool_data.get("communities", []))
        whop_products = len(whop_data.get("products", []))

        skool_revenue = sum([
            v.get("estimated_monthly_revenue", 0)
            for v in skool_data.get("revenue_estimates", {}).values()
        ])

        whop_revenue = sum([
            v.get("estimated_monthly_revenue", 0)
            for v in whop_data.get("revenue_estimates", {}).values()
        ])

        return {
            "skool": {
                "items_counted": skool_communities,
                "estimated_total_revenue": round(skool_revenue, 2),
                "avg_revenue_per_item": round(skool_revenue / max(skool_communities, 1), 2)
            },
            "whop": {
                "items_counted": whop_products,
                "estimated_total_revenue": round(whop_revenue, 2),
                "avg_revenue_per_item": round(whop_revenue / max(whop_products, 1), 2)
            }
        }

    def _identify_affiliate_opportunities(self) -> List[Dict]:
        """Identify high-potential affiliate opportunities"""
        opportunities = []

        # High-growth products/communities
        top_growth = self.get_top_growth_categories(3)
        for item in top_growth:
            opportunities.append({
                "type": "high_growth_category",
                "category": item["category"],
                "growth_rate": item["growth_rate"],
                "potential": "high",
                "recommendation": f"Focus affiliate efforts on {item['category']} - experiencing {item['growth_rate']}% growth"
            })

        # High-revenue items
        skool_revenue = self.data.get("skool", {}).get("revenue_estimates", {})
        top_skool = sorted(
            skool_revenue.items(),
            key=lambda x: x[1].get("estimated_monthly_revenue", 0),
            reverse=True
        )[:3]

        for name, metrics in top_skool:
            opportunities.append({
                "type": "high_revenue_community",
                "name": name,
                "platform": "skool",
                "monthly_revenue": round(metrics.get("estimated_monthly_revenue", 0), 2),
                "potential": "high",
                "recommendation": f"{name} on Skool - estimated ${metrics.get('estimated_monthly_revenue', 0):.0f}/month"
            })

        return opportunities

    def get_benchmarks(self) -> Dict:
        """Generate industry benchmarks"""
        metrics = self.calculate_revenue_metrics()
        growth_data = self.calculate_category_growth()

        growth_rates = []
        for category, platform_data in growth_data.items():
            for platform, data in platform_data.items():
                if data and "growth_rate" in data:
                    growth_rates.append(data["growth_rate"])

        benchmarks = {
            "average_growth_rate": round(statistics.mean(growth_rates), 2) if growth_rates else 0,
            "median_growth_rate": round(statistics.median(growth_rates), 2) if growth_rates else 0,
            "max_growth_rate": round(max(growth_rates), 2) if growth_rates else 0,
            "min_growth_rate": round(min(growth_rates), 2) if growth_rates else 0,
            "avg_revenue_per_item_skool": metrics["skool"].get("avg_revenue", 0),
            "avg_revenue_per_item_whop": metrics["whop"].get("avg_revenue", 0),
            "total_estimated_market_size": metrics["skool"]["total_estimated_revenue"] + metrics["whop"]["total_estimated_revenue"]
        }

        return benchmarks

    def generate_report(self) -> Dict:
        """Generate comprehensive analysis report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "top_growth_categories": self.get_top_growth_categories(10),
            "market_trends": self.get_market_trends(),
            "benchmarks": self.get_benchmarks()
        }
