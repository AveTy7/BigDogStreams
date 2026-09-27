from bs4 import BeautifulSoup
import json
import requests


def scrape_mybuffstreams(target_url):
  # UNTOUCHED: Your original MyBuffStreams logic
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    print(f"Fetching content from MyBuffStreams: {target_url}")
    response = requests.get(target_url, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching {target_url}: {e}")
    return []

  soup = BeautifulSoup(response.text, "html.parser")
  site_links = []

  competition_elements = soup.find_all(class_="competition")

  for el in competition_elements:
    if el.name == "a" and el.has_attr("href"):
      href = el["href"]
      text = el.get_text(strip=True)
      site_links.append(
          {
              "source_site": target_url,
              "text": text if text else "(No text)",
              "href": href,
          }
      )

    for a_tag in el.find_all("a", href=True):
      href = a_tag["href"]
      text = a_tag.get_text(strip=True)
      link_entry = {
          "source_site": target_url,
          "text": text if text else "(No text)",
          "href": href,
      }

      if link_entry not in site_links:
        site_links.append(link_entry)

  return site_links


def scrape_strikeout(target_url):
  # Enhanced headers mimicking a live desktop browser to pass basic bot checks
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/122.0.0.0 Safari/537.36"
      ),
      "Accept": (
          "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
          "image/webp,image/apng,*/*;q=0.8"
      ),
      "Accept-Language": "en-US,en;q=0.9",
      "Accept-Encoding": "gzip, deflate, br",
      "Referer": "https://strikeout.im/",
      "Sec-Ch-Ua": (
          '"Chromium";v="122", "Not(A:Brand";v="8", "Google Chrome";v="122"'
      ),
      "Sec-Ch-Ua-Mobile": "?0",
      "Sec-Ch-Ua-Platform": '"Windows"',
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "same-origin",
      "Sec-Fetch-User": "?1",
      "Upgrade-Insecure-Requests": "1",
  }

  try:
    print(f"Fetching content from StrikeOut: {target_url}")
    response = requests.get(target_url, headers=headers, timeout=20)
    print(
        f"  [DEBUG] Status Code: {response.status_code} | Content Length:"
        f" {len(response.text)}"
    )
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching {target_url}: {e}")
    return []

  soup = BeautifulSoup(response.text, "html.parser")
  site_links = []

  # Search for tags containing either data-openurl or data-openuri
  matching_tags = []
  for tag in soup.find_all(True):
    if tag.has_attr("data-openurl") or tag.has_attr("data-openuri"):
      matching_tags.append(tag)

  print(f"  [DEBUG] Found {len(matching_tags)} target attributes on StrikeOut.")

  for tag in matching_tags:
    open_url = tag.get("data-openurl") or tag.get("data-openuri")
    text = tag.get_text(strip=True)

    if not open_url:
      continue

    if open_url.startswith("/"):
      full_href = f"https://strikeout.im{open_url}"
    elif open_url.startswith("http"):
      full_href = open_url
    else:
      full_href = f"https://strikeout.im/{open_url}"

    link_entry = {
        "source_site": target_url,
        "text": text if text else "(No text)",
        "href": full_href,
    }

    if link_entry not in site_links:
      site_links.append(link_entry)

  return site_links


if __name__ == "__main__":
  mybuffstreams_urls = [
      "https://mybuffstreams.plus/mlb-live-streams",
      "https://mybuffstreams.plus/nflstreams2",
      "https://mybuffstreams.plus/nbastreams2",
  ]

  strikeout_urls = [
      "https://strikeout.im/nfl",
      "https://strikeout.im/nba",
      "https://strikeout.im/mlb",
      "https://strikeout.im/ncaaf",
  ]

  all_links = []

  # Scrape MyBuffStreams sources
  for url in mybuffstreams_urls:
    links = scrape_mybuffstreams(url)
    all_links.extend(links)

  # Scrape StrikeOut sources
  for url in strikeout_urls:
    links = scrape_strikeout(url)
    all_links.extend(links)

  # Package and save all combined links into links.json
  output_data = {"links": all_links}

  with open("links.json", "w") as f:
    json.dump(output_data, f, indent=4)

  print(
      f"\nSuccessfully extracted and saved a total of {len(all_links)} links"
      " to links.json"
  )
