import os
import urllib.parse

IPA_FOLDER = './tipa'
REPO = 'wm0104/wm0104.ipa'
HTML_FILE = 'index.html'
MARKER = '<!-- AUTO_INSERT_HERE -->'

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

if MARKER not in html:
    print('Error: 找不到标记')
    exit(1)

cards = ''

for fn in os.listdir(IPA_FOLDER):
    if fn.endswith('.ipa'):
        base = os.path.splitext(fn)[0]

        if '-' in base:
            parts = base.split('-', 1)
            name = parts[0].strip()
            ver = parts[1].strip()
        elif '.' in base:
            parts = base.rsplit('.', 1)
            name = parts[0].strip()
            ver = parts[1].strip()
        else:
            name = base
            ver = 'v1.0'

        safe_name = urllib.parse.quote(fn)

        down = f'https://github.com/{REPO}/raw/main/tipa/{safe_name}'

        cards += f'<div class="app-item"><div class="app-meta-box"><div class="app-info"><div class="app-name">{name}</div><div class="app-version">{ver} · ipa</div><div class="app-desc">点击下载安装</div></div></div><a href="{down}" class="download-btn">下载</a></div>'

html = html.replace(MARKER, cards)

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print('Done!')
