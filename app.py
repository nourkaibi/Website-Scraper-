from flask import Flask, render_template, request, send_file
import requests
import pandas as pd
import re
import os
from io import BytesIO
from datetime import datetime

app = Flask(__name__)

CSV_PATH = "data/hacker_news_stories.csv"


# -----------------------------
# 1. Category keywords
# -----------------------------
CATEGORY_KEYWORDS = {
    "AI": [
        "ai", "llm", "gpt", "chatgpt", "claude", "gemini", "copilot",
        "machine learning", "artificial intelligence", "deep learning",
        "neural network", "transformer", "model", "inference", "prompt",
        "agent", "agents", "embedding", "rag", "openai", "generative ai"
    ],

    "Cybersecurity": [
        "cve", "exploit", "malware", "breach", "ransomware", "vulnerability",
        "phishing", "zero-day", "botnet", "security", "infosec", "cyber",
        "attack", "threat", "backdoor", "leak", "ddos", "spyware",
        "trojan", "encryption", "authentication", "password", "privacy",
        "token", "firewall", "bug bounty", "data leak"
    ],

    "Programming": [
        "python", "javascript", "typescript", "java", "rust", "golang",
        "programming", "coding", "developer", "software", "framework",
        "compiler", "open source", "api", "library", "sdk", "debug",
        "debugging", "git", "github", "code", "cli", "terminal", "package",
        "repository", "release"
    ],

    "Web Development": [
        "react", "vue", "angular", "frontend", "backend", "html", "css",
        "web", "node", "next.js", "nuxt", "browser", "webapp", "http",
        "website", "server", "django", "flask", "fastapi", "javascript",
        "typescript", "api"
    ],

    "Data & Databases": [
        "sql", "database", "postgres", "postgresql", "mysql", "sqlite",
        "mongodb", "redis", "data engineering", "analytics", "etl",
        "warehouse", "bigquery", "spark", "data pipeline", "dataset",
        "csv", "json", "query", "data", "storage", "vector database"
    ],

    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "devops", "cloud",
        "infrastructure", "terraform", "ci/cd", "deployment", "serverless",
        "observability", "monitoring", "container", "linux", "server",
        "hosting", "network"
    ],

    "Startups & Business": [
        "startup", "funding", "founder", "saas", "business", "market",
        "revenue", "venture", "product", "company", "acquisition", "pricing",
        "customer", "sales", "founders", "startup", "investor", "ipo"
    ],

    "Hardware": [
        "chip", "cpu", "gpu", "hardware", "semiconductor", "raspberry pi",
        "amd", "intel", "nvidia", "device", "embedded", "firmware",
        "robot", "laptop", "memory", "processor", "arm", "risc-v"
    ],

    "Science & Research": [
        "research", "study", "science", "paper", "experiment", "physics",
        "biology", "chemistry", "astronomy", "mathematics", "academic",
        "university", "lab", "scientists", "medicine", "space"
    ],

    "Crypto & Blockchain": [
        "crypto", "bitcoin", "ethereum", "blockchain", "token", "web3",
        "defi", "wallet", "nft", "solana", "mining", "smart contract"
    ],

    "General Tech": [
        "show hn", "ask hn", "tool", "app", "platform", "system",
        "technology", "internet", "digital", "online", "computer",
        "build", "built", "launch", "release", "project", "service"
    ]
}


# -----------------------------
# 2. High priority terms
# -----------------------------
HIGH_PRIORITY_TERMS = [
    "cve", "exploit", "malware", "breach", "ransomware", "vulnerability",
    "zero-day", "phishing", "backdoor", "trojan", "spyware", "leak", "attack"
]


# -----------------------------
# 3. Safe keyword matching
# -----------------------------
def keyword_in_text(keyword, text):
    """
    Uses word boundaries to avoid fake matches.
    Example: 'ai' should not match inside 'fail'.
    """
    keyword = keyword.lower()
    text = text.lower()

    pattern = r"\b" + re.escape(keyword) + r"\b"
    return re.search(pattern, text, re.IGNORECASE) is not None


# -----------------------------
# 4. Classification function
# -----------------------------
def classify_story(title, link=""):
    """
    Classifies a story using title + link.
    This improves classification because some useful words appear in the URL.
    """
    text = f"{title} {link}".lower()

    category_scores = {}
    category_matches = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        matches = []

        for keyword in keywords:
            if keyword_in_text(keyword, text):
                matches.append(keyword)

        if matches:
            category_scores[category] = len(matches)
            category_matches[category] = matches

    if not category_scores:
        return {
            "category": "Other",
            "matched_keyword": "None",
            "matched_keywords": [],
            "classification_reason": "This story was classified as Other because no category keyword was matched."
        }

    best_category = max(category_scores, key=category_scores.get)
    matched_keywords = category_matches[best_category]
    primary_keyword = matched_keywords[0]

    classification_reason = (
        f"This story was classified as {best_category} because it matched "
        f"{len(matched_keywords)} keyword(s): {', '.join(matched_keywords)}."
    )

    return {
        "category": best_category,
        "matched_keyword": primary_keyword,
        "matched_keywords": matched_keywords,
        "classification_reason": classification_reason
    }


# -----------------------------
# 5. Priority function
# -----------------------------
def assign_priority(category, score, comments, title, matched_keywords):
    text = title.lower()
    matched_keywords_lower = [keyword.lower() for keyword in matched_keywords]

    if (
        category == "Cybersecurity"
        or score >= 200
        or comments >= 100
        or any(term in matched_keywords_lower for term in HIGH_PRIORITY_TERMS)
        or any(keyword_in_text(term, text) for term in HIGH_PRIORITY_TERMS)
    ):
        return "High"

    if score >= 75 or comments >= 30:
        return "Medium"

    return "Low"


# -----------------------------
# 6. Fetch Hacker News stories
# -----------------------------
def fetch_hacker_news_stories(limit=100):
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    item_base_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

    try:
        response = requests.get(top_stories_url, timeout=15)
        response.raise_for_status()
        top_story_ids = response.json()[:limit]
    except requests.RequestException:
        return []

    stories = []

    for rank, story_id in enumerate(top_story_ids, start=1):
        try:
            story_response = requests.get(item_base_url.format(story_id), timeout=15)
            story_response.raise_for_status()
            story_data = story_response.json()
        except requests.RequestException:
            continue

        if not story_data or story_data.get("type") != "story":
            continue

        title = story_data.get("title", "No title")
        author = story_data.get("by", "Unknown")
        score = story_data.get("score", 0)
        comments = story_data.get("descendants", 0)
        timestamp = story_data.get("time", 0)

        date_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        link = story_data.get(
            "url",
            f"https://news.ycombinator.com/item?id={story_id}"
        )

        classification = classify_story(title, link)

        category = classification["category"]
        matched_keyword = classification["matched_keyword"]
        matched_keywords = classification["matched_keywords"]
        classification_reason = classification["classification_reason"]

        priority = assign_priority(
            category,
            score,
            comments,
            title,
            matched_keywords
        )

        stories.append({
            "rank": rank,
            "title": title,
            "author": author,
            "score": score,
            "comments": comments,
            "date_time": date_time,
            "link": link,
            "category": category,
            "matched_keyword": matched_keyword,
            "matched_keywords": ", ".join(matched_keywords) if matched_keywords else "None",
            "priority": priority,
            "classification_reason": classification_reason
        })

    return stories


# -----------------------------
# 7. CSV functions
# -----------------------------
def save_to_csv(stories):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(stories)
    df.to_csv(CSV_PATH, index=False)


def load_csv():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame()


# -----------------------------
# 8. Main dashboard route
# -----------------------------
@app.route("/")
def index():
    stories = fetch_hacker_news_stories(limit=100)
    save_to_csv(stories)

    category_counts = {}
    keyword_counts = {}

    matched_keywords_count = 0
    cybersecurity_count = 0
    high_priority_count = 0
    total_score = 0

    for story in stories:
        total_score += story["score"]

        category = story["category"]
        category_counts[category] = category_counts.get(category, 0) + 1

        if story["matched_keywords"] != "None":
            keywords = [
                keyword.strip()
                for keyword in story["matched_keywords"].split(",")
                if keyword.strip()
            ]

            matched_keywords_count += len(keywords)

            for keyword in keywords:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

        if category == "Cybersecurity":
            cybersecurity_count += 1

        if story["priority"] == "High":
            high_priority_count += 1

    average_score = round(total_score / len(stories), 1) if stories else 0

    most_active_category = (
        max(category_counts, key=category_counts.get)
        if category_counts
        else "Other"
    )

    top_keywords = sorted(
        keyword_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:8]

    stats = {
        "stories_collected": len(stories),
        "matched_keywords": matched_keywords_count,
        "average_score": average_score,
        "cybersecurity_stories": cybersecurity_count,
        "high_priority_stories": high_priority_count,
        "most_active_category": most_active_category
    }

    return render_template(
        "index.html",
        stories=stories,
        stats=stats,
        category_counts=category_counts,
        top_keywords=top_keywords
    )


# -----------------------------
# 9. Export all stories
# -----------------------------
@app.route("/export/all")
def export_all():
    if not os.path.exists(CSV_PATH):
        return "CSV file not found. Please refresh the dashboard first.", 404

    return send_file(
        CSV_PATH,
        as_attachment=True,
        download_name="hacker_news_stories.csv"
    )


# -----------------------------
# 10. Export filtered stories
# -----------------------------
@app.route("/export/filtered")
def export_filtered():
    df = load_csv()

    if df.empty:
        return "CSV file not found or empty. Please refresh the dashboard first.", 404

    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "").strip().lower()
    priority = request.args.get("priority", "").strip().lower()

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["title"].astype(str).str.lower().str.contains(search, na=False)
            | filtered_df["author"].astype(str).str.lower().str.contains(search, na=False)
            | filtered_df["category"].astype(str).str.lower().str.contains(search, na=False)
            | filtered_df["matched_keywords"].astype(str).str.lower().str.contains(search, na=False)
        ]

    if category:
        filtered_df = filtered_df[
            filtered_df["category"].astype(str).str.lower() == category
        ]

    if priority:
        filtered_df = filtered_df[
            filtered_df["priority"].astype(str).str.lower() == priority
        ]

    output = BytesIO()
    csv_string = filtered_df.to_csv(index=False)
    output.write(csv_string.encode("utf-8"))
    output.seek(0)

    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="filtered_hacker_news_stories.csv"
    )


# -----------------------------
# 11. Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)