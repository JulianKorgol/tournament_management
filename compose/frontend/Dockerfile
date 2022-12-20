FROM node:16.18-buster

WORKDIR /app

COPY ./../frontend/package.json /app

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]