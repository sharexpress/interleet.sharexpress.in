# ─────────────────────────────────────────────
# Interleet Sandbox — C++ (g++ 13 / C++17)
# Alpine with GCC toolchain
# ─────────────────────────────────────────────
FROM alpine:3.19

# Install g++ and standard library headers
RUN apk add --no-cache g++ libstdc++ libc-dev make

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

RUN chown judge:judge /workspace

USER judge

CMD ["g++", "--version"]
