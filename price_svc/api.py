from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Query
import pandas as pd
import yfinance as yf
from diskcache import Cache

from .symbol_map import to_yahoo

cache = Cache(".cache")

price_app = FastAPI(title="price_svc")


@price_app.get("/price/history")
async def get_history(
    symbol: str = Query(..., description="SYM:EXCHANGE"),
    interval: str = Query("1d", pattern="^(1d|1wk|1mo)$"),
    period: str = Query("1y", pattern="^(1y|6mo|5y)$"),
):
    key = f"{symbol}:{interval}:{period}"
    data: Optional[List[dict]] = cache.get(key)
    if data is None:
        yahoo_symbol = to_yahoo(symbol)
        df = yf.download(
            yahoo_symbol,
            interval=interval,
            period=period,
            auto_adjust=True,
            threads=False,
            progress=False,
        )
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.index = df.index.tz_localize(None)
        df.reset_index(inplace=True)
        df.rename(columns={"index": "date", "Datetime": "date", "Date": "date"}, inplace=True)
        data = [
            {
                "date": d["date"].strftime("%Y-%m-%d"),
                **{k: float(v) for k, v in d.items() if k != "date"},
            }
            for d in df.to_dict("records")
        ]
        cache.set(key, data, expire=60 * 60 * 8)
    return {"symbol": symbol, "rows": data}
