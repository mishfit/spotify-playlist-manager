#!/usr/bin/env python3
"""
Spotify Playlist Retriever
Uses Authorization Code Flow to access user playlists
"""

import os
import sys
import base64
import json
from urllib.parse import urlencode, parse_qs
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://127.0.0.1:8888/callback'
SCOPE = 'playlist-read-private playlist-read-collaborative'

# Global variable to store authorization code
auth_code = None


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP server handler to receive OAuth callback"""

    def do_GET(self):
        global auth_code

        # Parse the authorization code from the callback URL
        query = parse_qs(self.path.split('?')[1] if '?' in self.path else '')

        if 'code' in query:
            auth_code = query['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization successful!</h1><p>You can close this window.</p></body></html>')
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization failed!</h1></body></html>')

    def log_message(self, format, *args):
        """Suppress server logs"""
        pass


def get_authorization_code():
    """Step 1: Get authorization code from user"""
    global auth_code

    # Build authorization URL
    auth_params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE
    }

    auth_url = f'https://accounts.spotify.com/authorize?{urlencode(auth_params)}'

    print(f'\n🎵 Opening browser for Spotify authorization...')
    print(f'If the browser does not open, visit this URL:\n{auth_url}\n')

    # Open browser for user authorization
    webbrowser.open(auth_url)

    # Start local server to receive callback
    server = HTTPServer(('127.0.0.1', 8888), CallbackHandler)
    print('⏳ Waiting for authorization...')

    # Handle one request (the callback)
    server.handle_request()
    server.server_close()

    return auth_code


def get_access_token(auth_code):
    """Step 2: Exchange authorization code for access token"""

    # Encode client credentials
    credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'
    b64_credentials = base64.b64encode(credentials.encode()).decode()

    # Request access token
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {b64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f'❌ Error getting access token: {response.text}')
        sys.exit(1)


def get_user_playlists(access_token):
    """Step 3: Get user's playlists"""

    playlists_url = 'https://api.spotify.com/v1/me/playlists'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    all_playlists = []

    while playlists_url:
        response = requests.get(playlists_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            all_playlists.extend(data['items'])
            playlists_url = data.get('next')  # Handle pagination
        else:
            print(f'❌ Error getting playlists: {response.text}')
            sys.exit(1)

    return all_playlists


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print('❌ Error: Missing Spotify credentials in .env file')
        sys.exit(1)

    print('🎵 Spotify Playlist Retriever')
    print('=' * 50)

    # Step 1: Get authorization code
    code = get_authorization_code()

    if not code:
        print('❌ Failed to get authorization code')
        sys.exit(1)

    print('✅ Authorization code received')

    # Step 2: Exchange for access token
    print('🔑 Requesting access token...')
    access_token = get_access_token(code)
    print('✅ Access token received')

    # Step 3: Get playlists
    print('📋 Fetching playlists...\n')
    playlists = get_user_playlists(access_token)

    # Display playlists
    print(f'Found {len(playlists)} playlists:\n')
    print('=' * 80)

    for i, playlist in enumerate(playlists, 1):
        name = playlist['name']
        tracks = playlist['tracks']['total']
        owner = playlist['owner']['display_name']
        public = '🌍 Public' if playlist['public'] else '🔒 Private'

        print(f'{i:3d}. {name}')
        print(f'      Owner: {owner} | Tracks: {tracks} | {public}')
        print(f'      URL: {playlist["external_urls"]["spotify"]}')
        print('-' * 80)

    # Save to JSON file
    output_file = 'playlists.json'
    with open(output_file, 'w') as f:
        json.dump(playlists, f, indent=2)

    print(f'\n💾 Full playlist data saved to {output_file}')


if __name__ == '__main__':
    main()
