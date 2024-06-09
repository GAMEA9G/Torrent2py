import json
from torrents2py import search_torrents
from qbittorrent import Client
import webbrowser

# Load the JSON file containing corrections
with open('corrections.json') as f:
    corrections = json.load(f)

def correct_spelling(word):
    # Check if the word exists in the corrections dictionary
    if word.lower() in corrections:
        return corrections[word.lower()]
    else:
        return word

# Filters and input
movie_name = input('Enter movie name: ')

# Correct the spelling of the movie name
corrected_movie_name = ' '.join(correct_spelling(word) for word in movie_name.split())

# Perform a search with the corrected movie name and filters
results = search_torrents(corrected_movie_name)

print("\nFiltered Search Results:")
for index, result in enumerate(results, start=1):
    print(f"Torrent {index} Information:"
          f"\n   Title:    {result.get('Title')}"
          f"\n   Uploaded: {result.get('Uploaded')}"
          f"\n   Size:     {result.get('Size')}"
          f"\n   Seeds:    {result.get('Seeds')}"
          f"\n   Peers:    {result.get('Peers')}"
          f"\n   Magnet Link:    {result.get('MagnetLink')}")

# Prompt the user to select a torrent
while True:
    selection = input("Which of these you want to play (type 'exit' to quit): ")

    if selection.lower() == 'exit':
        break

    try:
        selected_index = int(selection) - 1
        if 0 <= selected_index < len(results):
            # Initialize qBittorrent client
            qb = Client('http://127.0.0.1:8080/')
            qb.login('admin', 'adminadmin')
            qb.download_from_link(results[selected_index].get('MagnetLink'))

            print("Torrent added to download queue.")
            break  # Exit the loop after successfully adding the torrent
        else:
            print("Invalid selection. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number or 'exit' to quit.")

# Note: Make sure you have qBittorrent running and accessible at http://127.0.0.1:8080/
