import json, os, http.client, urllib.request, urllib.error, sys
OWNER, REPO, TAG = "Radiosky-bilibili", "yichang-3d", "v1.3-beta2"
NAME = "v1.3 beta 2 — same as beta 1, with a light atmospheric haze in preview"
ASSET, ASSET_NAME = "index_multi2.html", "yichang-3d-v1.3-beta2.html"
tok = os.environ["GITHUB_TOKEN"]
BODY = """> ⚠️ **Beta —— 已知存在画面缺陷，请勿视为稳定版。** 稳定版请看 [v1.2](https://github.com/Radiosky-bilibili/yichang-3d/releases/tag/v1.2)。

下载 `yichang-3d-v1.3-beta2.html` —— **44.3 MB**，单文件，保存后完全离线可用。

---

## 本版相对 beta 1 的变化

**只改了一处：预览模式下加了一层很轻的大气感。**

| 参数 | beta 1 | **beta 2** |
| --- | --- | --- |
| 大气透视 `uAtmo`（预览模式） | 0（完全没有） | **0.10** |
| 雾浓度系数（预览模式） | ×1.0 | ×1.0（不变） |
| 天空霾 `uHaze`（预览模式） | 0 | **0.03** |

对比一下就知道这个量级有多轻：飞行模式下的 `uAtmo` 会随高度涨到 **0.92**（4100 m 时约 0.63）。预览模式只给 **0.10**，目的是让远处有一点空气感，而不是起雾。

**其他一切未动** —— 绿盘子保留、天空配色未改、六块高清补丁保留、出生点保留。

---

## 已知问题

### 1. 新增的高清贴片存在色彩与接缝问题 —— `[未修复]`

五块新增贴片（三峡大坝、秭归县、三峡机场、宜昌东站、宜昌北站）在拉近观看时，色调与周围底图不一致，且可见接缝。

实测各影像源的平均 RGB：

| 影像 | 平均 RGB |
| --- | --- |
| 主底图（Esri z14） | (69, 80, 62) |
| 城区层（z16） | (78, 87, 70) |
| **三峡大坝贴片（z17）** | **(87, 97, 92)** 偏亮偏蓝 |
| **秭归县贴片（z16）** | **(93, 107, 103)** 偏亮偏青 |
| 三峡机场（z16） | (90, 96, 72) |
| 宜昌东站（z16） | (99, 102, 82) |
| 宜昌北站（z16） | (75, 85, 63) |

初步判断与 Esri 在不同缩放层级做的色调处理差异有关；另有迹象表明着色器中用变量索引 `vec4` 数组的部分在移动 GPU 上可能取样错位。两者叠加即为所见现象。**待确认后修复。**

### 2. 其他

- 交互式 3D 需要 **WebGL 2**，较老设备可能吃力。
- 内嵌 **Esri 影像（非开放数据）**，再分发前请阅读许可说明。

---

## 本版包含的功能（与 beta 1 相同）

- **六块高清细节层**：宜昌城区核心（2.05 m/px）、三峡大坝（**1.72 m/px**）、秭归县、三峡机场、宜昌东站、宜昌北站（2.05 m/px）
- **纸飞机出生点**：高度 **4200 m**，正对**葛洲坝**
- **飞行时的大气透视**：离地越高远处越白（300 m→0%，4100 m→63%，6000 m→92%）；开启体积云时自动关闭
- **体积云**：光线步进，六个可调参数（云量／云底高度／云层厚度／浓度／风速／渲染步数）
- **待机自动演示**：60 秒无操作自动巡航切地标
- **设置面板可滚动**（手机端）
- **版权与归属提示**：源码头部与设置面板底部

## 使用方法

1. 下载上面的 HTML —— 这一个文件就是完整程序。
2. 打开：**iPhone / iPad** 存到「文件」里点一下；**电脑**双击。飞行模式也能用。
3. 想看色彩问题：点底部「三峡大坝」快速跳转，然后拉近。

## 环境要求

支持 WebGL 2 的浏览器：Safari 15+、Chrome、Edge、Firefox。

## 署名、数据与免责

AI 生成作品：**DeepSeekHardness** 与 **MINIS**、**Doubao** 共同构建。

- **卫星影像 © Esri, Maxar, Earthstar Geographics 与 GIS User Community —— 非开放数据，本项目不授予任何影像权利。再分发前请自行取得授权，或替换为开放影像。**
- 高程来自 **AWS Open Data *Terrain Tiles*（Mapzen）**；完整署名清单见 README。
- 坐标为 GCJ-02，与 WGS-84 相差数百米。
- 按原样提供，**不得用于导航或任何安全相关用途**。
"""
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
    print("已存在，复用")
else:
    st, rel = api("POST", f"https://api.github.com/repos/{OWNER}/{REPO}/releases", {
        "tag_name": TAG, "target_commitish": "main", "name": NAME,
        "body": BODY, "draft": False, "prerelease": True})
    if st not in (200,201): sys.exit("创建失败 %s %s" % (st, str(rel)[:200]))
    print("已创建:", rel["html_url"])
size = os.path.getsize(ASSET)
print("上传 %.1f MB ..." % (size/1e6))
conn = http.client.HTTPSConnection("uploads.github.com", timeout=1800)
conn.putrequest("POST", "/repos/%s/%s/releases/%s/assets?name=%s" % (OWNER, REPO, rel["id"], ASSET_NAME))
for k,v in [("Authorization","Bearer "+tok),("User-Agent","minis"),
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
a = rel["assets"][0]
print("附件:", a["name"], "%.1f MB" % (a["size"]/1e6), a["state"])
print("prerelease =", rel["prerelease"], "|", rel["html_url"])
