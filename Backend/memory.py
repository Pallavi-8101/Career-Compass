from copy import deepcopy
from datetime import datetime
from threading import RLock


class ConversationMemory:

    def __init__(self):
        self.sessions = {}
        self.lock = RLock()

    def create_session(self, session_id):
        with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    "session_id": session_id,
                    "profile": {},
                    "analysis": None,
                    "goal": None,
                    "history": [],
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }

            return deepcopy(self.sessions[session_id])

    def get_session(self, session_id):
        with self.lock:
            if session_id not in self.sessions:
                self.create_session(session_id)

            return deepcopy(self.sessions[session_id])

    def update_profile(self, session_id, profile):
        with self.lock:
            self.create_session(session_id)

            current = self.sessions[session_id]["profile"]

            for key, value in profile.items():
                if value is not None:
                    current[key] = value

            self.sessions[session_id]["updated_at"] = datetime.now().isoformat()

    def set_analysis(self, session_id, analysis):
        with self.lock:
            self.create_session(session_id)

            self.sessions[session_id]["analysis"] = analysis
            self.sessions[session_id]["updated_at"] = datetime.now().isoformat()

    def set_goal(self, session_id, goal):
        with self.lock:
            self.create_session(session_id)

            self.sessions[session_id]["goal"] = goal
            self.sessions[session_id]["updated_at"] = datetime.now().isoformat()

    def add_message(self, session_id, role, content):
        with self.lock:
            self.create_session(session_id)

            self.sessions[session_id]["history"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })

            # Keep recent conversation manageable
            self.sessions[session_id]["history"] = \
                self.sessions[session_id]["history"][-20:]

            self.sessions[session_id]["updated_at"] = datetime.now().isoformat()

    def get_history(self, session_id, limit=10):
        session = self.get_session(session_id)
        return session["history"][-limit:]

    def reset(self, session_id):
        with self.lock:
            self.sessions.pop(session_id, None)

    def clear(self):
        with self.lock:
            self.sessions.clear()


memory_store = ConversationMemory()