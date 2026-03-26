const https = require('http');
const { TextDecoder } = require('util');
const td = new TextDecoder('gbk');

const stockMap = {
  'sh600352': { name: 'ZJLS', cost: 15.952, stop: 12.0 },
  'sz300033': { name: 'THS', cost: 423.488, stop: 280 },
  'sh831330': { name: 'PSDH', cost: 20.361, stop: 0 },
  'sz000988': { name: 'HGKJ', cost: 116.87, stop: 0 },
  'sh688295': { name: 'ZFSC', cost: 37.843, stop: 0 },
  'sh600487': { name: 'HTGD', cost: 42.391, stop: 0 },
  'sz300499': { name: 'GLGF', cost: 41.625, stop: 38.0 },
  'sh601168': { name: 'XBKY', cost: 24.863, stop: 0 },
  'sh600893': { name: 'HFDC', cost: 47.196, stop: 0 },
  'bj920046': { name: 'YNDL', cost: 329.555, stop: 27 },
  'bj430046': { name: 'SBR', cost: 0.478, stop: 0 },
  'sh600089': { name: 'TBDG', cost: 24.765, stop: 25.0 },
  'sh600114': { name: 'DMGF', cost: 32.428, stop: 25.0 },
  'sz301638': { name: 'NWSZ', cost: 32.635, stop: 28.0 },
};

const codes = Object.keys(stockMap).join(',');
const url = 'http://hq.sinajs.cn/list=' + codes;
https.get(url, { 'headers': { 'Referer': 'http://finance.sina.com.cn', 'User-Agent': 'Mozilla/5.0' } }, res => {
  let d = [];
  res.on('data', c => d.push(c));
  res.on('end', () => {
    const buf = Buffer.concat(d);
    const str = td.decode(buf);
    const lines = str.split('\n');
    let results = [];
    lines.forEach(l => {
      const m = l.match(/hq_str_(\w+)="([^"]+)"/);
      if (m) {
        const parts = m[2].split(',');
        const code = m[1];
        const info = stockMap[code];
        if (!info) return;
        const price = parseFloat(parts[3]);
        const yesterday = parseFloat(parts[2]);
        const chg = (price - yesterday).toFixed(3);
        const pct = ((price - yesterday) / yesterday * 100).toFixed(2);
        const pnl = ((price - info.cost) * (code.startsWith('bj') ? 1 : 1)).toFixed(0);
        const alert = (info.stop > 0 && price <= info.stop) ? ' STOP!' : '';
        console.log(info.name + '|' + price + '|' + chg + '|' + pct + '|' + pnl + '|' + alert);
      }
    });
  });
}).on('error', e => console.log(e));
