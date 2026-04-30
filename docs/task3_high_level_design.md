Data flows as follows:
Hacker News API → Data Collection → Processing & Classification → Storage → Backend → Frontend
Dashboard → User
System Components
The seven core components and their responsibilities are:
1. Frontend Dashboard
• Displays collected stories in a structured table with summary cards.
• Supports search, keyword filtering, refresh, and export controls.
2. Backend Application Server
• Handles requests from the frontend and coordinates all modules.
• Returns processed, organized data to the dashboard.
3. Data Collection Module
• Retrieves story IDs and detailed fields: title, author, score, date, and link.
• Serves as the system's entry point for real story data.
4. Data Processing & Classification Module
• Cleans and validates raw data; converts timestamps to readable format.
• Assigns topic labels (e.g., AI, Security, Startup, Programming, Data) based on title
keywords.
Page 2
Project 8: Website Scraper — Cyber Security IT360
5. Storage Module
• Persists processed data using CSV files or a SQLite database.
• Makes results available for display and export across executions.
6. Export Module
• Enables users to download results as CSV or Excel files for further analysis.
7. Logging & Error Handling Module
• Records operations, detects missing or invalid data, and logs failures.
• Prevents silent crashes and simplifies debugging.
Data Flow
The end-to-end data flow in ten steps:
1. The user opens the dashboard.
2. The frontend requests the latest stories from the backend.
3. The backend triggers the Data Collection Module.
4. Story data is retrieved from the Hacker News API.
5. Raw data is passed to the Processing & Classification Module.
6. The system cleans, formats, and categorizes the stories.
7. Processed data is saved to the Storage Module.
8. The backend returns the results to the frontend.
9. The dashboard renders tables, summary cards, and charts.
10. The user can search, filter, refresh, or export the data.
Key Features & Added Value
• Display recent stories with title, author, score, date, and link.
• Classify stories into predefined topics for targeted monitoring.
• Search and filter within the collected dataset.
• Show dashboard statistics (story count, keyword distribution).
• Export data to CSV or Excel for external reporting.
Unlike browsing Hacker News directly, this dashboard organizes stories into meaningful
categories, shows summary analytics, and supports data export — making it a genuine monitoring
tool rather than a simple feed viewer.
Page 3
Project 8: Website Scraper — Cyber Security IT360
Step 4: Tools & Development Phases
Technology Stack
Backend
• Python — main language for backend logic and data processing; readable, widely used
in automation and cybersecurity.
• Flask — lightweight web framework for routing, API endpoints, and connecting frontend
to backend.
• Requests library — HTTP calls to the Hacker News API for story retrieval.
• JSON (built-in) — parses story objects returned by the API.
Frontend
• HTML / CSS / JavaScript — builds the dashboard layout, tables, filters, and interactive
controls.
• Bootstrap (optional) — responsive design components to improve visual polish quickly.
• Chart.js (optional) — displays category distributions and score trends as charts.
Data & Storage
• CSV / SQLite — CSV for a minimal implementation; SQLite for persistent, queryable
storage.
• Pandas (optional) — simplifies data cleaning, deduplication, and CSV export.
Development Phases
Phase 1 — Planning
Define project scope, data fields to collect, keyword categories, and dashboard features.
Phase 2 — Environment Setup
Install Python, Flask, and required libraries; create folder structure; verify local environment.
Phase 3 — Data Retrieval
Build the data collection module: fetch story IDs and detailed fields from the Hacker News API;
test retrieval.
Phase 4 — Processing & Classification
Clean and validate data, format timestamps, and assign topic labels based on title keywords.
Phase 5 — Storage & Export
Implement CSV/SQLite storage and export functionality; test data persistence and file output.
Page 4
Project 8: Website Scraper — Cyber Security IT360
Phase 6 — Dashboard Interface
Design the frontend: story table, summary cards, search/filter controls, refresh, and export
buttons.
Phase 7 — Integration
Connect frontend to backend routes; test live data display, filters, and export from the interface.
Phase 8 — Testing & Debugging
Verify data accuracy, search/filtering, export output, and error handling; fix identified bugs.
Phase 9 — Documentation & Submission
Document code, prepare screenshots and sample outputs, finalize report, and prepare for
presentation.
Expected Deliverables
• Working backend application (Python + Flask).
• Functional frontend dashboard with search, filter, and export.
• Data collection and processing modules with keyword classification.
• Storage mechanism (CSV or SQLite) and export functionality.
• Sample output files and final project report.
Anticipated Challenges
• Parsing and handling inconsistent API response structures.
• Connecting frontend and backend without errors.
• Designing accurate keyword classification rules.
• Managing time across integration, testing, and documentation phases.
These risks are mitigated by implementing and testing the project incrementally, one phase at a
time.
