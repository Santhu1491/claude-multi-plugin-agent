from agent.integrations.java_plugin_adapter import JavaPluginAdapter


def test_java_plugin_adapter():
    adapter = JavaPluginAdapter()

    result = adapter.execute({
        "operation": "analyze",
        "parameters": {
            "message": "Analyze a Java REST API"
        }
    })

    print("\nJava adapter result:")
    print(result)

    assert result["success"] is True