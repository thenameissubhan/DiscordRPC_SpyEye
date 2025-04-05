import requests

def search_steam_games(query):
    """
    Search for Steam games based on a name query.

    :param query: The name of the game to search for.
    :return: A list of games matching the query.
    """
    # Alternative Steam API endpoint
    url = "https://store.steampowered.com/api/storesearch/"

    # Parameters for the search
    params = {
        'term': query,   # Search term
        'cc': 'US',      # Country code (adjust as needed)
        'l': 'english',  # Language (adjust as needed)
    }

    try:
        print(f"Sending request to Steam API with query: {query}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Debugging: Print the raw response to check its structure
        print(f"Response received: {data}")

        # Check if the response contains games
        if 'items' in data:
            games = data['items']
            return games
        else:
            print("No games found for the search query.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Steam API: {e}")
        return []

if __name__ == "__main__":
    search_query = input("Enter the name of the game to search for: ").strip()

    if not search_query:
        print("Please provide a valid search term.")
    else:
        results = search_steam_games(search_query)

        if results:
            print(f"Found {len(results)} games matching '{search_query}':")
            for game in results:
                print(f"- {game['name']} (App ID: {game['id']})")
        else:
            print("No games found.")