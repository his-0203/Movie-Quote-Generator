export default (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
    // Preflight request
    if (req.method === 'OPTIONS') {
      res.status(200).end();
      return;
    }
  
    // 실제 요청 처리 로직 추가
    res.status(200).json({ message: 'CORS headers set successfully!' });
  };