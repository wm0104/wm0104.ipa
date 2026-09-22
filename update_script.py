import os
import urllib.parse
import re

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

for fn in sorted(os.listdir(IPA_FOLDER)):
    if not (fn.lower().endswith('.ipa') or fn.lower().endswith('.tipa')):
        continue

    base = os.path.splitext(fn)[0]

    match = re.match(r'^(.*?)[\s._-]?v?(\d+(?:\.\d+)+)$', base, re.IGNORECASE)

    if match:
        name = match.group(1).strip()
        ver = match.group(2).strip()
    else:
        name = base
        ver = 'v1.0'

    icon_name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()

    icon_url = f'https://raw.githubusercontent.com/{REPO}/main/icon/{icon_name}.png'

    safe_name = urllib.parse.quote(fn)

    down = f'https://raw.githubusercontent.com/{REPO}/main/tipa/{safe_name}'

    cards += f'''
<div class="app-item">
    <div class="app-meta-box">
        <img
            src="{icon_url}"
            class="app-icon"
            alt="{name}"
            onerror="this.style.display='none'"
        >
        <div class="app-info">
            <div class="app-name">{name}</div>
            <div class="app-version">{ver} · ipa</div>
            <div class="app-desc">点击下载安装</div>
        </div>
    </div>
    <a href="{down}" class="download-btn">下载</a>
</div>
'''

html = html.replace(MARKER, cards + '\n' + MARKER)

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print('Done!')
