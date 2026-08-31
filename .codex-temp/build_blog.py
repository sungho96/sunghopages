import html
import json
import os
from pathlib import Path

ROOT = Path(r"C:\Users\zx028\OneDrive\바탕 화면\GithubPages")
DATA = ROOT / ".codex-temp" / "blog-data.json"
POSTS_DIR = ROOT / "posts"

CATEGORY_KEYS = {
    "2D AppleStory": "2d-applestory",
    "3D RPG": "3d-rpg",
    "TowerRandomDefence": "towerrandomdefence",
}


def esc(value):
    return html.escape(value or "", quote=True)


def slug_for(post):
    slug = post.get("slug") or "post"
    return "".join(ch if ch.isalnum() or ch == "-" else "-" for ch in slug).strip("-") or "post"


def nav(prefix=""):
    return f"""<header class="site-header">
      <a class="brand" href="{prefix}index.html">이성호</a>
      <nav class="nav" aria-label="주요 메뉴">
        <a href="{prefix}resume.html">이력서</a>
        <span aria-hidden="true"></span>
        <a href="{prefix}cover-letter.html">자기소개서</a>
        <span aria-hidden="true"></span>
        <a href="{prefix}portfolio.html">포트폴리오</a>
        <span aria-hidden="true"></span>
        <a href="{prefix}blog.html">블로그</a>
        <span aria-hidden="true"></span>
        <a href="#more">More</a>
      </nav>
    </header>"""


def footer(prefix=""):
    return f"""<footer class="footer" id="more">
      <div class="footer-inner">
        <section>
          <h2>Phone</h2>
          <p>010-5263-3509</p>
        </section>
        <section>
          <h2>Email</h2>
          <p><a href="mailto:zx028906@naver.com">zx028906@naver.com</a></p>
        </section>
        <section>
          <h2>github</h2>
          <p><a href="https://github.com/sungho96">https://github.com/sungho96</a></p>
        </section>
      </div>
    </footer>"""


def shell(title, description, body, prefix=""):
    return f"""<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}">
    <link rel="stylesheet" href="{prefix}styles.css">
  </head>
  <body>
    {nav(prefix)}
{body}
    {footer(prefix)}
  </body>
</html>
"""


def paragraphize(text):
    chunks = [chunk.strip() for chunk in (text or "").split("\n\n") if chunk.strip()]
    return "\n".join(f"            <p>{esc(chunk).replace(chr(10), '<br>')}</p>" for chunk in chunks)


def build():
    posts = json.loads(DATA.read_text(encoding="utf-8"))
    POSTS_DIR.mkdir(exist_ok=True)

    for post in posts:
        post["file"] = f"posts/{slug_for(post)}.html"
        post["categoryKey"] = CATEGORY_KEYS.get(post["category"], "all")

    cards = []
    for post in posts:
        summary = (post.get("content") or "").replace("\n", " ")
        if len(summary) > 180:
            summary = summary[:180].rstrip() + "..."
        image = f'<img src="{esc(post.get("image"))}" alt="{esc(post["title"])}">' if post.get("image") else '<div class="blog-thumb-placeholder"></div>'
        cards.append(f"""          <article class="blog-card" data-category="{esc(post["categoryKey"])}">
            <a class="blog-thumb" href="{esc(post["file"])}">{image}</a>
            <div class="blog-card-body">
              <p class="blog-meta">{esc(post["category"])} · {esc(post.get("date"))} · {esc(post.get("readTime"))}</p>
              <h2><a href="{esc(post["file"])}">{esc(post["title"])}</a></h2>
              <p>{esc(summary)}</p>
            </div>
          </article>""")

    blog_body = f"""
    <main class="blog-page">
      <section class="blog-hero">
        <p>Development Blog</p>
        <h1>블로그</h1>
      </section>
      <section class="blog-wrap">
        <div class="blog-filters" aria-label="블로그 카테고리">
          <button type="button" class="active" data-filter="all">AllPOST</button>
          <button type="button" data-filter="2d-applestory">2D AppleStory</button>
          <button type="button" data-filter="3d-rpg">3D RPG</button>
          <button type="button" data-filter="towerrandomdefence">TowerRandomDefence</button>
        </div>
        <div class="blog-list">
{os.linesep.join(cards)}
        </div>
      </section>
    </main>
    <script>
      const buttons = document.querySelectorAll('.blog-filters button');
      const cards = document.querySelectorAll('.blog-card');
      buttons.forEach((button) => {{
        button.addEventListener('click', () => {{
          buttons.forEach((item) => item.classList.remove('active'));
          button.classList.add('active');
          const filter = button.dataset.filter;
          cards.forEach((card) => {{
            card.hidden = filter !== 'all' && card.dataset.category !== filter;
          }});
        }});
      }});
    </script>
"""
    (ROOT / "blog.html").write_text(shell("블로그 | 이성호", "Unity 개발 블로그", blog_body), encoding="utf-8")

    for post in posts:
        image = f'<img class="post-image" src="{esc(post.get("image"))}" alt="{esc(post["title"])}">' if post.get("image") else ""
        post_body = f"""
    <main class="post-page">
      <article class="post-article">
        <a class="back-link" href="../blog.html">블로그로 돌아가기</a>
        <p class="blog-meta">{esc(post["category"])} · {esc(post.get("date"))} · {esc(post.get("readTime"))}</p>
        <h1>{esc(post["title"])}</h1>
        {image}
        <div class="post-content">
{paragraphize(post.get("content"))}
        </div>
      </article>
    </main>
"""
        (ROOT / post["file"]).write_text(shell(f"{post['title']} | 이성호", post["title"], post_body, "../"), encoding="utf-8")


if __name__ == "__main__":
    build()
