"""Upload files to the AntonRoggo Publisher Dropbox app folder and print a temporary link for each.

  python3 tools/dropbox_upload.py <dropbox_folder> <file> [<file> ...]

Uses DROPBOX_APP_KEY / DROPBOX_APP_SECRET / DROPBOX_REFRESH_TOKEN from the environment.
Paths are inside the app folder (e.g. "/Ready to Post"). Prints "<name>\t<temporary link>" per file
(links last 4 hours; Metricool copies the video when the post is created).
"""
import json, os, sys, urllib.request, urllib.parse, base64

def token():
    data = urllib.parse.urlencode({"grant_type": "refresh_token",
                                   "refresh_token": os.environ["DROPBOX_REFRESH_TOKEN"]}).encode()
    req = urllib.request.Request("https://api.dropbox.com/oauth2/token", data=data)
    auth = base64.b64encode(f'{os.environ["DROPBOX_APP_KEY"]}:{os.environ["DROPBOX_APP_SECRET"]}'.encode()).decode()
    req.add_header("Authorization", "Basic " + auth)
    return json.load(urllib.request.urlopen(req))["access_token"]

def call(tok, url, body=None, data=None, arg=None):
    req = urllib.request.Request(url, data=data if data is not None else json.dumps(body).encode())
    req.add_header("Authorization", "Bearer " + tok)
    if arg is not None:
        req.add_header("Dropbox-API-Arg", json.dumps(arg))
        req.add_header("Content-Type", "application/octet-stream")
    else:
        req.add_header("Content-Type", "application/json")
    return json.load(urllib.request.urlopen(req))

def upload(tok, path, local):
    size, chunk = os.path.getsize(local), 100 * 1024 * 1024
    with open(local, "rb") as f:
        if size <= chunk:
            return call(tok, "https://content.dropboxapi.com/2/files/upload", data=f.read(),
                        arg={"path": path, "mode": "overwrite", "mute": True})
        s = call(tok, "https://content.dropboxapi.com/2/files/upload_session/start", data=f.read(chunk), arg={})
        off = chunk
        while size - off > chunk:
            call(tok, "https://content.dropboxapi.com/2/files/upload_session/append_v2", data=f.read(chunk),
                 arg={"cursor": {"session_id": s["session_id"], "offset": off}})
            off += chunk
        return call(tok, "https://content.dropboxapi.com/2/files/upload_session/finish", data=f.read(),
                    arg={"cursor": {"session_id": s["session_id"], "offset": off},
                         "commit": {"path": path, "mode": "overwrite", "mute": True}})

if __name__ == "__main__":
    folder, files = sys.argv[1].rstrip("/"), sys.argv[2:]
    tok = token()
    for local in files:
        meta = upload(tok, f"{folder}/{os.path.basename(local)}", local)
        link = call(tok, "https://api.dropboxapi.com/2/files/get_temporary_link", {"path": meta["path_lower"]})["link"]
        print(f"{os.path.basename(local)}\t{link}")
