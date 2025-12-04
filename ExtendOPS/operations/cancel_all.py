#!/usr/bin/env python3
"""
Cancel all open orders
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(__file__))
from extended_executor import ExtendedExecutor

async def main():
    executor = ExtendedExecutor()
    if not await executor.initialize():
        return

    cancelled = await executor.cancel_all_orders()
    print(f"\n✅ Cancelled {cancelled} orders")

if __name__ == "__main__":
    asyncio.run(main())
