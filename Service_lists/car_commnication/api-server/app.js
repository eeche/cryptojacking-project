const express = require('express');
const Influx = require('influx');

const app = express();
const influx = new Influx.InfluxDB({
  host: 'db',
  database: 'vehicle_data',
});

app.get('/data', async (req, res) => {
  try {
    const result = await influx.query(`
      select * from vehicle_metrics
      order by time desc
      limit 10
    `);
    res.json(result);
  } catch (error) {
    res.status(500).send(error.toString());
  }
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`API server is running on port ${PORT}`);
});
