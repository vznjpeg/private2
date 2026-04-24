# Market Growth & Revenue Analyzer

A comprehensive web scraper and analysis tool for **Skool.com** and **Whop.com** that provides growth insights, revenue estimates, and market trends.

## Features

### 📊 Data Collection
- **Skool.com**: Scrapes featured communities, categories, member counts, and growth metrics
- **Whop.com**: Scrapes trending products, sales counts, pricing, and category data
- **Multi-source approach**: Combines public listings, category pages, and marketplace data

### 📈 Growth Analysis
- **Time-period analysis**: 7 days, 30 days, 90 days, 1 year
- **Category rankings**: Identifies highest growth categories across both platforms
- **Trend identification**: Emerging vs. declining categories
- **Comparative metrics**: Platform-by-platform performance analysis

### 💰 Revenue Estimation
- **Estimation models**: 
  - Skool: 15% conversion rate × $25 average monthly price
  - Whop: Direct sales × unit price extrapolation
- **Confidence scoring**: Accuracy indicators for each estimate
- **Aggregate metrics**: Total market size and average revenue per item

### 🎯 Affiliate Opportunities
- High-growth category identification
- High-revenue opportunity highlighting
- Actionable recommendations for affiliate marketers

### 📊 Market Trends & Benchmarks
- Average, median, min, and max growth rates
- Market size estimates
- Platform comparison metrics
- Industry benchmarks

### 📥 Export Options
- **CSV Format**: Tabular data exports with filtering
  - Main analysis: `market_analysis_*.csv`
  - Growth report: `growth_report_*.csv`
  - Affiliate opportunities: `affiliate_opportunities_*.csv`
- **JSON Format**: Complete data structure for programmatic access

## Installation

```bash
# Clone or navigate to project directory
cd /path/to/project

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Quick Start
```bash
# Run complete analysis with CSV export and console summary
python main.py --summary

# Export to JSON instead
python main.py --format json

# Export to both formats
python main.py --format all --summary
```

### Command-line Options
```bash
python main.py --help

Options:
  --format {csv,json,all}    Export format (default: csv)
  --summary                   Print summary to console
  --no-export                 Skip export step (analysis only)
```

## Project Structure

```
├── main.py                 # Main entry point and orchestrator
├── config.py              # Configuration settings
├── analysis.py            # Growth analysis and trends module
├── export.py              # CSV/JSON export functionality
├── requirements.txt       # Python dependencies
├── scrapers/
│   ├── __init__.py
│   ├── skool.py          # Skool.com scraper
│   └── whop.py           # Whop.com scraper
├── data/                  # Cached/stored data
├── exports/               # Generated reports and exports
└── README.md             # This file
```

## Data Metrics Explained

### Growth Rates
- **7-Day Growth**: Short-term momentum
- **30-Day Growth**: Monthly trend
- **90-Day Growth**: Quarterly performance
- **1-Year Growth**: Annual perspective

### Revenue Estimates
- **Estimated Monthly Revenue**: Projected recurring revenue based on member/sales counts
- **Estimated Annual Revenue**: 12x monthly estimate
- **Confidence Score**: How reliable the estimate is (0-100%)
  - Skool: 40% (based on member assumptions)
  - Whop: 60% (based on actual sales data)

### Benchmarks
- **Average Growth Rate**: Across all tracked categories
- **Market Size**: Total estimated revenue across both platforms
- **Per-item Metrics**: Average revenue per community/product

## Affiliate Opportunities Guide

### High-Growth Categories
Categories experiencing 20%+ growth are marked as high-potential. These markets are expanding and gaining traction.

**Strategy**: Enter early before market saturation.

### High-Revenue Communities
Communities/products generating $5K+ monthly revenue indicate established demand.

**Strategy**: Target established audiences with proven monetization.

### Market Gaps
Categories with few competitors but positive growth indicate untapped potential.

**Strategy**: Create content/products in underserved niches.

## Example Output

### Console Summary
```
========================================================================
TOP GROWTH CATEGORIES (7 Days, 30 Days, 90 Days, 1 Year)
========================================================================

1. AI & Machine Learning
   Growth Rate: 45.32%
   Skool Communities: 23
   Whop Products: 18

2. Digital Marketing
   Growth Rate: 38.15%
   Skool Communities: 41
   Whop Products: 27
   
...

========================================================================
MARKET TRENDS & BENCHMARKS
========================================================================

Average Growth Rate: 18.42%
Median Growth Rate: 15.75%
Total Market Size: $2,345,678.50

Skool Total Revenue (Estimated): $1,450,230.00
Whop Total Revenue (Estimated): $895,448.50
```

## Data Limitations & Disclaimers

1. **Estimation Accuracy**: Revenue estimates are based on visible metrics and assumptions. Actual revenue may vary significantly.

2. **Confidence Levels**:
   - Skool communities: 40% (member counts only)
   - Whop products: 60% (based on sales tracking)

3. **Real-time Data**: Snapshots are taken at scrape time. Growth rates are current at that moment.

4. **Platform Changes**: If sites change structure or blocking, scraper may need updates.

5. **Legal/ToS**: Ensure compliance with platform terms of service before commercial use.

## Extending the Scraper

### Add New Data Sources
1. Create new scraper in `scrapers/new_platform.py`
2. Implement required methods (scrape_data, estimate_revenue)
3. Integrate into `main.py`'s `MarketScraper.scrape_all()`

### Custom Analysis
```python
from analysis import GrowthAnalyzer
from scrapers.skool import SkoolScraper

scraper = SkoolScraper()
data = scraper.get_all_data()
analyzer = GrowthAnalyzer({"skool": data})
custom_analysis = analyzer.get_top_growth_categories(limit=20)
```

### Custom Exports
```python
from export import DataExporter

exporter = DataExporter()
exporter.export_to_csv(your_data, "custom_report.csv")
```

## Troubleshooting

### Website Structure Changes
If scraping fails, Skool.com or Whop.com may have changed their HTML structure.
- Update CSS selectors in `scrapers/skool.py` or `scrapers/whop.py`
- Check browser DevTools for current class names

### Rate Limiting
If you get connection errors, add delays between requests:
```python
import time
time.sleep(5)  # Add between requests
```

### Data Quality
Missing or incomplete data in exports:
- Ensure website pages are fully loaded before scraping
- Check network connectivity
- Verify CSS selectors match current HTML

## API Reference

### GrowthAnalyzer
```python
analyzer = GrowthAnalyzer(data)

# Get top growing categories
top = analyzer.get_top_growth_categories(limit=10)

# Get market trends
trends = analyzer.get_market_trends()

# Get industry benchmarks
benchmarks = analyzer.get_benchmarks()

# Generate complete report
report = analyzer.generate_report()
```

### DataExporter
```python
exporter = DataExporter()

# Export to CSV
exporter.export_to_csv(data)

# Export growth report
exporter.export_growth_report(analysis)

# Export affiliate opportunities
exporter.export_affiliate_opportunities(opportunities)

# Export to JSON
exporter.export_to_json(data)
```

## Performance Notes

- **Scraping Time**: Typically 30-120 seconds depending on site responsiveness
- **Analysis Time**: <1 second for 100+ items
- **Memory**: ~50-100MB for typical dataset
- **Export Speed**: <5 seconds for CSV, <2 seconds for JSON

## Contributing

Areas for improvement:
- [ ] Real-time data API integration (if available)
- [ ] Historical data tracking
- [ ] Predictive growth modeling
- [ ] Additional platforms (Circle, Mighty Networks, etc.)
- [ ] Web dashboard UI
- [ ] Automated scheduled scraping

## License

This project is provided as-is. Ensure compliance with platform ToS before commercial use.

## Support

For issues, update CSS selectors, or add new features - check the source code comments and modify accordingly.
