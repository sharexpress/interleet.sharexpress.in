"""Java Executor — compiles with javac, runs with JVM"""
from app.engine.enums import Language
from app.engine.executors.base import BaseExecutor


class JavaExecutor(BaseExecutor):
    language = Language.JAVA
    docker_image = "interleet-java:latest"
    filename = "Solution.java"
    compile_command = ["sh", "-c", "javac Solution.java 2>&1"]
    run_command = ["sh", "-c", "java -Xmx200m -Xss64m Solution < stdin.txt"]
    requires_compile = True
