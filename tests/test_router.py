from agent.core.router import Router


def test_router_prefers_explicit_python_technology():
    router = Router()

    request = {
        "technology": "python",
        "content": "compile Java code",
    }

    assert router.route(request) == "python"


def test_router_prefers_explicit_java_technology():
    router = Router()

    request = {
        "technology": "java",
        "content": "analyze Python code",
    }

    assert router.route(request) == "java"