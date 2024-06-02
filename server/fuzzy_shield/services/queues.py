import asyncio

"""Used internally by status updater and other service, once done, task handed down to EXTERNAL_UPDATES_QUEUE """
INTERNAL_UPDATES_QUEUE = asyncio.Queue()

EXTERNAL_UPDATES_QUEUE = asyncio.Queue()
