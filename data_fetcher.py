# data_fetcher.py
"""
EpiClimate HMAS — Real Data Fetcher
Reference: docs/api_reference.md
Reference: docs/architecture.md (Real Data Sources section)

Fetches real live outbreak data from free public health sources.
All functions return structured Python lists or dicts.
All functions return empty fallbacks on failure — never raise exceptions.

Sources:
  WHO Disease Outbreak News RSS   https://www.who.int/feeds/entity/csr/don/en/rss.xml
  ProMED Early Warning RSS        https://promedmail.org/promed-rss/
  ReliefWeb Disasters API         https://api.reliefweb.int/v1/disasters
  GDELT Global News API           https://api.gdeltproject.org/api/v2/doc/doc
"""

import xml.etree.ElementTree as ET
import requests
from utils import safe_api_call

WHO_DON_RSS    = "https://www.who.int/feeds/entity/csr/don/en/rss.xml"
PROMED_RSS     = "https://promedmail.org/promed-rss/"
RELIEFWEB_URL  = "https://api.reliefweb.int/v1/disasters"
GDELT_DOC_URL  = "https://api.gdeltproject.org/api/v2/doc/doc"


def fetch_who_outbreaks(disease: str = None, country: str = None,
                        max_items: int = 5) -> list:
    """
    Fetches real WHO Disease Outbreak News alerts.
    Filters by disease and country keywords if provided.
    Returns list of {title, link, description, pub_date, source}
    """
    print(f"  [DataFetcher] Fetching WHO Disease Outbreak News...")
    try:
        response = requests.get(WHO_DON_RSS, timeout=10)
        response.raise_for_status()
        root  = ET.fromstring(response.content)
        items = []

        for item in root.iter("item"):
            title    = item.findtext("title", "").lower()
            desc     = item.findtext("description", "").lower()
            combined = title + " " + desc

            if disease and disease.lower() not in combined:
                continue
            if country and country.lower() not in combined:
                continue

            items.append({
                "title":       item.findtext("title", ""),
                "link":        item.findtext("link", ""),
                "description": item.findtext("description", ""),
                "pub_date":    item.findtext("pubDate", ""),
                "source":      "WHO Disease Outbreak News"
            })

            if len(items) >= max_items:
                break

        print(f"  [DataFetcher] WHO: {len(items)} matching alerts found")
        return items

    except Exception as e:
        print(f"  [DataFetcher] WHO RSS failed: {e}")
        return []


def fetch_promed_alerts(disease: str = None, country: str = None,
                        max_items: int = 5) -> list:
    """
    Fetches ProMED early warning disease alerts.
    ProMED is often 2-4 weeks ahead of official WHO declarations.
    Returns list of {title, link, description, pub_date, source}
    """
    print(f"  [DataFetcher] Fetching ProMED alerts...")
    try:
        response = requests.get(PROMED_RSS, timeout=10,
                                headers={"User-Agent": "EpiClimate-HMAS/1.0"})
        response.raise_for_status()
        root  = ET.fromstring(response.content)
        items = []

        for item in root.iter("item"):
            title    = item.findtext("title", "").lower()
            desc     = item.findtext("description", "").lower()
            combined = title + " " + desc

            if disease and disease.lower() not in combined:
                continue
            if country and country.lower() not in combined:
                continue

            items.append({
                "title":       item.findtext("title", ""),
                "link":        item.findtext("link", ""),
                "description": item.findtext("description", "")[:500],
                "pub_date":    item.findtext("pubDate", ""),
                "source":      "ProMED"
            })

            if len(items) >= max_items:
                break

        print(f"  [DataFetcher] ProMED: {len(items)} matching alerts found")
        return items

    except Exception as e:
        print(f"  [DataFetcher] ProMED RSS failed: {e}")
        return []


def fetch_reliefweb_outbreaks(country: str = None, max_items: int = 3) -> list:
    """
    Fetches active epidemic disasters from ReliefWeb (UN humanitarian platform).
    Returns list of {name, countries, status, date_start, url, source}
    """
    print(f"  [DataFetcher] Fetching ReliefWeb disasters...")
    data = safe_api_call(RELIEFWEB_URL, {
        "appname":        "epiclimate-hmas",
        "filter[field]":  "type.name",
        "filter[value]":  "Epidemic",
        "sort[]":         "date.created:desc",
        "limit":          max_items * 3
    })

    if not data or "data" not in data:
        print(f"  [DataFetcher] ReliefWeb: no data returned")
        return []

    results = []
    for item in data.get("data", []):
        fields       = item.get("fields", {})
        country_list = [c.get("name", "") for c in fields.get("country", [])]

        if country and not any(country.lower() in c.lower() for c in country_list):
            continue

        results.append({
            "name":       fields.get("name", ""),
            "countries":  country_list,
            "status":     fields.get("status", ""),
            "date_start": fields.get("date", {}).get("created", "")[:10],
            "url":        item.get("href", ""),
            "source":     "ReliefWeb"
        })

        if len(results) >= max_items:
            break

    print(f"  [DataFetcher] ReliefWeb: {len(results)} matching disasters found")
    return results


def fetch_gdelt_news(query: str, max_items: int = 5) -> list:
    """
    Searches real-time global news using GDELT (no API key needed).
    Returns list of {title, url, domain, date, source}
    """
    print(f"  [DataFetcher] Fetching GDELT news: '{query}'...")
    data = safe_api_call(GDELT_DOC_URL, {
        "query":      query,
        "mode":       "artlist",
        "maxrecords": max_items,
        "format":     "json",
        "sort":       "DateDesc"
    })

    if not data or "articles" not in data:
        print(f"  [DataFetcher] GDELT: no articles returned")
        return []

    results = []
    for article in data.get("articles", [])[:max_items]:
        results.append({
            "title":  article.get("title", ""),
            "url":    article.get("url", ""),
            "domain": article.get("domain", ""),
            "date":   article.get("seendate", "")[:8],
            "source": "GDELT"
        })

    print(f"  [DataFetcher] GDELT: {len(results)} articles found")
    return results


def fetch_all_outbreak_intelligence(country: str, disease: str) -> dict:
    """
    Master function — fetches real data from ALL sources for one country + disease.
    Call this from DiseaseTrackerAgent.

    Returns:
    {
      who_alerts:       list,
      promed_alerts:    list,
      reliefweb_events: list,
      news_articles:    list,
      has_real_data:    bool
    }
    """
    print(f"  [DataFetcher] Collecting all intelligence: {disease} in {country}...")

    who_data       = fetch_who_outbreaks(disease=disease, country=country)
    promed_data    = fetch_promed_alerts(disease=disease, country=country)
    reliefweb_data = fetch_reliefweb_outbreaks(country=country)
    gdelt_data     = fetch_gdelt_news(f"{disease} outbreak {country}", max_items=5)

    has_data = any([who_data, promed_data, reliefweb_data, gdelt_data])
    total    = len(who_data) + len(promed_data) + len(reliefweb_data) + len(gdelt_data)

    print(f"  [DataFetcher] Total real data points collected: {total}")

    return {
        "who_alerts":       who_data,
        "promed_alerts":    promed_data,
        "reliefweb_events": reliefweb_data,
        "news_articles":    gdelt_data,
        "has_real_data":    has_data
    }
