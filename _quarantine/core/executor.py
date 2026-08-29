
from core.app import open_application
from core.browser import open_website

class Executor:

    def __init__(self):
        self.handlers = {
    "open_app": self.handle_open_app,
    "open_website": self.handle_open_website,
}

    def execute(self, plan: dict):

        intent = plan["intent"]
        parameters = plan["parameters"]

        handler = self.handlers.get(intent)

        if handler:
            return handler(parameters)

        print(f"Unknown intent: {intent}")
        return False

    def handle_open_app(self, parameters):

        app_name = parameters["app_name"]

        return open_application(app_name)
    
    def handle_open_website(self, parameters):
      url = parameters["url"]
      return open_website(url)