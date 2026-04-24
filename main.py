#!/usr/bin/env python3

import argparse
import json
from pathlib import Path
from datetime import datetime
import logging

from scrapers.skool import SkoolScraper
from scrapers.whop import WhopScraper
from analysis import GrowthAnalyzer
from export import DataExporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MarketScraper:
    """Main orchestrator for web scraping and analysis"""

    def __init__(self):
        self.skool = SkoolScraper()
        self.whop = WhopScraper()
        self.exporter = DataExporter()

    def scrape_all(self) -> dict:
        """Scrape data from all platforms"""
        logger.info("Starting data collection...")

        data = {
            "skool": self.skool.get_all_data(),
            "whop": self.whop.get_all_data(),
            "scraped_at": datetime.now().isoformat()
        }

        logger.info(f"Skool: {len(data['skool'].get('communities', []))} communities found")
        logger.info(f"Whop: {len(data['whop'].get('products', []))} products found")

        return data

    def analyze(self, data: dict) -> dict:
        """Analyze scraped data"""
        logger.info("Starting analysis...")

        analyzer = GrowthAnalyzer(data)
        report = analyzer.generate_report()

        logger.info("Analysis complete")
        return report

    def run_full_pipeline(self, export_format: str = "csv"):
        """Run complete scrape and analysis pipeline"""
        logger.info("=" * 60)
        logger.info("MARKET GROWTH & REVENUE ANALYSIS")
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        logger.info("=" * 60)

        # Scrape
        raw_data = self.scrape_all()

        # Analyze
        analysis = self.analyze(raw_data)

        # Export
        logger.info("Exporting data...")
        export_files = []

        if export_format in ["csv", "all"]:
            export_files.append(self.exporter.export_to_csv(raw_data))
            export_files.append(self.exporter.export_growth_report(analysis))

            # Export affiliate opportunities
            opportunities = analysis.get("market_trends", {}).get("affiliate_opportunities", [])
            export_files.append(self.exporter.export_affiliate_opportunities(opportunities))

        if export_format in ["json", "all"]:
            export_files.append(self.exporter.export_to_json(raw_data))

        logger.info("=" * 60)
        logger.info("EXPORT COMPLETE")
        logger.info("=" * 60)
        for file in export_files:
            logger.info(f"  ✓ {file}")

        return {
            "raw_data": raw_data,
            "analysis": analysis,
            "export_files": [str(f) for f in export_files]
        }

    def print_summary(self, results: dict):
        """Print summary of analysis"""
        analysis = results.get("analysis", {})

        print("\n" + "=" * 70)
        print("TOP GROWTH CATEGORIES (7 Days, 30 Days, 90 Days, 1 Year)")
        print("=" * 70)

        for idx, cat in enumerate(analysis.get("top_growth_categories", [])[:5], 1):
            print(f"\n{idx}. {cat['category']}")
            print(f"   Growth Rate: {cat['growth_rate']:.2f}%")
            print(f"   Skool Communities: {cat.get('skool_data', {}).get('community_count', 0)}")
            print(f"   Whop Products: {cat.get('whop_data', {}).get('product_count', 0)}")

        print("\n" + "=" * 70)
        print("MARKET TRENDS & BENCHMARKS")
        print("=" * 70)

        benchmarks = analysis.get("benchmarks", {})
        print(f"\nAverage Growth Rate: {benchmarks.get('average_growth_rate', 0):.2f}%")
        print(f"Median Growth Rate: {benchmarks.get('median_growth_rate', 0):.2f}%")
        print(f"Total Market Size: ${benchmarks.get('total_estimated_market_size', 0):,.2f}")

        comparison = analysis.get("market_trends", {}).get("platform_comparison", {})
        print(f"\nSkool Total Revenue (Estimated): ${comparison.get('skool', {}).get('estimated_total_revenue', 0):,.2f}")
        print(f"Whop Total Revenue (Estimated): ${comparison.get('whop', {}).get('estimated_total_revenue', 0):,.2f}")

        print("\n" + "=" * 70)
        print("TOP AFFILIATE OPPORTUNITIES")
        print("=" * 70)

        for idx, opp in enumerate(analysis.get("market_trends", {}).get("affiliate_opportunities", [])[:5], 1):
            print(f"\n{idx}. {opp.get('name') or opp.get('category')}")
            print(f"   Type: {opp.get('type')}")
            print(f"   {opp.get('recommendation')}")

        print("\n" + "=" * 70 + "\n")

def main():
    parser = argparse.ArgumentParser(
        description="Web Scraper for Skool.com and Whop.com - Market Analysis Tool"
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "all"],
        default="csv",
        help="Export format (default: csv)"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary to console"
    )
    parser.add_argument(
        "--no-export",
        action="store_true",
        help="Skip export step"
    )

    args = parser.parse_args()

    scraper = MarketScraper()

    if args.no_export:
        raw_data = scraper.scrape_all()
        analysis = scraper.analyze(raw_data)
        results = {"raw_data": raw_data, "analysis": analysis, "export_files": []}
    else:
        results = scraper.run_full_pipeline(export_format=args.format)

    if args.summary:
        scraper.print_summary(results)

if __name__ == "__main__":
    main()
