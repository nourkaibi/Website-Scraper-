# Website Scraper - Hacker News Monitoring Dashboard

This project is a university Cyber Security IT360 project.

The original project topic is **Project 8: Website Scraper**.  
Our final implementation is a **Hacker News Monitoring Dashboard**.

## Project Idea

This project is not trying to rebuild Hacker News.

Instead, it collects selected Hacker News stories, extracts useful information, classifies stories into categories, displays them in a dashboard, and allows exporting the results as a CSV file.

## Main Features

- Fetches stories from Hacker News
- Extracts useful fields:
  - title
  - author
  - score
  - comments
  - date/time
  - link
- Classifies stories using keyword matching
- Uses expanded categories:
  - AI
  - Security
  - Programming
  - Startup
  - Data
  - Hardware
  - Science
  - Web
  - DevOps
  - Careers
  - Policy
  - Other
- Avoids fake keyword matches
- Displays results in a dashboard
- Supports search
- Supports category filtering
- Shows basic statistics
- Shows a category chart
- Saves results to CSV
- Allows CSV export

## Technologies Used

- Python
- Flask
- Requests
- Pandas
- HTML
- CSS
- JavaScript
- Chart.js
- Hacker News API

## Folder Structure

```text
website-scraper/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── hacker_news_stories.csv
│
├── templates/
│   └── index.html
│
├── static/
│   ├── logo.png
│   ├── style.css
│   └── script.js
│
└── docs/
    ├── task1_main_concepts.md
    ├── task2_existing_solutions.md
    ├── task3_high_level_design.md
    └── task4_tools_and_phases.md