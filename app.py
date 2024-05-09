import json
from flask import Flask, render_template, request, redirect, url_for
from torrents2py import search_torrents
from qbittorrent import Client

app = Flask(__name__)

# Load the JSON file containing corrections
with open('corrections.json') as f:
    corrections = json.load(f)

def correct_spelling(word):
    if word.lower() in corrections:
        return corrections[word.lower()]
    else:
        return word

def get_quality(filename):
    # Define quality based on certain keywords in the filename
    if 'WEB' in filename:
        return 3  # Highest quality
    elif '1080p' in filename:
        return 2  # High quality
    elif '720p' in filename:
        return 1  # Medium quality
    else:
        return 0  # Default quality

def sort_results(results):
    # Sort results based on quality and other criteria
    return sorted(results, key=lambda x: (get_quality(x['Title']), 'cam' in x['Title'], 'www' in x['Title']), reverse=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        corrected_movie_name = ' '.join(correct_spelling(word) for word in movie_name.split())
        results = search_torrents(corrected_movie_name)
        sorted_results = sort_results(results)
        return render_template('index.html', results=sorted_results)
    return render_template('index.html', results=None)

@app.route('/download/<path:magnet_link>', methods=['GET'])
def download_torrent(magnet_link):
    # You might want to sanitize the magnet link here
    # For simplicity, we assume it's safe
    qb = Client('http://127.0.0.1:8080/')
    qb.login('admin', 'adminadmin')
    qb.download_from_link(magnet_link)
    return "Torrent added to download queue."

if __name__ == '__main__':
    app.run(debug=True)
