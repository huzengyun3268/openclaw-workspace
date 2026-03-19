// 股票早报生成脚本
const https = require('https');
const http = require('http');

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

// 北交所股票用bj后缀，其他用sh/sz前缀
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
          // 格式: v_sh600089="...."
          const match = data.match(/"([^"]+)"/);
          if (!match) return reject(new Error('No data for ' + code));
          const fields = match[1].split('~');
          if (fields.length < 40) return reject(new Error('Invalid data for ' + code));
          const price = parseFloat(fields[3]); // 现价
          const prevClose = parseFloat(fields[4]); // 昨收
          const changePercent = prevClose > 0 ? ((price - prevClose) / prevClose * 100).toFixed(2) : '0.00';
          resolve({ price, changePercent, prevClose });
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

function getTrendEmoji(pct) {
  const p = parseFloat(pct);
  if (p > 2) return '🔴';
  if (p > 0) return '🔴';
  if (p === 0) return '⚪';
  if (p > -2) return '🟢';
  return '🟢';
}

async function main() {
  console.log('📊 股票早报 - ' + new Date().toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' }));
  console.log('='.repeat(50));

  let totalCost = 0;
  let totalValue = 0;
  const lines = [];

  for (const stock of stocks) {
    try {
      const { price, changePercent } = await fetchStockPrice(stock.code);
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
        profitRate: `${profitSign}${profitRate}%`,
        shares: stock.shares,
      });
      console.log(`${trend} ${stock.name}(${stock.code}): 现价=${price}, 涨跌=${changePercent}%, 成本=${stock.cost}, 盈亏=${profit}(${profitRate}%)`);
    } catch (e) {
      console.error(`获取 ${stock.name}(${stock.code}) 失败: ${e.message}`);
      lines.push({ name: stock.name, code: stock.code, error: e.message });
    }
    await new Promise(r => setTimeout(r, 200));
  }

  const totalProfit = totalValue - totalCost;
  const totalProfitRate = (totalProfit / totalCost * 100).toFixed(2);
  const totalSign = totalProfit >= 0 ? '+' : '';

  console.log('='.repeat(50));
  console.log(`合计: 总市值=${totalValue.toFixed(2)}, 总成本=${totalCost.toFixed(2)}, 总盈亏=${totalSign}${totalProfit.toFixed(2)}(${totalSign}${totalProfitRate}%)`);

  // 生成飞书消息
  const feishuMsg = lines.map(l => {
    if (l.error) return `• ${l.name}(${l.code}): 获取行情失败`;
    return `${l.trend} ${l.name} 现价${l.price}(${l.change}) 成本${l.cost} 盈亏${l.profit}(${l.profitRate}%)`;
  }).join('\n');

  const summary = `📈 股票早报 ${new Date().toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n${feishuMsg}\n\n💰 合计盈亏: ${totalSign}${totalProfit.toFixed(2)}元 (${totalSign}${totalProfitRate}%)`;

  console.log('\n--- 飞书消息 ---');
  console.log(summary);

  // 保存到文件供调用方使用
  require('fs').writeFileSync('stock_report.txt', summary, 'utf8');
}

main().catch(console.error);
