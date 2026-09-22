import os
import re
import urllib.parse

IPA_FOLDER = './tipa'
REPO = 'wm0104/wm0104.ipa'
HTML_FILE = 'index.html'

START_MARKER = '<!-- AUTO_START -->'
END_MARKER = '<!-- AUTO_END -->'


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


with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()


if START_MARKER not in html or END_MARKER not in html:
    raise SystemExit(
        'index.html 中找不到 AUTO_START 或 AUTO_END'
    )


apps = {}

files = [
    fn
    for fn in os.listdir(IPA_FOLDER)
    if fn.lower().endswith(('.ipa', '.tipa'))
]


for fn in files:

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

        old = apps[key]

        if version_tuple(version) > version_tuple(old['version']):

            old_path = os.path.join(
                IPA_FOLDER,
                old['file']
            )

            if os.path.exists(old_path):
                os.remove(old_path)
                print(
                    f"删除旧版本: {old['file']}"
                )

            apps[key] = {
                'name': name,
                'version': version,
                'file': fn
            }

        else:

            new_path = os.path.join(
                IPA_FOLDER,
                fn
            )

            if os.path.exists(new_path):
                os.remove(new_path)
                print(
                    f"删除旧版本: {fn}"
                )


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
        f'https://github.com/{REPO}'
        f'/raw/refs/heads/main/'
        f'tipa/{safe_filename}'
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

            <div class="app-version">
                {version} · ipa
            </div>

            <div class="app-desc">
                点击下载安装
            </div>

        </div>

    </div>

    <a
        href="{download_url}"
        class="download-btn"
    >下载</a>

</div>
'''


start = html.index(START_MARKER) + len(START_MARKER)
end = html.index(END_MARKER)


html = (
    html[:start]
    + '\n'
    + cards
    + '\n'
    + html[end:]
)


with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)


print()
print('======================')
print('更新完成')
print('当前应用数量:', len(apps))
print('======================')
