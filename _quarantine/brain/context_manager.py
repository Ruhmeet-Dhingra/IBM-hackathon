def resolve(self, text: str) -> str:

    lowered = text.lower()

    if "it" in lowered:

        app = self.memory.recall("last_app")
        if app:
            return app

        component = self.memory.recall("selected_component")
        if component:
            return component

        project = self.memory.recall("last_project")
        if project:
            return project

    return text