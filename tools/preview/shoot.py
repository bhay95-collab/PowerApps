import asyncio, sys, glob, os
from playwright.async_api import async_playwright
async def main(files):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium' if os.path.exists('/opt/pw-browsers/chromium') else None)
        for f in files:
            pg = await b.new_page(device_scale_factor=2, viewport={'width': 900, 'height': 1200})
            await pg.goto('file://' + os.path.abspath(f))
            el = await pg.query_selector('.phone')
            await el.screenshot(path=f.replace('.html', '.png'))
            await pg.close()
        await b.close()
asyncio.run(main(sys.argv[1:]))
