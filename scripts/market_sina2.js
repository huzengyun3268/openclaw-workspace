const https = require('https');
const iconv = require('iconv-lite');

function req(url, headers) {
  return new Promise((resolve) => {
    const r = https.get(url, {headers: headers || {'User-Agent':'Mozilla/5.0'}}, res => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        const str = iconv.decode(buf, 'gbk');
        resolve(str);
      });
    });
    r.on('error', () => resolve(null));
  });
}

function parseSinaData(raw) {
  const lines = raw.trim().split('\n');
  const results = [];
  for (const line of lines) {
    const match = line.match(/hq_str_\w+="([^"]+)"/);
    if (!match) continue;
    const parts = match[1].split(',');
    if (parts.length < 4) continue;
    results.push({
      name: parts[0],
      price: parseFloat(parts[1]),
      prevClose: parseFloat(parts[2]),
      pct: parseFloat(parts[3])
    });
  }
  return results;
}

async function main() {
  const headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer':'https://finance.sina.com.cn/'
  };
  
  // 大盘指数
  const idxCodes = 's_sh000001,s_sz399001,s_sz399006,s_sh000300,s_sz399688,s_sz399005';
  const r0 = await req('https://hq.sinajs.cn/list=' + idxCodes, headers);
  const idx = parseSinaData(r0);
  console.log('=== 大盘 09:30 ===');
  for (const s of idx) {
    const flag = s.pct > 0 ? '🟢' : s.pct < -2 ? '🔴' : '🟡';
    console.log(flag + ' ' + s.name + ': ' + s.price.toFixed(2) + ' (' + (s.pct>0?'+':'') + s.pct.toFixed(2) + '%)');
  }
  
  // ETF
  const etfCodes = 'sh512760,sh512290,sh515050,sh512690,sh512660,sh512400,sz159992,sz159745,sh512480,sh512950,sh512980,sz159628,sh512170,sh512010';
  const r1 = await req('https://hq.sinajs.cn/list=' + etfCodes, headers);
  const etfs = parseSinaData(r1);
  etfs.sort((a,b) => b.pct - a.pct);
  console.log('\n=== ETF异动 ===');
  for (const e of etfs) {
    const flag = e.pct > 1 ? '🟢+' : e.pct > 0 ? '🟢' : e.pct < -1 ? '🔴' : '🟡';
    console.log(flag + ' ' + e.name + ': ' + e.price.toFixed(3) + ' (' + (e.pct>0?'+':'') + e.pct.toFixed(2) + '%)');
  }
  
  // 持仓
  const holdCodes = 'sh600352,sh600089,sz300033,sh603248,sz300189,sz920046,sh600114,sz301638,sz430046,sz831330';
  const r2 = await req('https://hq.sinajs.cn/list=' + holdCodes, headers);
  const holds = parseSinaData(r2);
  console.log('\n=== 持仓实时 ===');
  for (const s of holds) {
    const pct = ((s.price - s.prevClose) / s.prevClose * 100).toFixed(2);
    const flag = parseFloat(pct) > 2 ? '🟢+' : parseFloat(pct) < -2 ? '🔴' : '🟡';
    console.log(flag + ' ' + s.name + ': ' + s.price.toFixed(2) + ' (' + (parseFloat(pct)>0?'+':'') + pct + '%)');
  }
}
main().catch(console.error);
