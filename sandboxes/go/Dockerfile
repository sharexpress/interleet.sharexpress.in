# ─────────────────────────────────────────────
# Interleet Sandbox — Go 1.22
# Minimal Alpine-based Go runtime + compiler
# ─────────────────────────────────────────────
FROM golang:1.22-alpine

# Disable CGO to produce static binaries (safer sandbox)
ENV CGO_ENABLED=0 \
    GOPATH=/go \
    GOCACHE=/tmp/gocache

# Build tools (needed for go build)
RUN apk add --no-cache gcc musl-dev

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

# Allow judge user to write compiled output here
RUN chown -R judge:judge /workspace && \
    mkdir -p /tmp/gocache && chown -R judge:judge /tmp/gocache

USER judge

CMD ["go", "version"]
