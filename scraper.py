from bs4 import BeautifulSoup
import json
import requests


def scrape_strikeout(target_url):
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    print(f"Fetching content from StrikeOut: {target_url}")
    response = requests.get(target_url, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching {target_url}: {e}")
    return []

  soup = BeautifulSoup(response.text, "html.parser")
  site_links = []

  # Adjust target tags/classes based on StrikeOut's layout structure
  # Looking for general event/stream links containers or anchor tags
  for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    text = a_tag.get_text(strip=True)

    # Filter for relevant internal/external stream links if needed
    if href and href.startswith("http") or href.startswith("/"):
      link_entry = {
          "source_site": target_url,
          "text": text if text else "(No text)",
          "href": href,
      }

      if link_entry not in site_links:
        site_links.append(link_entry)

  return site_links


if __name__ == "__main__":
  strikeout_urls = [
      "https://strikeout.im/nfl",
      "https://strikeout.im/nba",
      "https://strikeout.im/mlb",
      "https://strikeout.im/ncaaf",
  ]

  all_strikeout_links = []

  for url in strikeout_urls:
    links = scrape_strikeout(url)
    all_strikeout_links.extend(links)

  output_data = {"links": all_strikeout_links}

  with open("strikeout_links.json", "w") as f:
    json.dump(output_data, f, indent=4)

  print(
      f"\nSuccessfully extracted and saved a total of"
      f" {len(all_strikeout_links)} links to strikeout_links.json"
  )
