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


def scrape_isportsurge(target_url):
  # UNTOUCHED: Your original iSportsurge logic
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    print(f"Fetching content from iSportsurge: {target_url}")
    response = requests.get(target_url, headers=headers)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching {target_url}: {e}")
    return []

  soup = BeautifulSoup(response.text, "html.parser")
  site_links = []

  elements = soup.find_all(
      "a", class_="row MaclariListele align-items-center align-content-center"
  )

  for el in elements:
    if el.has_attr("href"):
      href = el["href"]
      text = el.get_text(strip=True)

      if href.startswith("/"):
        full_href = f"https://isportsurge.ws{href}"
      elif href.startswith("http"):
        full_href = href
      else:
        full_href = f"https://isportsurge.ws/{href}"

      link_entry = {
          "source_site": target_url,
          "text": text if text else "(No text)",
          "href": full_href,
      }

      if link_entry not in site_links:
        site_links.append(link_entry)

  return site_links


def scrape_streameast(target_url):
  # UPDATED: Uses CSS selectors matching your screenshot structure cleanly
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    print(f"Fetching content from StreamEast: {target_url}")
    response = requests.get(target_url, headers=headers, timeout=10)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching {target_url}: {e}")
    return []

  soup = BeautifulSoup(response.text, "html.parser")
  site_links = []

  # Directly target the anchor tags inside the live stream cards shown in your screenshot
  stream_links = soup.select("article.stream-card.live a.card-link")

  for a_tag in stream_links:
    if a_tag.has_attr("href"):
      href = a_tag["href"]
      text = a_tag.get_text(strip=True)

      if href.startswith("/"):
        full_href = f"https://streameasto.cx{href}"
      elif href.startswith("http"):
        full_href = href
      else:
        full_href = f"https://streameasto.cx/{href}"

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

  isportsurge_urls = [
      "https://isportsurge.ws/nfl/livestreams3",
      "https://isportsurge.ws/nba/livestreams3",
      "https://isportsurge.ws/mlb/livestreams2",
      "https://isportsurge.ws/cfb/livestreams2",
      "https://isportsurge.ws/ncaa/livestreams2",
  ]

  streameast_urls = [
      "https://streameasto.cx/nfl",
      "https://streameasto.cx/mlb",
      "https://streameasto.cx/nba",
      "https://streameasto.cx/cfb",
      "https://streameasto.cx/ncaab",
  ]

  all_links = []

  # Scrape MyBuffStreams sources
  for url in mybuffstreams_urls:
    links = scrape_mybuffstreams(url)
    all_links.extend(links)

  # Scrape iSportsurge sources
  for url in isportsurge_urls:
    links = scrape_isportsurge(url)
    all_links.extend(links)

  # Scrape StreamEast sources
  for url in streameast_urls:
    links = scrape_streameast(url)
    all_links.extend(links)

  # Package and save all combined links into links.json
  output_data = {"links": all_links}

  with open("links.json", "w") as f:
    json.dump(output_data, f, indent=4)

  print(
      f"\nSuccessfully extracted and saved a total of {len(all_links)} links"
      " to links.json"
  )
