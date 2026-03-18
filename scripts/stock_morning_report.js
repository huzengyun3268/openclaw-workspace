// stock_morning_report.js
// 股票早报生成脚本 - 通过浏览器fetch获取数据

const stocks = [
  { secid: '1.600089', name: '特变电工', cost: 24.765, qty: 52300 },
  { secid: '1.600352', name: '浙江龙盛', cost: 15.912, qty: 141700 },
  { secid: '1.603248', name: '锡华科技', cost: 35.490, qty: 2000 },
  { secid: '0.300033', name: '同花顺', cost: 511.220, qty: 600 },
  { secid: '0.300189', name: '神农种业', cost: 17.099, qty: 5000 },
  { secid: '1.920046', name: '亿能电力', cost: 35.936, qty: 12731 },
  { secid: '0.831330', name: '普适导航', cost: 20.415, qty: 6370 },
  { secid: '0.430046', name: '圣博润', cost: 0.478, qty: 10334 },
];

async function getStockPrice(secid) {
  const url = `http://push2.eastmoney.com/api/qt/stock/get?secid=${secid}&fields=f43,f57,f58,f169,f170&ut=fa5fd1943c7b386f172d6893dbfba10b`;
  const resp = await fetch(url);
  const json = await resp.json();
  const d = json.data;
  return {
    price: d.f43 / 100,
    change: d.f169 / 100,
    changePct: d.f170 / 100,
  };
}

async function main() {
  const now = new Date();
  const dateStr = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

  let report = `📊 **持仓早报 ${dateStr}**\n\n`;
  let totalProfit = 0;

  for (const stock of stocks) {
    try {
      const data = await getStockPrice(stock.secid);
      const profit = (data.price - stock.cost) * stock.qty;
      const profitPct = (data.price - stock.cost) / stock.cost * 100;
      totalProfit += profit;
      const emoji = profit >= 0 ? '✅' : '❌';
      report += `${emoji} **${stock.name}** ${data.price.toFixed(2)}元 (${data.changePct >= 0 ? '+' : ''}${data.changePct.toFixed(2)}%)\n`;
      report += `   成本 ${stock.cost.toFixed(3)} | 盈亏 ${profit >= 0 ? '+' : ''}${profit.toFixed(0)}元 (${profitPct >= 0 ? '+' : ''}${profitPct.toFixed(1)}%)\n\n`;
    } catch (e) {
      report += `❓ **${stock.name}** 数据获取失败\n\n`;
    }
  }

  report += `━━━━━━━━━━━━━━━━━━\n`;
  report += `💰 合计盈亏: ${totalProfit >= 0 ? '+' : ''}${totalProfit.toFixed(0)}元\n`;
  report += `📅 更新时间: ${now.toLocaleString('zh-CN', {timeZone:'Asia/Shanghai'})}`;

  console.log(report);
  console.log('---MESSAGE---');
  console.log(report);
}

main().catch(console.error);
