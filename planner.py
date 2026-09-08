import re


class AgentPlanner:

    """
    Career Compass Agent Planner

    Responsibilities:
    - Detect the user's intent
    - Detect career names mentioned in comparison questions
    - Decide which tools should run
    - Prevent unnecessary profile analysis
    """

    def __init__(self):

        # ======================================================
        # CAREER COMPARISON KEYWORDS
        # ======================================================

        self.compare_keywords = [

            "compare",
            "comparison",
            "difference between",
            "difference",
            "vs",
            "versus",
            "or better",
            "which is better",
            "which one is better",
            "which career is better",
            "better career"
        ]

        # ======================================================
        # GREETING KEYWORDS
        # ======================================================

        self.greeting_keywords = [

            "hi",
            "hello",
            "hey",
            "hii",
            "heyy",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        # ======================================================
        # HELP KEYWORDS
        # ======================================================

        self.help_keywords = [

            "help",
            "what can you do",
            "how can you help",
            "features",
            "commands"
        ]

        # ======================================================
        # CAREER DISCOVERY KEYWORDS
        # ======================================================

        self.career_keywords = [

            "career recommendation",
            "recommend a career",
            "recommend careers",
            "best career",
            "best careers",
            "which career",
            "which career suits me",
            "career for me",
            "career options",
            "career path",
            "what career",
            "suggest a career",
            "suggest careers"
        ]

        # ======================================================
        # SKILL GAP KEYWORDS
        # ======================================================

        self.skill_keywords = [

            "skill gap",
            "skills missing",
            "missing skills",
            "what skills",
            "skills should i learn",
            "skills do i need",
            "improve my skills",
            "skills to improve",
            "skills am i missing"
        ]

        # ======================================================
        # ROADMAP KEYWORDS
        # ======================================================

        self.roadmap_keywords = [

            "roadmap",
            "learning path",
            "career plan",
            "step by step",
            "what should i learn first",
            "what should i do next",
            "plan for my career"
        ]

        # ======================================================
        # PROJECT KEYWORDS
        # ======================================================

        self.project_keywords = [

            "project ideas",
            "projects",
            "project",
            "portfolio project",
            "portfolio projects",
            "what project",
            "what projects"
        ]

        # ======================================================
        # LEARNING KEYWORDS
        # ======================================================

        self.learning_keywords = [

            "learn",
            "learning",
            "course",
            "courses",
            "resource",
            "resources",
            "study",
            "tutorial",
            "how do i learn"
        ]

        # ======================================================
        # JOB READINESS KEYWORDS
        # ======================================================

        self.readiness_keywords = [

            "job readiness",
            "job ready",
            "am i ready",
            "ready for job",
            "readiness score",
            "placement ready",
            "placement readiness"
        ]

        # ======================================================
        # MARKET KEYWORDS
        # ======================================================

        self.market_keywords = [

            "market",
            "job market",
            "market demand",
            "demand",
            "future scope",
            "scope",
            "opportunities",
            "job opportunities"
        ]

        # ======================================================
        # FOLLOW-UP KEYWORDS
        # ======================================================

        self.follow_up_keywords = [

            "tell me more",
            "explain more",
            "continue",
            "what next",
            "then what",
            "go on"
        ]

    # ==========================================================
    # NORMALIZE TEXT
    # ==========================================================

    def normalize(self, text):

        if not text:
            return ""

        text = text.lower().strip()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text

    # ==========================================================
    # CHECK KEYWORDS
    # ==========================================================

    def contains_keyword(
        self,
        text,
        keywords
    ):

        for keyword in keywords:

            if keyword in text:
                return True

        return False

    # ==========================================================
    # CLASSIFY USER INTENT
    # ==========================================================

    def classify(self, message):

        text = self.normalize(message)

        # ======================================================
        # EMPTY MESSAGE
        # ======================================================

        if not text:
            return "unknown"

        # ======================================================
        # CAREER COMPARISON
        #
        # IMPORTANT:
        # This MUST be checked before career discovery.
        #
        # Example:
        # "Compare Operations Analyst with Data Analyst"
        #
        # Otherwise "career" or role-related wording may
        # incorrectly trigger career_discovery.
        # ======================================================

        if self.contains_keyword(
            text,
            self.compare_keywords
        ):

            return "career_compare"

        # Extra patterns such as:
        # "Data Analyst vs Operations Analyst"

        if re.search(
            r"\b[a-z ]+\s+(?:vs|versus)\s+[a-z ]+\b",
            text
        ):

            return "career_compare"

        # ======================================================
        # GREETING
        # ======================================================

        if text in self.greeting_keywords:

            return "greeting"

        if len(text.split()) <= 4:

            for greeting in self.greeting_keywords:

                if text.startswith(greeting):

                    return "greeting"

        # ======================================================
        # HELP
        # ======================================================

        if self.contains_keyword(
            text,
            self.help_keywords
        ):

            return "help"

        # ======================================================
        # JOB READINESS
        # ======================================================

        if self.contains_keyword(
            text,
            self.readiness_keywords
        ):

            return "readiness"

        # ======================================================
        # SKILL GAP
        # ======================================================

        if self.contains_keyword(
            text,
            self.skill_keywords
        ):

            return "skill_gap"

        # ======================================================
        # ROADMAP
        # ======================================================

        if self.contains_keyword(
            text,
            self.roadmap_keywords
        ):

            return "roadmap"

        # ======================================================
        # PROJECTS
        # ======================================================

        if self.contains_keyword(
            text,
            self.project_keywords
        ):

            return "project"

        # ======================================================
        # MARKET
        # ======================================================

        if self.contains_keyword(
            text,
            self.market_keywords
        ):

            return "market"

        # ======================================================
        # LEARNING
        # ======================================================

        if self.contains_keyword(
            text,
            self.learning_keywords
        ):

            return "learning"

        # ======================================================
        # CAREER DISCOVERY
        # ======================================================

        if self.contains_keyword(
            text,
            self.career_keywords
        ):

            return "career_discovery"

        # ======================================================
        # FOLLOW-UP
        # ======================================================

        if self.contains_keyword(
            text,
            self.follow_up_keywords
        ):

            return "follow_up"

        # ======================================================
        # DEFAULT
        # ======================================================

        return "unknown"

    # ==========================================================
    # CREATE TOOL EXECUTION PLAN
    # ==========================================================

    def create_plan(
        self,
        intent,
        has_profile,
        has_analysis
    ):

        plan = []

        # ======================================================
        # GREETING / HELP
        # ======================================================

        if intent in [
            "greeting",
            "help"
        ]:

            return plan

        # ======================================================
        # CAREER COMPARISON
        #
        # IMPORTANT:
        #
        # A career comparison should NOT automatically run
        # profile analysis.
        #
        # Example:
        #
        # "Compare Operations Analyst with Data Analyst"
        #
        # This is asking for role-vs-role information,
        # not "Which career matches my profile?"
        #
        # The comparison should use career_roles.json.
        # ======================================================

        if intent == "career_compare":

            plan.append(
                "career_compare_tool"
            )

            return plan

        # ======================================================
        # CAREER DISCOVERY
        # ======================================================

        if intent == "career_discovery":

            if has_profile and not has_analysis:

                plan.append(
                    "analyze_profile"
                )

            if has_profile:

                plan.append(
                    "career_tool"
                )

            return plan

        # ======================================================
        # SKILL GAP
        # ======================================================

        if intent == "skill_gap":

            if has_profile and not has_analysis:

                plan.append(
                    "analyze_profile"
                )

            if has_analysis:

                plan.append(
                    "skill_tool"
                )

            return plan

        # ======================================================
        # ROADMAP
        # ======================================================

        if intent == "roadmap":

            if has_profile and not has_analysis:

                plan.append(
                    "analyze_profile"
                )

            if has_analysis:

                plan.append(
                    "roadmap_tool"
                )

            return plan

        # ======================================================
        # PROJECTS
        # ======================================================

        if intent == "project":

            if has_profile and not has_analysis:

                plan.append(
                    "analyze_profile"
                )

            if has_analysis:

                plan.append(
                    "project_tool"
                )

            return plan

        # ======================================================
        # LEARNING
        # ======================================================

        if intent == "learning":

            if has_profile and not has_analysis:

                plan.append(
                    "analyze_profile"
                )

            if has_analysis:

                plan.append(
                    "learning_tool"
                )

            return plan

        # ======================================================
        # JOB READINESS
        # ======================================================

        if intent == "readiness":

            if has_profile and not has_analysis:

                plan.append(
                    "analyze_profile"
                )

            if has_analysis:

                plan.append(
                    "readiness_tool"
                )

            return plan

        # ======================================================
        # MARKET
        # ======================================================

        if intent == "market":

            if has_profile and not has_analysis:

                plan.append(
                    "analyze_profile"
                )

            if has_analysis:

                plan.append(
                    "market_tool"
                )

            return plan

        # ======================================================
        # FOLLOW-UP
        # ======================================================

        if intent == "follow_up":

            if has_profile and not has_analysis:

                plan.append(
                    "analyze_profile"
                )

            return plan

        # ======================================================
        # UNKNOWN
        # ======================================================

        return plan