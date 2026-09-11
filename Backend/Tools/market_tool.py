class MarketTool:

    def get(self, analysis):

        if not analysis:
            return {}

        return (
            analysis.get("market_information")
            or analysis.get("market")
            or {}
        )