export default (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Preflight request
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // 실제 요청 처리 로직 추가 (예: 이미지 프록시)
  const { url } = req.query;

  if (!url) {
    res.status(400).json({ error: 'URL parameter is required' });
    return;
  }

  fetch(url)
    .then(response => response.buffer())
    .then(buffer => {
      res.setHeader('Content-Type', 'image/png');
      res.send(buffer);
    })
    .catch(error => {
      res.status(500).json({ error: 'Failed to fetch image' });
    });
};
