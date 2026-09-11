class ProjectTool:

    def get(self, analysis):

        if not analysis:
            return []

        return (
            analysis.get("projects")
            or analysis.get("recommended_projects")
            or []
        )