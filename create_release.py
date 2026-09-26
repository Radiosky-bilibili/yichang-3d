#!/usr/bin/env python3
"""Create the v1.0 release for Radiosky-bilibili/yichang-3d and attach index.html.

Token comes from $GITHUB_TOKEN (never printed).
    GITHUB_TOKEN=... python3 create_release.py
"""
import http.client
import json
import os
import sys
import urllib.request
import urllib.error

REPO = "Radiosky-bilibili/yichang-3d"
TAG = "v1.0"
NAME = "3D Yichang v1.0"
ASSET = "/var/minis/workspace/yichang3d-repo/index.html"

BODY = """## 3D Yichang v1.0

A single-file, offline 3D map of the Three Gorges around Yichang (Hubei, China).

**Download `index.html` from the assets below (31.5 MB), then just open it** — any WebGL 2
browser will do (Safari 15+, Chrome, Edge, Firefox). No server, no install: the file makes
zero network requests after downloading, so it works fully offline and in airplane mode.

### What is inside

- 63.1 x 46.3 km of real terrain — the Three Gorges Dam in the west to Yichang Sanxia Airport in the east
- Esri World Imagery (z14 whole extent + z16 over the city core) and an AWS Terrarium elevation model, both inlined as base64
- Three view modes: **satellite / elevation / shaded relief**
- 20 landmarks with short descriptions, a quick-jump bar, guided tour, auto-rotate and top view
- A **flyable paper plane**: drag to steer, ▲▼ throttle, HUD showing speed, altitude, heading and height above ground, plus ground shadow, clouds you can fly through, low-altitude haze and mountain mist
- Live settings: terrain exaggeration, sun azimuth, sun elevation, fog density, label size, mesh resolution (512 / 768 / 1024) and six display toggles

### Build notes for this release

- The river water-surface overlay has been removed — the Yangtze is visible as it appears in the satellite imagery itself.
- Two packaging artefacts present in earlier single-file exports are fixed: a shader uniform declared with the wrong type, and a material that double-declared a vertex attribute.

### Please note

- This is an **AI-generated project**, built by **DeepSeekHardness** together with **MINIS** and **Doubao**. Expect rough edges.
- Satellite imagery (c) Esri, Maxar, Earthstar Geographics and the GIS User Community; elevation from AWS Open Data "Terrain Tiles" (Mapzen). This project grants no rights to that imagery — see the README for details.
- Drawn on the GCJ-02 datum, so positions are ~500 m off from raw GPS. **Not for navigation or surveying.**
"""


def api(url, method="GET", payload=None, token=None, raw=False):
    data = None
    if payload is not None:
        data = payload if raw else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "minis-helper")
    if not raw and payload is not None:
        req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            txt = r.read().decode()
            return r.status, (json.loads(txt) if txt.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]


def main():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("GITHUB_TOKEN 未设置")
        return 1

    st, rel = api("https://api.github.com/repos/%s/releases/tags/%s" % (REPO, TAG), token=token)
    if st == 200:
        print("已存在 tag %s 的 release: %s" % (TAG, rel.get("html_url")))
    else:
        st, rel = api("https://api.github.com/repos/%s/releases" % REPO, method="POST",
                      payload={"tag_name": TAG, "target_commitish": "main",
                               "name": NAME, "body": BODY,
                               "draft": False, "prerelease": False}, token=token)
        print("[POST release]", st, "->", rel.get("html_url") if isinstance(rel, dict) else rel)
        if st != 201:
            return 1
    rid = rel["id"]

    if any(a["name"] == "index.html" for a in rel.get("assets", [])):
        print("index.html 已作为附件存在，跳过上传")
    else:
        size = os.path.getsize(ASSET)
        print("上传 index.html（%.1f MB）…" % (size / 1048576))
        conn = http.client.HTTPSConnection("uploads.github.com", timeout=900)
        with open(ASSET, "rb") as f:
            conn.request("POST", "/repos/%s/releases/%d/assets?name=index.html" % (REPO, rid),
                         body=f,
                         headers={"Authorization": "Bearer " + token,
                                  "Content-Type": "text/html",
                                  "Content-Length": str(size),
                                  "Accept": "application/vnd.github+json",
                                  "User-Agent": "minis-helper"})
            resp = conn.getresponse()
            out = resp.read().decode()
        print("[upload asset]", resp.status)
        try:
            a = json.loads(out)
            print("  name:", a.get("name"), "| size:", a.get("size"),
                  "| state:", a.get("state"))
        except Exception:
            print(" ", out[:300])
        conn.close()

    st, fin = api("https://api.github.com/repos/%s/releases/tags/%s" % (REPO, TAG), token=token)
    print("\n== 最终状态 ==")
    print("release:", fin.get("html_url"))
    print("tag:", fin.get("tag_name"), "| name:", fin.get("name"), "| draft:", fin.get("draft"))
    for a in fin.get("assets", []):
        print("asset:", a["name"], "%.1f MB" % (a["size"] / 1048576), a["state"])
        print("  download:", a["browser_download_url"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
