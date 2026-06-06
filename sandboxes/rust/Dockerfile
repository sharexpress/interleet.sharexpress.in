# ─────────────────────────────────────────────
# Interleet Sandbox — Rust 1.78
# Alpine-based Rust compiler (musl target)
# ─────────────────────────────────────────────
FROM rust:1.78-alpine

ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    CARGO_NET_OFFLINE=true

# Build tools for musl linking
RUN apk add --no-cache musl-dev gcc

# Pre-warm the registry cache (speeds up first compile)
RUN rustc --version && cargo --version

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

RUN chown -R judge:judge /workspace

USER judge

CMD ["rustc", "--version"]
