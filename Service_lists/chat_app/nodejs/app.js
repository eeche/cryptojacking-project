const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const mongoose = require('mongoose');
const redis = require('redis');
const session = require('express-session');
const RedisStore = require('connect-redis')(session);

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

mongoose.connect('mongodb://mongodb/chat', { useNewUrlParser: true, useUnifiedTopology: true });

const redisClient = redis.createClient({ host: 'redis', port: 6379 });

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'secret-key',
  resave: false,
  saveUninitialized: true
}));

io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('chat message', (msg) => {
    io.emit('chat message', msg);
  });
  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});
