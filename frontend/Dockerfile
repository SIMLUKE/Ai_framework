FROM node

WORKDIR /app

COPY  package.json .

RUN npm i -g typescript
RUN npm i -g react-scripts


RUN npm i

COPY  . .

CMD [ "npm", "run", "start" ]
