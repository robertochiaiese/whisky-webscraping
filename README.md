# 🥃 Whisky Scraper with Redis

This project is a simple **web scraping script** written in Python that collects whisky product data from [saporideisassi.it](https://www.saporideisassi.it/80-whisky) and stores the results in a **Redis database**.  

It is a small demo project that shows how to:
- Scrape product information from multiple pages using `requests` and `BeautifulSoup`.
- Extract details such as **name, price, description, provenance, type, and brand**.
- Store structured product data in Redis using a hash format.

---

## 📦 Features

For each whisky, the scraper retrieves:
- **Name**
- **Price**
- **Product URL**
- **Description**
- **Provenance** (origin)
- **Type** (e.g., Single Malt, Blended)
- **Brand**

Data is stored in Redis with the whisky name as the key.

---

## ⚙️ Requirements

- Python 3.8+
- Running Redis server (local or remote)

Install Python dependencies with:

```bash
pip install -r requirements.txt
