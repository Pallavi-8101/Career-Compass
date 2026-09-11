class SkillTool:

    def analyze(self, analysis):

        if not analysis:
            return {
                "strong_skills": [],
                "improvement_skills": [],
                "recommended_skills": []
            }

        skills = analysis.get("skills", {})

        strong = (
            analysis.get("strong_skills")
            or skills.get("strong")
            or []
        )

        improve = (
            analysis.get("skills_to_improve")
            or skills.get("improve")
            or skills.get("missing")
            or []
        )

        recommended = (
            analysis.get("recommended_skills")
            or []
        )

        return {
            "strong_skills": strong,
            "improvement_skills": improve,
            "recommended_skills": recommended
        }