"""Dropbox helper for publishing: upload finished videos and get links Metricool can download.

Reads DROPBOX_APP_KEY, DROPBOX_APP_SECRET and DROPBOX_REFRESH_TOKEN from the environment,
swaps them for a short-lived access token, and never prints any of them.
Paths are inside the app folder (Apps/<app name>/...).

  python3 tools/dropbox_api.py ls [/folder]
  python3 tools/dropbox_api.py upload <local file> </dropbox/path.mp4>
  python3 tools/dropbox_api.py upload-links </dropbox/folder> <name.mp4> [...]   # one-time upload URLs (4 h), JSON
  python3 tools/dropbox_api.py share </dropbox/path.mp4>                         # public direct-download link
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request
import base64

API = "https://api.dropboxapi.com/2/"
CONTENT = "https://content.dropboxapi.com/2/"


def token():
    auth = base64.b64encode(f"{os.environ['DROPBOX_APP_KEY']}:{os.environ['DROPBOX_APP_SECRET']}".encode()).decode()
    body = urllib.parse.urlencode({"grant_type": "refresh_token",
                                   "refresh_token": os.environ["DROPBOX_REFRESH_TOKEN"]}).encode()
    req = urllib.request.Request("https://api.dropbox.com/oauth2/token", body,
                                 {"Authorization": f"Basic {auth}"})
    return json.load(urllib.request.urlopen(req))["access_token"]


def call(tok, endpoint, args, data=None):
    if data is None:
        req = urllib.request.Request(API + endpoint, json.dumps(args).encode(),
                                     {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    else:
        req = urllib.request.Request(CONTENT + endpoint, data,
                                     {"Authorization": f"Bearer {tok}", "Content-Type": "application/octet-stream",
                                      "Dropbox-API-Arg": json.dumps(args)})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode(errors="replace")}


def direct(url):
    # Dropbox share links download the file itself with dl=1
    return url.replace("dl=0", "dl=1") if "dl=0" in url else url + ("&" if "?" in url else "?") + "dl=1"


def share(tok, path):
    r = call(tok, "sharing/create_shared_link_with_settings",
             {"path": path, "settings": {"audience": "public", "access": "viewer"}})
    if "error" in r:
        links = call(tok, "sharing/list_shared_links", {"path": path, "direct_only": True}).get("links", [])
        if not links:
            return r
        r = links[0]
    return {"path": path, "url": direct(r["url"]), "audience": r.get("link_permissions", {}).get(
        "resolved_visibility", {}).get(".tag")}


def main():
    cmd, args = sys.argv[1], sys.argv[2:]
    tok = token()
    if cmd == "ls":
        r = call(tok, "files/list_folder", {"path": args[0] if args else ""})
        out = r if "error" in r else [{"name": e["name"], "path": e["path_display"], "size": e.get("size")}
                                       for e in r["entries"]]
    elif cmd == "upload":
        with open(args[0], "rb") as f:   # single request: fine up to 150 MB
            out = call(tok, "files/upload", {"path": args[1], "mode": "overwrite", "mute": True}, f.read())
    elif cmd == "upload-links":
        out = {}
        for name in args[1:]:
            r = call(tok, "files/get_temporary_upload_link",
                     {"commit_info": {"path": f"{args[0].rstrip('/')}/{name}", "mode": "overwrite", "mute": True},
                      "duration": 14400})
            out[name] = r.get("link", r)
    elif cmd == "share":
        out = [share(tok, p) for p in args]
    else:
        sys.exit(__doc__)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
