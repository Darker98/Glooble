# Stage 1: Build
FROM node:18 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy Vite's build output to Nginx
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
