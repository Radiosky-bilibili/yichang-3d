<div align="center">
  <img src="./figures/logo.png" width="88%" alt="宜昌 3D 地图 · 3D Yichang" />
</div>

<div align="center">
  <b>English</b> &nbsp;·&nbsp; <a href="./README.zh-CN.md">中文</a>
</div>
<br>

<div align="center" style="line-height: 1.9;">
  <!-- 试玩入口 -->
  <a href="https://b23.tv/aunUQsI"><img alt="哔哩哔哩 Toy"
    src="https://img.shields.io/badge/%F0%9F%8E%AE%20Bilibili%20Toy-立刻试玩(国内)-fb7299?color=fb7299&logoColor=white"/></a>
  <a href="https://radiosky-bilibili.github.io/yichang-3d/"><img alt="Live Demo"
    src="https://img.shields.io/badge/%E2%96%B6%20Live%20Demo-GitHub%20Pages-2ea44f?color=2ea44f&logoColor=white"/></a>
  <br>
  <!-- 技术栈 -->
  <a href="https://threejs.org/"><img alt="three.js"
    src="https://img.shields.io/badge/three.js-r146-black?logo=threedotjs&logoColor=white"/></a>
  <img alt="WebGL 2" src="https://img.shields.io/badge/WebGL-2-orange?logo=webgl&logoColor=white"/>
  <img alt="Single file" src="https://img.shields.io/badge/single%20file-32.5%20MB-blue"/>
  <img alt="Offline" src="https://img.shields.io/badge/offline-yes-success"/>
  <br>
  <!-- 许可与规模 -->
  <a href="./LICENSE"><img alt="License: MIT"
    src="https://img.shields.io/badge/License-MIT-f5de53?color=f5de53"/></a>
  <img alt="Made with AI" src="https://img.shields.io/badge/made%20with-AI-9b59b6"/>
  <img alt="Coverage" src="https://img.shields.io/badge/coverage-63%20%C3%97%2046%20km-informational"/>
</div>

<br>

> ### ⚠️ Read this before you redistribute the file
>
> **The satellite imagery embedded in this project belongs to Esri and its partners — it is not open data, and this project cannot pass on any rights to it.**
>
> The imagery is baked into `index.html` as base64, so **downloading that file gives you a copy of Esri's imagery**. For a personal, offline, non-commercial look, that is the situation this project was built for. **If you want to redistribute, republish, mirror, package, sell or build on it, you must obtain your own licence from Esri first — or replace the imagery with open data.** See [Copyright, attribution and licensing](#-copyright-attribution-and-licensing) for the details and for two ways out.
>
> The **code** is MIT and yours to use freely. It is the **imagery** that carries the restriction.

**A single-file, offline 3D map of the Yangtze valley around Yichang (Hubei, China), running entirely in the browser.**

Everything lives inside one **32.5 MB `.html` file**: the renderer, the shaders, the interface, the satellite imagery and the elevation model. There is no server, no build step, no package manager and — once downloaded — no network access at all. Open the file and start flying.

**Play it now — no download needed:**

- **In China / on Bilibili:** [**宜昌 3D 地图 · 纸飞机飞行 · 真实体积云**](https://b23.tv/aunUQsI) — running as a Bilibili Toy (Beta), works inside the Bilibili app. Best option on a phone.
- **Anywhere else:** <https://radiosky-bilibili.github.io/yichang-3d/> — the same map on GitHub Pages.

**Download a copy:** [v1.2 — index.html, 32.5 MB](https://github.com/Radiosky-bilibili/yichang-3d/releases/download/v1.2/yichang-3d-v1.2.html) — the current stable build, fully offline once saved
&nbsp;·&nbsp; [**FPV river flight**](https://github.com/Radiosky-bilibili/yichang-3d/releases/tag/FPV), 31.6 MB — a standalone build for the automatic river camera

*The Bilibili Toy build and the GitHub Pages build are the same map, packaged differently. The interactive 3D requires WebGL 2, so an older device may struggle.*

The map covers **63.1 × 46.3 km** of real terrain, from the Three Gorges Dam in the west to Yichang Sanxia Airport in the east, with the Yangtze cutting through the middle.

![Yichang 3D map — satellite view of the Three Gorges](desktop-overview.jpg)

---

## Table of Contents

1. [Features](#-features)
2. [Gallery](#-gallery)
3. [Quick start](#-quick-start)
4. [Controls](#-controls)
5. [Coverage and data sources](#-coverage-and-data-sources)
6. [Under the hood](#-under-the-hood)
7. [About this project](#-about-this-project)
8. [Copyright, attribution and licensing](#-copyright-attribution-and-licensing)
9. [Known limitations](#-known-limitations)
10. [Repository layout](#-repository-layout)
11. [Credits & thanks](#-credits--thanks)
12. [How it was made — the making-of repository](#-how-it-was-made--the-making-of-repository)

---

## Features

### 1. Look at the map and get to know the landmarks

- **Three view modes** — *Satellite* (real Esri imagery), *Elevation* (hypsometric colour ramp), *Shaded relief* (hillshaded greyscale).
- **20 landmarks** with names and elevations, plus the two river labels. Tap a marker to open a card with a short description; the labels are hidden automatically when terrain occludes them and shoved apart so they never overlap.
- **Quick-jump bar** at the bottom — tap *Three Gorges Dam*, *Gezhouba Dam*, *Yichang downtown* or *Yichang Sanxia Airport* to fly the camera there.
- **Guided tour / auto-rotate / top view** buttons: let the camera drift around the map by itself, or cycle landmark to landmark every few seconds.
- **A compass, a live scale bar, an FPS readout**, graticule (lat/lon grid) and optional contour lines.

### 2. Fly a virtual paper plane

- A folded paper plane, built as geometry (wide flat wing on top, narrow V tail below).
- Drag anywhere on the screen to steer — left/right to bank and turn, up/down to pitch. Two throttle buttons on the right.
- Flight HUD: **speed (km/h), altitude (m), heading (°), height above ground** and a throttle bar.
- The world wakes up when you fly: a soft shadow under the plane, volumetric cloud puffs you can climb over and fly through, a low-altitude haze layer that fades as you gain height, and mountain mist that sits thick in the valleys and thin on the ridges.

### 3. Plenty of things to tune

The settings panel exposes the whole look of the map:

| Setting | Range | Default |
| --- | --- | --- |
| Terrain exaggeration | 0 – 3× | 1.5× |
| Sun azimuth | 0 – 360° | 135° |
| Sun elevation | 5 – 85° | 42° |
| Fog / haze density | 0 – 100 | 18 |
| Label size | 70 – 150 % | 100 % |
| Terrain mesh resolution | 512 / **768** / 1024 vertices per side | 768 |

Six independent toggles: **landmark labels, graticule, contour lines, relief shading, mountain mist, ground shadow.** Moving the sun slider relights the entire terrain, the sky and the fog colour in real time — no rebuild, no reload.

### 4. Fly the whole river — FPV auto-flight *(separate build)*

A cinematic flight camera that follows the Yangtze for **82.4 km**, from the reservoir above the Three Gorges Dam all the way down to Yichang Sanxia Airport.

- **Tap the route button** at the top of the right-hand button stack (or press `F`) and the map hands the camera over to the flight and clears its own interface out of the way.
- The camera hugs the valley: it skims roughly **150 m above the water**, banks into the bends, opens its field of view as it accelerates (cruise ≈ 670 km/h, up to ≈ 820 km/h on the open stretches) and drifts gently like a handheld rig.
- **It introduces the landmarks by itself.** Along the way it climbs several hundred metres and turns to face each landmark — the Three Gorges Dam, Xiling Gorge, Sanxia Renjia, Sanyoudong, Gezhouba Dam, Yichang downtown, Yichang East Station, Yichang Sanxia Airport — a card fades in with the name, elevation and distance off-route, and a reticle locks onto the target; it becomes an edge arrow when the landmark slides out of frame. Landmarks that sit well off the river are picked up early and shot with a longer lens.
- **Chase-cam HUD**: speed, altitude, height above ground, heading, a whole-route progress bar with landmark ticks and the distance to the next landmark.
- **Bottom bar**: speed (0.7× / 1× / 1.4×), landmark tracking on/off, HUD on/off, **previous / next landmark (◀ ▶, or `←` `→`)** so you never have to sit through the long stretches, and exit.
- **Idle auto-cruise**: leave the map alone for two minutes and the built-in landmark tour starts by itself — 20 landmarks, one every 4.2 s, then it stops and gives the map back. Any touch takes over immediately. You can switch it off or change the delay under *Display settings → Idle auto-cruise*.
- It is **real-time rendering, not a video**: the file contains no video data at all, just this map's own renderer being flown by a script. The whole feature adds about 40 KB to the 31 MB page.

---

## Gallery

Desktop and mobile, side by side — one pair per scene.

| Desktop | Mobile |
| :---: | :---: |
| <img src="desktop-overview.jpg" width="620" alt="Desktop — map overview with the bottom quick-jump bar"><br>*Map overview* | <img src="screenshot-overview.jpg" width="130" alt="Mobile — map overview"><br>*Map overview* |
| <img src="desktop-landmark.jpg" width="620" alt="Desktop — landmark card with elevation, coordinates and description"><br>*Landmark card* | <img src="screenshot-landmark.jpg" width="130" alt="Mobile — landmark card"><br>*Landmark card* |
| <img src="desktop-flight.jpg" width="620" alt="Desktop — flying the paper plane, HUD showing speed, altitude and heading"><br>*Flying the paper plane* | <img src="screenshot-flight.jpg" width="130" alt="Mobile — flying the paper plane"><br>*Flying the paper plane* |
| <img src="desktop-settings.jpg" width="620" alt="Desktop — the settings panel"><br>*Settings panel* | <img src="screenshot-settings.jpg" width="130" alt="Mobile — the settings panel"><br>*Settings panel* |
| <img src="desktop-fpv.jpg" width="620" alt="Desktop — the FPV river flight over Yichang downtown: landmark card, locked-on reticle and chase-cam HUD"><br>*FPV river flight* | <img src="screenshot-fpv.jpg" width="130" alt="Mobile — the FPV river flight, portrait layout"><br>*FPV river flight* |

---

## Quick start

**Option 1 — open it right now, nothing to install**

<https://radiosky-bilibili.github.io/yichang-3d/>

Hosted with GitHub Pages straight from the `main` branch. Give it a few seconds on the first
visit: the page carries its own 31 MB of imagery and elevation data.

**Option 2 — download it and keep it offline**

1. Grab `index.html` (31.6 MB — one file, and it is the entire program) from the
   [v1.2 **preview** release](https://github.com/Radiosky-bilibili/yichang-3d/releases/tag/v1.2), which adds the FPV
   river flight and is still being tested; the [stable v1.1](https://github.com/Radiosky-bilibili/yichang-3d/releases/tag/v1.1)
   is the same map without it. Everything is listed under [all releases](../../releases).
2. Open it:
   - **iPhone / iPad** — save it to *Files* and tap it.
   - **Desktop** — just double-click it.
3. That's it. Airplane mode is fine — the file never talks to the network.

**Requirements:** any browser with WebGL 2 (Safari 15+, Chrome, Edge, Firefox). It runs happily on a phone; "Fine" terrain mode looks best and costs the most.

---

## Controls

| Action | Gesture / button |
| --- | --- |
| Orbit the map | one-finger drag (or left-drag) |
| Zoom | pinch (or mouse wheel) |
| Pan | two-finger drag (or right-drag) |
| Fly the plane | drag while in flight mode — horizontal = turn, vertical = pitch |
| Throttle | ▲ / ▼ buttons (hold to change continuously) |
| Leave flight mode | *Exit flight* button; the camera returns to the plane's position |
| Start / leave the FPV river flight *(FPV build only)* | route button at the top of the right-hand stack, or `F` / `Esc` |
| Next / previous landmark in flight *(FPV build only)* | ◀ / ▶ in the bottom bar, or `←` `→` |

---

## Coverage and data sources

| | |
| --- | --- |
| Extent | 110.918° – 111.577° E, 30.487° – 30.902° N (63.1 × 46.3 km) |
| Elevation range | −153 m … 1492 m |
| Elevation model | AWS Open Data *Terrain Tiles* (Terrarium PNG, z12, ≈ 33 m per sample), 1024 × 1024 grid |
| Imagery ⚠️ | Esri World Imagery: global z14 (8.2 m/px) + **six high-detail patches** (city core 2.05, Three Gorges Dam 1.72, Zigui / airport / two railway stations 2.05 m/px). **Not open data — see the notice at the top.** | Datum | GCJ-02 aligned (see the note under *Copyright*) |
| Landmarks | 20 points of interest + 2 river labels |

---

## Under the hood

- **three.js r146**, inlined into the file (MIT licensed), WebGL 2.
- **Height is applied on the GPU.** The terrain mesh stores only X/Z plus a packed slope value; the vertical shader samples the Terrarium-encoded elevation texture and displaces every vertex. Changing exaggeration is a single uniform write, so it is instant.
- **Hypsometric colour ramp** generated as a 256 × 1 texture, blended in the fragment shader for the elevation view.
- **Level of detail in the shader:** contour line width and the strength of the urban detail layer adapt to the metres-per-pixel the camera is currently seeing.
- **Label system in HTML**, not in GL: screen-space placement, occlusion culling by ray-marching against the elevation field, greedy anti-overlap (big landmarks win), clamped inside the viewport, and kept clear of the top bar and the bottom quick-jump bar.
- **A small debug API** is left in on purpose: `window.frame()` forces a single render (useful when the tab is in the background and `requestAnimationFrame` is throttled) and `window.noAnim()` kills CSS transitions for clean screenshots.

- **The FPV flight is a scripted camera, not a video.** The route is the Yangtze centreline traced by hand over the imagery and then snapped to the DEM valley floor (82.4 km, 688 points) and re-parameterised by arc length. Every frame the script takes a point on that curve, samples the terrain around it for a safe clearance, blends the look-at point from "ahead along the river" towards the next landmark, and hands the camera to the map's normal `requestAnimationFrame` loop — the renderer, the terrain and the imagery are all the map's own.
- **The HUD is a DOM canvas layer**, not part of the WebGL scene: drawing 1920 × 1080 of interface into a texture cost ~57 ms per frame, the DOM layer costs ~1.4 ms and the browser composites it for free. It re-lays itself out for portrait or landscape, and the bottom of the interface is pushed up by the measured height of the control bar.

---

## About this project

This is an **AI-generated project**. It was created by **DeepSeekHardness**, working together with two AI collaborators: **MINIS** and **Doubao**. The WebGL renderer, the shaders, the interface, the landmark data and this README were all produced by AI.

So please keep expectations realistic:

- It is a **demo and a toy**, not a product. Expect rough edges, unfinished corners and the occasional visual glitch.
- Parts of it were assembled by an automated export step, and such steps can introduce artefacts. Two of them have already been patched in this version: a shader uniform declared with the wrong type, and a material that double-declared a vertex attribute.
- It has been tested on one phone, in one browser. Your mileage may vary.
- Numbers on screen (elevations, distances) come from coarse public data and are for atmosphere, not for measurement.

---

## Copyright, attribution and licensing

### This project

The app code in this repository (the HTML, the JavaScript, the GLSL, the UI design, the landmark write-ups and this README) was **generated by AI** at the direction of *DeepSeekHardness* together with *MINIS* and *Doubao*.

**Licence: [MIT](LICENSE).** You are free to use, copy, modify, merge, publish, distribute, sublicense and sell this project's own code. Keep the copyright notice and the permission notice with any substantial portion you redistribute — that is the only condition.

A note on authorship, stated plainly: in some jurisdictions — the United States among them — purely AI-generated output may not be eligible for copyright protection, because copyright requires human authorship; other jurisdictions treat AI-assisted works with human creative direction as protectable. This project does not try to resolve that question. The code, the orchestration, the testing, the corrections and the data integration were carried out by the people named below, who take the position that the work as a whole is theirs to license, and who license it to you under MIT terms. Where a jurisdiction declines to recognise copyright in some part of it, that part is simply free to use.

The MIT licence covers **this project's own code only**. The third-party components and data below keep their own terms, and those terms still bind you.

### Third-party code

| Component | Terms | What that means for you |
| --- | --- | --- |
| three.js (inlined, r146) | MIT License, © 2010–2023 three.js authors | The inlined bundle already carries its SPDX `MIT` header — keep it. If you strip the header, add the MIT notice and copyright line back. |
| Everything else | written for this project | covered by the permissive statement above |

### Third-party data — imagery and elevation

- **Satellite imagery: Esri World Imagery.** The tiles are © Esri, Maxar, Earthstar Geographics and the GIS User Community, delivered by Esri's ArcGIS World Imagery service. **This project does not own the imagery and grants you no rights to it.**

  **Please read this before you redistribute a build.** The imagery is baked into `index.html` as base64, which means *this repository redistributes Esri's imagery*. That is fine for a static non-commercial demo of the kind this is, but it is **not** a right this project can pass on to you. Concretely:

  | What you want to do | What it means |
  | --- | --- |
  | Look at it, run it locally, learn from the code | Fine. |
  | Fork the repo and keep the imagery | You are now redistributing Esri imagery yourself. Get your own licence, or swap the imagery out (below). |
  | Use it commercially, or in a product | Get a licence from Esri. |
  | Treat this repo as a source of imagery | Please don't. |

  **Two clean ways out, if you need one:**

  1. **Swap in open imagery.** The recommended replacement is **Sentinel-2** (ESA / Copernicus, CC BY-SA 3.0 IGO) — free to use, modify and redistribute with attribution. Its resolution is 10 m/px against the 8.2 m/px used here, so it costs about 20% of the detail, not a lot. The build scripts for downloading, mosaicking and re-registering imagery are in [yichang3d-toolkit](https://github.com/Radiosky-bilibili/yichang3d-toolkit); the same pipeline was used to produce the base map shipped in that repository.

  2. **Load imagery at runtime** instead of embedding it, and point it at a tile service whose terms you are happy with. This is a code change, not a data change: the terrain shader just needs a texture, and it does not care where the texture came from. You lose the offline single-file property.

  The elevation data has none of these problems — see below.
- **Elevation: AWS Open Data "Terrain Tiles" — Terrarium PNG format, by Mapzen (a Linux Foundation project).** Served from `s3://elevation-tiles-prod`. The tiles are assembled from a patchwork of national and global DEMs, and **attribution is required for several of them**. If you redistribute this project or a build of it, carry this list with it:

  ```
  * Mapzen
  * ArcticDEM terrain data DEM(s) were created from DigitalGlobe, Inc., imagery and
    funded under National Science Foundation awards 1043681, 1559691, and 1542736;
  * Australia terrain data (c) Commonwealth of Australia (Geoscience Australia) 2017;
  * Austria terrain data (c) offene Daten Oesterreichs - Digitales Gelaendemodell (DGM) Oesterreich;
  * Canada terrain data contains information licensed under the Open Government
    Licence - Canada;
  * Europe terrain data produced using Copernicus data and information funded by the
    European Union - EU-DEM layers;
  * Global ETOPO1 terrain data U.S. National Oceanic and Atmospheric Administration;
  * Mexico terrain data source: INEGI, Continental relief, 2016;
  * New Zealand terrain data Copyright 2011 Crown copyright (c) Land Information New
    Zealand and the New Zealand Government (All rights reserved);
  * Norway terrain data (c) Kartverket;
  * United Kingdom terrain data (c) Environment Agency copyright and/or database right
    2015. All rights reserved;
  * United States 3DEP (formerly NED) and global GMTED2010 and SRTM terrain data
    courtesy of the U.S. Geological Survey.
  ```

  The authoritative list lives at [tilezen/joerd docs/attribution.md](https://github.com/tilezen/joerd/blob/master/docs/attribution.md). This project's area of interest is in China, so the DEMs that actually contribute here are the global ones — **SRTM / GMTED2010 / 3DEP (USGS)** and **ETOPO1 (NOAA)** — but the full list is reproduced above because the tile set is global and a reader cannot tell which tiles went into which pixel.

  Cite it as: *Terrain Tiles was accessed from https://registry.opendata.aws/terrain-tiles.*
- **Landmark names, coordinates and descriptions** were compiled from public sources (encyclopaedias, municipal and tourism pages) and are included for information and orientation only. No ownership is claimed over them and no accuracy is guaranteed.

### Non-affiliation and trademarks

This is an independent hobby project. It is **not** affiliated with, endorsed by, sponsored by or in any way connected to Esri, Maxar, Amazon Web Services, Mapzen, the three.js project, the municipal government of Yichang, the Three Gorges Corporation, or the makers of MINIS or Doubao. All product names, brands and logos are the property of their respective owners and are used here only to identify what the project is built with. Landmark names are used descriptively.

### Coordinates: this map is deliberately offset

The map is drawn on the **GCJ-02** datum, the obfuscated coordinate system required for public maps in mainland China. Positions therefore differ from **WGS-84** (raw GPS) by a few hundred metres — around 500 m in this area. On purpose, and not a bug.

### No warranty, and not for navigation

The project is provided **"as is", without warranty of any kind**, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and non-infringement. The author accepts no liability for any damage or loss arising from its use. Specifically:

- Do **not** use it for navigation, driving, hiking, boating or aviation.
- Do **not** use it for surveying, engineering, urban planning, hazard assessment or any safety-critical decision.
- Elevation is a coarse global DEM (≈ 33 m sampling) and is drawn with a vertical exaggeration of 1.5× by default, so heights and slopes are stylised, not measured.

---

## Known limitations

- **AI-generated** — expect quirks, and expect the occasional artefact left behind by the automated packaging step.
- **Single 31 MB file**: first load takes a moment on a phone; parsing the inline imagery is the slow part. After that it is instant and fully offline.
- **Imagery and DEM resolution** limit how far you can zoom usefully; the z16 city layer only covers the downtown core.
- **Windows can wander**: landmark descriptions are condensed from public sources and may be out of date, and the imagery is a snapshot of one moment in time.
- **No saved state**: camera position, settings and flight state reset on reload.

---

## Repository layout

```
index.html                    the entire application — one self-contained file
screenshot-overview.jpg       mobile — satellite overview of the map
screenshot-landmark.jpg       mobile — a landmark card
screenshot-flight.jpg         mobile — flying the paper plane
screenshot-settings.jpg       mobile — the settings panel
desktop-overview.jpg          desktop — satellite overview of the map
desktop-landmark.jpg          desktop — a landmark card
desktop-flight.jpg            desktop — flying the paper plane
desktop-fpv.jpg               desktop — the FPV river flight (landmark card + chase-cam HUD)
screenshot-fpv.jpg            mobile — the FPV river flight, portrait
desktop-settings.jpg          desktop — the settings panel
README.md                     this file (English)
README.zh-CN.md               the same document in Chinese
LICENSE                       MIT licence for this project's own code
```

---

## Credits & thanks

**Author & project lead — Radiosky_bilibili.** The idea is his: he picked the subject, set the
scope and gave the direction, and he was the main tester — the shader fixes, the packaging
clean-ups and the whole shape of the app came out of what he spotted while flying the plane
around. Without him keeping at it, there would be no map.

**AI collaborators — DeepSeekHardness, MINIS and Doubao** — wrote the code, the shaders, the
interface and this README, working under that direction.

- **3D engine:** three.js by mrdoob and contributors (MIT).
- **Imagery:** Esri World Imagery — © Esri, Maxar, Earthstar Geographics and the GIS User Community.
- **Elevation:** AWS Open Data Terrain Tiles, originally produced by Mapzen.
- **Place names and landmark facts:** public sources.

## How it was made — the making-of repository

The long version of this project — how the 82 km flight route was made, and the three times the
approach was wrong before it was right — lives in a separate repository:

**<https://github.com/Radiosky-bilibili/yichang3d-toolkit>**

It contains:

- **[MAKING-OF.md](https://github.com/Radiosky-bilibili/yichang3d-toolkit/blob/main/MAKING-OF.md)** —
  a field log rather than a tutorial: automatic river detection failing, going back to
  hand-drawn points, smoothing a route *without* sanding off intent, a 555 m registration trap
  that nearly broke the terrain, and a HUD that got 40× faster by being drawn somewhere else.
  (Also [in English](https://github.com/Radiosky-bilibili/yichang3d-toolkit/blob/main/MAKING-OF.en.md).)
- **The tools**, ready to open: the route-drawing tool, the route-checking tool, the smoothing
  preview.
- **The scripts** in the order they were used: mosaic elevation tiles, register them, smooth a
  route with a leash, render a base map from a DEM, build the app, record frames to video.
- **The data**: the 32 hand-drawn points, the 129 smoothed control points, and the final
  688-point route.

Worth a look if you want to see what the process actually looked like —
including the parts that didn't work.

**Follow the author.** Radiosky posts his projects on Bilibili as **Radiosky_电波天空** — if you
enjoyed this map, following him there is the best way to say thanks:
<https://space.bilibili.com/1274098107>

*If you use this in a school project, a blog post or a demo, a mention of Radiosky_bilibili,
DeepSeekHardness, MINIS and Doubao is appreciated, even though nothing here obliges you to.*
