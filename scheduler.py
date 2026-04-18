"""
PsyTrends Scheduler - Runs analysis on a 24-hour cycle
"""

import schedule
import time
import logging
from datetime import datetime
from dashboard import run_cycle

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('psytrends.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def scheduled_run():
    """Run the analysis cycle and log results"""
    try:
        logger.info("=" * 80)
        logger.info("Starting PsyTrends analysis cycle")
        logger.info("=" * 80)
        run_cycle()
        logger.info("Analysis cycle completed successfully")
    except Exception as e:
        logger.error(f"Error during analysis cycle: {e}", exc_info=True)

def main():
    """Main scheduler loop"""
    logger.info("PsyTrends Scheduler started")
    
    # Schedule the job
    schedule.every(24).hours.do(scheduled_run)
    
    # Run immediately on startup
    scheduled_run()
    
    logger.info("Scheduler is running. Press Ctrl+C to stop.")
    
    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute if a job needs to run

if __name__ == "__main__":
    main()
