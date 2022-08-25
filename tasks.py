from models.Browser import Browser
import asyncio
def create_task(data):
    runner = Browser(data['domain'])
    page = asyncio.get_event_loop().run_until_complete(runner.open_browser(data['domain']))
    return page
   