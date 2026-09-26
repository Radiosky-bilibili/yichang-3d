#!/usr/bin/env python3
"""Fill in the GitHub repo description + topics for Radiosky-bilibili/yichang-3d.

Reads the token from $GITHUB_TOKEN (never printed). Usage:
    GITHUB_TOKEN=... python3 setup_repo_meta.py            # description + topics
    GITHUB_TOKEN=... python3 setup_repo_meta.py --check    # only show current state
"""
import json
import os
import sys
import urllib.request
import urllib.error

REPO = "Radiosky-bilibili/yichang-3d"
API = "https://api.github.com/repos/" + REPO

DESCRIPTION = (
    "A single-file, offline 3D map of the Three Gorges around Yichang (Hubei, China) - "
    "63 x 46 km of real satellite imagery and elevation data in one 31 MB HTML file, "
    "with a freely flyable paper plane. Built by AI; not for navigation."
)

TOPICS = [
    "threejs", "webgl", "webgl2", "glsl", "shader", "terrain", "dem",
    "satellite-imagery", "3d-map", "interactive-map", "yichang", "three-gorges",
    "hubei", "china", "single-file", "offline", "paper-plane", "ai-generated",
]


def call(url, method="GET", payload=None, token=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "minis-helper")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode()
            return r.status, (json.loads(body) if body.strip() else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]


def main():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    check_only = "--check" in sys.argv

    st, cur = call(API, token=token or None)
    if st != 200:
        print("读取仓库失败:", st, cur)
        return 1
    print("当前 description:", repr(cur.get("description")))
    print("当前 topics:", cur.get("topics"))
    if check_only:
        return 0

    if not token:
        print("\nGITHUB_TOKEN 未设置 —— 只查看，未做任何修改。")
        return 1

    st, res = call(API, method="PATCH", payload={"description": DESCRIPTION}, token=token)
    print("\n[PATCH description]", st, "->", res.get("description") if isinstance(res, dict) else res)
    if st != 200:
        print("  提示：fine-grained token 需要 Administration: Read and write 权限；经典 token 需要 repo 权限")

    st2, res2 = call(API + "/topics", method="PUT",
                     payload={"names": TOPICS}, token=token)
    print("[PUT topics]", st2, "->", res2.get("names") if isinstance(res2, dict) else res2)

    st3, fin = call(API, token=token)
    print("\n== 最终状态 ==")
    print("description:", fin.get("description"))
    print("topics:", fin.get("topics"))
    print("url:", fin.get("html_url"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
