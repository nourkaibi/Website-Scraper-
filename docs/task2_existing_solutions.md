Project 8: Website Scraper
Course: Cyber Security IT360
Instructor: Manel Abdelkader
Group Members:
Elaa Ben Ayech
Hadil Tlili
Maha Wanna
Nour ElHouda Kaibi
Major/Minor: BA/IT
Academic Year: 2025/2026
Task 1: Main Concepts of Web Scraping
1. Introduction
A web scraper is a software system designed to automatically collect data from websites.
Instead of manually browsing pages and copying information, a scraper sends requests to web
servers, retrieves web content, extracts relevant information, and stores it in a structured
format such as CSV, JSON, or a database.
Web scraping plays an important role in many domains including business intelligence, research,
and cybersecurity. It allows organizations to collect large volumes of data efficiently and analyze
them for insights, trends, or threats.
2. Fundamental Concepts
HTTP Requests
Web scraping begins with sending HTTP or HTTPS requests to a website’s server, similar to how
a browser loads a webpage.
HTML Structure
Web pages are built using HTML. The scraper reads the page structure and identifies where
useful data is located.
Parsing
Parsing is the process of analyzing the HTML content to locate specific elements such as tags,
classes, or IDs.
Data Extraction
Once the correct elements are identified, the scraper extracts useful information such as titles,
prices, dates, or user comments.
Data Cleaning
The extracted data is often unstructured and must be cleaned by removing duplicates,
formatting text, and handling missing values.
Data Storage
The processed data is stored in formats such as CSV files, Excel sheets, JSON files, or databases
for further use.
Automation
Scrapers can run automatically at scheduled times, allowing continuous data collection.
3. Architecture of a Web Scraper
A robust scraper architecture includes several layers: a networking layer for sending requests, a
parsing engine for analyzing HTML or DOM structures, an extraction layer for collecting relevant
data, a processing layer for cleaning and validation, and a storage layer for persistence.
Advanced systems also include proxy management, scheduling, and fault tolerance mechanisms.
A typical web scraping system consists of:
Request Module:
Sends requests to the target website
Parser Module:
Analyzes HTML content
Extractor Module:
Retrieves required data
Data Processing Module:
Cleans and formats data
Storage Module:
Saves data into files or databases
Controller/Scheduler:
Manages execution and repetition
Error Handling Module:
Handles failures such as connection issues
4. Workflow Steps
1) Define the target website and required data
2) Send a request to the website
3) Receive the webpage content
4) Parse the HTML structure
5) Extract the relevant data
6) Clean and process the data
7) Store the data in a structured format
8) Repeat the process if needed
5. Security and Ethical and Legal Aspects
Since this project is related to cybersecurity, it is important to consider:
o Scraping should only target publicly accessible data
o Respect website policies such as robots.txt and terms of service
o Avoid sending excessive requests that may overload servers
o Protect collected data from unauthorized access
o Avoid scraping sensitive or personal data without permission
o Ensure compliance with legal regulations
6. Conclusion
Web scraping is a powerful technique for collecting and analyzing large amounts of web data. It
automates repetitive tasks and enables organizations to gain insights efficiently. However, it
must be used responsibly, especially in cybersecurity contexts where data sensitivity and ethical
considerations are critical.
