# ─────────────────────────────────────────────
# Interleet Sandbox — Java 21 (JDK)
# Eclipse Temurin JDK on Alpine
# ─────────────────────────────────────────────
FROM eclipse-temurin:21-jdk-alpine

ENV JAVA_OPTS="-Xmx256m -Xss64m -XX:+UseSerialGC" \
    _JAVA_OPTIONS="-Djava.security.egd=file:/dev/urandom"

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

RUN chown judge:judge /workspace

USER judge

CMD ["java", "-version"]
