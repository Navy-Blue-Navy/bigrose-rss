import requests
import hashlib
import html
from datetime import datetime
from email.utils import format_datetime
import xml.etree.ElementTree as ET

API_URL = "https://big-rose.jp/wp-json/wp/v2/event_post"
SITE_URL = "https://big-rose.jp/event_post/"
OUTPUT = "bigrose.xml"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

params = {
    "per_page": 100,
    "orderby": "date",
    "order": "desc"
}

response = requests.get(
    API_URL,
    headers=HEADERS,
    params=params,
    timeout=30
)

print("REST API HTTP:", response.status_code)
response.raise_for_status()

posts = response.json()

print("取得件数:", len(posts))

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = "福山ビッグ・ローズ イベント情報"
ET.SubElement(channel, "link").text = SITE_URL
ET.SubElement(channel, "description").text = "福山ビッグ・ローズのイベント情報"
ET.SubElement(channel, "language").text = "ja"

for i, post in enumerate(posts, 1):
    title = html.unescape(post.get("title", {}).get("rendered", "")).strip()
    link = post.get("link", "").strip()
    date_text = post.get("date", "")

    if not title or not link or not date_text:
        continue

    dt = datetime.fromisoformat(date_text)

    item = ET.SubElement(channel, "item")

    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    ET.SubElement(item, "description").text = title
    ET.SubElement(item, "pubDate").text = format_datetime(dt)
    ET.SubElement(item, "guid").text = hashlib.sha256(
        link.encode("utf-8")
    ).hexdigest()

    if i <= 10:
        print()
        print(f"[{i}] {title}")
        print("    ", date_text)
        print("    ", link)

tree = ET.ElementTree(rss)
ET.indent(tree, space="  ")

tree.write(
    OUTPUT,
    encoding="utf-8",
    xml_declaration=True
)

print()
print("RSS作成成功")
print("保存件数:", len(posts))
print("保存:", OUTPUT)
