# Website Scraper - Hacker News Monitoring Dashboard

This project is a university Cyber Security IT360 project.

The original project topic is **Project 8: Website Scraper**.  
Our final implementation is a **Hacker News Monitoring Dashboard**.

## Project Idea

This project is not trying to rebuild Hacker News.

Instead, it collects selected Hacker News stories from the Hacker News API, extracts useful information, classifies stories into technology categories, assigns priority levels, displays the results in an interactive dashboard, and allows exporting the data as CSV files.

The goal is to transform raw Hacker News stories into structured, classified, prioritized, and exportable information.

## Main Features

- Fetches top stories from the Hacker News API
- Extracts useful fields:
  - rank
  - title
  - author
  - score
  - comments
  - date/time
  - link
- Classifies stories using rule-based keyword matching
- Uses safer regex matching to avoid fake keyword matches
  - Example: AI should not match inside the word "fail"
- Classifies stories into categories:
  - AI
  - Cybersecurity
  - Programming
  - Web Development
  - Data & Databases
  - Cloud & DevOps
  - Startups & Business
  - Hardware
  - Science & Research
  - Crypto & Blockchain
  - General Tech
  - Other
- Assigns priority levels:
  - High
  - Medium
  - Low
- Displays dashboard statistics:
  - stories collected
  - matched keywords
  - average score
  - cybersecurity stories
  - high priority stories
  - most active category
- Shows a category chart using Chart.js
- Shows top matched keywords
- Supports search
- Supports category filtering
- Supports priority filtering
- Provides a story details drawer with classification reason
- Saves results to CSV
- Allows exporting:
  - all stories
  - filtered stories

## Technologies Used

- Python
- Flask
- Requests
- Pandas
- Regex
- HTML
- CSS
- JavaScript
- Chart.js
- Hacker News API
- CSV storage
- GitHub

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
├── docs/
│   ├── task1_main_concepts.md
│   ├── task2_existing_solutions.md
│   ├── task3_high_level_design.md
│   ├── task4_tools_and_phases.md
│   └── diagrams/
│
├── screenshots/
│
└── presentation/
    └── Project_Presentation.pdf

## How to Run the Application

1. Clone or download the repository.

```bash
git clone https://github.com/nourkaibi/Website-Scraper-.git

2. Open the project folder.

cd Website-Scraper-

3. Install the required libraries.

pip install -r requirements.txt

Or install them manually:

pip install flask requests pandas

4. Run the Flask application.
python app.py

5.Open the dashboard in the browser.

http://127.0.0.1:5000