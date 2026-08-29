from enum import Enum


class EntityType(Enum):
    APPLICATION = "application"
    WEBSITE = "website"
    PROJECT = "project"

    COMPONENT = "component"

    FILE = "file"

    PLUGIN = "plugin"

    QUERY = "query"

    PERSON = "person"

    UNKNOWN = "unknown"



class Action(Enum):
    LAUNCH_APPLICATION = "launch_application"

    CLOSE_APPLICATION = "close_application"

    OPEN_WEBSITE = "open_website"

    SHOW_COMPONENT = "show_component"

    HIDE_COMPONENT = "hide_component"

    OPEN_PROJECT = "open_project"

    LOCATE_PROJECT = "locate_project"

    GENERATE_PLUGIN = "generate_plugin"

    NEEDS_REASONING = "needs_reasoning"