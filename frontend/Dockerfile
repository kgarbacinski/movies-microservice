FROM node:19-alpine3.16

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json ./
COPY yarn.lock /.
RUN yarn install
COPY .. ./

CMD ["yarn", "start"]