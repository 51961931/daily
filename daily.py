import os
import datetime
import requests
import xml.etree.ElementTree as ET # 用来解析 Google News 的 RSS 数据

# 1. 获取当前时间
current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# 2. 定义大V列表 (保持不变)
tech_influencers = [
    {"name": "Elon Musk", "handle": "elonmusk", "tag": "Tech King", "desc": "Tesla, SpaceX, xAI, X 老板"},
    {"name": "Sam Altman", "handle": "sama", "tag": "OpenAI", "desc": "ChatGPT 之父，OpenAI CEO"},
    {"name": "Tim Cook", "handle": "tim_cook", "tag": "Apple", "desc": "苹果 CEO，供应链大师"},
    {"name": "Jensen Huang", "handle": "NVIDIA", "tag": "NVIDIA", "desc": "黄仁勋，AI 算力霸主 (皮衣刀客)"},
    {"name": "Yann LeCun", "handle": "ylecun", "tag": "Meta AI", "desc": "图灵奖得主，Meta 首席科学家"},
    {"name": "Demis Hassabis", "handle": "demishassabis", "tag": "DeepMind", "desc": "AlphaGo 之父，Google DeepMind"},
    {"name": "MKBHD", "handle": "MKBHD", "tag": "Reviewer", "desc": "千万粉顶流数码博主"},
    {"name": "Ming-Chi Kuo", "handle": "mingchikuo", "tag": "Analyst", "desc": "郭明錤，苹果最准分析师"},
    {"name": "Satya Nadella", "handle": "satyanadella", "tag": "Microsoft", "desc": "微软 CEO"},
    {"name": "Sundar Pichai", "handle": "sundarpichai", "tag": "Google", "desc": "谷歌 CEO"},
    {"name": "Hugging Face", "handle": "huggingface", "tag": "AI Hub", "desc": "AI 界的 GitHub"},
    {"name": "Andrej Karpathy", "handle": "karpathy", "tag": "AI Dev", "desc": "前 Tesla AI 总监，现大神级讲师"},
    {"name": "Lex Fridman", "handle": "lexfridman", "tag": "Podcast", "desc": "硬核科技访谈，采访过所有人"},
    {"name": "Paul Graham", "handle": "paulg", "tag": "YC", "desc": "硅谷创业教父"},
    {"name": "Vitalik Buterin", "handle": "VitalikButerin", "tag": "Crypto", "desc": "V神，虽然你不想要Web3，但他也是技术大神"}, # 如果不喜欢可以删掉
    {"name": "Linus Torvalds", "handle": "Linux", "tag": "Linux", "desc": "Linux 之父 (非X活跃，致敬位)"}, 
    {"name": "Mark Gurman", "handle": "markgurman", "tag": "Scoop", "desc": "彭博社苹果爆料记者"},
    {"name": "The Verge", "handle": "verge", "tag": "Media", "desc": "主流科技媒体"},
    {"name": "Wired", "handle": "WIRED", "tag": "Media", "desc": "连线杂志，深度科技报道"},
    {"name": "TechCrunch", "handle": "TechCrunch", "tag": "Media", "desc": "创业公司与独角兽资讯"}
]

# 3. 新功能：抓取 Google News 新闻
# 我们定义几个关键词，去抓取相关的中文新闻
search_keywords = ["马斯克", "OpenAI", "苹果公司", "英伟达", "人工智能"]
news_list = []

def get_google_news(keyword):
    # Google News RSS 地址 (中文)
    url = f"https://news.google.com/rss/search?q={keyword}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            # 解析前 3 条新闻
            items = root.findall('./channel/item')[:3]
            results = []
            for item in items:
                title = item.find('title').text
                link = item.find('link').text
                pubDate = item.find('pubDate').text
                # 清理标题 (Google RSS 标题通常包含 ' - 媒体名'，看起来太乱，我们去掉)
                clean_title = title.split(" - ")[0] 
                source = title.split(" - ")[-1] if " - " in title else "新闻"
                results.append({"title": clean_title, "link": link, "date": pubDate[:16], "source": source})
            return results
    except Exception as e:
        print(f"抓取 {keyword} 失败: {e}")
        return []
    return []

# 循环抓取所有关键词的新闻
for key in search_keywords:
    print(f"正在抓取 {key} 的新闻...")
    items = get_google_news(key)
    if items:
        news_list.append({"keyword": key, "items": items})


# 4. 生成 HTML 网页
html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科技大V与今日头条</title>
    <style>
        :root {{ --primary: #007bff; --bg: #f4f6f9; --card-bg: #ffffff; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background-color: var(--bg); margin: 0; padding: 0; color: #333; }}
        
        .container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
        
        /* 头部 */
        .header {{ text-align: center; padding: 40px 0; }}
        .header h1 {{ margin: 0; font-size: 2.2rem; color: #2c3e50; }}
        .header p {{ color: #7f8c8d; margin-top: 10px; }}

        /* 新闻板块 (新功能) */
        .news-section {{ background: #fff; border-radius: 12px; padding: 25px; margin-bottom: 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .news-title {{ font-size: 1.5rem; border-left: 5px solid var(--primary); padding-left: 15px; margin-bottom: 20px; color: #2c3e50; }}
        .news-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .news-column h3 {{ color: var(--primary); border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .news-item {{ margin-bottom: 15px; }}
        .news-item a {{ text-decoration: none; color: #34495e; font-weight: 500; font-size: 1rem; display: block; margin-bottom: 5px; }}
        .news-item a:hover {{ color: var(--primary); text-decoration: underline; }}
        .news-meta {{ font-size: 0.8rem; color: #95a5a6; }}

        /* 大V 卡片板块 */
        .section-title {{ text-align: center; margin-bottom: 30px; font-size: 1.5rem; color: #2c3e50; font-weight: bold; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }}
        .card {{ background: var(--card-bg); border-radius: 10px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 0.2s; border: 1px solid #eee; display: flex; flex-direction: column; }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        
        .card-top {{ display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px; }}
        .tag {{ background: #e3f2fd; color: #1976d2; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }}
        .name {{ font-size: 1.1rem; font-weight: bold; margin: 0; }}
        .handle {{ color: #7f8c8d; font-size: 0.85rem; margin-bottom: 10px; }}
        .desc {{ font-size: 0.9rem; color: #555; line-height: 1.5; flex-grow: 1; margin-bottom: 15px; }}
        .btn {{ display: block; text-align: center; background: #24292e; color: white; text-decoration: none; padding: 8px; border-radius: 6px; font-size: 0.9rem; transition: background 0.2s; }}
        .btn:hover {{ background: #000; }}
        
        .footer {{ text-align: center; margin-top: 50px; color: #bdc3c7; font-size: 0.8rem; padding-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Daily Tech Observer</h1>
            <p>更新时间 (UTC): {current_time}</p>
        </div>

        <div class="news-section">
            <div class="news-title">📰 今日科技头条 (基于 Google News)</div>
            <div class="news-grid">
"""

# 动态插入新闻列
for category in news_list:
    html_content += f"""
                <div class="news-column">
                    <h3>🔥 {category['keyword']}</h3>
    """
    for item in category['items']:
        html_content += f"""
                    <div class="news-item">
                        <a href="{item['link']}" target="_blank">{item['title']}</a>
                        <div class="news-meta">{item['source']} · {item['date']}</div>
                    </div>
        """
    html_content += "</div>"

html_content += f"""
            </div>
        </div>

        <div class="section-title">🔭 重点关注大V ({len(tech_influencers)}位)</div>
        <div class="grid">
"""

# 动态插入大V卡片
for person in tech_influencers:
    html_content += f"""
            <div class="card">
                <div class="card-top">
                    <span class="tag">{person['tag']}</span>
                </div>
                <div class="name">{person['name']}</div>
                <div class="handle">@{person['handle']}</div>
                <div class="desc">{person['desc']}</div>
                <a href="https://x.com/{person['handle']}" target="_blank" class="btn">去主页看看 →</a>
            </div>
    """

html_content += """
        </div>
        <div class="footer">
            Powered by GitHub Actions & Python
        </div>
    </div>
</body>
</html>
"""

# 5. 写入文件
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ 页面生成完毕：包含新闻和人物列表")
