# Api-Charts

This project provides a FastAPI service exposing two endpoints:

- `/price/history` – Fetches historical OHLCV data from Yahoo Finance.
- `/chart` – Returns a PNG screenshot of a TradingView widget for a symbol.

## Development

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

Run the server:

```bash
uvicorn run:app --reload
```

## Testing

```bash
pytest -v
```

## Docker

```bash
docker build -t api-charts .
docker run -p 8000:8000 api-charts
```

