class RoadmapTool:

    def get(self, analysis):

        if not analysis:
            return []

        return (
            analysis.get("roadmap")
            or analysis.get("career_roadmap")
            or []
        )