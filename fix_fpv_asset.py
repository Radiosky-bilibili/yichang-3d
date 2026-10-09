import json, os, http.client, urllib.request, urllib.error, sys
tok = os.environ["GITHUB_TOKEN"]
OWNER, REPO, RID = "Radiosky-bilibili", "yichang-3d", 397689875
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

st, rel = api("GET", f"/repos/{OWNER}/{REPO}/releases/{RID}")
old = rel['assets'][0]
print("旧附件: %s  %.1f MB" % (old['name'], old['size']/1e6))

# 先上传新名字的附件（用 release 里已有的那个 blob？不行，需要本地文件）
# 检查本地有没有对应的 31.6 MB 文件
cands = ['/var/minis/workspace/fpv/yichang-3d-fpv.html', '/var/minis/workspace/fpv/app.html']
src = None
for c in cands:
    if os.path.exists(c) and os.path.getsize(c) == old['size']:
        src = c; break
if src:
    print("本地匹配文件:", src)
    size = os.path.getsize(src)
    up = "/repos/%s/%s/releases/%d/assets?name=%s" % (OWNER, REPO, RID, "yichang-3d-FPV.html")
    conn = http.client.HTTPSConnection("uploads.github.com", timeout=1800)
    conn.putrequest("POST", up)
    for k,v in [("Authorization","Bearer "+tok),("User-Agent","minis"),
                ("Content-Type","text/html"),("Content-Length",str(size))]:
        conn.putheader(k,v)
    conn.endheaders()
    with open(src,"rb") as f:
        left = size
        while left:
            c = f.read(1<<20)
            if not c: break
            conn.send(c); left -= len(c)
    r = conn.getresponse(); out = json.loads(r.read().decode() or "{}")
    print("新附件上传:", r.status, out.get("name"), out.get("state"))
    conn.close()
    if r.status in (200,201):
        st2, _ = api("DELETE", f"/repos/{OWNER}/{REPO}/releases/assets/{old['id']}")
        print("删除旧附件:", st2)
else:
    print("⚠ 本地没找到大小匹配的文件，跳过改名")
    print("  候选:", [(c, os.path.getsize(c) if os.path.exists(c) else 'N/A') for c in cands])
