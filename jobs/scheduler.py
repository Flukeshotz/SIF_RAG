from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from jobs.refresh_corpus import trigger_refresh
from datetime import datetime

scheduler = BackgroundScheduler()

def start_scheduler():
    """Initializes the background scheduler for nightly ingestion."""
    if not scheduler.running:
        # Schedule to run every day at 02:00 AM
        scheduler.add_job(
            trigger_refresh, 
            trigger=CronTrigger(hour=2, minute=0), 
            id='daily_corpus_refresh',
            replace_existing=True
        )
        scheduler.start()
        print("APScheduler started: daily_corpus_refresh scheduled for 02:00 AM UTC.")

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
