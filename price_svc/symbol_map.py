EX_SUFFIX = {
    "EGX": ".CA",
    "TADAWUL": ".SR",
    "LSE": ".L",
    "NASDAQ": "",
    "NYSE": "",
}


def to_yahoo(symbol: str) -> str:
    """Convert SYM:EXCHANGE to Yahoo Finance symbol."""
    if ':' not in symbol:
        return symbol
    sym, ex = symbol.split(':', 1)
    suffix = EX_SUFFIX.get(ex.upper(), '')
    return f"{sym}{suffix}"
