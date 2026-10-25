"""Export product names from a store's products API into an Excel file."""

import argparse
import logging
import time

import pandas as pd
import requests

log = logging.getLogger("exporter")

NAME_KEYS = ("name", "title", "product_name", "product_title")


def find_items(data):
    """Return the product list from an API response."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "items", "products", "results"):
            value = data.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, dict):
                inner = find_items(value)
                if inner:
                    return inner
    return []


def get_name(item):
    """Return the product name from a product dict, or an empty string."""
    for key in NAME_KEYS:
        if item.get(key):
            return str(item[key]).strip()
    return ""


def fetch_all(base_url, seller_id, origin, limit=50, delay=0.5):
    """Fetch every page of products and return a list of unique names."""
    products = {}
    page = 1
    with requests.Session() as session:
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept": "application/json",
                "Origin": origin,
                "Referer": origin + "/",
            }
        )
        while True:
            response = session.get(
                base_url,
                params={"seller_id": seller_id, "page": page, "limit": limit},
                timeout=30,
            )
            response.raise_for_status()
            items = find_items(response.json())

            new = 0
            for item in items:
                name = get_name(item)
                product_id = item.get("id", name)
                if name and product_id not in products:
                    products[product_id] = name
                    new += 1

            log.info("Page %d: %d items, %d new, %d total", page, len(items), new, len(products))
            if not items or new == 0:
                break
            page += 1
            time.sleep(delay)
    return list(products.values())


def save_excel(names, output):
    """Save names to Excel. Falls back to a timestamped file if locked."""
    df = pd.DataFrame({"Serial": range(1, len(names) + 1), "Product Name": names})
    try:
        df.to_excel(output, index=False)
        return output
    except PermissionError:
        backup = f"products_{int(time.time())}.xlsx"
        df.to_excel(backup, index=False)
        log.warning("%s is locked (open in Excel?). Saved to %s instead.", output, backup)
        return backup


def main():
    parser = argparse.ArgumentParser(description="Export product names from a products API to Excel.")
    parser.add_argument("--url", required=True, help="Products API endpoint")
    parser.add_argument("--seller-id", required=True, type=int, help="Seller/store ID")
    parser.add_argument("--origin", required=True, help="Site origin, e.g. https://example.com")
    parser.add_argument("--output", default="products.xlsx", help="Output Excel file")
    parser.add_argument("--limit", type=int, default=50, help="Items per page")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        names = fetch_all(args.url, args.seller_id, args.origin, args.limit)
    except requests.RequestException as exc:
        log.error("Request failed: %s", exc)
        raise SystemExit(1)

    if not names:
        log.error("No products found.")
        raise SystemExit(1)

    saved = save_excel(names, args.output)
    log.info("Done. %d products saved to %s", len(names), saved)


if __name__ == "__main__":
    main()