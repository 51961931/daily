import requests
import datetime
import os

# 1. 获取当前时间
current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# 2. 任务一：抓取每日格言 (使用 v1.hitokoto.cn 的免费 API)
try:
    resp = requests.get("https://v1.hitokoto.cn/?c=i") # c=i 代表获取诗词
    if resp.status_code == 200:
        data = resp.json()
        # 拿到句子和作者
        quote_text = data.get("hitokoto", "暂无名言")
        quote_author = data.get("from", "佚名")
    else:
        quote_text = "API 请求失败"
        quote_author = "系统"
except Exception as e:
    quote_text = "网络出错啦"
    quote_author = "系统"

# 3. 任务二：抓取 GitHub 上近期热门的 Python 项目 (使用 GitHub 官方 API)
# 搜索条件：过去 7 天创建的，按 star 排序，取前 5 个
date_7_days_ago = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
url = f"https://api.github.com/search/repositories?q=language:python+created:>{date_7_days_ago}&sort=stars&order=desc"
projects = []

try:
    # 加上 headers 伪装成浏览器，虽然 GitHub API 不强制，但为了保险
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        items = r.json().get("items", [])[:5] # 只取前5个
        for item in items:
            projects.append({
                "name": item['name'],
                "desc": item['description'] or "暂无描述",
                "stars": item['stargazers_count'],
                "url": item['html_url']
            })
    else:
        print("GitHub API 返回错误:", r.status_code)
except Exception as e:
    print("获取项目失败:", e)


# 4. 生成漂亮的 HTML 网页
html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的每日自动日报</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f6f8fa; color: #24292e; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .quote-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .quote-text {{ font-size: 1.4em; font-style: italic; margin-bottom: 10px; }}
        .quote-author {{ text-align: right; font-size: 0.9em; opacity: 0.9; }}
        
        .project-list {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .project-item {{ padding: 20px 0; border-bottom: 1px solid #eaecef; }}
        .project-item:last-child {{ border-bottom: none; }}
        .project-title {{ font-size: 1.2em; font-weight: bold; color: #0366d6; text-decoration: none; }}
        .project-title:hover {{ text-decoration: underline; }}
        .project-desc {{ color: #586069; margin: 8px 0; font-size: 0.95em; }}
        .project-meta {{ font-size: 0.85em; color: #6a737d; }}
        .footer {{ text-align: center; margin-top: 50px; color: #959da5; font-size: 0.8em; }}
    </style>
</head>
<body>

    <div class="header">
        <h1>🚀 每日自动日报</h1>
        <p>更新时间: {current_time}</p>
    </div>

    <div class="quote-card">
        <div class="quote-text">“{quote_text}”</div>
        <div class="quote-author">—— {quote_author}</div>
    </div>

    <div class="project-list">
        <h2 style="border-bottom: 2px solid #eaecef; padding-bottom: 10px;">🔥 本周 GitHub 热门 Python 项目</h2>
        {''.join([f'''
        <div class="project-item">
            <a href="{p['url']}" target="_blank" class="project-title">{p['name']}</a>
            <p class="project-desc">{p['desc']}</p>
            <div class="project-meta">⭐ Stars: {p['stars']}</div>
        </div>
        ''' for p in projects])}
    </div>

    <div class="footer">
        Powered by GitHub Actions & Python
    </div>

</body>
</html>
"""

# 5. 写入文件
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ 网页生成成功！")
