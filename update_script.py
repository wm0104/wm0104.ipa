import os
import urllib.parse

IPA_FOLDER = './tipa'
ICON_FOLDER = './icon'
REPO = 'wm0104/wm0104.ipa'
HTML_FILE = 'index.html'
MARKER = '<!-- AUTO_INSERT_HERE -->'

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

if MARKER not in html:
    print('Error: 找不到标记，请检查 index.html 里有没有 <!-- AUTO_INSERT_HERE -->')
    exit(1)

cards = ''
for fn in os.listdir(IPA_FOLDER):
    if fn.endswith('.ipa') or fn.endswith('.tipa'):
        base = os.path.splitext(fn)[0]
        parts = base.split('-')
        name = parts[0].strip()
        ver = parts[1].strip() if len(parts) > 1 else 'v1.0'
        typ = 'ipa' if fn.endswith('.ipa') else 'tipa'

           # ⭐ 核心逻辑：用前缀匹配找图标，且忽略大小写
        # 例如 IPA 名为 Loon，图标文件叫 loon.png 或 LOON.png 都能匹配上
        icon_filename = None
        for f in os.listdir(ICON_FOLDER):
            if f.lower().endswith('.png') and name.lower().startswith(f[:-4].lower()):
                icon_filename = f
                break

        if icon_filename:
            icon_url = f'https://raw.githubusercontent.com/{REPO}/main/icon/{urllib.parse.quote(icon_filename)}'
            icon_html = f'<a href="{icon_url}" class="app-icon-link"><img src="{icon_url}" class="app-icon"></a>'
        else:
            icon_html = ''

        safe = urllib.parse.quote(fn)
        down = f'https://raw.githubusercontent.com/{REPO}/main/tipa/{safe}'

        cards += f'<div class="app-item"><div class="app-meta-box">{icon_html}<div class="app-info"><div class="app-name">{name}</div><div class="app-version">{ver} · {typ}</div><div class="app-desc">点击下载安装</div></div></div><a href="{down}" class="download-btn">下载</a></div>'

html = html.replace(MARKER, cards)
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
