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

    OPEN_URL = "open_url"

    SEARCH_WEB = "search_web"

    SHOW_COMPONENT = "show_component"

    HIDE_COMPONENT = "hide_component"

    OPEN_PROJECT = "open_project"

    LOCATE_PROJECT = "locate_project"

    GENERATE_PLUGIN = "generate_plugin"

    PROPOSE_PLUGIN = "propose_plugin"

    PREVIEW_PLUGIN = "preview_plugin"

    APPROVE_PLUGIN = "approve_plugin"

    REJECT_PLUGIN = "reject_plugin"

    RUN_PLUGIN = "run_plugin"

    NEEDS_REASONING = "needs_reasoning"

    SEARCH_KNOWLEDGE_BASE = "search_knowledge_base"
