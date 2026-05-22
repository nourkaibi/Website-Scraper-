document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const categoryFilter = document.getElementById("categoryFilter");
    const priorityFilter = document.getElementById("priorityFilter");
    const rows = document.querySelectorAll("#storiesTable tbody tr");

    const storyDrawer = document.getElementById("storyDrawer");
    const drawerOverlay = document.getElementById("drawerOverlay");
    const closeDrawer = document.getElementById("closeDrawer");

    const aboutBtn = document.getElementById("aboutBtn");
    const aboutModal = document.getElementById("aboutModal");
    const closeAbout = document.getElementById("closeAbout");

    const exportFilteredBtnBottom = document.getElementById("exportFilteredBtnBottom");

    function filterStories() {
        const search = searchInput.value.toLowerCase().trim();
        const category = categoryFilter.value.toLowerCase().trim();
        const priority = priorityFilter.value.toLowerCase().trim();

        rows.forEach(row => {
            const title = row.dataset.title.toLowerCase();
            const rowCategory = row.dataset.category.toLowerCase();
            const rowPriority = row.dataset.priority.toLowerCase();

            const matchesSearch = !search || title.includes(search);
            const matchesCategory = !category || rowCategory === category;
            const matchesPriority = !priority || rowPriority === priority;

            row.style.display = (matchesSearch && matchesCategory && matchesPriority) ? "" : "none";
        });
    }

    function openDrawer(row) {
        document.getElementById("drawerTitle").textContent = row.dataset.title;
        document.getElementById("drawerAuthor").textContent = row.dataset.author;
        document.getElementById("drawerScore").textContent = row.dataset.score;
        document.getElementById("drawerComments").textContent = row.dataset.comments;
        document.getElementById("drawerCategory").textContent = row.dataset.category;
        document.getElementById("drawerKeyword").textContent = row.dataset.keyword;
        document.getElementById("drawerPriority").textContent = row.dataset.priority;
        document.getElementById("drawerDate").textContent = row.dataset.date;
        document.getElementById("drawerReason").textContent = row.dataset.reason;
        document.getElementById("drawerLink").href = row.dataset.link;

        storyDrawer.classList.remove("hidden");
        drawerOverlay.classList.remove("hidden");
        storyDrawer.setAttribute("aria-hidden", "false");
    }

    function closeDrawerPanel() {
        storyDrawer.classList.add("hidden");
        drawerOverlay.classList.add("hidden");
        storyDrawer.setAttribute("aria-hidden", "true");
    }

    function exportFilteredStories() {
        const search = encodeURIComponent(searchInput.value.trim());
        const category = encodeURIComponent(categoryFilter.value.trim());
        const priority = encodeURIComponent(priorityFilter.value.trim());

        window.location.href = `/export/filtered?search=${search}&category=${category}&priority=${priority}`;
    }

    searchInput.addEventListener("input", filterStories);
    categoryFilter.addEventListener("change", filterStories);
    priorityFilter.addEventListener("change", filterStories);

    document.querySelectorAll(".details-btn").forEach(button => {
        button.addEventListener("click", () => {
            const row = button.closest("tr");
            openDrawer(row);
        });
    });

    closeDrawer.addEventListener("click", closeDrawerPanel);
    drawerOverlay.addEventListener("click", closeDrawerPanel);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeDrawerPanel();
            aboutModal.classList.add("hidden");
        }
    });

    aboutBtn.addEventListener("click", () => {
        aboutModal.classList.remove("hidden");
    });

    closeAbout.addEventListener("click", () => {
        aboutModal.classList.add("hidden");
    });

    aboutModal.addEventListener("click", (event) => {
        if (event.target === aboutModal) {
            aboutModal.classList.add("hidden");
        }
    });

    if (exportFilteredBtnBottom) {
        exportFilteredBtnBottom.addEventListener("click", exportFilteredStories);
    }

    const chartCanvas = document.getElementById("categoryChart");

    if (chartCanvas && typeof categoryData !== "undefined") {
        const labels = Object.keys(categoryData);
        const values = Object.values(categoryData);

        if (labels.length > 0 && values.length > 0) {
            new Chart(chartCanvas, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Stories",
                        data: values,
                        backgroundColor: [
                            "#111111",
                            "#f4c524",
                            "#e1783c",
                            "#4f7d39",
                            "#c74d2d",
                            "#8a6a13",
                            "#d5b041",
                            "#5b5b5b",
                            "#e6d9b0",
                            "#a34d2f",
                            "#7d8f52",
                            "#2c5f8a"
                        ],
                        borderColor: "#111111",
                        borderWidth: 2,
                        borderRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: "#111111",
                            titleColor: "#ffffff",
                            bodyColor: "#ffffff",
                            borderColor: "#f4c524",
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                color: "#111111",
                                font: {
                                    weight: "700"
                                }
                            },
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: "#111111",
                                precision: 0,
                                stepSize: 1
                            },
                            grid: {
                                color: "rgba(17,17,17,0.12)"
                            }
                        }
                    }
                }
            });
        } else {
            chartCanvas.parentElement.innerHTML = `
                <div style="height:100%;display:flex;align-items:center;justify-content:center;font-weight:700;color:#5a544b;">
                    No category data available yet.
                </div>
            `;
        }
    }
});