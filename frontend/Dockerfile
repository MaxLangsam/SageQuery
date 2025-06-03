# Frontend Dockerfile for SageQuery
FROM node:18-alpine as build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine as prod
WORKDIR /app
COPY --from=build /app /app
RUN npm install -g serve
EXPOSE 5173
CMD ["serve", "-s", "dist", "-l", "5173"] 