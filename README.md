# Spotify Playlist Manager

A Python-based tool for interacting with the Spotify API to retrieve and manage playlists.

## Features

- OAuth 2.0 Authorization Code Flow implementation
- Retrieve all user playlists with complete metadata
- Export playlist data to JSON format
- Support for both public and private playlists

## Prerequisites

- Python 3.9+
- A Spotify Developer account
- Spotify API credentials (Client ID and Client Secret)

## Setup

### 1. Get Spotify API Credentials

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app (or use an existing one)
3. Note your **Client ID** and **Client Secret**
4. In your app settings, add the following Redirect URI:
   ```
   http://127.0.0.1:8888/callback
   ```
5. Save your app settings

### 2. Configure Environment Variables

1. Copy the template file:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

3. **Important:** The `.env` file is git-ignored and should never be committed to version control.

### 3. Install Dependencies

```bash
pip3 install -r requirements.txt
```

## Usage

### Get Your Playlists

Run the playlist retrieval script:

```bash
python3 get_playlists.py
```

The script will:
1. Open your browser for Spotify authorization
2. Request access to your playlists
3. Retrieve all your playlists (with pagination support)
4. Display a summary in the terminal
5. Save complete data to `playlists.json`

### Output

The script displays:
- Playlist name and owner
- Number of tracks
- Public/Private status
- Spotify URL

Example output:
```
Found 34 playlists:

  1. Epic Dance Party
      Owner: mishochu | Tracks: 72 | 🌍 Public
      URL: https://open.spotify.com/playlist/6h1aKe7ireMTprk3A9ZGDK
```

## Files

- `get_playlists.py` - Main script to retrieve playlists
- `playlists.json` - Output file with complete playlist data (generated after running the script)
- `requirements.txt` - Python dependencies
- `.env` - Your API credentials (not committed to git)
- `.env.template` - Template for environment variables
- `.env.asc` - PGP-encrypted credentials for authorized users

## Security

### Credentials Storage

This project uses multiple layers of security:

1. **Local `.env` file** - For development use, excluded from git
2. **PGP-encrypted `.env.asc`** - Encrypted for authorized recipients:
   - mishochu@mishochu.com
   - mishochu@nokware.net
   - mishochu@gmail.com
   - jenkins@nokware.net

### Decrypting Credentials

If you're an authorized recipient, decrypt the credentials with:

```bash
gpg --decrypt .env.asc > .env
```

## API Reference

This tool uses the Spotify Web API:

- **Authorization**: [Authorization Code Flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow)
- **Endpoint**: `GET /v1/me/playlists`
- **Scopes**: `playlist-read-private playlist-read-collaborative`

## Troubleshooting

### Redirect URI Error

If you get a redirect URI mismatch error:
- Ensure `http://127.0.0.1:8888/callback` is added to your app's Redirect URIs in the Spotify Developer Dashboard
- Note: Use `127.0.0.1` not `localhost` (Spotify requires IP addresses)

### Browser Doesn't Open

If the browser doesn't open automatically:
- Copy the authorization URL from the terminal
- Paste it into your browser manually
- Complete the authorization flow

### SSL Warning

You may see an OpenSSL warning - this is informational and won't affect functionality:
```
NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+
```

## Future Enhancements

Potential features to add:
- Create new playlists
- Modify existing playlists
- Add/remove tracks
- Playlist analysis and recommendations
- Duplicate playlist detection
- Batch playlist operations

## License

This project is for personal use.

## Contributing

This is a personal project, but suggestions are welcome via issues.
