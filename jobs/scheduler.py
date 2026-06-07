from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from jobs.refresh_corpus import trigger_refresh
from datetime import datetime

scheduler = BackgroundScheduler()

def start_scheduler():
    """Initializes the background scheduler for nightly ingestion and frequent market updates."""
    if not scheduler.running:
        # Schedule to run every day at 02:00 AM
        scheduler.add_job(
            trigger_refresh, 
            trigger=CronTrigger(hour=2, minute=0), 
            id='daily_corpus_refresh',
            replace_existing=True
        )
        
        # Live market simulation: every 1 minute
        from jobs.nav_updater import update_navs
        scheduler.add_job(
            update_navs,
            'interval',
            minutes=1,
            id='live_market_simulation',
            replace_existing=True
        )
        
        # Intelligence feed updates: every 1 hour
        from jobs.intelligence_updater import update_intelligence
        scheduler.add_job(
            update_intelligence,
            'interval',
            hours=1,
            id='intelligence_feed_updater',
            replace_existing=True
        )
        
        scheduler.start()
        print("APScheduler started: daily_corpus_refresh at 02:00 AM UTC, live_market_simulation every 1m, intelligence feed every 1h.")

def get_scheduler_status():
    """Returns the current status of the background scheduler."""
    job = scheduler.get_job('daily_corpus_refresh')
    
    status = "healthy" if scheduler.running else "stopped"
    next_run = job.next_run_time.isoformat() if job and job.next_run_time else "N/A"
    
    return {
        "status": status,
        "next_refresh": next_run,
        "last_refresh": "Check ingestion_report.json for latest run details.",
        "documents_processed": "N/A (Dynamic)",
        "chunks_generated": "N/A (Dynamic)"
    }
