# Product API Exporter

A small Python CLI that pulls product names from a store's products API,
handles pagination, and exports them to Excel.

## Why I built it

Product pages loaded their data dynamically, so HTML scraping with Selenium
returned nothing. I inspected the network traffic in Chrome DevTools, found
the underlying JSON API, and replaced the browser automation with direct
API calls. It runs in seconds instead of minutes.

## Features

- Automatic pagination until all products are fetched
- De-duplication by product ID
- Clear logging
- Handles a locked Excel file by saving to a backup file
- Unit tests for the parsing logic

## Installation

    pip install -r requirements.txt

## Usage

    python exporter.py --url <API_URL> --seller-id 8 --origin https://example.com --output products.xlsx

## Example output

| Serial | Product Name   |
|--------|----------------|
| 1      | Wireless Mouse |
| 2      | USB Hub        |

## Project structure

    product-api-exporter/
    ├── exporter.py
    ├── tests/
    │   └── test_exporter.py
    ├── requirements.txt
    ├── .gitignore
    ├── LICENSE
    └── README.md

## Run tests

    python -m pytest

## Tech

Python, requests, pandas, openpyxl, pytest

## Disclaimer

Use only on stores you own or have permission to access.
Respect the site's terms of service.