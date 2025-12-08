import os
import datetime

# 1. 获取当前时间
current_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# 2. 精选 20 个科技大V列表 (无Web3，专注 AI、硬件、科技巨头)
# 数据结构：名字, X账号(不带@), 领域/标签, 简介
tech_influencers = [
    # --- AI & 大模型 ---
    {"name": "Elon Musk", "handle": "elonmusk", "tag": "Tech King", "desc": "Tesla, SpaceX, xAI, 还有 X 的老板"},
    {"name": "Sam Altman", "handle": "sama", "tag": "OpenAI", "desc": "ChatGPT 之父，OpenAI CEO"},
    {"name": "Greg Brockman", "handle": "gdb", "tag": "OpenAI", "desc": "OpenAI 联合创始人，技术硬核"},
    {"name": "Yann LeCun", "handle": "ylecun", "tag": "AI Scientist", "desc": "Meta 首席 AI 科学家，图灵奖得主"},
    {"name": "Andrej Karpathy", "handle": "karpathy", "tag": "AI Educator", "desc": "前 Tesla AI 总监，现专注 AI 教学与开发"},
    {"name": "Demis Hassabis", "handle": "demishassabis", "tag": "DeepMind", "desc": "Google DeepMind 创始人，AlphaGo 之父"},
    {"name": "Andrew Ng", "handle": "AndrewYNg", "tag": "AI Educator", "desc": "吴恩达，AI 教育家，Coursera 创始人"},
    {"name": "Hugging Face", "handle": "huggingface", "tag": "AI Community", "desc": "AI 界的 Github，开源模型大本营"},
    {"name": "Lex Fridman", "handle": "lexfridman", "tag": "Podcast", "desc": "顶级科技播客，经常采访马斯克和奥特曼"},
    {"name": "Francois Chollet", "handle": "fchollet", "tag": "Keras", "desc": "Keras 作者，Google AI 研究员"},

    # --- 苹果 & 硬件 & 手机 ---
    {"name": "Tim Cook", "handle": "tim_cook", "tag": "Apple", "desc": "苹果 CEO"},
    {"name": "Marques Brownlee", "handle": "MKBHD", "tag": "Reviewer", "desc": "地表最强科技数码博主"},
    {"name": "Ming-Chi Kuo", "handle": "mingchikuo", "tag": "Analyst", "desc": "郭明錤，最准的苹果供应链分析师"},
    {"name": "Mark Gurman", "handle": "markgurman", "tag": "Bloomberg", "desc": "彭博社记者，苹果爆料非常准"},
    {"name": "Mrwhosetheboss", "handle": "Mrwhosetheboss", "tag": "Reviewer", "desc": "顶级手机评测博主，特效华丽"},
    
    # --- 科技巨头 & 极客 ---
    {"name": "Satya Nadella", "handle": "satyanadella", "tag": "Microsoft", "desc": "微软 CEO，带领微软重回巅峰"},
    {"name": "Sundar Pichai", "handle": "sundarpichai", "tag": "Google", "desc": "谷歌 CEO"},
    {"name": "Paul Graham", "handle": "paulg", "tag": "VC/Startup", "desc": "Y Combinator 创始人，硅谷创业教父"},
    {"name": "John Carmack", "handle": "ID_AA_Carmack", "tag": "Legend", "desc": "传奇程序员，前 Oculus CTO，FPS游戏之父"},
    {"name": "The Verge", "handle": "verge", "tag": "Tech News", "desc": "顶级科技媒体，一手资讯"},
]

# 3. 生成 HTML
html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科技大佬观察室</title>
    <style>
        :root {{ --primary: #1da1f2; --bg: #f5f8fa; --card-bg: #ffffff; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; background-color: var(--bg); margin: 0; padding: 20px; color: #14171a; }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        
        .header {{ text-align: center; margin-bottom: 40px; padding: 20px 0; }}
        .header h1 {{ margin: 0; font-size: 2.5em; color: #14171a; }}
        .header p {{ color: #657786; margin-top: 10px; }}
        
        /* 网格布局 */
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }}
        
        /* 卡片样式 */
        .card {{ background: var(--card-bg); border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: transform 0.2s, box-shadow 0.2s; border: 1px solid #e1e8ed; display: flex; flex-direction: column; }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 8px 16px rgba(0,0,0,0.1); }}
        
        .top-row {{ display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px; }}
        .tag {{ background-color: #e8f5fd; color: var(--primary); padding: 4px 8px; border-radius: 999px; font-size: 0.75em; font-weight: bold; }}
        
        .name {{ font-size: 1.2em; font-weight: bold; margin: 0; }}
        .handle {{ color: #657786; font-size: 0.9em; margin-bottom: 12px; }}
        .desc {{ font-size: 0.9em; color: #14171a; line-height: 1.5; flex-grow: 1; margin-bottom: 20px; }}
        
        .btn {{ display: block; text-align: center; background-color: #000; color: white; text-decoration: none; padding: 10px; border-radius: 8px; font-weight: bold; transition: background 0.2s; }}
        .btn:hover {{ background-color: #333; }}
        
        .footer {{ text-align: center; margin-top: 40px; color: #657786; font-size: 0.8em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔭 科技大佬观察室</h1>
            <p>追踪 {len(tech_influencers)} 位全球顶级科技领袖 · 最后更新: {current_time}</p>
        </div>

        <div class="grid">
"""

for person in tech_influencers:
    html_content += f"""
            <div class="card">
                <div class="top-row">
                    <span class="tag">{person['tag']}</span>
                </div>
                <div class="name">{person['name']}</div>
                <div class="handle">@{person['handle']}</div>
                <div class="desc">{person['desc']}</div>
                <a href="https://x.com/{person['handle']}" target="_blank" class="btn">访问主页 →</a>
            </div>
    """

html_content += """
        </div>
        <div class="footer">
            Powered by GitHub Actions | Data curated manually
        </div>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ 科技大佬观察室页面生成成功！")
