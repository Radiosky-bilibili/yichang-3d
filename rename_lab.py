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

# 计划：id → 新 tag / 新名
PLAN = {
  407914535: ("lab-detail-patches", "lab · detail patches — six high-resolution imagery insets"),
  407940818: ("lab-preview-haze",   "lab · preview haze — a light atmospheric layer for the map view"),
  397689875: ("lab-river-flight",   "lab · river flight — an automatic cinematic camera down the Yangtze"),
}
for rid, (newtag, newname) in PLAN.items():
    st, rel = api("GET", f"/repos/{OWNER}/{REPO}/releases/{rid}")
    if st != 200:
        print("  ✗ id=%d 取不到 (%s)" % (rid, st)); continue
    old = rel['tag_name']
    st2, r2 = api("PATCH", f"/repos/{OWNER}/{REPO}/releases/{rid}",
                  {"tag_name": newtag, "name": newname})
    print("  %-14s → %-22s %s" % (old, newtag, "✓" if st2==200 else "✗ %d" % st2))

# 删掉那个多余的草稿（beta2 的旧版）
print()
st, rels = api("GET", f"/repos/{OWNER}/{REPO}/releases")
for r in rels:
    if r['draft'] and r['tag_name'] == 'v1.3-beta2':
        st2, _ = api("DELETE", f"/repos/{OWNER}/{REPO}/releases/{r['id']}")
        print("  删除重复草稿 v1.3-beta2: %s" % st2)
        st3, _ = api("DELETE", f"/repos/{OWNER}/{REPO}/git/refs/tags/v1.3-beta2")
        print("  删除其 tag: %s" % st3)
