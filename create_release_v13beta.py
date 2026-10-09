import json, os, http.client, urllib.request, urllib.error, sys
OWNER, REPO = "Radiosky-bilibili", "yichang-3d"
TAG = "v1.3-beta"
NAME = "v1.3 beta — six high-detail patches · new spawn point · altitude haze ⚠️ KNOWN COLOUR BUG"
ASSET = "index_multi2.html"
ASSET_NAME = "yichang-3d-v1.3-beta.html"
tok = os.environ.get("GITHUB_TOKEN","")
if not tok: sys.exit("缺少 GITHUB_TOKEN")
body = open("release_v13beta_notes.md", encoding="utf-8").read()
hdr = {"Authorization":"Bearer "+tok, "Accept":"application/vnd.github+json",
       "User-Agent":"minis-release", "Content-Type":"application/json"}
def api(m, u, pl=None):
    d = json.dumps(pl).encode() if pl is not None else None
    r = urllib.request.Request(u, data=d, headers=hdr, method=m)
    try:
        with urllib.request.urlopen(r, timeout=120) as x:
            b = x.read(); return x.status, json.loads(b.decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")
st, rel = api("GET", f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}")
if st == 200:
    print("release 已存在，复用:", rel["html_url"])
else:
    st, rel = api("POST", f"https://api.github.com/repos/{OWNER}/{REPO}/releases", {
        "tag_name": TAG, "target_commitish": "main", "name": NAME,
        "body": body, "draft": False, "prerelease": True})
    if st not in (200,201): sys.exit("创建失败 %s %s" % (st, str(rel)[:300]))
    print("已创建:", rel["html_url"], "| prerelease =", rel["prerelease"])
size = os.path.getsize(ASSET)
print("上传 %.1f MB ..." % (size/1e6))
up = "/repos/%s/%s/releases/%s/assets?name=%s" % (OWNER, REPO, rel["id"], ASSET_NAME)
conn = http.client.HTTPSConnection("uploads.github.com", timeout=1800)
conn.putrequest("POST", up)
for k,v in [("Authorization","Bearer "+tok),("User-Agent","minis-release"),
            ("Content-Type","text/html"),("Content-Length",str(size))]:
    conn.putheader(k,v)
conn.endheaders()
with open(ASSET,"rb") as f:
    left = size
    while left:
        c = f.read(1<<20)
        if not c: break
        conn.send(c); left -= len(c)
r = conn.getresponse(); out = json.loads(r.read().decode() or "{}")
print("上传:", r.status, out.get("state"), out.get("size"))
conn.close()
st, rel = api("GET", f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}")
for a in rel.get("assets", []):
    print("附件:", a["name"], "%.1f MB" % (a["size"]/1e6), a["state"])
print("prerelease =", rel["prerelease"], "|", rel["html_url"])
