"""
UniqueDigit Multi-Store & Amazon Deals Ingestion (Zero-Block Architecture)
==========================================================================
Delegates directly to pipeline_amazon_deals.py for 100% accurate studio cutouts,
zero Amazon Akamai bot blocks, and auto-affiliate URL generation.
"""

import sys
from pipeline_amazon_deals import run_autonomous_deals_sync, fix_existing_deals_in_d1

if __name__ == "__main__":
    if "--fix" in sys.argv:
        fix_existing_deals_in_d1()
    else:
        # First ensure all existing deals have correct images, then sync new live deals
        fix_existing_deals_in_d1()
        run_autonomous_deals_sync(limit=3)

