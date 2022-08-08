from models.Browser import Browser
import asyncio
def create_task(domain):
    runner = Browser(domain)
    page = asyncio.get_event_loop().run_until_complete(runner.open_browser(domain))
    return page
   