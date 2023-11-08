# ebay-monitor-bot

### Requirements
- Python 3.9

### Commands
- `!register`: Registers the channel this is sent from as the channel to send updates to
  - Usage: `!register <use_existing>`
    - `use_existing` (optional, default=True): Whether the bot should use the existing watchlist under `./watchlist.json`
- `!watchlistGet`: Returns the current watchlist
- `!watchlistAdd`: Adds an item to the watchlist
  - Usage: `!watchlistAdd <name> <link> <price> <interval>`
    - `name`: Name of the item in the watchlist
    - `link`: Link to watch where the search is sorte by newly listed, ex.`https://www.ebay.com/sch/i.html?_from=R40&_nkw=refrigerator&_sacat=0&_sop=10` 
    - `price`: Maximum price to watch out for
    - `interval` (optional, default=60): Polling interval to check if there are new listings. Must be a multiple of 10. In seconds
- `!watchlistRemove`: Removes an item from the watchlist
  - Usage: `!watchlistRemove <name>`
    - `name`: Name of the item in the watchlist
