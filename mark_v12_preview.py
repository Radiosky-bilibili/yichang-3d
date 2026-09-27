#!/usr/bin/env python3
"""Mark the yichang-3d v1.2 release as a preview (prerelease) and add a warning banner.

Idempotent: re-running only re-applies the banner if it is missing.
Usage: python3 mark_v12_preview.py [--check]
"""
import json
import os
import sys
import urllib.request
import urllib.error

OWNER, REPO, TAG = "Radiosky-bilibili", "yichang-3d", "v1.2"
TOKEN = os.environ["GITHUB_TOKEN"]
NAME = "v1.2 (preview) — FPV river flight (real-time camera, for testing)"

BANNER = """> ### ⚠️ Preview build — please treat this as a test
>
> This release is a **preview**. It exists so the new **FPV river flight** can be tried and
> commented on: it has **not** been through proper testing (one phone, one browser, a handful of
> flights). Expect rough edges — landmark framing, the pace of the flight, camera moves and the
> on-screen interface are all still being tuned.
>
> **The last stable build is [v1.1](https://github.com/Radiosky-bilibili/yichang-3d/releases/tag/v1.1)**
> (desktop right-click drag panning fix), which is the same map without the FPV flight.
>
> Bug reports — and notes like “this landmark is framed badly” or “this section is too slow” —
> are exactly what this build is for. Thanks for trying it.

"""


def api(path, method="GET", payload=None):
    req = urllib.request.Request(
        "https://api.github.com" + path, method=method,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={"Authorization": "token " + TOKEN, "Accept": "application/vnd.github+json",
                 "User-Agent": "yichang3d-release"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def main():
    st, rel = api("/repos/%s/%s/releases/tags/%s" % (OWNER, REPO, TAG))
    if st != 200:
        print("release not found:", st)
        sys.exit(1)
    body = rel.get("body") or ""
    if BANNER.strip() not in body:
        body = BANNER + body
    payload = {"prerelease": True, "name": NAME, "body": body}
    if "--check" in sys.argv:
        print(json.dumps({"tag": rel["tag_name"], "name": rel["name"],
                          "prerelease": rel["prerelease"],
                          "has_banner": BANNER.strip() in (rel.get("body") or "")}, indent=1))
        return
    st, out = api("/repos/%s/%s/releases/%d" % (OWNER, REPO, rel["id"]), "PATCH", payload)
    print("PATCH ->", st, "| prerelease:", out.get("prerelease"), "| name:", out.get("name"))
    st, all_rel = api("/repos/%s/%s/releases" % (OWNER, REPO))
    for r in all_rel:
        print("  %-6s prerelease=%-5s %s" % (r["tag_name"], r["prerelease"], (r["name"] or "")[:56]))
    print("  latest (stable) =", next((r["tag_name"] for r in all_rel
                                       if not r["draft"] and not r["prerelease"]), "-"))


if __name__ == "__main__":
    main()
