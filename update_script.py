import os
import re
import urllib.parse

IPA_FOLDER = './tipa'
REPO = 'wm0104/wm0104.ipa'
HTML_FILE = 'index.html'
MARKER = '<!-- AUTO_INSERT_HERE -->'

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

if MARKER not in html:
    raise SystemExit(
        f"未找到标记 {MARKER!r}，请在 {HTML_FILE} 中添加该标记"
    )


def get_app_info(filename):
    base = os.path.splitext(filename)[0]

    match = re.match(
        r'^(.*?)[\s._-]?v?(\d+(?:\.\d+)+)$',
        base,
        re.IGNORECASE
    )

    if match:
        name = match.group(1).strip()
        version = match.group(2).strip()
    else:
        name = base
        version = '1.0'

    return name, version


def version_tuple(version):
    return tuple(int(x) for x in version.split('.'))


apps = {}

for fn in os.listdir(IPA_FOLDER):

    if not (
        fn.lower().endswith('.ipa')
        or fn.lower().endswith('.tipa')
    ):
        continue

    name, version = get_app_info(fn)

    key = re.sub(
        r'[^a-zA-Z0-9]',
        '',
        name
    ).lower()

    if key not in apps:

        apps[key] = {
            'name': name,
            'version': version,
            'file': fn
        }

    else:

        old_version = apps[key]['version']

        if version_tuple(version) > version_tuple(old_version):

            old_file = apps[key]['file']
            old_path = os.path.join(
                IPA_FOLDER,
                old_file
            )

            if os.path.exists(old_path):
                os.remove(old_path)
                print(f'删除旧版本: {old_file}')

            apps[key] = {
                'name': name,
                'version': version,
                'file': fn
            }

        else:

            old_path = os.path.join(
                IPA_FOLDER,
                fn
            )

            if os.path.exists(old_path):
                os.remove(old_path)
                print(f'删除旧版本: {fn}')


cards = ''

for app in sorted(
    apps.values(),
    key=lambda x: x['name'].lower()
):

    name = app['name']
    version = app['version']
    filename = app['file']

    icon_name = re.sub(
        r'[^a-zA-Z0-9]',
        '',
        name
    ).lower()

    icon_url = (
        f'https://raw.githubusercontent.com/'
        f'{REPO}/main/icon/{icon_name}.png'
    )

    safe_filename = urllib.parse.quote(
        filename,
        safe=''
    )

    download_url = (
        f'https://raw.githubusercontent.com/'
        f'{REPO}/main/tipa/{safe_filename}'
    )

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
            <div class="app-version">{version} · ipa</div>
            <div class="app-desc">点击下载安装</div>
        </div>
    </div>

    <a
        href="{download_url}"
        class="download-btn"
        download
    >下载</a>
</div>
'''


start = html.index(MARKER)

html = (
    html[:start]
    + cards
    + '\n'
    + MARKER
    + html[start + len(MARKER):]
)


with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)


print('Done!')
print(f'当前网页应用数量: {len(apps)}')
