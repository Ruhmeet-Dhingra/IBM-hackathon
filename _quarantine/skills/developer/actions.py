from devloper.developer_service import DeveloperService


_service = DeveloperService()


def generate_plugin(specification: str):
    return _service.generate_plugin(specification)


def analyze_project(path: str):
    return _service.analyze_project(path)


def review_code(path: str):
    return _service.review_code(path)


def create_project(specification: str):
    return _service.create_project(specification)