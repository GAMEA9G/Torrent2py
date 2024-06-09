import json
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from torrents2py import search_torrents
from qbittorrent import Client
import subprocess
import webbrowser
import sys
import os
import glob
import os
import webview


app = Flask(__name__)
window = webview.create_window('watch movie',app)
# Directory to store downloaded movies
DOWNLOAD_DIR = 'static/downloads'

# Load the JSON file containing corrections
with open('corrections.json') as f:
    corrections = json.load(f)

def correct_spelling(word):
    return corrections.get(word.lower(), word)

def get_quality(filename):
    if 'WEBDB' in filename:
        return 3  # Highest quality
    elif '1080p' in filename:
        return 2  # High quality
    elif '720p' in filename:
        return 1  # Medium quality
    else:
        return 0  # Default quality

def webtorrent_stream(magnet_link: str):
    cmd = ["peerflix", magnet_link, "--vlc"]
    try:
        if sys.platform.startswith('linux'):
            subprocess.Popen(['gnome-terminal', '--'] + cmd)
        elif sys.platform.startswith('win32'):
            subprocess.Popen(['cmd.exe', '/c', 'start'] + cmd, shell=True)
    except Exception as e:
        print(f"Error starting webtorrent: {e}")


def sort_results(results):
    return sorted(results, key=lambda x: (get_quality(x['Title']), 'cam' in x['Title'], 'www' in x['Title']), reverse=True)


def play_video(video_path):
    try:
        app.video_path = video_path
    except Exception as e:
        print(f"Error storing video path: {e}")



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        corrected_movie_name = ' '.join(correct_spelling(word) for word in movie_name.split())
        try:
            results = search_torrents(corrected_movie_name)
            sorted_results = sort_results(results)
        except Exception as e:
            print(f"Error searching torrents: {e}")
            sorted_results = []
        return render_template('index.html', results=sorted_results)
    return render_template('index.html', results=None)

@app.route('/download/<path:magnet_link>', methods=['GET'])
def download_torrent(magnet_link):
    
    webtorrent_stream(magnet_link)
    
    return "vlc"
    
    

    
    
    
    
       
    

@app.route('/stream/<filename>')
def stream_movie(filename):
    try:
        return send_from_directory(DOWNLOAD_DIR, filename)
    except Exception as e:
        return f"Error streaming movie: {e}", 404

@app.route('/stream_video', methods=['GET'])
def stream_video():
    return render_template('stream.html', video_path=app.video_path)

if __name__ == '__main__':
   
   
    #app.run(debug=True)
    webview.start()
