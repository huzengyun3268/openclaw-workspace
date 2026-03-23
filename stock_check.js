// 股票实时行情监控 - Node.js版
const https = require('https');

// 持仓列表 (来自USER.md)
const WATCH_LIST = [
  { secid: '1.600352', name: '浙江龙盛', cost: 15.91, qty: 106700 },
  { secid: '1.600089', name: '特变电工', cost: 24.765, qty: 52300 },
  { secid: '0.301667', name: '纳百川', cost: 82.715, qty: 3000 },
  { secid: '1.920046', name: '亿能电力', cost: 35.936, qty: 12731 },
  { secid: '0.300033', name: '同花顺', cost: 511.22, qty: 600 },
  { secid: '0.831330', name: '普适导航', cost: 20.415, qty: 6370 },
  { secid: '0.300189', name: '神农种业', cost: 17.099, qty: 5000 },
  { secid: '0.430046', name: '圣博润', cost: 0.478, qty: 10334 },
  { secid: '1.600114', name: '东睦股份(老婆)', cost: 32.428, qty: 9200 },
  { secid: '0.301638', name: '南网数字(老婆)', cost: 32.635, qty: 1700 },
];

function fetchStock(secid) {
  return new Promise((resolve) => {
    const url = `https://push2.eastmoney.com/api/qt/stock/get?secid=${secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f169,f170,f107,f117&ut=fa5fd1943c7b386f172d6893dbfba10b`;
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.data);
        } catch (e) {
          resolve(null);
        }
      });
    }).on('error', () => resolve(null));
  });
}

function getIcon(pct) {
  if (pct >= 9.5) return '🚨 涨停!';
  if (pct <= -9.5) return '🚨 跌停!';
  if (pct >= 5) return '🔥 大涨';
  if (pct >= 3) return '📈 上涨';
  if (pct >= 1) return '↗ 小幅上涨';
  if (pct > -1) return '➡ 持平';
  if (pct > -3) return '↘ 小幅下跌';
  if (pct > -5) return '📉 下跌';
  if (pct > -9.5) return '💥 大跌';
  return '💥 跌停!';
}

async function main() {
  console.log('============================================================');
  console.log('  股票实时行情监控  ' + new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' }));
  console.log('============================================================\n');

  const alerts = [];
  const results = [];

  for (const stock of WATCH_LIST) {
    const d = await fetchStock(stock.secid);
    if (!d) {
      console.log(`❌ ${stock.name} (${stock.secid}): 获取失败`);
      continue;
    }

    const price = d.f43 / 100;
    const changePct = d.f170 / 100;
    const change = d.f169 / 100;
    const profit = (price - stock.cost) * stock.qty;
    const profitPct = (price - stock.cost) / stock.cost * 100;
    const icon = getIcon(changePct);

    const row = {
      name: stock.name,
      code: d.f57,
      price: price.toFixed(2),
      changePct: changePct.toFixed(2),
      change: change.toFixed(2),
      cost: stock.cost.toFixed(3),
      profit: profit.toFixed(0),
      profitPct: profitPct.toFixed(1),
      icon,
      high: (d.f44 / 100).toFixed(2),
      low: (d.f45 / 100).toFixed(2),
      open: (d.f46 / 100).toFixed(2),
    };

    results.push(row);
    console.log(`${icon} ${row.name} (${row.code})`);
    console.log(`   现价: ¥${row.price}  涨跌: ${row.changePct}% (${row.change})`);
    console.log(`   今高: ${row.high}  今低: ${row.low}  开盘: ${row.open}`);
    console.log(`   成本: ¥${row.cost}  持仓盈亏: ¥${row.profit} (${row.profitPct}%)`);
    console.log();

    // 警报条件
    if (Math.abs(changePct) >= 5) {
      alerts.push({ stock, row, reason: changePct > 0 ? '涨幅≥5%' : '跌幅≥5%' });
    }
    if (profitPct >= 10) {
      alerts.push({ stock, row, reason: `持仓盈利已达${profitPct.toFixed(1)}%` });
    }
    if (profitPct <= -8) {
      alerts.push({ stock, row, reason: `持仓亏损已达${Math.abs(profitPct).toFixed(1)}%` });
    }
  }

  console.log('------------------------------------------------------------');
  const totalProfit = results.reduce((s, r) => s + parseFloat(r.profit), 0);
  const totalProfitPct = results.length > 0 ? (totalProfit / results.reduce((s, r) => s + parseFloat(r.cost) * WATCH_LIST.find(w => w.name === r.name).qty, 0) * 100).toFixed(1) : '0';
  console.log(`合计持仓盈亏: ¥${totalProfit.toFixed(0)}`);
  console.log('------------------------------------------------------------\n');

  // 发送飞书通知
  if (alerts.length > 0) {
    let msg = `🚨 *股票异动警报* — ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n\n`;
    for (const a of alerts) {
      msg += `⚠️ ${a.row.name} (${a.row.code})\n`;
      msg += `   现价 ¥${a.row.price}  涨跌 ${a.row.changePct}%\n`;
      msg += `   原因: ${a.reason}\n\n`;
    }
    msg += `---\n📊 合计盈亏: ¥${totalProfit.toFixed(0)}`;
    console.log('ALERT_MESSAGE:');
    console.log(msg);
  } else {
    console.log('✅ 无异常警报');
  }
}

main().catch(console.error);
