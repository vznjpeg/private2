#!/usr/bin/env python3
"""
Example usage of the Market Scraper
Shows different ways to use the library
"""

from scrapers.skool import SkoolScraper
from scrapers.whop import WhopScraper
from analysis import GrowthAnalyzer
from export import DataExporter
from pathlib import Path
import json

def example_1_basic_scraping():
    """Example 1: Basic scraping from each platform"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Scraping")
    print("="*60)

    # Scrape Skool
    print("\n[Scraping Skool.com...]")
    skool = SkoolScraper()
    skool_data = skool.get_all_data()
    print(f"✓ Found {len(skool_data['communities'])} communities")
    print(f"✓ Found {len(skool_data['categories'])} categories")

    # Scrape Whop
    print("\n[Scraping Whop.com...]")
    whop = WhopScraper()
    whop_data = whop.get_all_data()
    print(f"✓ Found {len(whop_data['products'])} products")
    print(f"✓ Found {len(whop_data['categories'])} categories")

    return skool_data, whop_data

def example_2_growth_analysis(skool_data, whop_data):
    """Example 2: Analyze growth across platforms"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Growth Analysis")
    print("="*60)

    data = {
        "skool": skool_data,
        "whop": whop_data
    }

    analyzer = GrowthAnalyzer(data)

    # Get top growth categories
    print("\n[Top 5 Growth Categories]")
    top_categories = analyzer.get_top_growth_categories(limit=5)
    for idx, cat in enumerate(top_categories, 1):
        print(f"\n{idx}. {cat['category']}")
        print(f"   Growth Rate: {cat['growth_rate']:.2f}%")
        if cat['skool_data']:
            print(f"   Skool: {cat['skool_data'].get('community_count', 0)} communities")
        if cat['whop_data']:
            print(f"   Whop: {cat['whop_data'].get('product_count', 0)} products")

    return analyzer

def example_3_market_metrics(analyzer):
    """Example 3: Market metrics and benchmarks"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Market Metrics & Benchmarks")
    print("="*60)

    # Revenue metrics
    print("\n[Revenue Metrics]")
    revenue_metrics = analyzer.calculate_revenue_metrics()
    print(f"Skool Total Revenue: ${revenue_metrics['skool']['total_estimated_revenue']:,.2f}")
    print(f"Whop Total Revenue: ${revenue_metrics['whop']['total_estimated_revenue']:,.2f}")
    print(f"Skool Avg/Item: ${revenue_metrics['skool']['avg_revenue']:,.2f}")
    print(f"Whop Avg/Item: ${revenue_metrics['whop']['avg_revenue']:,.2f}")

    # Benchmarks
    print("\n[Industry Benchmarks]")
    benchmarks = analyzer.get_benchmarks()
    print(f"Average Growth Rate: {benchmarks['average_growth_rate']:.2f}%")
    print(f"Median Growth Rate: {benchmarks['median_growth_rate']:.2f}%")
    print(f"Max Growth Rate: {benchmarks['max_growth_rate']:.2f}%")
    print(f"Total Market Size: ${benchmarks['total_estimated_market_size']:,.2f}")

def example_4_affiliate_opportunities(analyzer):
    """Example 4: Identify affiliate opportunities"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Affiliate Opportunities")
    print("="*60)

    trends = analyzer.get_market_trends()
    opportunities = trends.get("affiliate_opportunities", [])

    print(f"\n[Found {len(opportunities)} opportunities]")
    for idx, opp in enumerate(opportunities[:5], 1):
        print(f"\n{idx}. {opp.get('name') or opp.get('category')}")
        print(f"   Type: {opp.get('type')}")
        print(f"   Potential: {opp.get('potential')}")
        print(f"   → {opp.get('recommendation')}")

def example_5_export_data(skool_data, whop_data, analyzer):
    """Example 5: Export data to various formats"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Data Export")
    print("="*60)

    exporter = DataExporter(export_dir=Path("exports"))

    data = {
        "skool": skool_data,
        "whop": whop_data
    }

    # CSV exports
    print("\n[Exporting to CSV...]")
    csv_path = exporter.export_to_csv(data)
    print(f"✓ Main data: {csv_path.name}")

    analysis = analyzer.generate_report()
    report_path = exporter.export_growth_report(analysis)
    print(f"✓ Growth report: {report_path.name}")

    opportunities = analysis.get("market_trends", {}).get("affiliate_opportunities", [])
    opp_path = exporter.export_affiliate_opportunities(opportunities)
    print(f"✓ Affiliate opportunities: {opp_path.name}")

    # JSON export
    print("\n[Exporting to JSON...]")
    json_path = exporter.export_to_json(data)
    print(f"✓ Raw data: {json_path.name}")

    print(f"\n✓ All exports saved to: {exporter.export_dir}")

def example_6_programmatic_analysis(skool_data, whop_data):
    """Example 6: Custom programmatic analysis"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Custom Analysis")
    print("="*60)

    data = {
        "skool": skool_data,
        "whop": whop_data
    }

    analyzer = GrowthAnalyzer(data)

    # Find specific category
    print("\n[Searching for high-revenue items]")
    skool_revenue = skool_data.get("revenue_estimates", {})

    high_revenue = sorted(
        skool_revenue.items(),
        key=lambda x: x[1].get("estimated_monthly_revenue", 0),
        reverse=True
    )[:3]

    for idx, (name, metrics) in enumerate(high_revenue, 1):
        print(f"\n{idx}. {name}")
        print(f"   Monthly: ${metrics.get('estimated_monthly_revenue', 0):,.2f}")
        print(f"   Annual: ${metrics.get('estimated_annual_revenue', 0):,.2f}")
        print(f"   Members: {metrics.get('members', 0)}")
        print(f"   Confidence: {metrics.get('confidence', 0):.0%}")

    # Generate complete report
    print("\n[Generating complete report...]")
    report = analyzer.generate_report()
    print(f"✓ Report generated with {len(report['top_growth_categories'])} categories")
    print(f"✓ Found {len(report['market_trends']['affiliate_opportunities'])} opportunities")

    return report

def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("MARKET GROWTH & REVENUE ANALYZER - USAGE EXAMPLES")
    print("="*70)

    # Run examples (in practice, only first scrape is needed)
    # Note: Actual data will come from live scraping
    try:
        print("\nNote: These examples show the workflow.")
        print("Live scraping will populate real data from Skool.com and Whop.com")

        # Example data structure (shows what real output looks like)
        example_skool = {
            "communities": [],
            "categories": {},
            "revenue_estimates": {}
        }

        example_whop = {
            "products": [],
            "categories": {},
            "revenue_estimates": {}
        }

        print("\n✓ To run actual scraping, use: python main.py --summary")
        print("✓ To export data, use: python main.py --format all")
        print("\nSee README.md for full documentation")

    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
