FROM bitnami/git AS ente-gitloader
RUN git clone https://github.com/ente-io/ente.git && cd ente && git submodule update --init --recursive

FROM node:20-bookworm-slim AS builder

WORKDIR ./ente

COPY --from=ente-gitloader /ente/web .
#COPY . .
#COPY apps/ .

# Will help default to yarn versoin 1.22.22
RUN corepack enable

# Endpoint for Ente Server
ENV NEXT_PUBLIC_ENTE_ENDPOINT=DOCKER_RUNTIME_REPLACE_ENDPOINT
ENV NEXT_PUBLIC_ENTE_ALBUMS_ENDPOINT=DOCKER_RUNTIME_REPLACE_ALBUMS_ENDPOINT

RUN yarn cache clean
RUN yarn install --network-timeout 1000000000
RUN yarn build:photos && yarn build:accounts && yarn build:auth && yarn build:cast

FROM node:20-bookworm-slim

WORKDIR /app

COPY --from=builder /ente/apps/photos/out /app/photos
COPY --from=builder /ente/apps/accounts/out /app/accounts
COPY --from=builder /ente/apps/auth/out /app/auth
COPY --from=builder /ente/apps/cast/out /app/cast

RUN npm install -g serve

ENV PHOTOS=3000
EXPOSE ${PHOTOS}

ENV ACCOUNTS=3001
EXPOSE ${ACCOUNTS}

ENV AUTH=3002
EXPOSE ${AUTH}

ENV CAST=3003
EXPOSE ${CAST}

# The albums app does not have navigable pages on it, but the
# port will be exposed in-order to self up the albums endpoint
# `apps.public-albums` in museum.yaml configuration file.
ENV ALBUMS=3004
EXPOSE ${ALBUMS}

ARG ENDPOINT="http://localhost:8080"
ENV ENDPOINT "$ENDPOINT"
ARG ALBUMS_ENDPOINT="http://localhost:8082"
ENV ALBUMS_ENDPOINT "$ALBUMS_ENDPOINT"
COPY <<EOF /docker-entrypoint.d/replace_ente_endpoints.sh
echo "Replacing endpoints"
echo "  Endpoint: \$ENDPOINT"
echo "  Albums Endpoint: \$ALBUMS_ENDPOINT"

replace_enpoints() {
  sed -i -e 's,DOCKER_RUNTIME_REPLACE_ENDPOINT,'"\$ENDPOINT"',g' \$1
  sed -i -e 's,DOCKER_RUNTIME_REPLACE_ALBUMS_ENDPOINT,'"\$ALBUMS_ENDPOINT"',g' \$1
}
for jsfile in `find '/app' -type f -name '*.js'`
do
    replace_enpoints "\$jsfile"
done
EOF

RUN chmod +x /docker-entrypoint.d/replace_ente_endpoints.sh && sed -i '1a /docker-entrypoint.d/replace_ente_endpoints.sh' /usr/local/bin/docker-entrypoint.sh

CMD ["sh", "-c", "serve /app/photos -l tcp://0.0.0.0:${PHOTOS} & serve /app/accounts -l tcp://0.0.0.0:${ACCOUNTS} & serve /app/auth -l tcp://0.0.0.0:${AUTH} & serve /app/cast -l tcp://0.0.0.0:${CAST}"]