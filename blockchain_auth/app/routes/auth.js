const express = require('express');
const router = express.Router();
const { invoke, query } = require('../blockchain');

router.post('/register', async (req, res) => {
    const { username, password } = req.body;
    try {
        await invoke('registerUser', [username, password]);
        res.status(201).send('User registered successfully');
    } catch (error) {
        res.status(500).send('Error registering user');
    }
});

router.post('/login', async (req, res) => {
    const { username, password } = req.body;
    try {
        const result = await query('authenticateUser', [username, password]);
        if (result) {
            res.status(200).send('Authentication successful');
        } else {
            res.status(401).send('Authentication failed');
        }
    } catch (error) {
        res.status(500).send('Error authenticating user');
    }
});

module.exports = router;
