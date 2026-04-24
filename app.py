from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import json
import asyncio
import logging
from typing import Dict, List, Optional

from scrapers.skool import SkoolScraper
from scrapers.whop import WhopScraper
from analysis import GrowthAnalyzer
from export import DataExporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Market Growth & Revenue Analyzer", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
class ScrapeState:
    def __init__(self):
        self.is_running = False
        self.progress = ""
        self.data = None
        self.analysis = None
        self.error = None

state = ScrapeState()

# Pydantic models
class ExportRequest(BaseModel):
    format: str = "csv"  # csv or json

class FilterRequest(BaseModel):
    platform: Optional[str] = None
    min_growth: Optional[float] = None
    max_growth: Optional[float] = None
    category: Optional[str] = None

@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/api/status")
async def get_status():
    """Get scraping status"""
    return {
        "is_running": state.is_running,
        "progress": state.progress,
        "has_data": state.data is not None,
        "error": state.error
    }

@app.post("/api/scrape")
async def start_scrape(background_tasks: BackgroundTasks):
    """Start scraping process"""
    if state.is_running:
        raise HTTPException(status_code=400, detail="Scraping already in progress")

    background_tasks.add_task(run_scrape)
    return {"message": "Scraping started", "status": "running"}

async def run_scrape():
    """Background task to run scraping"""
    try:
        state.is_running = True
        state.error = None

        logger.info("Starting scrape process...")
        state.progress = "Scraping Skool.com..."

        skool = SkoolScraper()
        skool_data = skool.get_all_data()
        logger.info(f"Skool: {len(skool_data.get('communities', []))} communities")

        state.progress = "Scraping Whop.com..."
        whop = WhopScraper()
        whop_data = whop.get_all_data()
        logger.info(f"Whop: {len(whop_data.get('products', []))} products")

        state.progress = "Analyzing data..."
        state.data = {
            "skool": skool_data,
            "whop": whop_data,
            "scraped_at": datetime.now().isoformat()
        }

        analyzer = GrowthAnalyzer(state.data)
        state.analysis = analyzer.generate_report()

        state.progress = "Complete"
        state.is_running = False

        logger.info("Scraping complete")

    except Exception as e:
        logger.error(f"Scrape error: {e}")
        state.error = str(e)
        state.is_running = False

@app.get("/api/data")
async def get_data():
    """Get latest scraped data"""
    if state.data is None:
        raise HTTPException(status_code=404, detail="No data available. Run scrape first.")
    return state.data

@app.get("/api/analysis")
async def get_analysis():
    """Get latest analysis"""
    if state.analysis is None:
        raise HTTPException(status_code=404, detail="No analysis available. Run scrape first.")
    return state.analysis

@app.get("/api/growth-categories")
async def get_growth_categories(limit: int = 10):
    """Get top growth categories"""
    if state.analysis is None:
        raise HTTPException(status_code=404, detail="No analysis available")

    return {
        "categories": state.analysis.get("top_growth_categories", [])[:limit]
    }

@app.get("/api/benchmarks")
async def get_benchmarks():
    """Get market benchmarks"""
    if state.analysis is None:
        raise HTTPException(status_code=404, detail="No analysis available")

    return state.analysis.get("benchmarks", {})

@app.get("/api/market-trends")
async def get_market_trends():
    """Get market trends"""
    if state.analysis is None:
        raise HTTPException(status_code=404, detail="No analysis available")

    trends = state.analysis.get("market_trends", {})
    return {
        "emerging": trends.get("emerging_categories", [])[:5],
        "declining": trends.get("declining_categories", [])[:5],
        "platform_comparison": trends.get("platform_comparison", {}),
        "affiliate_opportunities": trends.get("affiliate_opportunities", [])[:10]
    }

@app.get("/api/revenue-metrics")
async def get_revenue_metrics():
    """Get revenue metrics"""
    if state.analysis is None:
        raise HTTPException(status_code=404, detail="No analysis available")

    trends = state.analysis.get("market_trends", {})
    market_size = trends.get("market_size", {})

    return {
        "skool": market_size.get("skool", {}),
        "whop": market_size.get("whop", {}),
        "total_market_size": state.analysis.get("benchmarks", {}).get("total_estimated_market_size", 0)
    }

@app.post("/api/export")
async def export_data(request: ExportRequest):
    """Export data in specified format"""
    if state.data is None:
        raise HTTPException(status_code=404, detail="No data available")

    try:
        exporter = DataExporter()

        if request.format == "csv":
            filepath = exporter.export_to_csv(state.data)
            filename = filepath.name
        elif request.format == "json":
            filepath = exporter.export_to_json(state.data)
            filename = filepath.name
        else:
            raise HTTPException(status_code=400, detail="Invalid format")

        return {
            "message": "Export successful",
            "filename": filename,
            "path": str(filepath)
        }

    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/export-report")
async def export_report(request: ExportRequest):
    """Export analysis report"""
    if state.analysis is None:
        raise HTTPException(status_code=404, detail="No analysis available")

    try:
        exporter = DataExporter()

        if request.format == "csv":
            filepath = exporter.export_growth_report(state.analysis)
            filename = filepath.name
        elif request.format == "json":
            filepath = exporter.export_to_json(state.analysis)
            filename = filepath.name
        else:
            raise HTTPException(status_code=400, detail="Invalid format")

        return {
            "message": "Export successful",
            "filename": filename,
            "path": str(filepath)
        }

    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/exports")
async def list_exports():
    """List available exports"""
    exporter = DataExporter()
    exports = exporter.get_export_paths()
    return {
        "exports": [
            {
                "name": name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            }
            for name, file in exports.items()
        ]
    }

# Serve static dashboard
@app.get("/")
async def root():
    """Serve dashboard"""
    dashboard_path = Path("dashboard.html")
    if dashboard_path.exists():
        return FileResponse(dashboard_path, media_type="text/html")
    return {"message": "Market Growth Analyzer API"}

@app.get("/dashboard")
async def dashboard():
    """Serve dashboard"""
    dashboard_path = Path("dashboard.html")
    if dashboard_path.exists():
        return FileResponse(dashboard_path, media_type="text/html")
    return {"message": "Dashboard not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
