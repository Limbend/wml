ARG NODE_VERSION=20.18.0
FROM node:${NODE_VERSION}-slim AS base

WORKDIR /app

FROM base AS package-installer
ADD ./package.json .
ADD ./package-lock.json .
RUN npm install


FROM base AS dev
ADD . .
COPY --from=package-installer /app/node_modules /app/node_modules

CMD ["npm", "run", "dev", "--", "--host"]


FROM package-installer AS build
ADD . .
COPY --from=package-installer /app/node_modules /app/node_modules
RUN npm run build


FROM base AS prod
COPY --from=build /app/.output /app/.output
# Optional, only needed if you rely on unbundled dependencies
# COPY --from=package-installer /app/node_modules /app/node_modules

CMD ["node", ".output/server/index.mjs"]