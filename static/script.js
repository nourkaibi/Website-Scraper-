let allStories = [];
let selectedCategory = "All";
let categoryChart = null;

const sidebar = document.getElementById("sidebar");
const openSidebarBtn = document.getElementById("openSidebarBtn");
const closeSidebarBtn = document.getElementById("closeSidebarBtn");
const aboutPanel = document.getElementById("aboutPanel");

async function loadStories() {
    const tableBody = document.getElementById("storiesTable");
    tableBody.innerHTML = "<tr><td colspan='8'>Loading stories...</td></tr>";

    try {
        const response = await fetch("/api/stories");
        allStories = await response.json();

        selectedCategory = "All";
        setActiveFilterButton("All");

        updateLastUpdated();
        applyFilters();

    } catch (error) {
        tableBody.innerHTML = "<tr><td colspan='8'>Error loading stories. Please try again.</td></tr>";
        console.error(error);
    }
}

function applyFilters() {
    const searchValue = document.getElementById("searchInput").value.toLowerCase();

    const filteredStories = allStories.filter(story => {
        const title = String(story.title || "").toLowerCase();
        const author = String(story.author || "").toLowerCase();
        const category = String(story.category || "").toLowerCase();
        const matchedKeyword = String(story.matched_keyword || "").toLowerCase();

        const matchesSearch =
            title.includes(searchValue) ||
            author.includes(searchValue) ||
            category.includes(searchValue) ||
            matchedKeyword.includes(searchValue);

        const matchesCategory =
            selectedCategory === "All" || story.category === selectedCategory;

        return matchesSearch && matchesCategory;
    });

    updateStats(filteredStories);
    displayStories(filteredStories);
    updateChart(filteredStories);
}

function displayStories(stories) {
    const tableBody = document.getElementById("storiesTable");
    tableBody.innerHTML = "";

    if (stories.length === 0) {
        tableBody.innerHTML = "<tr><td colspan='8'>No stories found.</td></tr>";
        return;
    }

    stories.forEach(story => {
        const row = document.createElement("tr");

        const keywordHtml =
            story.matched_keyword === "No match"
                ? `<span class="keyword-empty">No match</span>`
                : `<span class="keyword-badge">${escapeHtml(story.matched_keyword)}</span>`;

        row.innerHTML = `
            <td data-label="Rank">${story.rank}</td>
            <td data-label="Title">${escapeHtml(story.title)}</td>
            <td data-label="Author">${escapeHtml(story.author)}</td>
            <td data-label="Score">${story.score}</td>
            <td data-label="Published">${escapeHtml(story.time)}</td>
            <td data-label="Category">
                <span class="category-badge ${getCategoryBadgeClass(story.category)}">
                    ${escapeHtml(story.category)}
                </span>
            </td>
            <td data-label="Keyword">${keywordHtml}</td>
            <td data-label="Link">
                <a href="${escapeHtml(story.url)}" target="_blank" class="open-link">
                    <i class="ri-external-link-line"></i>
                </a>
            </td>
        `;

        tableBody.appendChild(row);
    });
}

function updateStats(stories) {
    const totalStories = stories.length;

    const totalScore = stories.reduce((sum, story) => sum + story.score, 0);
    const averageScore = totalStories > 0 ? Math.round(totalScore / totalStories) : 0;

    const matchedKeywords = stories.filter(story => story.matched_keyword !== "No match").length;

    document.getElementById("totalStories").textContent = totalStories;
    document.getElementById("averageScore").textContent = averageScore;
    document.getElementById("matchedKeywords").textContent = matchedKeywords;
}

function updateLastUpdated() {
    const now = new Date();

    document.getElementById("lastUpdated").textContent = "Now";
    document.getElementById("lastUpdatedFull").textContent =
        now.toLocaleDateString() + " " + now.toLocaleTimeString();
}

function getCategoryCounts(stories) {
    const categories = [
    "AI",
    "Cybersecurity",
    "Programming",
    "Web Development",
    "Data & Databases",
    "Cloud & DevOps",
    "Startups & Business",
    "Hardware",
    "Science & Research",
    "Crypto & Blockchain",
    "Other"
];

   const counts = {
    "AI": 0,
    "Cybersecurity": 0,
    "Programming": 0,
    "Web Development": 0,
    "Data & Databases": 0,
    "Cloud & DevOps": 0,
    "Startups & Business": 0,
    "Hardware": 0,
    "Science & Research": 0,
    "Crypto & Blockchain": 0,
    "Other": 0
};
    stories.forEach(story => {
        if (counts.hasOwnProperty(story.category)) {
            counts[story.category]++;
        } else {
            counts["Other"]++;
        }
    });

    return {
        labels: categories,
        values: categories.map(category => counts[category])
    };
}

function updateChart(stories) {
    const chartData = getCategoryCounts(stories);
    const chartCanvas = document.getElementById("categoryChart");

    if (categoryChart !== null) {
        categoryChart.destroy();
    }

    categoryChart = new Chart(chartCanvas, {
        type: "bar",
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    label: "Stories",
                    data: chartData.values,
                    backgroundColor: "#3b82f6",
                    borderRadius: 6
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

function setActiveFilterButton(category) {
    const buttons = document.querySelectorAll(".filter-btn");

    buttons.forEach(button => {
        if (button.dataset.category === category) {
            button.classList.add("active");
        } else {
            button.classList.remove("active");
        }
    });
}

function setActiveNav(section) {
    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach(item => {
        if (item.dataset.section === section) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);

    if (section) {
        section.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}
function handleSidebarNavigation(section) {
    aboutPanel.classList.add("hidden");

    if (section === "dashboard") {
        setActiveNav("dashboard");
        scrollToSection("dashboardSection");
    }

    if (section === "stories") {
        setActiveNav("stories");
        scrollToSection("storiesSection");
    }

    if (section === "search") {
        setActiveNav("search");
        document.getElementById("searchInput").focus();
        scrollToSection("searchBox");
    }

    if (section === "keywords") {
        setActiveNav("keywords");
        scrollToSection("keywordsSection");
    }

    if (section === "about") {
        setActiveNav("about");
        aboutPanel.classList.remove("hidden");
        scrollToSection("aboutPanel");
    }
}

function closeSidebar() {
    sidebar.classList.add("closed");
}

function openSidebar() {
    sidebar.classList.remove("closed");
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

document.getElementById("searchInput").addEventListener("input", applyFilters);

document.querySelectorAll(".filter-btn").forEach(button => {
    button.addEventListener("click", function () {
        selectedCategory = this.dataset.category;
        setActiveFilterButton(selectedCategory);
        applyFilters();
    });
});

document.querySelectorAll(".nav-item[data-section]").forEach(item => {
    item.addEventListener("click", function () {
        handleSidebarNavigation(this.dataset.section);
    });
});

closeSidebarBtn.addEventListener("click", closeSidebar);
openSidebarBtn.addEventListener("click", openSidebar);

document.getElementById("profileBtn").addEventListener("click", function () {
    alert("Profile menu connected. You can add login/logout features here later.");
});

loadStories();
function getCategoryBadgeClass(category) {
    const badgeClasses = {
        "AI": "badge-AI",
        "Cybersecurity": "badge-Cybersecurity",
        "Programming": "badge-Programming",
        "Web Development": "badge-WebDevelopment",
        "Data & Databases": "badge-DataDatabases",
        "Cloud & DevOps": "badge-CloudDevOps",
        "Startups & Business": "badge-StartupsBusiness",
        "Hardware": "badge-Hardware",
        "Science & Research": "badge-ScienceResearch",
        "Crypto & Blockchain": "badge-CryptoBlockchain",
        "Other": "badge-Other"
    };

    return badgeClasses[category] || "badge-Other";
}