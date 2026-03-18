// 实时股票数据工具
// 用法: node stock.js [股票代码]
// 例如: node stock.js 600352

const https = require('https');

const stockCode = process.argv[2] || '600352';

// 判断股票市场
let secid;
if (stockCode.startsWith('6')) {
  secid = '1.' + stockCode; // 上海
} else if (stockCode.startsWith('0') || stockCode.startsWith('3')) {
  secid = '0.' + stockCode; // 深圳
} else if (stockCode.startsWith('8') || stockCode.startsWith('4')) {
  secid = '0.' + stockCode; // 北京
} else {
  secid = '1.' + stockCode;
}

const url = `https://push2.eastmoney.com/api/qt/stock/get?secid=${secid}&fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f59,f60,f116,f117,f162,f163,f164,f167,f168,f169,f170,f171,f173,f177`;

https.get(url, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    try {
      const json = JSON.parse(data);
      if (json.data) {
        const d = json.data;
        const change = ((d.f43 - d.f60) / d.f60 * 100).toFixed(2);
        console.log(`\n${d.f58} (${d.f57})`);
        console.log(`最新价: ${d.f43 / 100}元`);
        console.log(`涨跌: ${change}%`);
        console.log(`昨收: ${d.f60 / 100}元`);
        console.log(`最高: ${d.f44 / 100}元`);
        console.log(`最低: ${d.f47 / 100}元`);
      } else {
        console.log('未找到该股票');
      }
    } catch (e) {
      console.log('解析错误');
    }
  });
}).on('error', () => {
  console.log('网络错误');
});
