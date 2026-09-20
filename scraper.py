from bs4 import BeautifulSoup
import json
import requests


def scrape_game_links(target_url):
  # Use a standard User-Agent header to prevent basic bot-blocking
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
    print(f"Error fetching the webpage: {e}")
    return []

  # Parse the HTML source code
  soup = BeautifulSoup(response.text, "html.parser")

  links_data = []

  # Find all <a> tags that contain an href attribute
  for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    text = a_tag.get_text(strip=True)

    links_data.append({"text": text if text else "(No text)", "href": href})

  return links_data


if __name__ == "__main__":
  # Target website specified
  URL_TO_SCRAPE = "https://mybuffstreams.plus/mlb-live-streams"

  links = scrape_game_links(URL_TO_SCRAPE)

  # Package and save the extracted links into links.json
  output_data = {"links": links}

  with open("links.json", "w") as f:
    json.dump(output_data, f, indent=4)

  print(
      f"\nSuccessfully extracted and saved {len(links)} links to links.json"
  )
