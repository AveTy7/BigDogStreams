from bs4 import BeautifulSoup
import json
import requests


def scrape_site(target_url):
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    print(f"Fetching content from: {target_url}")
    response = requests.get(target_url, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching {target_url}: {e}")
    return []

  soup = BeautifulSoup(response.text, "html.parser")
  site_links = []

  # Find all elements with class="competition"
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


if __name__ == "__main__":
  urls_to_scrape = [
      "https://mybuffstreams.plus/mlb-live-streams",
      "https://mybuffstreams.plus/nflstreams2",
      "https://mybuffstreams.plus/nbastreams2",
  ]

  all_links = []

  for url in urls_to_scrape:
    links = scrape_site(url)
    all_links.extend(links)

  # Package and save all links into links.json
  output_data = {"links": all_links}

  with open("links.json", "w") as f:
    json.dump(output_data, f, indent=4)

  print(
      f"\nSuccessfully extracted and saved a total of {len(all_links)} links"
      " to links.json"
  )
