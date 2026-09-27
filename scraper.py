from bs4 import BeautifulSoup
import json
import requests


def scrape_mybuffstreams(target_url):
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

  # DEBUG: Let's check how many total tags and buttons exist
  all_buttons = soup.find_all(class_=lambda x: x and "btn" in x)
  print(f"  [DEBUG] Found {len(all_buttons)} elements with 'btn' in class.")

  # Check if any element has *any* data-* attribute
  data_elems = [tag for tag in soup.find_all(True) if tag.attrs]
  print(f"  [DEBUG] Total elements with attributes: {len(data_elems)}")

  # Find anchor tags containing data-openurl
  matching_tags = soup.find_all("a", attrs={"data-openurl": True})
  print(f"  [DEBUG] Found {len(matching_tags)} tags with data-openurl.")

  for a_tag in matching_tags:
    open_url = a_tag["data-openurl"]
    text = a_tag.get_text(strip=True)

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

  for url in mybuffstreams_urls:
    links = scrape_mybuffstreams(url)
    all_links.extend(links)

  for url in strikeout_urls:
    links = scrape_strikeout(url)
    all_links.extend(links)

  output_data = {"links": all_links}

  with open("links.json", "w") as f:
    json.dump(output_data, f, indent=4)

  print(
      f"\nSuccessfully extracted and saved a total of {len(all_links)} links"
      " to links.json"
  )
