import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataExporter:
    """Export scraped data and analysis to various formats"""

    def __init__(self, export_dir: Path = Path("exports")):
        self.export_dir = export_dir
        self.export_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_to_csv(self, data: Dict, filename: str = None) -> Path:
        """Export data to CSV format"""
        if not filename:
            filename = f"market_analysis_{self.timestamp}.csv"

        filepath = self.export_dir / filename

        try:
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Write header
                writer.writerow([
                    "Timestamp", "Platform", "Category", "Item Name",
                    "Growth Rate (%)", "Members/Sales",
                    "Est. Monthly Revenue", "Est. Annual Revenue", "Confidence"
                ])

                # Write Skool data
                skool_data = data.get("skool", {})
                for community in skool_data.get("communities", []):
                    name = community.get("name", "")
                    category = community.get("category", "")
                    members = community.get("members", 0)

                    revenue = skool_data.get("revenue_estimates", {}).get(name, {})
                    est_monthly = revenue.get("estimated_monthly_revenue", 0)
                    est_annual = revenue.get("estimated_annual_revenue", 0)
                    confidence = revenue.get("confidence", 0)

                    # Get growth rate from categories
                    growth_rate = skool_data.get("categories", {}).get(category, {}).get("growth_rate", 0)

                    writer.writerow([
                        self.timestamp, "Skool", category, name,
                        f"{growth_rate:.2f}", members,
                        f"${est_monthly:,.2f}", f"${est_annual:,.2f}", f"{confidence:.0%}"
                    ])

                # Write Whop data
                whop_data = data.get("whop", {})
                for product in whop_data.get("products", []):
                    name = product.get("name", "")
                    category = product.get("category", "")
                    sales = product.get("sales_count", 0)

                    revenue = whop_data.get("revenue_estimates", {}).get(name, {})
                    est_monthly = revenue.get("estimated_monthly_revenue", 0)
                    est_annual = revenue.get("estimated_annual_revenue", 0)
                    confidence = revenue.get("confidence", 0)

                    # Get growth rate from categories
                    growth_rate = whop_data.get("categories", {}).get(category, {}).get("growth_rate", 0)

                    writer.writerow([
                        self.timestamp, "Whop", category, name,
                        f"{growth_rate:.2f}", sales,
                        f"${est_monthly:,.2f}", f"${est_annual:,.2f}", f"{confidence:.0%}"
                    ])

            logger.info(f"Data exported to {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise

    def export_growth_report(self, analysis: Dict, filename: str = None) -> Path:
        """Export growth analysis report to CSV"""
        if not filename:
            filename = f"growth_report_{self.timestamp}.csv"

        filepath = self.export_dir / filename

        try:
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Header
                writer.writerow(["Growth Analysis Report", f"Generated: {self.timestamp}"])
                writer.writerow([])

                # Top Growth Categories
                writer.writerow(["Top Growth Categories"])
                writer.writerow(["Rank", "Category", "Growth Rate (%)", "Skool Communities", "Whop Products"])

                for idx, cat_data in enumerate(analysis.get("top_growth_categories", []), 1):
                    category = cat_data["category"]
                    growth = cat_data["growth_rate"]
                    skool_count = cat_data.get("skool_data", {}).get("community_count", 0)
                    whop_count = cat_data.get("whop_data", {}).get("product_count", 0)

                    writer.writerow([idx, category, f"{growth:.2f}", skool_count, whop_count])

                writer.writerow([])

                # Market Trends
                trends = analysis.get("market_trends", {})
                writer.writerow(["Market Trends"])
                writer.writerow(["Metric", "Value"])

                comparison = trends.get("platform_comparison", {})
                writer.writerow(["Skool Total Revenue", f"${comparison.get('skool', {}).get('estimated_total_revenue', 0):,.2f}"])
                writer.writerow(["Whop Total Revenue", f"${comparison.get('whop', {}).get('estimated_total_revenue', 0):,.2f}"])

                writer.writerow([])

                # Benchmarks
                benchmarks = analysis.get("benchmarks", {})
                writer.writerow(["Industry Benchmarks"])
                writer.writerow(["Metric", "Value"])

                writer.writerow(["Average Growth Rate", f"{benchmarks.get('average_growth_rate', 0):.2f}%"])
                writer.writerow(["Median Growth Rate", f"{benchmarks.get('median_growth_rate', 0):.2f}%"])
                writer.writerow(["Max Growth Rate", f"{benchmarks.get('max_growth_rate', 0):.2f}%"])
                writer.writerow(["Total Market Size", f"${benchmarks.get('total_estimated_market_size', 0):,.2f}"])

            logger.info(f"Growth report exported to {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error exporting growth report: {e}")
            raise

    def export_to_json(self, data: Dict, filename: str = None) -> Path:
        """Export data to JSON format"""
        if not filename:
            filename = f"market_data_{self.timestamp}.json"

        filepath = self.export_dir / filename

        try:
            with open(filepath, 'w') as jsonfile:
                json.dump(data, jsonfile, indent=2)

            logger.info(f"Data exported to {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise

    def export_affiliate_opportunities(self, opportunities: List[Dict], filename: str = None) -> Path:
        """Export affiliate opportunities to CSV"""
        if not filename:
            filename = f"affiliate_opportunities_{self.timestamp}.csv"

        filepath = self.export_dir / filename

        try:
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow(["Opportunity Type", "Name/Category", "Platform", "Metric", "Potential", "Recommendation"])

                for opp in opportunities:
                    opp_type = opp.get("type", "")
                    name = opp.get("name") or opp.get("category", "")
                    platform = opp.get("platform", "")
                    metric = ""

                    if opp_type == "high_growth_category":
                        metric = f"{opp.get('growth_rate', 0):.2f}% growth"
                    elif opp_type == "high_revenue_community":
                        metric = f"${opp.get('monthly_revenue', 0):,.2f}/month"

                    potential = opp.get("potential", "")
                    recommendation = opp.get("recommendation", "")

                    writer.writerow([opp_type, name, platform, metric, potential, recommendation])

            logger.info(f"Affiliate opportunities exported to {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Error exporting affiliate opportunities: {e}")
            raise

    def get_export_paths(self) -> Dict[str, Path]:
        """Get paths to all available exports"""
        exports = {}
        for file in self.export_dir.glob("*"):
            if file.is_file():
                exports[file.name] = file
        return exports
