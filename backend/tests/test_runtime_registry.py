from app.engine.runtimes.registry import RuntimeRegistry


def test_bundled_runtime_metadata_is_complete():
    runtimes = RuntimeRegistry.get_all()

    assert {runtime["id"] for runtime in runtimes} == {
        "algorithm",
        "frontend",
        "devops",
        "compose",
    }
    for runtime in runtimes:
        assert runtime["executionMode"]
        assert runtime["capabilities"]
        assert runtime["limits"]
        assert runtime["artifacts"]
        assert runtime["pipeline"]


def test_registry_returns_copies_and_resolves_execution_mode():
    runtime = RuntimeRegistry.get_runtime("devops")
    runtime["name"] = "changed by caller"

    assert RuntimeRegistry.get_runtime("devops")["name"] == "Infrastructure Sandbox"
    assert RuntimeRegistry.execution_mode("devops") == "devops"
    assert RuntimeRegistry.runtime_for_mode("browser")["id"] == "frontend"
