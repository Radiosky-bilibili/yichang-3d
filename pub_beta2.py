import json, os, http.client, urllib.request, urllib.error, sys
OWNER, REPO, TAG = "Radiosky-bilibili", "yichang-3d", "v1.3-beta2"
NAME = "v1.3 beta 2 — PREVIEW ONLY, unverified, known and suspected bugs"
ASSET, ASSET_NAME = "index_multi2.html", "yichang-3d-v1.3-beta2.html"
tok = os.environ["GITHUB_TOKEN"]

BODY = """> # ⚠️ 预览版 —— 请勿用于任何正式用途
>
> **这是一个未经充分测试的预览版。它包含已知缺陷，并且很可能还包含尚未被发现的缺陷。**
> 请**不要**把它当作稳定版本使用、分发或依赖。正式版本请看 [v1.2](https://github.com/Radiosky-bilibili/yichang-3d/releases/tag/v1.2)。
>
> 具体来说，以下问题**已经确认存在**，另有若干**症状已被报告但尚未定位**（见下方"未确认的问题"一节）。

下载 `yichang-3d-v1.3-beta2.html` —— **44.3 MB**，单文件，保存后完全离线可用。

---

## 本版是什么

**v1.3 beta 1 + 一处改动**：预览模式下加入极轻的大气感。

| 参数（预览模式） | beta 1 | **beta 2** |
| --- | --- | --- |
| 大气透视 `uAtmo` | 0（完全没有） | **0.10** |
| 天空霾 `uHaze` | 0 | **0.03** |
| 雾浓度系数 | ×1.0 | ×1.0（不变） |

作为量级参考：**飞行模式**下 `uAtmo` 会随高度升至 0.92（4100 m 时约 0.63）；预览模式恒定 **0.10**，目的只是给远处一点空气感。

**除此之外的一切与 beta 1 完全相同** —— 经逐行比对确认，本版相对 beta 1 仅 **9 行**差异，全部位于预览模式的雾参数分支内。绿盘子保留、天空配色未改、六块高清补丁保留、出生点保留。

---

## ⚠️ 已确认的问题

### 1. 新增高清贴片的色彩与接缝问题 —— `[未修复]`

五块新增贴片（三峡大坝、秭归县、三峡机场、宜昌东站、宜昌北站）在拉近观看时，色调与周围底图不一致，且可见接缝与方块状边缘。

实测各影像源平均 RGB：

| 影像 | 平均 RGB | 说明 |
| --- | --- | --- |
| 主底图（Esri z14） | (69, 80, 62) | 基准 |
| 城区层（z16） | (78, 87, 70) | 略亮 |
| **三峡大坝贴片（z17）** | **(87, 97, 92)** | 偏亮、偏蓝灰 |
| **秭归县贴片（z16）** | **(93, 107, 103)** | 偏亮、偏青 |
| 三峡机场（z16） | (90, 96, 72) | 偏亮 |
| 宜昌东站（z16） | (99, 102, 82) | 偏亮 |
| 宜昌北站（z16） | (75, 85, 63) | 相对接近 |

**两个可能的原因（均未验证）**：

1. Esri 在不同缩放层级对影像做过不同的色调处理，高层级更接近原始影像，底层级做过统一 —— 直接叠加即出现色块。
2. 着色器中用**变量索引 `vec4` 数组**的部分，在某些移动 GPU 上可能取样错位，表现即为方块状接缝。

**尚未排除**：JPEG 编码参数差异、纹理色彩空间（已确认主底图与所有贴片均为 `NoColorSpace`，此项一致）。

---

## 🟡 未确认的问题（有报告，尚未定位）

在真机上有人报告了以下症状，**但在当前代码中未能复现，因此无法确认其来源**：

| 症状 | 状态 |
| --- | --- |
| **双指平移时，地图可以被移出外围底板的范围** | 已报告，未复现。本版的改动全部位于雾参数分支，理论上不影响相机与平移逻辑；但仍需排查。 |
| **外围底板看起来变小了** | 已报告，未复现。同上。 |
| **视角移动一卡一卡的（掉帧）** | 已报告，未复现。雾参数本身不改变任何逐帧计算量，但需要确认。 |

> **如果你遇到以上任一情况，请附上设备型号与复现步骤反馈。**
> 在得到确认之前，请假定本版**不适合日常使用**。

---

## 本版包含的功能（与 beta 1 相同）

- **六块高清细节层**：宜昌城区核心（2.05 m/px）、三峡大坝（**1.72 m/px**）、秭归县、三峡机场、宜昌东站、宜昌北站（2.05 m/px）—— *其中五块带有上述色彩问题*
- **纸飞机出生点**：高度 4200 m，正对葛洲坝
- **飞行时的大气透视**：离地越高远处越白；开启体积云时自动关闭
- **体积云**：光线步进，六个可调参数
- **待机自动演示**：60 秒无操作自动巡航
- **设置面板可滚动**（手机端）
- **版权与归属提示**

## 使用方法

1. 下载上面的 HTML —— 这一个文件就是完整程序。
2. 打开：**iPhone / iPad** 存到「文件」里点一下；**电脑**双击。飞行模式也能用。
3. 复现色彩问题：点底部「三峡大坝」快速跳转，然后拉近。

## 环境要求

支持 WebGL 2 的浏览器：Safari 15+、Chrome、Edge、Firefox。

## 署名、数据与免责

AI 生成作品：**DeepSeekHardness** 与 **MINIS**、**Doubao** 共同构建。

- **卫星影像 © Esri, Maxar, Earthstar Geographics 与 GIS User Community —— 非开放数据，本项目不授予任何影像权利。再分发前请自行取得授权，或替换为开放影像。**
- 高程来自 **AWS Open Data *Terrain Tiles*（Mapzen）**；完整署名清单见 README。
- 坐标为 GCJ-02，与 WGS-84 相差数百米。
- **按原样提供，未经充分测试，不得用于导航或任何安全相关用途。**
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

# 复用已存在的（草稿状态的）release
st, rel = api("GET", f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}")
if st != 200:
    st, rel = api("POST", f"https://api.github.com/repos/{OWNER}/{REPO}/releases", {
        "tag_name": TAG, "target_commitish": "main", "name": NAME,
        "body": BODY, "draft": False, "prerelease": True})
    if st not in (200,201): sys.exit("创建失败 %s" % st)
    print("已创建:", rel["html_url"])
else:
    # 已存在 → 更新说明并取消草稿
    st, rel = api("PATCH", f"https://api.github.com/repos/{OWNER}/{REPO}/releases/{rel['id']}", {
        "name": NAME, "body": BODY, "draft": False, "prerelease": True})
    print("已更新并公开:", rel["html_url"])

# 上传附件（如果还没有）
if not any(a['name'] == ASSET_NAME for a in rel.get('assets', [])):
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
else:
    print("附件已存在，跳过上传")

st, rel = api("GET", f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}")
for a in rel.get("assets", []):
    print("附件:", a["name"], "%.1f MB" % (a["size"]/1e6), a["state"])
print("draft =", rel["draft"], "| prerelease =", rel["prerelease"])
print("页面:", rel["html_url"])
