const https = require('https');
const fs = require('fs');

const stocks = [
  { code: 'sh600352', name: '浙江龙盛', stop: 12.0 },
  { code: 'sz300033', name: '同花顺',   stop: 280.0 },
  { code: 'sh600487', name: '亨通光电', stop: 38.0 },
  { code: 'sh600893', name: '航发动力', stop: 42.0 },
  { code: 'sh601168', name: '西部矿业', stop: 22.0 },
  { code: 'sh518880', name: '黄金ETF', stop: 0 },
  { code: 'sh600114', name: '东睦股份', stop: 25.0 },
  { code: 'sh600089', name: '特变电工', stop: 25.0 },
];

function getStock(code) {
  return new Promise((resolve) => {
    https.get('https://qt.gtimg.cn/q=' + code, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        const parts = data.split('~');
        resolve({ price: parseFloat(parts[3]), prevClose: parseFloat(parts[4]) });
      });
    }).on('error', () => resolve({ price: 0, prevClose: 0 }));
  });
}

(async () => {
  const now = new Date().toLocaleString('zh-CN', {timeZone: 'Asia/Shanghai'});
  const lines = ['【集合竞价监控 ' + now + '】', ''];
  
  for (const s of stocks) {
    const d = await getStock(s.code);
    if (d.price > 0 && d.prevClose > 0) {
      const chg = ((d.price - d.prevClose) / d.prevClose * 100).toFixed(2);
      const chgStr = chg >= 0 ? '+' + chg + '%' : chg + '%';
      let line = s.name + ' ' + d.price + ' (' + chgStr + ')';
      if (s.stop > 0 && d.price <= s.stop) line += ' ⚠️止损';
      lines.push(line);
    } else {
      lines.push(s.name + ' 无数据');
    }
  }
  
  const out = lines.join('\n');
  fs.writeFileSync('C:\\Users\\Administrator\\.openclaw\\workspace\\auction_result.txt', out, 'utf8');
  console.log(out);
})();
