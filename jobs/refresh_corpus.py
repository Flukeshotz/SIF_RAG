import asyncio
from ingestion.run import run_ingestion

def trigger_refresh():
    """Synchronous wrapper to trigger the async ingestion pipeline."""
    try:
        # We create a new event loop because this will be run inside a background thread by APScheduler
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_ingestion())
        loop.close()
    except Exception as e:
        print(f"Error during corpus refresh: {e}")
