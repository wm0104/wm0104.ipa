#!/bin/bash
# 这是一个简单的脚本，用来生成应用列表

# 1. 读取网页模板
HTML_FILE="./repo-page/index.html"

# 2. 定义一个空字符串，用来存放生成的应用卡片
APPS_HTML=""

# 3. 遍历 surge 文件夹里的所有 ipa 和 tipa 文件
for file in surge/*.ipa surge/*.tipa; do
    if [ -f "$file" ]; then
        # 获取文件名（去掉路径和扩展名）
        filename=$(basename "$file")
        base_name="${filename%.*}"
        
        # 提取应用名（假设文件名格式为 应用名-版本号.tipa）
        app_name=$(echo "$base_name" | cut -d'-' -f1)
        version=$(echo "$base_name" | cut -d'-' -f2)
        [ -z "$version" ] && version="v1.0"
        file_type="${filename##*.}"
        
        # 生成链接
        icon_url="https://raw.githubusercontent.com/wm0104/wm0104.icon/main/APP/${app_name}.png"
        encoded_filename=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$filename'))")
        download_url="https://raw.githubusercontent.com/wm0104/wm0104.ipa/main/surge/${encoded_filename}"
        
        # 拼接 HTML 卡片
        APPS_HTML="${APPS_HTML}<div class=\"app-item\"><div class=\"app-meta-box\"><a href=\"${icon_url}\" target=\"_blank\" class=\"app-icon-link\"><img src=\"${icon_url}\" class=\"app-icon\" alt=\"Icon\"></a><div class=\"app-info\"><div class=\"app-name\">${app_name}</div><div class=\"app-version\">${version} · ${file_type}</div><div class=\"app-desc\">点击下载安装</div></div></div><a href=\"${download_url}\" class=\"download-btn\">下载</a></div>"
    fi
done

# 4. 用生成的卡片替换掉模板里的标记
python3 -c "
with open('$HTML_FILE', 'r', encoding='utf-8') as f:
    content = f.read()
new_content = content.replace('<!-- AUTO_INSERT_HERE -->', '$APPS_HTML')
with open('$HTML_FILE', 'w', encoding='utf-8') as f:
    f.write(new_content)
"
echo "生成完成！"
