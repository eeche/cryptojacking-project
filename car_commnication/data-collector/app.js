const mqtt = require('mqtt');
const Influx = require('influx');

const client = mqtt.connect('mqtt://mqtt:1883');
const influx = new Influx.InfluxDB({
  host: 'db',
  database: 'vehicle_data',
  schema: [
    {
      measurement: 'vehicle_metrics',
      fields: {
        temperature: Influx.FieldType.FLOAT,
        speed: Influx.FieldType.FLOAT,
      },
      tags: ['vehicle_id']
    }
  ]
});

client.on('connect', () => {
  console.log('Connected to MQTT broker');
  client.subscribe('vehicle/data');
});

client.on('message', (topic, message) => {
  const data = JSON.parse(message.toString());
  influx.writePoints([
    {
      measurement: 'vehicle_metrics',
      tags: { vehicle_id: data.vehicle_id },
      fields: { temperature: data.temperature, speed: data.speed },
    }
  ]).then(() => {
    console.log('Data written to InfluxDB');
  }).catch(error => {
    console.error(`Error writing to InfluxDB: ${error.stack}`);
  });
});
