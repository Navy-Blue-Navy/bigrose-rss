import requests

SOURCE_URL = "https://big-rose.jp/event_post/feed/"
OUTPUT = "bigrose.xml"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}

response = requests.get(
    SOURCE_URL,
    headers=HEADERS,
    timeout=30
)

print("公式RSS HTTP:", response.status_code)

response.raise_for_status()

# XMLをバイト列のまま保存
# 文字コードやRSS内部の情報を余計に変更しない
with open(OUTPUT, "wb") as f:
    f.write(response.content)

print()
print("RSS取得成功")
print("保存:", OUTPUT)
print("サイズ:", len(response.content), "bytes")

# 内容確認
text = response.content.decode("utf-8", errors="replace")

print()
print("先頭500文字:")
print(text[:500])