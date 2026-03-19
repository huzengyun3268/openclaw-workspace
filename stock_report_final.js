// 最终整合早报
const https = require('https');

const stocks = [
  { name: '特变电工', code: '600089', cost: 24.765, shares: 52300 },
  { name: '浙江龙盛', code: '600352', cost: 15.912, shares: 141700 },
  { name: '锡华科技', code: '603248', cost: 35.490, shares: 2000 },
  { name: '同花顺', code: '300033', cost: 511.220, shares: 600 },
  { name: '神农种业', code: '300189', cost: 17.099, shares: 5000 },
  { name: '亿能电力', code: '920046', cost: 35.936, shares: 12731 },
  { name: '普适导航', code: '831330', cost: 20.415, shares: 6370 },
  { name: '圣博润', code: '430046', cost: 0.478, shares: 10334 },
];

// 新三板K线昨收
const snbData = {
  '831330': { price: 20.20, prevClose: 20.06 },   // 2026-03-18收盘, 2026-03-16收盘为昨收
  '430046': { price: 0.33, prevClose: 0.34 },
};

function getStockCode(code) {
  if (code.startsWith('9')) return 'bj' + code;
  if (code.startsWith('6')) return 'sh' + code;
  return 'sz' + code;
}

function fetchStockPrice(code) {
  return new Promise((resolve, reject) => {
    const fullCode = getStockCode(code);
    const url = `https://qt.gtimg.cn/q=${fullCode}`;
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const match = data.match(/"([^"]+)"/);
          if (!match) return reject(new Error('No data for ' + code));
          const fields = match[1].split('~');
          if (fields.length < 40) return reject(new Error('Invalid data for ' + code));
          const price = parseFloat(fields[3]);
          const prevClose = parseFloat(fields[4]);
          const changePercent = prevClose > 0 ? ((price - prevClose) / prevClose * 100).toFixed(2) : '0.00';
          resolve({ price, changePercent });
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

function getTrendEmoji(pct) {
  const p = parseFloat(pct);
  if (p > 0) return '🔴';
  if (p === 0) return '⚪';
  return '🟢';
}

async function main() {
  const date = new Date().toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' });
  const lines = [];
  let totalCost = 0;
  let totalValue = 0;

  for (const stock of stocks) {
    try {
      let price, changePercent;
      
      if (snbData[stock.code]) {
        // 新三板
        price = snbData[stock.code].price;
        const prevClose = snbData[stock.code].prevClose;
        changePercent = ((price - prevClose) / prevClose * 100).toFixed(2);
      } else {
        const r = await fetchStockPrice(stock.code);
        price = r.price;
        changePercent = r.changePercent;
      }

      const value = price * stock.shares;
      const cost = stock.cost * stock.shares;
      const profit = value - cost;
      const profitRate = (profit / cost * 100).toFixed(2);
      const trend = getTrendEmoji(changePercent);

      totalCost += cost;
      totalValue += value;

      const changeSign = parseFloat(changePercent) >= 0 ? '+' : '';
      const profitSign = profit >= 0 ? '+' : '';

      lines.push({
        trend,
        name: stock.name,
        price: price.toFixed(3),
        change: `${changeSign}${changePercent}%`,
        cost: stock.cost.toFixed(3),
        profit: `${profitSign}${profit.toFixed(2)}`,
        profitRate: `${profitSign}${profitRate}`,
      });
    } catch (e) {
      console.error(`获取 ${stock.name}(${stock.code}) 失败: ${e.message}`);
      lines.push({ name: stock.name, code: stock.code, error: true });
    }
    await new Promise(r => setTimeout(r, 200));
  }

  const totalProfit = totalValue - totalCost;
  const totalProfitRate = (totalProfit / totalCost * 100).toFixed(2);
  const totalSign = totalProfit >= 0 ? '+' : '';

  const feishuLines = lines.map(l => {
    if (l.error) return `• ${l.name}(${l.code}): 获取行情失败`;
    return `${l.trend} ${l.name} 现价${l.price}(${l.change}) 成本${l.cost} 盈亏${l.profit}(${l.profitRate}%)`;
  });

  const msg = `📈 股票早报 ${date}\n${feishuLines.join('\n')}\n\n💰 合计盈亏: ${totalSign}${totalProfit.toFixed(2)}元 (${totalSign}${totalProfitRate}%)`;
  
  console.log(msg);
  
  const fs = require('fs');
  fs.writeFileSync('stock_report_final.txt', msg, 'utf8');
  console.log('\n报告已保存到 stock_report_final.txt');
}

main().catch(console.error);
