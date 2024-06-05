const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello, Mobile Game!');
});

app.listen(port, () => {
  console.log(`Game server is running on port ${port}`);
});
