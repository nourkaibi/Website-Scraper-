from flask import Flask, render_template, jsonify, send_file
import requests
import pandas as pd
from datetime import datetime
import os
import re

app = Flask(__name__)

HN_BASE_URL = "https://hacker-news.firebaseio.com/v0"
CSV_FILE = "data/hacker_news_stories.csv"

CATEGORIES = {
    "AI": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "llm",
        "large language model",
        "gpt",
        "openai",
        "chatgpt",
        "claude",
        "gemini",
        "neural network",
        "computer vision",
        "natural language processing",
        "nlp",
        "model training",
        "inference"
    ],

    "Cybersecurity": [
        "security",
        "cybersecurity",
        "cyber",
        "hacker",
        "hacking",
        "malware",
        "ransomware",
        "phishing",
        "vulnerability",
        "exploit",
        "breach",
        "privacy",
        "encryption",
        "cve",
        "zero-day",
        "zeroday",
        "authentication",
        "password",
        "2fa",
        "oauth",
        "firewall"
    ],

    "Programming": [
        "programming",
        "code",
        "coding",
        "developer",
        "software",
        "python",
        "javascript",
        "typescript",
        "java",
        "rust",
        "go",
        "golang",
        "c++",
        "c#",
        "php",
        "ruby",
        "swift",
        "kotlin",
        "linux",
        "github",
        "open source",
        "compiler",
        "debugging"
    ],

    "Web Development": [
        "web",
        "frontend",
        "backend",
        "full stack",
        "html",
        "css",
        "react",
        "vue",
        "angular",
        "node",
        "node.js",
        "next.js",
        "api",
        "rest api",
        "graphql",
        "browser",
        "chrome",
        "firefox"
    ],

    "Data & Databases": [
        "data",
        "database",
        "databases",
        "sql",
        "nosql",
        "postgres",
        "postgresql",
        "mysql",
        "sqlite",
        "mongodb",
        "redis",
        "analytics",
        "dataset",
        "data pipeline",
        "warehouse",
        "bigquery",
        "snowflake"
    ],

    "Cloud & DevOps": [
        "cloud",
        "aws",
        "azure",
        "google cloud",
        "gcp",
        "docker",
        "kubernetes",
        "k8s",
        "devops",
        "ci/cd",
        "terraform",
        "serverless",
        "infrastructure",
        "deployment",
        "monitoring",
        "observability",
        "sre"
    ],

    "Startups & Business": [
        "startup",
        "startups",
        "founder",
        "co-founder",
        "funding",
        "venture",
        "vc",
        "yc",
        "y combinator",
        "business",
        "company",
        "saas",
        "product",
        "market",
        "revenue",
        "ipo",
        "acquisition"
    ],

    "Hardware": [
        "hardware",
        "chip",
        "chips",
        "semiconductor",
        "cpu",
        "gpu",
        "nvidia",
        "amd",
        "intel",
        "arm",
        "risc-v",
        "raspberry pi",
        "robot",
        "robotics",
        "device",
        "sensor",
        "battery"
    ],

    "Science & Research": [
        "science",
        "research",
        "paper",
        "study",
        "physics",
        "biology",
        "chemistry",
        "mathematics",
        "math",
        "space",
        "nasa",
        "climate",
        "energy",
        "medicine",
        "medical",
        "genomics"
    ],

    "Crypto & Blockchain": [
        "crypto",
        "cryptocurrency",
        "bitcoin",
        "ethereum",
        "blockchain",
        "web3",
        "wallet",
        "token",
        "nft",
        "defi",
        "smart contract"
    ]
}

def classify_story(title):
    if not title:
        return "Other", "No match"

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
            if re.search(pattern, title_lower):
                return category, keyword

    return "Other", "No match"


def fetch_hacker_news_stories(limit=30):
    stories = []

    try:
        response = requests.get(f"{HN_BASE_URL}/topstories.json", timeout=10)
        response.raise_for_status()
        story_ids = response.json()[:limit]

        for index, story_id in enumerate(story_ids, start=1):
            item_response = requests.get(
                f"{HN_BASE_URL}/item/{story_id}.json",
                timeout=10
            )
            item_response.raise_for_status()

            item = item_response.json()

            if not item:
                continue

            title = item.get("title", "No title")
            unix_time = item.get("time")

            if unix_time:
                readable_time = datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M")
            else:
                readable_time = "Unknown"

            category, matched_keyword = classify_story(title)

            story = {
                "rank": index,
                "id": item.get("id"),
                "title": title,
                "author": item.get("by", "Unknown"),
                "score": item.get("score", 0),
                "time": readable_time,
                "url": item.get(
                    "url",
                    f"https://news.ycombinator.com/item?id={item.get('id')}"
                ),
                "comments": item.get("descendants", 0),
                "category": category,
                "matched_keyword": matched_keyword
            }

            stories.append(story)

    except requests.RequestException as error:
        print(f"Error fetching Hacker News data: {error}")

    return stories


def save_to_csv(stories):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(stories)
    df.to_csv(CSV_FILE, index=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/stories")
def get_stories():
    stories = fetch_hacker_news_stories(limit=30)
    save_to_csv(stories)
    return jsonify(stories)


@app.route("/export")
def export_csv():
    if not os.path.exists(CSV_FILE):
        stories = fetch_hacker_news_stories(limit=30)
        save_to_csv(stories)

    return send_file(CSV_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)