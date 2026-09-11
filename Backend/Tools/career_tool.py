# ============================================================
# CAREER COMPASS - CAREER TOOL
# Career Analysis + Career Comparison
# ============================================================

import json
import os
import re


class CareerTool:

    def __init__(self, agent_engine):

        self.agent_engine = agent_engine

        # ----------------------------------------------------
        # FIND KNOWLEDGE BASE
        # ----------------------------------------------------

        backend_directory = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        project_directory = os.path.dirname(
            backend_directory
        )

        possible_paths = [

            os.path.join(
                backend_directory,
                "knowledge_base",
                "career_roles.json"
            ),

            os.path.join(
                project_directory,
                "Knowledge_base",
                "career_roles.json"
            ),

            os.path.join(
                project_directory,
                "knowledge_base",
                "career_roles.json"
            )

        ]

        self.career_roles_path = None

        for path in possible_paths:

            if os.path.isfile(path):

                self.career_roles_path = path

                break

        # ----------------------------------------------------
        # LOAD CAREER DATA
        # ----------------------------------------------------

        self.careers_data = self._load_careers()

        self.careers = self._extract_careers()

    # ========================================================
    # LOAD CAREERS
    # ========================================================

    def _load_careers(self):

        if not self.career_roles_path:

            print(
                "WARNING: career_roles.json not found."
            )

            return []

        try:

            with open(
                self.career_roles_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if isinstance(data, dict):

                careers = data.get(
                    "careers",
                    []
                )

                if isinstance(careers, list):

                    return careers

            if isinstance(data, list):

                return data

        except Exception as error:

            print(
                "Career roles loading error:",
                error
            )

        return []

    # ========================================================
    # EXTRACT CAREERS
    # ========================================================

    def _extract_careers(self):

        careers = []

        for career in self.careers_data:

            if not isinstance(
                career,
                dict
            ):

                continue

            title = career.get(
                "title"
            )

            if not title:

                continue

            careers.append(
                career
            )

        return careers

    # ========================================================
    # NORMALIZE TEXT
    # ========================================================

    def _normalize(self, value):

        if value is None:

            return ""

        value = str(value).lower().strip()

        value = re.sub(
            r"[^a-z0-9+#./&\-\s]",
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
    # GET CAREER NAMES
    # ========================================================

    def get_career_names(self):

        return [
            career.get("title")
            for career in self.careers
            if career.get("title")
        ]

    # ========================================================
    # FIND CAREER
    # ========================================================

    def find_career(self, career_name):

        if not career_name:

            return None

        target = self._normalize(
            career_name
        )

        # Exact normalized match

        for career in self.careers:

            title = career.get(
                "title",
                ""
            )

            if self._normalize(title) == target:

                return career

        # Partial match

        for career in self.careers:

            title = self._normalize(
                career.get(
                    "title",
                    ""
                )
            )

            if (
                target in title
                or
                title in target
            ):

                return career

        return None

    # ========================================================
    # EXTRACT CAREER NAMES FROM MESSAGE
    # ========================================================

    def extract_career_names(
        self,
        message
    ):

        if not message:

            return []

        normalized_message = self._normalize(
            message
        )

        matches = []

        # ----------------------------------------------------
        # IMPORTANT:
        # Longest names first prevents shorter names from
        # incorrectly matching part of longer career names.
        # ----------------------------------------------------

        careers = sorted(
            self.careers,
            key=lambda career: len(
                self._normalize(
                    career.get(
                        "title",
                        ""
                    )
                )
            ),
            reverse=True
        )

        for career in careers:

            title = career.get(
                "title"
            )

            if not title:

                continue

            normalized_title = self._normalize(
                title
            )

            if not normalized_title:

                continue

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(normalized_title)
                + r"(?![a-z0-9])"
            )

            if re.search(
                pattern,
                normalized_message
            ):

                if title not in matches:

                    matches.append(
                        title
                    )

        return matches

    # ========================================================
    # ANALYZE PROFILE
    # ========================================================

    def analyze(self, profile):

        method_names = [

            "analyze",
            "analyze_student",
            "analyze_profile",
            "run_analysis"

        ]

        for method_name in method_names:

            method = getattr(
                self.agent_engine,
                method_name,
                None
            )

            if callable(method):

                try:

                    return method(
                        profile
                    )

                except TypeError:

                    continue

        raise RuntimeError(
            "Could not find a compatible analysis method "
            "in CareerAgent."
        )

    # ========================================================
    # GET TOP CAREERS
    # ========================================================

    def get_top_careers(
        self,
        analysis
    ):

        if not analysis:

            return []

        for key in [

            "career_matches",
            "career_recommendations",
            "matches",
            "careers"

        ]:

            value = analysis.get(
                key
            )

            if isinstance(
                value,
                list
            ):

                return value

        career_match = analysis.get(
            "career_match"
        )

        if career_match:

            return [
                career_match
            ]

        return []

    # ========================================================
    # PROFILE SKILL NORMALIZATION
    # ========================================================

    def _normalize_skill(
        self,
        skill
    ):

        if not skill:

            return ""

        normalized = self._normalize(
            skill
        )

        aliases = {

            "powerbi": "power bi",

            "power bi": "power bi",

            "ms excel": "excel",

            "microsoft excel": "excel",

            "github": "git/github",

            "git hub": "git/github",

            "git": "git/github",

            "html": "html/css",

            "html5": "html/css",

            "css": "html/css",

            "css3": "html/css",

            "data visualisation":
                "data visualization",

            "problem-solving":
                "problem solving",

            "communication skills":
                "communication",

            "presentation skills":
                "presentation",

            "api":
                "apis"

        }

        return aliases.get(
            normalized,
            normalized
        )

    # ========================================================
    # GET PROFILE SKILLS
    # ========================================================

    def _get_profile_skills(
        self,
        profile
    ):

        skills = profile.get(
            "skills",
            []
        )

        if not isinstance(
            skills,
            list
        ):

            skills = [
                skills
            ]

        normalized = set()

        for skill in skills:

            value = self._normalize_skill(
                skill
            )

            if value:

                normalized.add(
                    value
                )

        return normalized

    # ========================================================
    # ROLE SKILLS
    # ========================================================

    def _get_role_skill_groups(
        self,
        career
    ):

        core = career.get(
            "core_skills",
            []
        )

        important = career.get(
            "important_skills",
            []
        )

        nice = career.get(
            "nice_to_have",
            career.get(
                "nice_skills",
                []
            )
        )

        if not isinstance(
            core,
            list
        ):

            core = []

        if not isinstance(
            important,
            list
        ):

            important = []

        if not isinstance(
            nice,
            list
        ):

            nice = []

        return (
            core,
            important,
            nice
        )

    # ========================================================
    # CALCULATE SKILL FIT
    #
    # Same basic weighting philosophy as Career Compass:
    #
    # Core      = 15
    # Important = 7
    # Nice      = 3
    # ========================================================

    def _calculate_skill_fit(
        self,
        profile,
        career
    ):

        profile_skills = self._get_profile_skills(
            profile
        )

        core, important, nice = (
            self._get_role_skill_groups(
                career
            )
        )

        total_weight = 0
        matched_weight = 0

        matched_core = []
        missing_core = []

        matched_important = []
        missing_important = []

        matched_nice = []
        missing_nice = []

        # ----------------------------------------------------
        # CORE
        # ----------------------------------------------------

        for skill in core:

            total_weight += 15

            normalized_skill = self._normalize_skill(
                skill
            )

            if normalized_skill in profile_skills:

                matched_weight += 15

                matched_core.append(
                    skill
                )

            else:

                missing_core.append(
                    skill
                )

        # ----------------------------------------------------
        # IMPORTANT
        # ----------------------------------------------------

        for skill in important:

            total_weight += 7

            normalized_skill = self._normalize_skill(
                skill
            )

            if normalized_skill in profile_skills:

                matched_weight += 7

                matched_important.append(
                    skill
                )

            else:

                missing_important.append(
                    skill
                )

        # ----------------------------------------------------
        # NICE TO HAVE
        # ----------------------------------------------------

        for skill in nice:

            total_weight += 3

            normalized_skill = self._normalize_skill(
                skill
            )

            if normalized_skill in profile_skills:

                matched_weight += 3

                matched_nice.append(
                    skill
                )

            else:

                missing_nice.append(
                    skill
                )

        if total_weight == 0:

            score = 0

        else:

            score = (
                matched_weight
                /
                total_weight
            ) * 100

        return {

            "skill_fit_score":
                round(score, 1),

            "matched_core":
                matched_core,

            "missing_core":
                missing_core,

            "matched_important":
                matched_important,

            "missing_important":
                missing_important,

            "matched_nice":
                matched_nice,

            "missing_nice":
                missing_nice,

            "matched_skills":
                (
                    matched_core
                    +
                    matched_important
                    +
                    matched_nice
                ),

            "missing_skills":
                (
                    missing_core
                    +
                    missing_important
                    +
                    missing_nice
                )

        }

    # ========================================================
    # COMPARE CAREERS
    # ========================================================

    def compare_careers(
        self,
        profile,
        requested_names
    ):

        if not isinstance(
            requested_names,
            list
        ):

            requested_names = []

        results = []

        for requested_name in requested_names:

            career = self.find_career(
                requested_name
            )

            if not career:

                continue

            fit = self._calculate_skill_fit(
                profile,
                career
            )

            result = {

                "title":
                    career.get(
                        "title",
                        requested_name
                    ),

                "category":
                    career.get(
                        "category",
                        ""
                    ),

                "description":
                    career.get(
                        "description",
                        ""
                    ),

                "core_skills":
                    career.get(
                        "core_skills",
                        []
                    ),

                "important_skills":
                    career.get(
                        "important_skills",
                        []
                    ),

                "nice_to_have":
                    career.get(
                        "nice_to_have",
                        career.get(
                            "nice_skills",
                            []
                        )
                    ),

                "skill_fit_score":
                    fit[
                        "skill_fit_score"
                    ],

                "matched_core":
                    fit[
                        "matched_core"
                    ],

                "missing_core":
                    fit[
                        "missing_core"
                    ],

                "matched_important":
                    fit[
                        "matched_important"
                    ],

                "missing_important":
                    fit[
                        "missing_important"
                    ],

                "matched_nice":
                    fit[
                        "matched_nice"
                    ],

                "missing_nice":
                    fit[
                        "missing_nice"
                    ],

                "matched_skills":
                    fit[
                        "matched_skills"
                    ],

                "missing_skills":
                    fit[
                        "missing_skills"
                    ]

            }

            results.append(
                result
            )

        # ----------------------------------------------------
        # PERSONALIZED WINNER
        # ----------------------------------------------------

        winner = None

        if results:

            winner = max(
                results,
                key=lambda item:
                    item.get(
                        "skill_fit_score",
                        0
                    )
            )

        return {

            "requested_careers":
                [
                    item["title"]
                    for item in results
                ],

            "careers":
                results,

            "best_match":
                winner["title"]
                if winner
                else None,

            "best_match_score":
                winner["skill_fit_score"]
                if winner
                else None

        }