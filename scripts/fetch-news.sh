#!/bin/bash
# 新聞來源交叉比對腳本

SOURCES=(
  "TechCrunch|https://techcrunch.com/feed/"
  "The Verge|https://www.theverge.com/rss/index.xml"
  "Wired|https://www.wired.com/feed/rss"
  "Reuters|https://www.reutersagency.com/feed/"
  "Bloomberg|https://feeds.bloomberg.com/markets/news.rss"
  "Forbes|https://www.forbes.com/real-time/feed2/"
  "Ars Technica|https://feeds.arstechnica.com/arstechnica/index"
)

echo "=== 抓取最新新聞 ==="
echo ""

# 抓取所有新聞標題
for item in "${SOURCES[@]}"; do
  IFS='|' read -r name url <<< "$item"
  echo "正在抓取: $name..."
  
  # 抓取標題（只取前20個）
  titles=$(curl -s "$url" 2>/dev/null | grep -o '<title>[^<]*</title>' | sed 's/<title>//g;s/<\/title>//g' | head -20)
  
  # 存到暫存檔
  echo "$titles" > /tmp/news_$(echo $name | tr ' ' '_').txt
done

echo ""
echo "完成抓取！"
echo "請查看 /tmp/news_*.txt 查看各來源的新聞"