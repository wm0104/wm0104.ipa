import os
import re
import urllib.parse

IPA_FOLDER = './tipa'
ICON_FOLDER = './icon'
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


def normalize_name(name):
    return re.sub(
        r'[^a-zA-Z0-9]',
        '',
        name
    ).lower()


def find_icon(filename):
    if not os.path.isdir(ICON_FOLDER):
        return None

    base = os.path.splitext(filename)[0]

    base_key = normalize_name(base)

    for icon_file in os.listdir(ICON_FOLDER):

        if not icon_file.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.webp')
        ):
            continue

        icon_name = os.path.splitext(icon_file)[0]

        icon_key = normalize_name(icon_name)

        if base_key.startswith(icon_key):
            return icon_file

    return None


with open(
    HTML_FILE,
    'r',
    encoding='utf-8'
) as f:
    html = f.read()


if START_MARKER not in html or END_MARKER not in html:
    raise SystemExit(
        'index.html 中找不到 AUTO_START 或 AUTO_END'
    )


apps = {}


files = [
    fn
    for fn in os.listdir(IPA_FOLDER)
    if fn.lower().endswith(
        ('.ipa', '.tipa')
    )
]


for fn in files:

    name, version = get_app_info(fn)

    key = normalize_name(name)

    if key not in apps:

        apps[key] = {
            'name': name,
            'version': version,
            'file': fn
        }

    else:

        old = apps[key]

        if version_tuple(version) > version_tuple(
            old['version']
        ):

            old_path = os.path.join(
                IPA_FOLDER,
                old['file']
            )

            if os.path.exists(old_path):

                os.remove(old_path)

                print(
                    '删除旧版本:',
                    old['file']
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
                    '删除旧版本:',
                    fn
                )


cards = ''


for app in sorted(
    apps.values(),
    key=lambda x: x['name'].lower()
):

    name = app['name']
    version = app['version']
    filename = app['file']

    icon_filename = find_icon(filename)


    if icon_filename:

        safe_icon = urllib.parse.quote(
            icon_filename,
            safe=''
        )

        icon_url = (
            f'https://raw.githubusercontent.com/'
            f'{REPO}/main/icon/{safe_icon}'
        )

        icon_html = f'''
        <img
            src="{icon_url}"
            class="app-icon"
            alt="{name}"
        >
        '''

        print(
            '图标匹配:',
            filename,
            '→',
            icon_filename
        )

    else:

        icon_html = ''

        print(
            '未找到图标:',
            filename
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


    extension = os.path.splitext(
        filename
    )[1].replace(
        '.',
        ''
    ).lower()


    cards += f'''
<div class="app-item">

    <div class="app-meta-box">

        {icon_html}

        <div class="app-info">

            <div class="app-name">
                {name}
            </div>

            <div class="app-version">
                {version} · {extension}
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


start = html.index(
    START_MARKER
) + len(START_MARKER)

end = html.index(
    END_MARKER
)


html = (
    html[:start]
    + '\n'
    + cards
    + '\n'
    + html[end:]
)


with open(
    HTML_FILE,
    'w',
    encoding='utf-8'
) as f:

    f.write(html)


print()
print('======================')
print('更新完成')
print('当前应用数量:', len(apps))
print('======================')
