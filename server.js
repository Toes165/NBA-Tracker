const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;
const PYTHON_API_URL = process.env.PYTHON_API_URL || 'https://sportapi-jvjd.onrender.com/scoreboard';


app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// API endpoint for scoreboard
app.get('/scoreboard', async (req, res) => {
  try {
    const response = await axios.get(PYTHON_API_URL);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching from Python API:', error.message);
    res.status(500).send('Error fetching live scores');
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
