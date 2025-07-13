from fastapi import FastAPI, Query, Response, HTTPException
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

chart_app = FastAPI(title="chart_svc")


@chart_app.get("/chart")
async def get_chart(symbol: str = Query(...), interval: str = Query("1D")):
    url = (
        "https://s.tradingview.com/widgetembed/?"
        f"symbol={symbol}&interval={interval}&hidetoptoolbar=1&hidesidetoolbar=1"
    )
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--ignore-certificate-errors"])
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        try:
            await page.wait_for_selector("body", timeout=30000)
        except PlaywrightTimeout:
            await browser.close()
            raise HTTPException(status_code=504, detail="Chart widget timeout")
        png = await page.screenshot(type="png")
        await browser.close()
    return Response(content=png, media_type="image/png")
