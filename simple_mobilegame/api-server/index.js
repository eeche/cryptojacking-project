const express = require('express');
const app = express();
const port = 3001;

app.get('/api', (req, res) => {
  res.send('API Server for Mobile Game!');
});

app.listen(port, () => {
  console.log(`API server is running on port ${port}`);
});
