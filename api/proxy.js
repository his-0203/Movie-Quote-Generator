// api/proxy.js
const axios = require('axios');

module.exports = async (req, res) => {
  const url = req.query.url;
  if (!url) {
    return res.status(400).send('URL is required');
  }

  try {
    const response = await axios.get(url, { responseType: 'arraybuffer' });
    res.setHeader('Content-Type', response.headers['content-type']);
    res.send(response.data);
  } catch (error) {
    res.status(500).send('Failed to fetch image');
  }
};