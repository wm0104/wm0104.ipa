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
    print('Error: marker not found')
    exit(1)

cards = ''
for fn in os.listdir(IPA_FOLDER):
    if fn.endswith('.ipa') or fn.endswith('.tipa'):
        base = os.path.splitext(fn)[0]
        parts = base.split('-')
        name = parts[0].strip()
        ver = parts[1].strip() if len(parts) > 1 else 'v1.0'
        typ = 'ipa' if fn.endswith('.ipa') else 'tipa'

        icon_filename = name + '.png'
        icon_path = os.path.join(ICON_FOLDER, icon_filename)
        if os.path.exists(icon_path):
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
