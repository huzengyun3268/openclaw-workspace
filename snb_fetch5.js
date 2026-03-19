// 补抓新三板行情 - 使用正确的字段
const https = require('https');

async function fetchEM(code) {
  return new Promise((resolve, reject) => {
    const secid = '0.' + code;
    // 获取更多字段：f43=最新价, f44=最高, f45=最低, f46=今开, f47=成交量, f48=成交额, f57=昨收, f58=名称, f107=涨跌额, f169=涨跌%
    const url = `https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&fields=f43,f44,f45,f46,f47,f48,f57,f58,f107,f169,f170&secid=${secid}&_=1`;
    
    https.get(url, { headers: { 
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
      'Referer': 'https://quote.eastmoney.com/'
    }}, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const d = json.data;
          if (!d) return reject(new Error('No data for ' + code));
          console.log(`  ${code}: all fields = ${JSON.stringify(d)}`);
          
          // f43=最新价(分), f57=昨收(分), f169=涨跌幅(万分比), f170=涨跌幅(万分比)
          const rawPrice = parseFloat(d.f43);
          const rawPrevClose = parseFloat(d.f57);
          
          // 判断是否是价格（正常A股）或股票代码（异常）
          let price, prevClose;
          if (rawPrice > 10000 || rawPrevClose === parseInt(code)) {
            // 价格字段异常，尝试其他方式
            price = null;
          } else {
            price = rawPrice / 100;
            prevClose = rawPrevClose / 100;
          }
          
          // f169是涨跌幅(万分比，百分比值*100)
          const changePct = d.f169 ? (parseFloat(d.f169) / 100).toFixed(2) : null;
          
          resolve({ 
            name: d.f58, 
            price: price ? price.toFixed(3) : 'N/A', 
            prevClose: prevClose ? prevClose.toFixed(3) : 'N/A',
            change: changePct,
            raw: d
          });
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function main() {
  for (const code of ['831330', '430046']) {
    try {
      const r = await fetchEM(code);
      console.log(`${code}: name=${r.name}, price=${r.price}, prevClose=${r.prevClose}, change=${r.change}%`);
    } catch (e) {
      console.log(`${code}: failed - ${e.message}`);
    }
    await new Promise(r => setTimeout(r, 1000));
  }
}

main().catch(console.error);
