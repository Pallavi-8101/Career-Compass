from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

from agent import CareerAgent
from companion_agent import CareerCompanionAgent


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)

# Allow the frontend to communicate with Flask
CORS(app)


# =========================================================
# INITIALIZE CAREER ENGINE
# =========================================================

career_engine = CareerAgent()


# =========================================================
# INITIALIZE CAREER COMPANION AGENT
# =========================================================

career_companion = CareerCompanionAgent(
    career_engine
)


# =========================================================
# HOME / HEALTH CHECK
# =========================================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "agent": "Career Compass Companion",
        "message": "Career Compass Agent is running.",
        "status": "online"
    })


# =========================================================
# ANALYZE STUDENT PROFILE
# =========================================================

@app.route("/api/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json(silent=True) or {}

        profile = data.get("profile", {})

        # -------------------------------------------------
        # Get existing session ID if supplied
        # -------------------------------------------------

        session_id = data.get("session_id")

        # -------------------------------------------------
        # Create a session if none exists
        # -------------------------------------------------

        if not session_id:

            session_id = career_companion.new_session()

        # -------------------------------------------------
        # Make sure memory session exists
        # -------------------------------------------------

        from memory import memory_store

        memory_store.create_session(
            session_id
        )

        # -------------------------------------------------
        # Save student profile
        # -------------------------------------------------

        if profile:

            career_companion.update_profile(
                session_id,
                profile
            )

        # -------------------------------------------------
        # Run career analysis
        # -------------------------------------------------

        analysis = career_companion.analyze_profile(
            session_id
        )

        # -------------------------------------------------
        # Return result
        # -------------------------------------------------

        return jsonify({
            "success": True,
            "session_id": session_id,
            "data": analysis
        })

    except Exception as error:

        print(
            "ERROR in /api/analyze:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# CHAT API
# =========================================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(silent=True) or {}

        # -------------------------------------------------
        # Read request
        # -------------------------------------------------

        session_id = data.get(
            "session_id"
        )

        message = data.get(
            "message"
        )

        profile = data.get(
            "profile"
        )

        analysis = data.get(
            "analysis"
        )

        # -------------------------------------------------
        # Validate message
        # -------------------------------------------------

        if not message:

            return jsonify({
                "success": False,
                "error": "Message is required."
            }), 400

        # -------------------------------------------------
        # Create session when needed
        # -------------------------------------------------

        if not session_id:

            session_id = career_companion.new_session()

        # -------------------------------------------------
        # Run Career Compass Agent
        # -------------------------------------------------

        result = career_companion.chat(
            session_id=session_id,
            message=message,
            profile=profile,
            analysis=analysis
        )

        # -------------------------------------------------
        # Return agent response
        # -------------------------------------------------

        return jsonify(result)

    except Exception as error:

        print(
            "ERROR in /api/chat:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# GET SESSION
# =========================================================

@app.route(
    "/api/session/<session_id>",
    methods=["GET"]
)
def get_session(session_id):

    try:

        from memory import memory_store

        session = memory_store.get_session(
            session_id
        )

        return jsonify({
            "success": True,
            "session": session
        })

    except Exception as error:

        print(
            "ERROR in /api/session:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# RESET SESSION
# =========================================================

@app.route(
    "/api/reset",
    methods=["POST"]
)
def reset_session():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        session_id = data.get(
            "session_id"
        )

        # -------------------------------------------------
        # Validate session ID
        # -------------------------------------------------

        if not session_id:

            return jsonify({
                "success": False,
                "error": "session_id is required."
            }), 400

        # -------------------------------------------------
        # Reset memory
        # -------------------------------------------------

        from memory import memory_store

        memory_store.reset(
            session_id
        )

        return jsonify({
            "success": True,
            "message": "Session reset successfully.",
            "session_id": session_id
        })

    except Exception as error:

        print(
            "ERROR in /api/reset:",
            error
        )

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# API TEST
# =========================================================

@app.route(
    "/api/test",
    methods=["GET"]
)
def test():

    return jsonify({
        "success": True,
        "message": "Career Compass API is working.",
        "endpoints": {
            "health": "/",
            "test": "/api/test",
            "analyze": "/api/analyze",
            "chat": "/api/chat",
            "session": "/api/session/<session_id>",
            "reset": "/api/reset"
        }
    })


# =========================================================
# 404 ERROR HANDLER
# =========================================================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "error": "Endpoint not found."
    }), 404


# =========================================================
# 500 ERROR HANDLER
# =========================================================

@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "success": False,
        "error": "Internal server error."
    }), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("        CAREER COMPASS COMPANION AGENT")
    print("=" * 60)
    print()
    print("Backend URL:")
    print("http://127.0.0.1:5000")
    print()
    print("Available API endpoints:")
    print()
    print("GET  /")
    print("GET  /api/test")
    print("POST /api/analyze")
    print("POST /api/chat")
    print("GET  /api/session/<session_id>")
    print("POST /api/reset")
    print()
    print("=" * 60)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )