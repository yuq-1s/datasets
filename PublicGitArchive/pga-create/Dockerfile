#==========================
# Stage 1: build pga-create
#==========================
FROM golang:1.12.4-alpine3.9 AS builder

RUN apk add --no-cache dumb-init=1.2.2-r1 git

# build pga-create
ENV PGA_CREATE_REPO=github.com/src-d/datasets/PublicGitArchive/pga-create
ENV PGA_CREATE_PATH=$GOPATH/src/$PGA_CREATE_REPO
COPY . ${PGA_CREATE_PATH}

RUN go build -tags norwfs -o /bin/pga-create ${PGA_CREATE_PATH}/cmd/pga-create

RUN cp ${PGA_CREATE_PATH}/select-repos.sh /bin/select-repos && chmod +x /bin/select-repos
RUN cp ${PGA_CREATE_PATH}/index-repos.sh /bin/index-repos && chmod +x /bin/index-repos

#=====================================================
# Stage 2: copy binaries and set environment variables
#=====================================================
FROM alpine:3.9.3

COPY --from=builder /bin/pga-create /bin/*-repos /usr/bin/dumb-init /bin/

# volume where the data generated by select-repos and index-repos will be persisted.
# under /pga/data is where the data generated by select-repos will be placed to be used by index-repos.
# under /pga/root-repositories must be located the siva files downloaded by borges, also the compressed
# index will be placed here by index-repos.
VOLUME ["/pga"]

# core-retrieval database configuration, default: postgres://testing:testing@0.0.0.0:5432/testing?sslmode=disable&connect_timeout=30
ENV CONFIG_DBUSER=testing
ENV CONFIG_DBPASS=testing
ENV CONFIG_DBHOST=0.0.0.0
ENV CONFIG_DBPORT=5432
ENV CONFIG_DBNAME=testing
ENV CONFIG_DBSSLMODE=disable
ENV CONFIG_DBTIMEOUT=30s

# pga-create configuration (BUCKET_SIZE must be the same value used by borges consumer)
ENV PGA_VERSION=version-undefined
ENV STARS=50
ENV BUCKET_SIZE=2

WORKDIR /pga
ENTRYPOINT ["/bin/dumb-init", "--"]

