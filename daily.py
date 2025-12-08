import os
import datetime
import requests # 记得我们之前在 requirements.txt 里装过这个

# 1. 获取当前时间
current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# 2. 模拟获取新闻 (以后你可以把这里改成去爬微博热搜、HackerNews 或 财联社)
# 这里为了演示，我们先写死，或者调用一个简单的公共 API
news_items = [
    {"title": "GitHub Copilot 更新了新功能", "link": "https://github.blog"},
    {"title": "Python 3.13 预计发布时间公布", "link": "https://python.org"},
    {"title": "每日早报：今天是个写代码的好日子", "link": "#"}
]

# 3. 生成更漂亮的 HTML
html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的每日新闻聚合</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f6f8fa; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        h1 {{ color: #24292e; }}
        .time {{ color: #586069; font-size: 0.9em; }}
        .news-item {{ margin: 15px 0; padding-bottom: 15px; border-bottom: 1px solid #eaecef; }}
        .news-item a {{ text-decoration: none; color: #0366d6; font-size: 1.2em; font-weight: 500; }}
        .news-item a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>📅 每日科技新闻</h1>
        <p class="time">更新时间 (UTC): {current_time}</p>
    </div>

    <div class="card">
"""

# 循环把新闻加入 HTML
for item in news_items:
    html_content += f"""
        <div class="news-item">
            <a href="{item['link']}" target="_blank">{item['title']}</a>
        </div>
    """

html_content += """
    </div>
    <footer style="text-align: center; color: #666; margin-top: 40px;">
        <p>Powered by GitHub Actions</p>
    </footer>
</body>
</html>
"""

# 4. 写入文件
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ 新闻网页生成完毕")
