/* =========================================================
   CAREER COMPASS - FRONTEND JAVASCRIPT
   ========================================================= */


const API_BASE_URL = "http://127.0.0.1:5000";


/* =========================================================
   GLOBAL STATE
   ========================================================= */

let sessionId =
    localStorage.getItem("careerCompassSession") || null;


let studentProfile =
    JSON.parse(
        localStorage.getItem("careerCompassProfile") || "{}"
    );


let selectedSkills =
    new Set(studentProfile.skills || []);


let isBusy = false;



/* =========================================================
   CAREER CATALOG
   ========================================================= */

let careerCatalog = [

    {
        title: "Data Analyst",
        category: "Analytics",

        description:
            "Use data, SQL, spreadsheets and visualization to turn business questions into insights.",

        skills: [
            "SQL",
            "Excel",
            "Data Visualization",
            "Statistics",
            "Power BI"
        ]
    },


    {
        title: "Data Scientist",
        category: "Data Science",

        description:
            "Build analytical and predictive solutions using statistics, programming and machine learning.",

        skills: [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Data Visualization"
        ]
    },


    {
        title: "Business Analyst",
        category: "Business",

        description:
            "Bridge business needs and technical solutions through requirements, analysis and communication.",

        skills: [
            "Excel",
            "SQL",
            "Communication",
            "Requirements Analysis",
            "Data Visualization"
        ]
    },


    {
        title: "Operations Analyst",
        category: "Operations",

        description:
            "Improve processes and decisions by analyzing operational data, KPIs and workflows.",

        skills: [
            "Excel",
            "SQL",
            "Data Visualization",
            "Statistics",
            "Communication"
        ]
    },


    {
        title: "Cloud Engineer",
        category: "Cloud & DevOps",

        description:
            "Design, deploy and maintain reliable cloud infrastructure and services.",

        skills: [
            "Cloud Computing",
            "Linux",
            "Networking",
            "Python",
            "DevOps"
        ]
    },


    {
        title: "Software Developer",
        category: "Software",

        description:
            "Design, build, test and maintain software applications and practical digital solutions.",

        skills: [
            "Python",
            "JavaScript",
            "HTML",
            "CSS",
            "SQL",
            "Git"
        ]
    }

];



/* =========================================================
   SKILL CATALOG
   ========================================================= */

const skillCatalog = [

    "Python",
    "SQL",
    "Excel",
    "Tableau",
    "Power BI",
    "Data Visualization",
    "Statistics",
    "Machine Learning",

    "JavaScript",
    "HTML",
    "CSS",
    "Java",
    "C++",
    "Git",

    "Linux",
    "Cloud Computing",
    "DevOps",
    "Networking",

    "Communication",
    "Problem Solving",
    "Business Analysis",
    "Requirements Analysis",
    "Project Management"

];



/* =========================================================
   PAGE LOAD
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        applySavedTheme();

        renderParticles();

        renderSkills();

        restoreProfileToForm();

        updateSkillCount();

        renderCareers();

        updateWelcome();

        setupCustomSkillInput();

        checkBackend();

        setTimeout(
            () => observeCards(),
            150
        );

    }
);



/* =========================================================
   SECTION NAVIGATION
   ========================================================= */

function showSection(sectionId) {

    document
        .querySelectorAll(".section")
        .forEach(
            section =>
                section.classList.remove("active")
        );


    const target =
        document.getElementById(sectionId);


    if (!target) return;


    target.classList.add("active");


    document
        .querySelectorAll(".nav-link")
        .forEach(
            button => {

                button.classList.toggle(
                    "active",
                    button.dataset.section === sectionId
                );

            }
        );


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });


    if (sectionId === "careers") {

        renderCareers();

    }

}



/* =========================================================
   DARK MODE
   ========================================================= */

function toggleTheme() {

    const dark =
        !document.body.classList.contains("dark");


    document.body.classList.toggle(
        "dark",
        dark
    );


    localStorage.setItem(
        "careerCompassTheme",
        dark ? "dark" : "light"
    );


    updateThemeButton();

}



function applySavedTheme() {

    const saved =
        localStorage.getItem(
            "careerCompassTheme"
        );


    const shouldDark =
        saved
            ? saved === "dark"
            : window.matchMedia &&
              window.matchMedia(
                  "(prefers-color-scheme: dark)"
              ).matches;


    document.body.classList.toggle(
        "dark",
        shouldDark
    );


    updateThemeButton();

}



function updateThemeButton() {

    const button =
        document.getElementById(
            "themeToggle"
        );


    if (!button) return;


    const dark =
        document.body.classList.contains(
            "dark"
        );


    button.textContent =
        dark ? "☀️" : "🌙";


    button.title =
        dark
            ? "Switch to light mode"
            : "Switch to dark mode";

}



/* =========================================================
   DYNAMIC WELCOME MESSAGE
   ========================================================= */

function updateWelcome() {

    const name =
        studentProfile.name ||
        document.getElementById("name")?.value ||
        "";


    const hour =
        new Date().getHours();


    let greeting;


    if (hour < 12) {

        greeting = "Good morning";

    }

    else if (hour < 18) {

        greeting = "Good afternoon";

    }

    else {

        greeting = "Good evening";

    }


    const welcome =
        document.getElementById(
            "welcomeLine"
        );


    if (welcome) {

        welcome.textContent =
            `${greeting}${name ? ", " + name : ""} 👋`;

    }


    const resultsGreeting =
        document.getElementById(
            "resultsGreeting"
        );


    if (resultsGreeting) {

        resultsGreeting.textContent =
            name
                ? `Here is your personalized career snapshot, ${name}.`
                : "Your personalized career snapshot.";

    }


    if (studentProfile.topCareer) {

        const heroCareer =
            document.getElementById(
                "heroCareer"
            );


        if (heroCareer) {

            heroCareer.textContent =
                studentProfile.topCareer;

        }

    }

}



/* =========================================================
   ANIMATED PARTICLES
   ========================================================= */

function renderParticles() {

    const container =
        document.getElementById(
            "particles"
        );


    if (!container) return;


    for (
        let i = 0;
        i < 18;
        i++
    ) {

        const particle =
            document.createElement(
                "span"
            );


        particle.className =
            "particle";


        particle.style.left =
            `${Math.random() * 100}%`;


        particle.style.animationDuration =
            `${10 + Math.random() * 15}s`;


        particle.style.animationDelay =
            `${-Math.random() * 20}s`;


        particle.style.transform =
            `scale(${0.5 + Math.random() * 1.5})`;


        container.appendChild(
            particle
        );

    }

}



/* =========================================================
   SKILLS
   ========================================================= */

function renderSkills() {

    const container =
        document.getElementById(
            "skillsContainer"
        );


    if (!container) return;


    container.innerHTML = "";


    skillCatalog.forEach(
        skill => {

            const button =
                document.createElement(
                    "button"
                );


            button.type = "button";


            button.className =
                "skill-button" +
                (
                    selectedSkills.has(skill)
                        ? " selected"
                        : ""
                );


            button.textContent =
                skill;


            button.onclick =
                () => {

                    if (
                        selectedSkills.has(
                            skill
                        )
                    ) {

                        selectedSkills.delete(
                            skill
                        );

                    }

                    else {

                        selectedSkills.add(
                            skill
                        );

                    }


                    button.classList.toggle(
                        "selected"
                    );


                    updateSkillCount();

                    saveCurrentProfile(false);

                };


            container.appendChild(
                button
            );

        }
    );

}



function addCustomSkill() {

    const input =
        document.getElementById(
            "customSkill"
        );


    if (!input) return;


    const value =
        input.value.trim();


    if (!value) return;


    selectedSkills.add(value);


    if (
        !skillCatalog.includes(value)
    ) {

        skillCatalog.push(value);

    }


    input.value = "";


    renderSkills();

    updateSkillCount();

    saveCurrentProfile(false);

}



function setupCustomSkillInput() {

    const input =
        document.getElementById(
            "customSkill"
        );


    if (!input) return;


    input.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Enter"
            ) {

                event.preventDefault();

                addCustomSkill();

            }

        }
    );

}



function updateSkillCount() {

    const element =
        document.getElementById(
            "skillCount"
        );


    if (element) {

        element.textContent =
            selectedSkills.size;

    }

}



/* =========================================================
   PROFILE
   ========================================================= */

function collectStudentProfile() {

    const profile = {

        name:
            valueOf("name"),

        degree:
            valueOf("degree"),

        cgpa:
            parseFloat(
                valueOf("cgpa")
            ) || undefined,

        target_role:
            valueOf("targetRole"),

        interests:
            splitList(
                valueOf("interests")
            ),

        skills:
            [...selectedSkills],

        projects:
            valueOf("projects"),

        experience:
            valueOf("experience")

    };


    Object.keys(profile)
        .forEach(
            key => {

                if (
                    profile[key] === "" ||
                    profile[key] === undefined ||
                    (
                        Array.isArray(
                            profile[key]
                        ) &&
                        !profile[key].length
                    )
                ) {

                    delete profile[key];

                }

            }
        );


    return profile;

}



function valueOf(id) {

    return (
        document
            .getElementById(id)
            ?.value
            .trim()
        || ""
    );

}



function splitList(text) {

    return text
        .split(",")
        .map(
            item =>
                item.trim()
        )
        .filter(Boolean);

}



/* =========================================================
   SAVE PROFILE
   ========================================================= */

function saveCurrentProfile(
    showToastMessage = false
) {

    const profile =
        collectStudentProfile();


    studentProfile = {

        ...studentProfile,

        ...profile

    };


    localStorage.setItem(
        "careerCompassProfile",
        JSON.stringify(
            studentProfile
        )
    );


    updateWelcome();


    if (showToastMessage) {

        showToast(
            "Profile saved locally ✓"
        );

    }

}



/* =========================================================
   RESTORE PROFILE
   ========================================================= */

function restoreProfileToForm() {

    const p =
        studentProfile;


    [
        "name",
        "degree",
        "targetRole",
        "interests",
        "projects",
        "experience"
    ]
    .forEach(
        id => {

            const element =
                document.getElementById(
                    id
                );


            if (!element) return;


            const key =
                id === "targetRole"
                    ? "target_role"
                    : id;


            if (
                p[key] !== undefined
            ) {

                element.value =
                    Array.isArray(
                        p[key]
                    )
                        ? p[key].join(", ")
                        : p[key];

            }

        }
    );


    if (
        p.cgpa !== undefined &&
        document.getElementById("cgpa")
    ) {

        document.getElementById(
            "cgpa"
        ).value = p.cgpa;

    }

}



/* =========================================================
   ANALYZE PROFILE
   ========================================================= */

async function analyzeProfile() {

    if (isBusy) return;


    const profile =
        collectStudentProfile();


    if (
        !profile.name &&
        !profile.skills?.length &&
        !profile.degree
    ) {

        showToast(
            "Add a little profile information first."
        );


        showSection(
            "profile"
        );


        return;

    }


    studentProfile = {

        ...studentProfile,

        ...profile

    };


    localStorage.setItem(
        "careerCompassProfile",
        JSON.stringify(
            studentProfile
        )
    );


    setLoading(
        true,
        "Analyzing your career profile...",
        "Evaluating skills, interests and career possibilities."
    );


    isBusy = true;


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/analyze`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            profile,

                            session_id:
                                sessionId

                        })

                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            data.success === false
        ) {

            throw new Error(
                data.error ||
                `Server error ${response.status}`
            );

        }


        sessionId =
            data.session_id ||
            sessionId;


        if (sessionId) {

            localStorage.setItem(
                "careerCompassSession",
                sessionId
            );

        }


        const analysis =
            data.analysis ||
            data.data ||
            data.result ||
            data;


        renderAnalysis(
            analysis
        );


        showSection(
            "results"
        );


        showToast(
            "Career analysis completed ✓"
        );

    }


    catch (error) {

        console.error(error);


        showToast(
            "Analysis failed. Check that Flask is running."
        );


        addBotMessage(
            "⚠️ I couldn't analyze your profile right now. Please make sure the Flask backend is running."
        );

    }


    finally {

        isBusy = false;

        setLoading(
            false
        );

    }

}



/* =========================================================
   RENDER ANALYSIS
   ========================================================= */

function renderAnalysis(
    analysis
) {

    if (
        !analysis ||
        typeof analysis !== "object"
    ) {

        return;

    }


    console.log(
        "Analysis received:",
        analysis
    );


    const careers =
        analysis.career_matches ||
        analysis.career_recommendations ||
        analysis.matches ||
        analysis.careers ||
        analysis.recommendations ||
        [];


    const normalized =
        Array.isArray(careers)
            ? careers
                .map(normalizeCareer)
                .filter(
                    item =>
                        item.title
                )
            : [];


    const top =
        normalized[0];


    const topTitle =
        top?.title ||
        analysis.top_career ||
        analysis.recommended_career ||
        analysis.best_career ||
        "—";


    const match =
        top?.score ??
        numberFrom(
            analysis.match_score ??
            analysis.score ??
            analysis.match
        );


    const readiness =
        numberFrom(
            analysis.readiness ??
            analysis.readiness_score ??
            analysis.job_readiness ??
            analysis.job_readiness_score
        );


    const gaps =
        analysis.missing_skills ||
        analysis.skill_gaps ||
        analysis.gaps ||
        analysis.missing ||
        [];


    setText(
        "topCareer",
        topTitle
    );


    setText(
        "matchScore",
        match !== null
            ? `${Math.round(match)}%`
            : "—"
    );


    setText(
        "readinessScore",
        readiness !== null
            ? `${Math.round(readiness)}%`
            : "—"
    );


    setText(
        "gapCount",
        Array.isArray(gaps)
            ? gaps.length
            : "—"
    );


    setText(
        "heroCareer",
        topTitle !== "—"
            ? topTitle
            : "Discover your fit"
    );


    renderCareerResults(
        normalized
    );


    renderSkillResults(
        Array.isArray(gaps)
            ? gaps
            : []
    );


    renderNextSteps(
        analysis,
        topTitle,
        gaps
    );


    studentProfile.topCareer =
        topTitle;


    studentProfile.lastAnalysis =
        analysis;


    localStorage.setItem(
        "careerCompassProfile",
        JSON.stringify(
            studentProfile
        )
    );

}



/* =========================================================
   NUMBER HELPER
   ========================================================= */

function numberFrom(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {

        return null;

    }


    if (
        typeof value === "number"
    ) {

        return value;

    }


    const match =
        String(value)
            .replace(",", "")
            .match(
                /-?\d+(\.\d+)?/
            );


    return match
        ? Number(match[0])
        : null;

}



/* =========================================================
   CAREER NORMALIZER
   ========================================================= */

function normalizeCareer(
    career
) {

    if (
        typeof career === "string"
    ) {

        return {

            title: career,

            score: null

        };

    }


    return {

        title:
            career.title ||
            career.name ||
            career.role ||
            career.career,

        score:
            numberFrom(
                career.score ??
                career.match_score ??
                career.skill_fit_score ??
                career.match_percentage
            ),

        category:
            career.category ||
            career.domain ||
            ""

    };

}



/* =========================================================
   CAREER RESULTS
   ========================================================= */

function renderCareerResults(
    careers
) {

    const box =
        document.getElementById(
            "careerResults"
        );


    if (!box) return;


    if (!careers.length) {

        box.innerHTML = `
            <p class="empty-message">
                No career recommendations were returned yet.
                Ask CareerBot for a recommendation.
            </p>
        `;

        return;

    }


    box.innerHTML =
        careers
            .slice(0, 5)
            .map(
                (career, index) => `

                <div class="result-item">

                    <div>

                        <strong>
                            #${index + 1}
                            ${escapeHTML(career.title)}
                        </strong>

                        ${
                            career.category
                                ? `
                                <div>
                                    ${escapeHTML(
                                        career.category
                                    )}
                                </div>
                                `
                                : ""
                        }

                    </div>


                    <span>

                        ${
                            career.score !== null
                                ? `${Number(
                                    career.score
                                ).toFixed(1)}%`
                                : "Recommended"
                        }

                    </span>

                </div>

            `
            )
            .join("");

}



/* =========================================================
   SKILL RESULTS
   ========================================================= */

function renderSkillResults(
    gaps
) {

    const box =
        document.getElementById(
            "skillResults"
        );


    if (!box) return;


    if (!gaps.length) {

        box.innerHTML = `
            <p class="empty-message">
                No explicit skill gaps were returned.
            </p>
        `;

        return;

    }


    box.innerHTML =
        gaps
            .slice(0, 8)
            .map(
                gap => {

                    const skill =
                        typeof gap === "string"
                            ? gap
                            : gap.skill ||
                              gap.name ||
                              gap.title ||
                              "Skill";


                    return `

                        <div class="result-item">

                            <strong>
                                ${escapeHTML(skill)}
                            </strong>

                            <span>
                                Priority
                            </span>

                        </div>

                    `;

                }
            )
            .join("");

}



/* =========================================================
   NEXT STEPS
   ========================================================= */

function renderNextSteps(
    analysis,
    career,
    gaps
) {

    const box =
        document.getElementById(
            "nextSteps"
        );


    if (!box) return;


    const source =
        analysis.next_steps ||
        analysis.nextSteps ||
        analysis.actions ||
        analysis.recommendations;


    let steps =
        Array.isArray(source)
            ? source
            : [];


    if (!steps.length) {

        steps = [];


        if (
            career &&
            career !== "—"
        ) {

            steps.push(
                `Learn the core skills used in ${career}.`
            );

        }


        if (gaps.length) {

            steps.push(
                `Prioritize your top ${Math.min(
                    gaps.length,
                    3
                )} skill gaps.`
            );

        }


        steps.push(
            "Build one practical project and document what you learned."
        );


        steps.push(
            "Re-check your readiness after completing the next learning milestone."
        );

    }


    box.innerHTML =
        steps
            .slice(0, 5)
            .map(
                (step, index) => `

                    <div class="result-item">

                        <strong>
                            ${index + 1}.
                        </strong>

                        <span>
                            ${escapeHTML(
                                typeof step === "string"
                                    ? step
                                    : JSON.stringify(step)
                            )}
                        </span>

                    </div>

                `
            )
            .join("");

}



/* =========================================================
   CAREER EXPLORER
   ========================================================= */

function renderCareers(
    filter = ""
) {

    const grid =
        document.getElementById(
            "careerGrid"
        );


    if (!grid) return;


    const query =
        filter
            .trim()
            .toLowerCase();


    const list =
        careerCatalog.filter(
            career => {

                return (
                    !query ||
                    [
                        career.title,
                        career.category,
                        career.description,
                        ...career.skills
                    ]
                        .join(" ")
                        .toLowerCase()
                        .includes(query)
                );

            }
        );


    const count =
        document.getElementById(
            "careerCount"
        );


    if (count) {

        count.textContent =
            `${list.length} career${
                list.length === 1
                    ? ""
                    : "s"
            }`;

    }


    grid.innerHTML =
        list
            .map(
                career => `

                    <article class="career-card">

                        <span class="career-category">

                            ${escapeHTML(
                                career.category
                            )}

                        </span>


                        <h3>
                            ${escapeHTML(
                                career.title
                            )}
                        </h3>


                        <p>
                            ${escapeHTML(
                                career.description
                            )}
                        </p>


                        <div class="career-skills">

                            ${
                                career.skills
                                    .slice(0, 5)
                                    .map(
                                        skill => `
                                            <span class="career-skill">
                                                ${escapeHTML(
                                                    skill
                                                )}
                                            </span>
                                        `
                                    )
                                    .join("")
                            }

                        </div>


                        <button
                            class="career-ask"
                            onclick="openCareerChat('Tell me whether ${escapeJS(
                                career.title
                            )} is a good fit for my profile.')">

                            Ask CareerBot about this →

                        </button>

                    </article>

                `
            )
            .join("");


    if (!list.length) {

        grid.innerHTML = `

            <div class="card">

                <p class="empty-message">

                    No matching career found.
                    Try another keyword.

                </p>

            </div>

        `;

    }

}



function searchCareers() {

    renderCareers(
        valueOf("careerSearch")
    );

}



/* =========================================================
   CHATBOT
   ========================================================= */

function toggleChat() {

    const chat =
        document.getElementById(
            "chatBox"
        );


    if (!chat) return;


    chat.classList.toggle(
        "open"
    );


    if (
        chat.classList.contains(
            "open"
        )
    ) {

        document
            .getElementById(
                "chatInput"
            )
            ?.focus();

    }

}



function openCareerChat(
    question
) {

    const chat =
        document.getElementById(
            "chatBox"
        );


    if (!chat) return;


    chat.classList.add(
        "open"
    );


    const input =
        document.getElementById(
            "chatInput"
        );


    if (input) {

        input.value =
            question;

    }


    sendChatMessage();

}



function handleChatKey(
    event
) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendChatMessage();

    }

}



/* =========================================================
   SEND CHAT MESSAGE
   ========================================================= */

async function sendChatMessage() {

    if (isBusy) return;


    const input =
        document.getElementById(
            "chatInput"
        );


    const message =
        input?.value.trim();


    if (!message) return;


    input.value = "";


    addUserMessage(
        message
    );


    showTypingIndicator();


    isBusy = true;


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/chat`,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            session_id:
                                sessionId,

                            message:
                                message,

                            profile:
                                collectStudentProfile(),

                            analysis:
                                studentProfile.lastAnalysis ||
                                null

                        })

                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            data.success === false
        ) {

            throw new Error(
                data.error ||
                `Server error ${response.status}`
            );

        }


        sessionId =
            data.session_id ||
            sessionId;


        if (sessionId) {

            localStorage.setItem(
                "careerCompassSession",
                sessionId
            );

        }


        if (data.profile) {

            studentProfile = {

                ...studentProfile,

                ...data.profile

            };


            localStorage.setItem(
                "careerCompassProfile",
                JSON.stringify(
                    studentProfile
                )
            );


            restoreProfileToForm();

        }


        removeTypingIndicator();


        addBotMessage(
            data.reply ||
            data.message ||
            "I processed your request."
        );


        if (data.analysis) {

            renderAnalysis(
                data.analysis
            );

        }

    }


    catch (error) {

        console.error(
            error
        );


        removeTypingIndicator();


        addBotMessage(
            "⚠️ I couldn't reach the Career Compass agent. Please confirm that `python app.py` is running on port 5000."
        );

    }


    finally {

        isBusy = false;

    }

}



/* =========================================================
   CHAT MESSAGE HELPERS
   ========================================================= */

function addUserMessage(
    message
) {

    addMessage(
        "user-message",
        escapeHTML(message)
    );

}



function addBotMessage(
    message
) {

    addMessage(
        "bot-message",
        formatBotMessage(message)
    );

}



function addMessage(
    className,
    html
) {

    const box =
        document.getElementById(
            "chatMessages"
        );


    if (!box) return;


    const element =
        document.createElement(
            "div"
        );


    element.className =
        `message ${className}`;


    element.innerHTML =
        `
            <div class="message-content">
                ${html}
            </div>
        `;


    box.appendChild(
        element
    );


    scrollChat();

}



/* =========================================================
   FORMAT BOT RESPONSE
   ========================================================= */

function formatBotMessage(
    message
) {

    let text =
        escapeHTML(
            message || ""
        );


    text =
        text.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    text =
        text.replace(
            /^[-•]\s+(.*)$/gm,
            "• $1<br>"
        );


    text =
        text.replace(
            /^(\d+)\.\s+(.*)$/gm,
            "<strong>$1.</strong> $2<br>"
        );


    return text.replace(
        /\n/g,
        "<br>"
    );

}



/* =========================================================
   TYPING INDICATOR
   ========================================================= */

function showTypingIndicator() {

    removeTypingIndicator();


    const box =
        document.getElementById(
            "chatMessages"
        );


    if (!box) return;


    const element =
        document.createElement(
            "div"
        );


    element.id =
        "careerBotTyping";


    element.className =
        "message bot-message typing-message";


    element.innerHTML = `

        <div class="message-content">

            <div class="typing-dots">

                <span class="typing-dot">
                    ●
                </span>

                <span class="typing-dot">
                    ●
                </span>

                <span class="typing-dot">
                    ●
                </span>

            </div>

        </div>

    `;


    box.appendChild(
        element
    );


    scrollChat();

}



function removeTypingIndicator() {

    document
        .getElementById(
            "careerBotTyping"
        )
        ?.remove();

}



function scrollChat() {

    const box =
        document.getElementById(
            "chatMessages"
        );


    if (!box) return;


    setTimeout(
        () => {

            box.scrollTop =
                box.scrollHeight;

        },
        30
    );

}



/* =========================================================
   BACKEND STATUS
   ========================================================= */

async function checkBackend() {

    const status =
        document.getElementById(
            "backendStatus"
        );


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/test`,
                {
                    cache: "no-store"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Backend offline"
            );

        }


        if (status) {

            status.textContent =
                "● Agent online";


            status.className =
                "status-pill online";

        }

    }


    catch {

        if (status) {

            status.textContent =
                "● Backend offline";


            status.className =
                "status-pill offline";

        }

    }

}



/* =========================================================
   LOADING
   ========================================================= */

function setLoading(
    show,
    title,
    text
) {

    const element =
        document.getElementById(
            "loading"
        );


    if (!element) return;


    element.classList.toggle(
        "show",
        show
    );


    if (title) {

        setText(
            "loadingTitle",
            title
        );

    }


    if (text) {

        setText(
            "loadingText",
            text
        );

    }

}



/* =========================================================
   TEXT HELPER
   ========================================================= */

function setText(
    id,
    value
) {

    const element =
        document.getElementById(
            id
        );


    if (element) {

        element.textContent =
            value;

    }

}



/* =========================================================
   TOAST
   ========================================================= */

function showToast(
    message
) {

    const toast =
        document.getElementById(
            "toast"
        );


    if (!toast) return;


    toast.textContent =
        message;


    toast.classList.add(
        "show"
    );


    clearTimeout(
        window.__toast
    );


    window.__toast =
        setTimeout(
            () => {

                toast.classList.remove(
                    "show"
                );

            },
            2600
        );

}



/* =========================================================
   SECURITY HELPERS
   ========================================================= */

function escapeHTML(
    value
) {

    return String(
        value ?? ""
    )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}



function escapeJS(
    value
) {

    return String(value)
        .replace(
            /\\/g,
            "\\\\"
        )
        .replace(
            /'/g,
            "\\'"
        );

}



/* =========================================================
   CARD ANIMATION
   ========================================================= */

function observeCards() {

    document
        .querySelectorAll(
            ".reveal-card"
        )
        .forEach(
            (element, index) => {

                element.style.animationDelay =
                    `${index * 80}ms`;

            }
        );

}