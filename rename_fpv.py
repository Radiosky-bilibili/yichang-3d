import json, os, urllib.request, urllib.error, sys
tok = os.environ["GITHUB_TOKEN"]
OWNER, REPO = "Radiosky-bilibili", "yichang-3d"
hdr = {"Authorization":"Bearer "+tok, "Accept":"application/vnd.github+json",
       "User-Agent":"minis", "Content-Type":"application/json"}
def api(m, p, pl=None):
    d = json.dumps(pl).encode() if pl is not None else None
    r = urllib.request.Request("https://api.github.com"+p, data=d, headers=hdr, method=m)
    try:
        with urllib.request.urlopen(r, timeout=90) as x:
            b = x.read(); return x.status, json.loads(b.decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")

NEW_TAG = "FPV"
NAME = "FPV river flight — a standalone cinematic camera for the whole Yangtze"

BODY = """**The FPV river flight, split out as its own build.** Not a preview of anything — it is a
separate, self-contained version of the map with one feature the main line does not have:
a cinematic camera that flies the entire river.

Download `yichang-3d-FPV.html` — **31.6 MB**, one self-contained file, fully offline once saved.

> **Why this exists as a separate release.** The main line (see [v1.2](https://github.com/Radiosky-bilibili/yichang-3d/releases/tag/v1.2))
> is the map you fly yourself. This build adds a second way to travel it — an automatic,
> rendered-in-real-time flight down the whole valley. Keeping it separate means the main
> line stays lean, and this one can be developed and tested on its own.

---

## What it is

### FPV river flight — 82.4 km, rendered live

Tap the **route button** in the right-hand button stack. The map hands the camera over to a
flight that follows the Yangtze from the reservoir above the Three Gorges Dam all the way down
to Yichang Sanxia Airport.

- Skims about **150 m above the water**, banks into the bends, opens its field of view from
  62° to 80° as it accelerates (cruise ≈ 670 km/h, up to ≈ 820 km/h on the open stretches),
  with a gentle handheld drift.
- **It introduces the landmarks by itself.** Approaching each of the 8 landmark beats, the
  camera climbs several hundred metres and turns to face it, fades in a card with name / kind /
  elevation / distance off-route, and locks a reticle onto the target — the reticle becomes an
  edge arrow when the landmark leaves the frame.
- **Chase-cam HUD**: speed, altitude, height above ground, heading, a whole-route progress bar
  with landmark ticks, and the distance to the next landmark.
- **Bottom bar**: speed (0.7× / 1× / 1.4×), landmark tracking on/off, HUD on/off,
  **previous / next landmark** so you can skip the long stretches, and exit.

### Notes

- **It is rendering, not a video.** There is no video data anywhere in the file: the whole
  feature is roughly 40 KB of JavaScript driving this map's own renderer, frame by frame.
- The route is the Yangtze centreline traced by hand over the imagery and then snapped to the
  DEM valley floor (82.4 km, 688 points, re-parameterised by arc length). The camera samples
  the terrain around every point to keep a safe clearance.
- The HUD is a **DOM canvas layer** rather than a WebGL texture: ~1.4 ms per frame instead of
  ~57 ms.

---

## Known limitations

- **This build is based on the older map code.** It does not have the volumetric clouds, the
  idle auto-tour, the six high-detail imagery patches or the altitude haze that the main line
  gained later.
- Interactive 3D requires **WebGL 2**; older devices may struggle.
- The imagery is **Esri World Imagery — not open data**. See the licensing section of the
  README before redistributing.

---

## How to use it

1. Download the HTML above — that one file is the entire program.
2. Open it: **iPhone / iPad** save to *Files* and tap it; **desktop** double-click.
   Airplane mode is fine, the file never talks to the network.
3. **Fly it:** the route button in the right-hand stack. `◀ ▶` / `← →` jump between landmarks,
   `Esc` leaves.

## Requirements

Any browser with WebGL 2 — Safari 15+, Chrome, Edge, Firefox.

## Credits, data and disclaimer

AI-generated: **DeepSeekHardness** together with **MINIS** and **Doubao**.
Satellite imagery © Esri, Maxar, Earthstar Geographics and the GIS User Community —
**not open data, no rights granted by this project**. Elevation from AWS Open Data
*Terrain Tiles* (Mapzen); see the README for the full attribution list.
Positions are on the GCJ-02 datum, a few hundred metres off WGS-84.
Provided as is — **not for navigation or any safety-critical use**.
"""

# 找到 FPV 那个 release（id 397689875）
st, rel = api("GET", f"/repos/{OWNER}/{REPO}/releases/397689875")
if st != 200:
    sys.exit("取 release 失败 %s" % st)
print("当前: tag=%s  name=%s" % (rel['tag_name'], rel['name']))
print("附件:", [(a['name'], a['size']) for a in rel.get('assets', [])])

# 改 tag + name + 说明（保持 prerelease=True，因为它是独立分支不是"正式主线"）
st, r = api("PATCH", f"/repos/{OWNER}/{REPO}/releases/397689875", {
    "tag_name": NEW_TAG, "name": NAME, "body": BODY,
    "prerelease": True, "draft": False})
print()
print("改名结果:", st, "| tag =", r.get('tag_name'), "| prerelease =", r.get('prerelease'))
print("页面:", r.get('html_url'))
