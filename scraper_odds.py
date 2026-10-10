import json
import urllib.parse
import urllib.request

# Put your API key here
API_KEY = "4ff5d35d05a7ea89db9e932712d6d69d"

targets = [
    {"sport_key": "americanfootball_nfl", "label": "NFL"},
    {"sport_key": "americanfootball_ncaaf", "label": "NCAAF"},
    {"sport_key": "americanfootball_ncaaf_fcs", "label": "NCAAF FCS"},
    {"sport_key": "baseball_mlb", "label": "MLB"},
    {"sport_key": "basketball_ncaab", "label": "CBK"},
    {"sport_key": "basketball_nba", "label": "NBA"},
]

all_scraped_data = []
global_id = 1

for target in targets:
  base_url = f"https://api.the-odds-api.com/v4/sports/{target['sport_key']}/odds/"
  params = {
      "apiKey": API_KEY,
      "regions": "us",
      "markets": "spreads",
      "oddsFormat": "american",
  }
  url = base_url + "?" + urllib.parse.urlencode(params)

  print(f"Fetching data for {target['label']}...")
  try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
      if response.status == 200:
        games = json.loads(response.read().decode("utf-8"))
        print(f"Successfully retrieved {len(games)} games for {target['label']}.")

        for game in games:
          home_team = game.get("home_team")
          away_team = game.get("away_team")
          commence_time = game.get("commence_time")

          bookmakers = game.get("bookmakers", [])
          spread_val = "N/A"
          if bookmakers:
            markets = bookmakers[0].get("markets", [])
            for market in markets:
              if market.get("key") == "spreads":
                outcomes = market.get("outcomes", [])
                for outcome in outcomes:
                  if outcome.get("name") == home_team:
                    spread_val = outcome.get("point")

          all_scraped_data.append({
              "id": global_id,
              "source": target["label"],
              "team": home_team,
              "opponent": away_team,
              "spread": spread_val,
              "commence_time": commence_time,
          })
          global_id += 1

          all_scraped_data.append({
              "id": global_id,
              "source": target["label"],
              "team": away_team,
              "opponent": home_team,
              "spread": (
                  -spread_val
                  if isinstance(spread_val, (int, float))
                  else "N/A"
              ),
              "commence_time": commence_time,
          })
          global_id += 1
  except Exception as e:
    print(f"Failed to fetch {target['label']}. Error: {e}")

output_filename = "odds_data.json"
with open(output_filename, "w", encoding="utf-8") as f:
  json.dump(all_scraped_data, f, indent=4)

print(
    f"\nSuccessfully saved a total of {len(all_scraped_data)} structured entries"
    f" to {output_filename}"
)
