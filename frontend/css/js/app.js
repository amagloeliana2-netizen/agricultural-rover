const HERO_IMAGE_URL =
    "https://images.openai.com/static-rsc-4/YoP7bA49mWh92OB5yE94ufui8HUXXf1UTcKB9NKxvoavVEi26ViWGA1Mzc8VZQcLsiD5x3jEEZIHviCXPub0h0N2NVXBRVLm1sFIP_kwGRFnt5PHNypgmS_yugSydtM-3dxHP6yuQVuRokJz6qgtAIVNU2UnIvHdDs8as2iwrRMwtqLcX8Kw58Dn0jHVnTFO?purpose=fullsize";


document.addEventListener("DOMContentLoaded", () => {
    initializeNavigation();
    initializeScrollState();
    initializeHeroImage();
    refreshDashboard();

    // Refresh live rover data every 5 seconds.
    setInterval(refreshDashboard, 5000);
});


function initializeNavigation() {
    const links = document.querySelectorAll(".main-nav a");

    links.forEach(link => {
        link.addEventListener("click", event => {
            const href = link.getAttribute("href");

            if (!href || !href.startsWith("#")) {
                return;
            }

            const target = document.querySelector(href);

            if (!target) {
                return;
            }

            event.preventDefault();

            target.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        });
    });
}


function initializeScrollState() {
    const sections = document.querySelectorAll("main section[id]");
    const links = document.querySelectorAll(".main-nav a");

    if (!sections.length || !links.length) {
        return;
    }

    const observer = new IntersectionObserver(
        entries => {
            entries.forEach(entry => {
                if (!entry.isIntersecting) {
                    return;
                }

                const id = entry.target.id;

                links.forEach(link => {
                    const active =
                        link.getAttribute("href") === `#${id}`;

                    if (active) {
                        link.setAttribute("aria-current", "page");
                    } else {
                        link.removeAttribute("aria-current");
                    }
                });
            });
        },
        {
            rootMargin: "-35% 0px -55% 0px"
        }
    );

    sections.forEach(section => {
        observer.observe(section);
    });
}


function initializeHeroImage() {
    const heroDiagram =
        document.querySelector(".hero-figure .rover-diagram");

    if (!heroDiagram) {
        return;
    }

    const image = document.createElement("img");

    image.src = HERO_IMAGE_URL;

    image.alt =
        "Agricultural field rover operating between crop rows with cameras and positioning equipment.";

    image.className = "hero-rover-image";

    image.loading = "eager";

    image.decoding = "async";

    image.style.width = "100%";
    image.style.height = "auto";
    image.style.display = "block";
    image.style.aspectRatio = "16 / 9";
    image.style.objectFit = "cover";
    image.style.objectPosition = "center 65%";

    heroDiagram.replaceWith(image);

    const figureHeader =
        document.querySelector(".hero-figure .figure-header");

    if (figureHeader) {
        const spans =
            figureHeader.querySelectorAll("span");

        if (spans.length >= 2) {
            spans[0].textContent = "FIG. 1";
            spans[1].textContent = "FIELD ROVER";
        }
    }

    const caption =
        document.querySelector(".hero-figure .figure-caption");

    if (caption) {
        const captionText =
            caption.querySelector("span");

        if (captionText) {
            captionText.textContent =
                "Fig. 1 — Agricultural field rover reference platform.";
        }
    }
}


async function apiRequest(endpoint, options = {}) {
    const response = await fetch(endpoint, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        },
        ...options
    });

    if (!response.ok) {
        throw new Error(
            `Request failed: ${response.status}`
        );
    }

    return response.json();
}


async function refreshDashboard() {
    try {
        await loadStatus();
    } catch (error) {
        console.warn(
            "Status unavailable:",
            error.message
        );
    }

    try {
        await loadTelemetry();
    } catch (error) {
        console.warn(
            "Telemetry unavailable:",
            error.message
        );
    }

    try {
        await loadLocation();
    } catch (error) {
        console.warn(
            "Location unavailable:",
            error.message
        );
    }

    try {
        await loadDetections();
    } catch (error) {
        console.warn(
            "Detections unavailable:",
            error.message
        );
    }
}


async function loadStatus() {
    const data =
        await apiRequest("/api/status");

    updateHeaderStatus(data);
    updateRoverName(data);
    updateBattery(data);
}


function updateHeaderStatus(data) {
    const headerStatus =
        document.querySelector(".header-status");

    if (!headerStatus) {
        return;
    }

    const indicator =
        headerStatus.querySelector(".status-indicator");

    const statusText =
        data && data.status
            ? String(data.status).toUpperCase()
            : "UNKNOWN";

    const textNodes =
        Array.from(headerStatus.childNodes)
            .filter(node => node.nodeType === Node.TEXT_NODE);

    if (textNodes.length) {
        textNodes[textNodes.length - 1].textContent =
            ` SYSTEM STATUS: ${statusText}`;
    }

    if (indicator) {
        indicator.setAttribute(
            "aria-label",
            `System ${statusText.toLowerCase()}`
        );
    }
}


function updateRoverName(data) {
    if (!data || !data.rover) {
        return;
    }

    const platformValue =
        findTextElement(
            ".hero-meta",
            "PLATFORM"
        );

    if (platformValue) {
        const value =
            platformValue.querySelector("strong");

        if (value) {
            value.textContent =
                data.rover === "Agricultural Rover 01"
                    ? "AR-01"
                    : data.rover;
        }
    }
}


function updateBattery(data) {
    if (
        !data ||
        data.battery === null ||
        data.battery === undefined
    ) {
        return;
    }

    const batteryValue =
        Number(data.battery);

    if (Number.isNaN(batteryValue)) {
        return;
    }

    const snapshotItems =
        document.querySelectorAll(
            ".snapshot-grid .snapshot-item"
        );

    snapshotItems.forEach(item => {
        const label =
            item.querySelector("span");

        const value =
            item.querySelector("strong");

        if (!label || !value) {
            return;
        }

        const labelText =
            label.textContent
                .trim()
                .toUpperCase();

        if (labelText === "BATTERY") {
            value.textContent =
                `${batteryValue.toFixed(0)} %`;
        }
    });
}


async function loadTelemetry() {
    const records =
        await apiRequest("/api/telemetry");

    if (!Array.isArray(records) || !records.length) {
        return;
    }

    const latest =
        records[0];

    updateTelemetryValues(latest);
}


function updateTelemetryValues(data) {
    if (!data) {
        return;
    }

    const snapshotItems =
        document.querySelectorAll(
            ".snapshot-grid .snapshot-item"
        );

    snapshotItems.forEach(item => {
        const label =
            item.querySelector("span");

        const value =
            item.querySelector("strong");

        if (!label || !value) {
            return;
        }

        const labelText =
            label.textContent
                .trim()
                .toUpperCase();

        if (
            labelText === "BATTERY" &&
            data.battery !== null &&
            data.battery !== undefined
        ) {
            value.textContent =
                `${Number(data.battery).toFixed(0)} %`;
        }

        if (
            labelText === "AIR TEMPERATURE" &&
            data.temperature !== null &&
            data.temperature !== undefined
        ) {
            value.textContent =
                `${Number(data.temperature).toFixed(1)} °C`;
        }

        if (
            labelText === "RELATIVE HUMIDITY" &&
            data.humidity !== null &&
            data.humidity !== undefined
        ) {
            value.textContent =
                `${Number(data.humidity).toFixed(0)} %`;
        }
    });

    const instruments =
        document.querySelectorAll(".instrument");

    instruments.forEach(instrument => {
        const definitions =
            instrument.querySelectorAll("dl > div");

        definitions.forEach(definition => {
            const term =
                definition.querySelector("dt");

            const value =
                definition.querySelector("dd");

            if (!term || !value) {
                return;
            }

            const termText =
                term.textContent
                    .trim()
                    .toLowerCase();

            if (
                termText === "temperature" &&
                data.temperature !== null &&
                data.temperature !== undefined
            ) {
                value.textContent =
                    `${Number(data.temperature).toFixed(1)} °C`;
            }

            if (
                termText === "humidity" &&
                data.humidity !== null &&
                data.humidity !== undefined
            ) {
                value.textContent =
                    `${Number(data.humidity).toFixed(0)} % RH`;
            }
        });
    });
}


async function loadLocation() {
    const records =
        await apiRequest("/api/location");

    if (!Array.isArray(records) || !records.length) {
        return;
    }

    const latest =
        records[0];

    updateLocationValues(latest);
}


function updateLocationValues(data) {
    if (!data) {
        return;
    }

    const latitude =
        formatCoordinate(
            Number(data.latitude),
            "N",
            "S"
        );

    const longitude =
        formatCoordinate(
            Number(data.longitude),
            "E",
            "W"
        );

    const snapshotItems =
        document.querySelectorAll(
            ".snapshot-grid .snapshot-item"
        );

    snapshotItems.forEach(item => {
        const label =
            item.querySelector("span");

        const strong =
            item.querySelector("strong");

        const small =
            item.querySelector("small");

        if (!label || !strong) {
            return;
        }

        const labelText =
            label.textContent
                .trim()
                .toUpperCase();

        if (labelText === "POSITION") {
            strong.textContent =
                latitude;

            if (small) {
                small.textContent =
                    longitude;
            }
        }
    });

    const instruments =
        document.querySelectorAll(".instrument");

    instruments.forEach(instrument => {
        const heading =
            instrument.querySelector("h3");

        if (!heading) {
            return;
        }

        const headingText =
            heading.textContent
                .trim()
                .toLowerCase();

        if (
            !headingText.includes("position") &&
            !headingText.includes("orientation")
        ) {
            return;
        }

        const definitions =
            instrument.querySelectorAll("dl > div");

        definitions.forEach(definition => {
            const term =
                definition.querySelector("dt");

            const value =
                definition.querySelector("dd");

            if (!term || !value) {
                return;
            }

            const termText =
                term.textContent
                    .trim()
                    .toLowerCase();

            if (termText === "latitude") {
                value.textContent =
                    latitude;
            }

            if (termText === "longitude") {
                value.textContent =
                    longitude;
            }
        });
    });
}


async function loadDetections() {
    const records =
        await apiRequest("/api/detections");

    if (!Array.isArray(records)) {
        return;
    }

    updateDetectionCount(records.length);
}


function updateDetectionCount(count) {
    const snapshotItems =
        document.querySelectorAll(
            ".snapshot-grid .snapshot-item"
        );

    snapshotItems.forEach(item => {
        const label =
            item.querySelector("span");

        const value =
            item.querySelector("strong");

        if (!label || !value) {
            return;
        }

        const labelText =
            label.textContent
                .trim()
                .toUpperCase();

        if (labelText === "DETECTIONS") {
            value.textContent =
                String(count);
        }
    });

    const resultText =
        document.querySelectorAll(
            ".results-grid span"
        );

    resultText.forEach(element => {
        const text =
            element.textContent.trim();

        if (/^n\s*=\s*\d+$/i.test(text)) {
            element.textContent =
                `n = ${count}`;
        }
    });
}


function formatCoordinate(
    value,
    positiveDirection,
    negativeDirection
) {
    if (
        typeof value !== "number" ||
        Number.isNaN(value)
    ) {
        return "—";
    }

    const direction =
        value >= 0
            ? positiveDirection
            : negativeDirection;

    return `${Math.abs(value).toFixed(4)}° ${direction}`;
}


function findTextElement(
    containerSelector,
    labelText
) {
    const container =
        document.querySelector(containerSelector);

    if (!container) {
        return null;
    }

    const children =
        container.querySelectorAll("div");

    for (const child of children) {
        const spans =
            child.querySelectorAll("span");

        if (!spans.length) {
            continue;
        }

        const firstSpan =
            spans[0].textContent
                .trim()
                .toUpperCase();

        if (firstSpan === labelText) {
            return child;
        }
    }

    return null;
}


async function checkBackendStatus() {
    try {
        const data =
            await apiRequest("/api/status");

        console.log(
            "AgriRover backend connected:",
            data
        );

        return data;

    } catch (error) {
        console.warn(
            "AgriRover backend unavailable:",
            error.message
        );

        return null;
    }
}