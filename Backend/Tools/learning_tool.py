class LearningTool:

    def get(self, analysis):

        if not analysis:
            return []

        return (
            analysis.get("learning_resources")
            or analysis.get("learning")
            or []
        )