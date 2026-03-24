const http = require('http');
const stocks = [
  {secid: '1.430046', name: '圣博润'},
  {secid: '0.831330', name: '普适导航'},
];
const promises = stocks.map(s => {
  return new Promise((resolve) => {
    const url = `http://push2.eastmoney.com/api/qt/stock/get?fields=f43,f44,f45,f46,f47,f48,f57,f58,f170&secid=${s.secid}`;
    http.get(url, {headers: {'User-Agent':'Mozilla/5.0','Referer':'https://finance.eastmoney.com'}}, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const j = JSON.parse(data);
          const p = j.data;
          if (p) {
            // 新三板价格除以100
            const price = p.f43 / 100;
            const close = p.f44 / 100;
            const high = p.f45 / 100;
            const low = p.f46 / 100;
            const pct = ((price - close) / close * 100).toFixed(2);
            console.log(p.f58 + ': ' + price + ' (' + pct + '%) H=' + high + ' L=' + low);
          }
        } catch(e) {
          console.log(s.name + ': error');
        }
        resolve();
      });
    }).on('error', () => resolve());
  });
});
Promise.all(promises).then(() => console.log('done'));
