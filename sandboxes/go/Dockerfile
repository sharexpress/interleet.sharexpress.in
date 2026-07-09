# ─────────────────────────────────────────────
# Interleet Sandbox — Go 1.22
# Minimal Alpine-based Go runtime + compiler
# ─────────────────────────────────────────────
FROM golang:1.22-alpine

# Disable CGO to produce static binaries (safer sandbox)
ENV CGO_ENABLED=0 \
    GOPATH=/go \
    GOCACHE=/tmp/gocache \
    GOPROXY=https://goproxy.io,direct

# Build tools (needed for go build)
RUN apk add --no-cache gcc musl-dev git

# Pre-cache Gin and pure Go SQLite module for APIs challenges
WORKDIR /tmp/warmup
RUN go mod init warmup && \
    go get github.com/gin-gonic/gin@v1.10.0 && \
    go get github.com/glebarez/go-sqlite && \
    go get github.com/lib/pq && \
    go get go.mongodb.org/mongo-driver/mongo && \
    go get github.com/go-sql-driver/mysql && \
    cd / && rm -rf /tmp/warmup

# Create a non-root judge user
RUN addgroup -S judge && adduser -S -G judge -H -s /bin/false judge

WORKDIR /workspace

# Allow judge user to write compiled output and read cache
RUN chown -R judge:judge /workspace && \
    mkdir -p /tmp/gocache && chown -R judge:judge /tmp/gocache && \
    chown -R judge:judge /go

USER judge

CMD ["go", "version"]
