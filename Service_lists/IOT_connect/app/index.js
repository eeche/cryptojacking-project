const express = require('express');
const bodyParser = require('body-parser');
const mqtt = require('mqtt');
const Influx = require('influx');
const app = express();

const influx = new Influx.InfluxDB({
    host: 'db',
    database: 'iot_data',
    schema: [
        {
            measurement: 'sensor_data',
            fields: {
                temperature: Influx.FieldType.FLOAT,
                humidity: Influx.FieldType.FLOAT,
            },
            tags: ['device_id']
        }
    ]
});

const client = mqtt.connect('mqtt://mqtt:1883');
client.on('connect', () => {
    client.subscribe('iot/data', (err) => {
        if (!err) {
            console.log('Subscribed to iot/data topic');
        }
    });
});

client.on('message', (topic, message) => {
    if (topic === 'iot/data') {
        const data = JSON.parse(message.toString());
        influx.writePoints([
            {
                measurement: 'sensor_data',
                tags: { device_id: data.device_id },
                fields: { temperature: data.temperature, humidity: data.humidity },
                timestamp: data.timestamp * 1000000000 // ns precision
            }
        ]).catch(err => {
            console.error(`Error saving data to InfluxDB! ${err.stack}`)
        });
    }
});

app.use(bodyParser.json());

app.get('/data', async (req, res) => {
    try {
        const results = await influx.query(`
            select * from sensor_data
            order by time desc
            limit 10
        `);
        res.json(results);
    } catch (error) {
        res.status(500).send(error.toString());
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
