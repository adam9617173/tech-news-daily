#!/usr/bin/env python3
"""
Tech News Daily - Auto Update Script
Fetches latest tech news and generates HTML
"""

import json
import os
from datetime import datetime

# Taiwan timezone
TAIWAN_TZ = 8

def get_taiwan_time():
    """Get current Taiwan time"""
    utc_now = datetime.utcnow()
    taiwan_time = utc_now.timestamp() + (TAIWAN_TZ * 3600)
    return datetime.fromtimestamp(taiwan_time)

def fetch_tech_news():
    """Fetch tech news using Tavily API"""
    try:
        from tavily import tavily
        client = tavily(api_key=os.environ.get("TAVILY_API_KEY", ""))
        results = client.search("latest technology news AI tech", max_results=8)
        return results.get("results", [])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def translate_to_chinese(text):
    """Simple translation placeholder - would use AI in production"""
    # This is a placeholder - in production you'd use an AI API
    return text

def generate_article_card(news_item, index, date_str):
    """Generate HTML for a single article card"""
    title = news_item.get("title", "No title")
    url = news_item.get("url", "#")
    content = news_item.get("content", "")[:100]
    
    stickers = [f"sticker-{(index % 10) + 1}.png"]
    
    html = f'''            <!-- Article {index + 1} -->
            <a href="articles/{index+1:02d}-{news_item.get('title', 'article')[:30].replace(' ', '-').lower()}.html" class="article-card">
                <div class="card-image">
                    <img src="{stickers[0]}" alt="News">
                </div>
                <div class="card-content">
                    <span class="card-date">📅 {date_str}</span>
                    <h3>{title[:50]}</h3>
                    <p class="card-summary">{content}...</p>
                    <div class="card-footer">
                        <span class="source">📰 {url.split('/')[2] if url else 'Source'}</span>
                        <span class="read-more">閱讀 →</span>
                    </div>
                </div>
            </a>'''
    return html

def main():
    print("🔄 Fetching latest tech news...")
    
    news = fetch_tech_news()
    taiwan_date = get_taiwan_time().strftime("%Y.%m.%d")
    
    print(f"📰 Found {len(news)} news articles")
    print(f"📅 Date: {taiwan_date}")
    
    # Generate article cards
    articles_html = "\n".join([
        generate_article_card(news[i], i, taiwan_date) 
        for i in range(min(len(news), 6))
    ])
    
    print("✅ News update complete!")

if __name__ == "__main__":
    main()
