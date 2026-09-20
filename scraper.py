from bs4 import BeautifulSoup
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

  game_links = set()

  # Find all <a> tags that contain an href attribute
  for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]

    # TODO: Adjust this filter pattern to match the specific structure
    # of the game URLs on your target website (e.g., containing '/game/' or specific keywords)
    if "game" in href or "schedule" in href:

      # Handle relative URLs by prepending the domain if needed
      if href.startswith("/"):
        href = "https://www.mlb.com" + href  # Update base domain as needed

      game_links.add(href)

  return list(game_links)


if __name__ == "__main__":
  # Replace with your specific target schedule URL
  URL_TO_SCRAPE = "https://www.mlb.com/dodgers/schedule"

  links = scrape_game_links(URL_TO_SCRAPE)

  print(f"\nSuccessfully extracted {len(links)} matching links:")
  for link in links:
    print(link)
