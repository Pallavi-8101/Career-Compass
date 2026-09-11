# ============================================================
# CAREERCOMPASS - INTELLIGENT CAREER ANALYSIS ENGINE
# Knowledge-Base Driven Career Recommendation System
# ============================================================

import json
import os
import re


class CareerAgent:

    def __init__(self):

        # ----------------------------------------------------
        # PROJECT PATHS
        # ----------------------------------------------------

        self.backend_directory = os.path.dirname(
            os.path.abspath(__file__)
        )

        # Support both layouts:
        # 1) project/backend/agent.py + project/knowledge_base/
        # 2) project/agent.py + project/knowledge_base/
        candidate_directories = [
            os.path.join(self.backend_directory, "knowledge_base"),
            os.path.join(os.path.dirname(self.backend_directory), "knowledge_base"),
        ]

        self.knowledge_base_directory = next(
            (
                path for path in candidate_directories
                if os.path.isdir(path)
            ),
            candidate_directories[0]
        )

        # ----------------------------------------------------
        # LOAD KNOWLEDGE BASE
        # ----------------------------------------------------

        self.careers_data = self.load_json(
            "career_roles.json",
            {"careers": []}
        )

        self.skills_data = self.load_json(
            "skills.json",
            {}
        )

        self.learning_data = self.load_json(
            "learning_resources.json",
            {}
        )

        self.market_data = self.load_json(
            "job_market.json",
            {}
        )

        # ----------------------------------------------------
        # EXTRACT CAREERS
        # ----------------------------------------------------

        careers = (
            self.careers_data.get("careers", [])
            if isinstance(self.careers_data, dict)
            else []
        )

        self.careers = (
            [career for career in careers if isinstance(career, dict)]
            if isinstance(careers, list)
            else []
        )

        # ----------------------------------------------------
        # ALIASES
        # ----------------------------------------------------

        self.skill_aliases = {

            "powerbi": "Power BI",
            "power bi": "Power BI",

            "tableau": "Tableau",

            "ms excel": "Excel",
            "microsoft excel": "Excel",

            "github": "Git/GitHub",
            "git hub": "Git/GitHub",
            "git": "Git/GitHub",

            "html": "HTML/CSS",
            "css": "HTML/CSS",
            "html css": "HTML/CSS",
            "html5": "HTML/CSS",
            "css3": "HTML/CSS",

            "machine learning": "Machine Learning",
            "ml": "Machine Learning",

            "statistics": "Statistics",
            "statistical analysis": "Statistics",

            "data visualisation": "Data Visualization",
            "data visualization": "Data Visualization",

            "problem solving": "Problem Solving",
            "problem-solving": "Problem Solving",

            "critical thinking": "Critical Thinking",

            "communication skills": "Communication",

            "teamwork": "Teamwork",

            "leadership": "Leadership",

            "time management": "Time Management",

            "presentation skills": "Presentation",

            "python programming": "Python",

            "java programming": "Java",

            "c++ programming": "C++",

            "javascript programming": "JavaScript",

            "api": "APIs",
            "apis": "APIs",

            "cloud": "Cloud Basics",
            "cloud computing": "Cloud Basics",

            "linux operating system": "Linux"
        }

        self.role_aliases = {

            "business intelligence analyst":
                "BI Analyst",

            "bi analyst":
                "BI Analyst",

            "data analytics":
                "Data Analyst",

            "data analysis":
                "Data Analyst",

            "data science":
                "Data Scientist",

            "machine learning engineer":
                "ML Engineer",

            "ml engineer":
                "ML Engineer",

            "artificial intelligence engineer":
                "AI Engineer",

            "ai engineer":
                "AI Engineer",

            "cyber security analyst":
                "Cybersecurity Analyst",

            "cybersecurity":
                "Cybersecurity Analyst",

            "security analyst":
                "Cybersecurity Analyst",

            "soc":
                "SOC Analyst",

            "soc analyst":
                "SOC Analyst",

            "web developer":
                "Full Stack Developer",

            "full stack":
                "Full Stack Developer",

            "frontend":
                "Frontend Developer",

            "front end":
                "Frontend Developer",

            "backend":
                "Backend Developer",

            "back end":
                "Backend Developer",

            "software developer":
                "Software Engineer",

            "software development":
                "Software Engineer",

            "devops":
                "DevOps Engineer",

            "cloud":
                "Cloud Engineer",

            "ui":
                "UI Designer",

            "ux":
                "UX Designer",

            "ui ux":
                "Product Designer"
        }

        # ----------------------------------------------------
        # DOMAIN KEYWORDS
        # ----------------------------------------------------

        self.domain_keywords = {

            "Data Science & Analytics": [
                "data",
                "analytics",
                "data science",
                "data analysis",
                "statistics",
                "dashboard",
                "visualization",
                "business intelligence",
                "bi",
                "reporting"
            ],

            "Software Development": [
                "software",
                "software development",
                "programming",
                "coding",
                "application development",
                "development"
            ],

            "Web Development": [
                "web",
                "website",
                "web development",
                "frontend",
                "front end",
                "backend",
                "back end",
                "full stack"
            ],

            "App Development": [
                "mobile",
                "mobile app",
                "android",
                "ios",
                "app development"
            ],

            "AI & Machine Learning": [
                "ai",
                "artificial intelligence",
                "machine learning",
                "ml",
                "deep learning",
                "nlp",
                "natural language",
                "computer vision"
            ],

            "Cybersecurity": [
                "cybersecurity",
                "cyber security",
                "security",
                "ethical hacking",
                "penetration testing",
                "soc",
                "network security"
            ],

            "Cloud & DevOps": [
                "cloud",
                "cloud computing",
                "devops",
                "deployment",
                "infrastructure",
                "site reliability",
                "sre"
            ],

            "Business & Management": [
                "business",
                "management",
                "business analysis",
                "product management",
                "project management",
                "marketing",
                "operations"
            ],

            "UI/UX & Design": [
                "ui",
                "ux",
                "design",
                "user experience",
                "user interface",
                "product design"
            ],

            "Database & Infrastructure": [
                "database",
                "databases",
                "db",
                "database administration",
                "infrastructure"
            ],

            "Software Testing": [
                "testing",
                "software testing",
                "qa",
                "quality assurance",
                "automation testing"
            ],

            "IT Infrastructure": [
                "it support",
                "technical support",
                "systems",
                "system administration",
                "infrastructure"
            ],

            "Research & Advanced Analytics": [
                "research",
                "research data",
                "scientific computing",
                "advanced analytics"
            ],

            "Finance & Analytics": [
                "finance",
                "financial analysis",
                "quantitative",
                "investment",
                "stock market"
            ],

            "Marketing & Analytics": [
                "marketing",
                "digital marketing",
                "advertising",
                "customer analytics"
            ],

            "Technology Management": [
                "technology management",
                "technical management",
                "project management",
                "technology leadership"
            ]
        }


    # ========================================================
    # JSON LOADER
    # ========================================================

    def load_json(self, filename, default):

        filepath = os.path.join(
            self.knowledge_base_directory,
            filename
        )

        try:

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except FileNotFoundError:

            print(
                f"[WARNING] Knowledge Base file not found: {filename}"
            )

            return default

        except json.JSONDecodeError as error:

            print(
                f"[WARNING] Invalid JSON file: {filename} ({error})"
            )

            return default

        except OSError as error:

            print(
                f"[WARNING] Could not read knowledge base file: {filename} ({error})"
            )

            return default


    # ========================================================
    # TEXT NORMALIZATION
    # ========================================================

    def normalize(self, value):

        if value is None:
            return ""

        value = str(value).strip().lower()

        value = re.sub(
            r"[^a-z0-9+#/ ]",
            " ",
            value
        )

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value.strip()


    # ========================================================
    # NORMALIZE SKILL
    # ========================================================

    def normalize_skill(self, skill):

        normalized = self.normalize(skill)

        return self.skill_aliases.get(
            normalized,
            str(skill).strip()
        )


    # ========================================================
    # NORMALIZE ROLE
    # ========================================================

    def normalize_role(self, role):

        normalized = self.normalize(role)

        for career in self.careers:

            title = career.get(
                "title",
                ""
            )

            if self.normalize(title) == normalized:
                return title

        return self.role_aliases.get(
            normalized,
            role
        )


    # ========================================================
    # CHECK UNDECIDED CAREER
    # ========================================================

    def is_undecided(self, target_role):

        if not target_role:
            return True

        value = self.normalize(target_role)

        undecided_values = [
            "",
            "not decided",
            "not decided / no specific interest",
            "no specific interest",
            "no specific career",
            "undecided",
            "not sure",
            "dont know",
            "don't know",
            "explore",
            "explore careers",
            "none",
            "no preference",
            "not yet decided"
        ]

        return value in undecided_values


    # ========================================================
    # GET STUDENT SKILLS
    # ========================================================

    def get_student_skills(self, student):

        skills = student.get(
            "skills",
            []
        )

        if not isinstance(skills, list):
            skills = [skills]

        normalized_skills = []

        for skill in skills:

            normalized_skill = self.normalize_skill(skill)

            if normalized_skill:
                normalized_skills.append(
                    normalized_skill
                )

        return list(
            dict.fromkeys(normalized_skills)
        )


    # ========================================================
    # GET ALL STUDENT INTERESTS
    # ========================================================

    def get_student_interests(self, student):

        interests = student.get(
            "interests",
            []
        )

        if not isinstance(interests, list):
            interests = [interests]

        result = []

        for interest in interests:

            if interest:
                result.append(
                    str(interest).strip()
                )

        return list(
            dict.fromkeys(result)
        )


    # ========================================================
    # DETECT DOMAIN
    # ========================================================

    def detect_domain(self, student):

        skills = self.get_student_skills(
            student
        )

        interests = self.get_student_interests(
            student
        )

        target_role = student.get(
            "target_role",
            ""
        )

        text_parts = []

        text_parts.extend(
            skills
        )

        text_parts.extend(
            interests
        )

        if target_role:
            text_parts.append(
                target_role
            )

        combined_text = self.normalize(
            " ".join(text_parts)
        )

        domain_scores = {}

        for domain, keywords in self.domain_keywords.items():

            score = 0

            for keyword in keywords:

                keyword_normalized = self.normalize(
                    keyword
                )

                if keyword_normalized in combined_text:

                    # Interest/target/domain phrases
                    # get a stronger contribution.
                    if keyword_normalized in [
                        self.normalize(i)
                        for i in interests
                    ]:
                        score += 5

                    elif keyword_normalized == self.normalize(
                        target_role
                    ):
                        score += 6

                    else:
                        score += 2

            domain_scores[domain] = score

        if not domain_scores:
            return "General Technology"

        best_domain = max(
            domain_scores,
            key=lambda d: domain_scores.get(d, 0)
        )

        if domain_scores[best_domain] == 0:

            return "General Technology"

        return best_domain


    # ========================================================
    # CALCULATE SKILL MATCH
    # ========================================================

    def calculate_skill_match(
        self,
        student_skills,
        career
    ):

        student_normalized = {
            self.normalize(skill)
            for skill in student_skills
        }

        core_skills = career.get(
            "core_skills",
            []
        )

        important_skills = career.get(
            "important_skills",
            []
        )

        nice_to_have = career.get(
            "nice_to_have",
            []
        )

        core_total = len(core_skills) * 15
        important_total = len(important_skills) * 7
        nice_total = len(nice_to_have) * 3

        total_weight = (
            core_total
            + important_total
            + nice_total
        )

        earned_weight = 0

        strong = []
        improve = []
        missing = []

        # ----------------------------------------------------
        # CORE SKILLS
        # ----------------------------------------------------

        for skill in core_skills:

            if self.normalize(skill) in student_normalized:

                earned_weight += 15
                strong.append(skill)

            else:

                missing.append(skill)

        # ----------------------------------------------------
        # IMPORTANT SKILLS
        # ----------------------------------------------------

        for skill in important_skills:

            if self.normalize(skill) in student_normalized:

                earned_weight += 7
                strong.append(skill)

            else:

                improve.append(skill)

        # ----------------------------------------------------
        # NICE TO HAVE
        # ----------------------------------------------------

        for skill in nice_to_have:

            if self.normalize(skill) in student_normalized:

                earned_weight += 3

            else:

                # Don't overwhelm the user with
                # optional missing skills.
                if len(improve) < 10:
                    improve.append(skill)

        if total_weight == 0:

            score = 0

        else:

            score = (
                earned_weight /
                total_weight
            ) * 100

        return {
            "score": round(score, 1),
            "strong": list(
                dict.fromkeys(strong)
            ),
            "improve": list(
                dict.fromkeys(improve)
            ),
            "missing": list(
                dict.fromkeys(missing)
            )
        }


    # ========================================================
    # INTEREST MATCH
    # ========================================================

    def calculate_interest_match(
        self,
        interests,
        career
    ):

        if not interests:
            return 0

        career_text = self.normalize(
            " ".join([
                career.get("title", ""),
                career.get("category", ""),
                career.get("description", "")
            ])
        )

        score = 0

        for interest in interests:

            interest_normalized = self.normalize(
                interest
            )

            if not interest_normalized:
                continue

            # Direct phrase match
            if interest_normalized in career_text:

                score += 8

                continue

            # Word-level match
            interest_words = set(
                interest_normalized.split()
            )

            career_words = set(
                career_text.split()
            )

            overlap = (
                interest_words &
                career_words
            )

            if overlap:
                score += min(
                    len(overlap) * 2,
                    5
                )

        return min(
            score,
            15
        )


    # ========================================================
    # DOMAIN MATCH
    # ========================================================

    def calculate_domain_match(
        self,
        detected_domain,
        career
    ):

        career_category = career.get(
            "category",
            ""
        )

        if not detected_domain:
            return 0

        if self.normalize(
            detected_domain
        ) == self.normalize(
            career_category
        ):

            return 12

        return 0


    # ========================================================
    # DEGREE MATCH
    # ========================================================

    def calculate_degree_match(
        self,
        student,
        career
    ):

        degree = self.normalize(
            student.get(
                "degree",
                ""
            )
        )

        if not degree:
            return 0

        category = self.normalize(
            career.get(
                "category",
                ""
            )
        )

        # Technology-oriented degrees
        technology_terms = [
            "computer",
            "data science",
            "information technology",
            "software",
            "engineering",
            "b.tech",
            "btech",
            "computer science",
            "it"
        ]

        if any(
            term in degree
            for term in technology_terms
        ):

            technology_categories = [
                "software development",
                "web development",
                "app development",
                "ai & machine learning",
                "cybersecurity",
                "cloud & devops",
                "database & infrastructure",
                "software testing",
                "it infrastructure",
                "data science & analytics",
                "research & advanced analytics",
                "technology management"
            ]

            if category in technology_categories:
                return 4

        return 0


    # ========================================================
    # PROJECT MATCH
    # ========================================================

    def calculate_project_bonus(
        self,
        student,
        career
    ):

        projects = student.get(
            "projects",
            []
        )

        if not projects:
            return 0

        if not isinstance(projects, list):
            projects = [projects]

        career_text = self.normalize(
            " ".join([
                career.get(
                    "title",
                    ""
                ),
                career.get(
                    "category",
                    ""
                ),
                career.get(
                    "description",
                    ""
                ),
                " ".join(
                    str(item)
                    for item in (
                        career.get("recommended_projects", [])
                        if isinstance(career.get("recommended_projects", []), list)
                        else [career.get("recommended_projects", "")]
                    )
                )
            ])
        )

        bonus = 0

        for project in projects:

            project_text = self.normalize(
                project
            )

            project_words = set(
                project_text.split()
            )

            career_words = set(
                career_text.split()
            )

            overlap = (
                project_words &
                career_words
            )

            if overlap:
                bonus += 2

        return min(
            bonus,
            6
        )


    # ========================================================
    # COMPLETE CAREER SCORE
    # ========================================================

    def calculate_career_score(
        self,
        student,
        career,
        detected_domain
    ):

        student_skills = self.get_student_skills(
            student
        )

        interests = self.get_student_interests(
            student
        )

        skill_result = self.calculate_skill_match(
            student_skills,
            career
        )

        skill_score = skill_result["score"]

        interest_score = self.calculate_interest_match(
            interests,
            career
        )

        domain_score = self.calculate_domain_match(
            detected_domain,
            career
        )

        degree_score = self.calculate_degree_match(
            student,
            career
        )

        project_score = self.calculate_project_bonus(
            student,
            career
        )

        # ----------------------------------------------------
        # FINAL SCORE
        # ----------------------------------------------------
        #
        # Skill match is the strongest factor.
        # Domain and interest help differentiate careers.
        #
        # Maximum:
        #
        # Skill      = 100
        # Interest   = 15
        # Domain     = 12
        # Degree     = 4
        # Projects   = 6
        #
        # Final normalized to 100.
        # ----------------------------------------------------

        raw_score = (
            skill_score * 0.70
            + interest_score * 0.12
            + domain_score * 0.12
            + degree_score * 0.03
            + project_score * 0.03
        )

        final_score = min(
            round(raw_score, 1),
            100
        )

        return {
            "score": final_score,
            "skill_score": skill_score,
            "interest_score": interest_score,
            "domain_score": domain_score,
            "degree_score": degree_score,
            "project_score": project_score,
            "skill_details": skill_result
        }


    # ========================================================
    # RANK ALL CAREERS
    # ========================================================

    def rank_careers(
        self,
        student
    ):

        detected_domain = self.detect_domain(
            student
        )

        ranked = []

        for career in self.careers:

            score_data = self.calculate_career_score(
                student,
                career,
                detected_domain
            )

            ranked.append({

                "role": career.get(
                    "title",
                    "Unknown Career"
                ),

                "category": career.get(
                    "category",
                    "General"
                ),

                "score": score_data["score"],

                "skill_score": score_data[
                    "skill_score"
                ],

                "interest_score": score_data[
                    "interest_score"
                ],

                "domain_score": score_data[
                    "domain_score"
                ],

                "degree_score": score_data[
                    "degree_score"
                ],

                "project_score": score_data[
                    "project_score"
                ]
            })

        ranked.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # Give rankings
        for index, item in enumerate(
            ranked,
            start=1
        ):

            item["rank"] = index

        return ranked


    # ========================================================
    # FIND CAREER
    # ========================================================

    def find_career(
        self,
        role_name
    ):

        normalized_role = self.normalize_role(
            role_name
        )

        for career in self.careers:

            if self.normalize(
                career.get(
                    "title",
                    ""
                )
            ) == self.normalize(
                normalized_role
            ):

                return career

        return None


    # ========================================================
    # GET JOB MARKET INFORMATION
    # ========================================================

    def get_market_information(
        self,
        career
    ):

        role = career.get(
            "title",
            ""
        )

        market = self.market_data

        # ----------------------------------------------------
        # FORMAT 1
        # {"Data Analyst": {...}}
        # ----------------------------------------------------

        if isinstance(
            market,
            dict
        ):

            if role in market:

                return market[role]

            # ------------------------------------------------
            # FORMAT 2
            # {"careers": [...]}
            # ------------------------------------------------

            market_careers = market.get(
                "careers",
                []
            )

            if isinstance(
                market_careers,
                list
            ):

                for item in market_careers:

                    if not isinstance(item, dict):
                        continue

                    if self.normalize(
                        item.get(
                            "title",
                            ""
                        )
                    ) == self.normalize(
                        role
                    ):

                        return item

        return {
            "demand_level": "Moderate",
            "common_industries": [],
            "entry_titles": [],
            "important_skills": [],
            "portfolio_expectations": [],
            "interview_focus": []
        }


    # ========================================================
    # GET LEARNING RESOURCE
    # ========================================================

    def get_learning_resource(
        self,
        skill
    ):

        normalized_skill = self.normalize(
            skill
        )

        # ----------------------------------------------------
        # Direct dictionary lookup
        # ----------------------------------------------------

        if isinstance(
            self.learning_data,
            dict
        ):

            for key, value in self.learning_data.items():

                if self.normalize(
                    key
                ) == normalized_skill:

                    return {
                        "skill": skill,
                        "resources": value
                    }

            # ------------------------------------------------
            # Sometimes resources are stored inside
            # {"resources": [...]}
            # ------------------------------------------------

            resources = self.learning_data.get(
                "resources",
                []
            )

            if isinstance(
                resources,
                list
            ):

                for resource in resources:

                    if not isinstance(resource, dict):
                        continue

                    resource_skill = resource.get(
                        "skill",
                        ""
                    )

                    if self.normalize(
                        resource_skill
                    ) == normalized_skill:

                        return resource

        return {
            "skill": skill,
            "resources": []
        }


    # ========================================================
    # GET LEARNING RESOURCES
    # ========================================================

    def get_learning_resources(
        self,
        skills
    ):

        results = []

        for skill in skills[:6]:

            resource = self.get_learning_resource(
                skill
            )

            results.append(
                resource
            )

        return results


    # ========================================================
    # GENERATE ROADMAP
    # ========================================================

    def generate_roadmap(
        self,
        career,
        missing_skills,
        improve_skills
    ):

        roadmap = []

        priority_skills = []

        # Core missing skills first
        priority_skills.extend(
            missing_skills[:3]
        )

        # Then important skills
        priority_skills.extend(
            improve_skills[:2]
        )

        priority_skills = list(
            dict.fromkeys(
                priority_skills
            )
        )

        # ----------------------------------------------------
        # MONTH 1
        # ----------------------------------------------------

        month1_skills = priority_skills[:2]

        roadmap.append({

            "month": "Month 1",

            "focus": "Foundation",

            "skills": month1_skills,

            "description":
                "Build strong fundamentals in the highest-priority skills required for your target career."
        })

        # ----------------------------------------------------
        # MONTH 2
        # ----------------------------------------------------

        month2_skills = priority_skills[2:4]

        roadmap.append({

            "month": "Month 2",

            "focus": "Skill Development",

            "skills": month2_skills,

            "description":
                "Strengthen practical skills through exercises, tutorials, and small hands-on tasks."
        })

        # ----------------------------------------------------
        # MONTH 3
        # ----------------------------------------------------

        roadmap.append({

            "month": "Month 3",

            "focus": "Project Building",

            "skills": [
                "Practical Project"
            ],

            "description":
                f"Build a portfolio project related to {career.get('title', 'your target career')} and demonstrate your newly acquired skills."
        })

        # ----------------------------------------------------
        # MONTH 4
        # ----------------------------------------------------

        roadmap.append({

            "month": "Month 4",

            "focus": "Job Preparation",

            "skills": [
                "Resume",
                "Interview Preparation",
                "Portfolio"
            ],

            "description":
                "Prepare your resume, improve your portfolio, practice interviews, and apply for internships or entry-level opportunities."
        })

        return roadmap


    # ========================================================
    # RECOMMEND PROJECTS
    # ========================================================

    def recommend_projects(
        self,
        career
    ):

        projects = career.get(
            "recommended_projects",
            []
        )

        if projects:
            return projects

        return [
            f"Build a real-world project related to {career.get('title', 'your career')}"
        ]


    # ========================================================
    # JOB READINESS
    # ========================================================

    def calculate_job_readiness(
        self,
        student,
        career_score
    ):

        readiness = career_score

        # ----------------------------------------------------
        # PROJECTS
        # ----------------------------------------------------

        projects = student.get(
            "projects",
            []
        )

        if projects:
            readiness += 5

        # ----------------------------------------------------
        # EXPERIENCE
        # ----------------------------------------------------

        experience = student.get(
            "experience",
            []
        )

        if experience:
            readiness += 5

        # ----------------------------------------------------
        # CGPA
        # ----------------------------------------------------

        try:

            cgpa = float(
                student.get(
                    "cgpa",
                    0
                )
            )

        except (
            ValueError,
            TypeError
        ):

            cgpa = 0

        if cgpa >= 9:
            readiness += 6

        elif cgpa >= 8:
            readiness += 5

        elif cgpa >= 7:
            readiness += 3

        # ----------------------------------------------------
        # SOFT SKILLS
        # ----------------------------------------------------

        soft_skill_names = {
            "communication",
            "problem solving",
            "critical thinking",
            "teamwork",
            "leadership",
            "time management",
            "adaptability",
            "presentation",
            "creativity"
        }

        student_skills = {
            self.normalize(skill)
            for skill in self.get_student_skills(
                student
            )
        }

        soft_skill_count = len(
            student_skills &
            soft_skill_names
        )

        readiness += min(
            soft_skill_count,
            4
        )

        return min(
            round(readiness),
            100
        )


    # ========================================================
    # READINESS LEVEL
    # ========================================================

    def get_readiness_level(
        self,
        score
    ):

        if score >= 85:
            return "Highly Ready"

        if score >= 70:
            return "Job Ready"

        if score >= 50:
            return "Developing"

        return "Beginner"


    # ========================================================
    # GENERATE REASONING
    # ========================================================

    def generate_reasoning(
        self,
        student,
        selected_career,
        selected_score,
        detected_domain,
        strong_skills,
        missing_skills
    ):

        role = selected_career.get(
            "title",
            "this career"
        )

        if strong_skills:

            strengths_text = ", ".join(
                strong_skills[:3]
            )

        else:

            strengths_text = "your current skill profile"

        if missing_skills:

            missing_text = ", ".join(
                missing_skills[:3]
            )

        else:

            missing_text = "the remaining career-specific skills"

        return (
            f"Your strongest current career direction is "
            f"{role}, with a {selected_score}% profile match. "
            f"Your profile shows strengths in {strengths_text}. "
            f"The analysis also considers your detected domain "
            f"({detected_domain}) and your interests. "
            f"To become more competitive for this career, "
            f"focus next on {missing_text}, then demonstrate "
            f"your skills through portfolio projects."
        )


    # ========================================================
    # MAIN ANALYSIS
    # ========================================================

    def analyze(
        self,
        student
    ):

        if not isinstance(student, dict):
            raise ValueError("Student profile must be a JSON object.")

        # ----------------------------------------------------
        # BASIC STUDENT INFORMATION
        # ----------------------------------------------------

        student_name = student.get(
            "name",
            "Student"
        )

        student_skills = self.get_student_skills(
            student
        )

        interests = self.get_student_interests(
            student
        )

        target_role = student.get(
            "target_role",
            ""
        )

        # ----------------------------------------------------
        # DOMAIN DETECTION
        # ----------------------------------------------------

        detected_domain = self.detect_domain(
            student
        )

        # ----------------------------------------------------
        # RANK CAREERS
        # ----------------------------------------------------

        ranked_careers = self.rank_careers(
            student
        )

        if not ranked_careers:

            return {
                "student_name": student_name,
                "career_match": {
                    "role": "No career found",
                    "score": 0
                },
                "career_matches": [],
                "skills": {
                    "strong": [],
                    "improve": [],
                    "missing": []
                },
                "recommended_skills": [],
                "job_readiness": 0,
                "job_readiness_level": "Beginner",
                "roadmap": [],
                "recommended_projects": [],
                "learning_resources": [],
                "market_information": {},
                "career_growth": [],
                "responsibilities": [],
                "reasoning": "No career roles were found in the Knowledge Base."
            }

        # ----------------------------------------------------
        # TARGET ROLE HANDLING
        # ----------------------------------------------------

        if not self.is_undecided(
            target_role
        ):

            normalized_target = self.normalize_role(
                target_role
            )

            target_career = self.find_career(
                normalized_target
            )

            if target_career:

                # Explicit target gets selected,
                # but ranking remains visible.
                selected_career = target_career

                selected_score_data = self.calculate_career_score(
                    student,
                    target_career,
                    detected_domain
                )

            else:

                selected_career = self.find_career(
                    ranked_careers[0]["role"]
                ) or {}

                selected_score_data = self.calculate_career_score(
                    student,
                    selected_career,
                    detected_domain
                )

        else:

            # No target selected:
            # choose highest-ranked career.
            selected_career = self.find_career(
                ranked_careers[0]["role"]
            ) or {}

            selected_score_data = self.calculate_career_score(
                student,
                selected_career,
                detected_domain
            )

        # ----------------------------------------------------
        # SKILL DETAILS
        # ----------------------------------------------------

        skill_details = selected_score_data[
            "skill_details"
        ]

        strong_skills = skill_details[
            "strong"
        ]

        improve_skills = skill_details[
            "improve"
        ]

        missing_skills = skill_details[
            "missing"
        ]

        # ----------------------------------------------------
        # RECOMMENDED SKILLS
        # ----------------------------------------------------

        recommended_skills = list(
            dict.fromkeys(
                missing_skills +
                improve_skills
            )
        )[:6]

        # ----------------------------------------------------
        # JOB READINESS
        # ----------------------------------------------------

        readiness = self.calculate_job_readiness(
            student,
            selected_score_data["score"]
        )

        readiness_level = self.get_readiness_level(
            readiness
        )

        # ----------------------------------------------------
        # ROADMAP
        # ----------------------------------------------------

        roadmap = self.generate_roadmap(
            selected_career,
            missing_skills,
            improve_skills
        )

        # ----------------------------------------------------
        # PROJECTS
        # ----------------------------------------------------

        projects = self.recommend_projects(
            selected_career
        )

        # ----------------------------------------------------
        # LEARNING
        # ----------------------------------------------------

        learning_resources = self.get_learning_resources(
            recommended_skills
        )

        # ----------------------------------------------------
        # MARKET INFORMATION
        # ----------------------------------------------------

        market_information = self.get_market_information(
            selected_career
        )

        # ----------------------------------------------------
        # REASONING
        # ----------------------------------------------------

        reasoning = self.generate_reasoning(
            student,
            selected_career,
            selected_score_data["score"],
            detected_domain,
            strong_skills,
            missing_skills
        )

        # ----------------------------------------------------
        # TOP CAREER MATCHES
        # ----------------------------------------------------

        career_matches = ranked_careers[:8]

        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        return {

            "student_name":
                student_name,

            "detected_domain":
                detected_domain,

            "target_role":
                target_role,

            "career_match": {

                "role":
                    selected_career.get(
                        "title",
                        "Unknown"
                    ),

                "category":
                    selected_career.get(
                        "category",
                        ""
                    ),

                "score":
                    selected_score_data[
                        "score"
                    ]
            },

            "career_matches":
                career_matches,

            "skills": {

                "strong":
                    strong_skills,

                "improve":
                    improve_skills,

                "missing":
                    missing_skills
            },

            "selected_skills":
                student_skills,

            "interests":
                interests,

            "recommended_skills":
                recommended_skills,

            "job_readiness":
                readiness,

            "job_readiness_level":
                readiness_level,

            "roadmap":
                roadmap,

            "recommended_projects":
                projects,

            "learning_resources":
                learning_resources,

            "market_information":
                market_information,

            "career_growth":
                selected_career.get(
                    "career_growth",
                    []
                ),

            "responsibilities":
                selected_career.get(
                    "responsibilities",
                    []
                ),

            "reasoning":
                reasoning
        }


    # ========================================================
    # HEALTH / DIAGNOSTICS
    # ========================================================

    def diagnostics(self):
        """Return safe diagnostics for the Flask health endpoint."""
        files = [
            "career_roles.json",
            "skills.json",
            "learning_resources.json",
            "job_market.json",
        ]

        return {
            "knowledge_base_directory": self.knowledge_base_directory,
            "knowledge_base_exists": os.path.isdir(self.knowledge_base_directory),
            "careers_loaded": len(self.careers),
            "files": {
                filename: os.path.isfile(
                    os.path.join(self.knowledge_base_directory, filename)
                )
                for filename in files
            },
        }


# ============================================================
# END OF CAREER AGENT
# ============================================================