#syntax=docker/dockerfile:1.6.0

FROM ubuntu:22.04

RUN apt-get update -yq && apt-get install -yq python3 curl

ARG TARGETARCH
ARG BLS_VERSION=0.3.0
ARG TVM_CLI_VERSION=0.39.0

WORKDIR /root

COPY --link "./generate_keys_and_bc_config.py" "./blockchain.conf.json.template" ./

RUN set -e \
    && curl -sSL "https://github.com/gosh-sh/gosh-bls-lib/releases/download/${BLS_VERSION}/bls_keypair_gen-linux-${TARGETARCH}.tar.gz" \
    | tar -xz -C /usr/local/bin/ \
    && curl -sSL "https://github.com/tvmlabs/tvm-cli/releases/download/${TVM_CLI_VERSION}/tvm-cli-linux-${TARGETARCH}.tar.gz" \
    | tar -xz -C /usr/local/bin/ \
    && chmod +x /usr/local/bin/*

WORKDIR /workdir
