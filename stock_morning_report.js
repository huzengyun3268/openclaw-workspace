const stocks = [
  {name:'特变电工', code:'600089', cost:24.765, shares:52300},
  {name:'浙江龙盛', code:'600352', cost:15.912, shares:141700},
  {name:'锡华科技', code:'603248', cost:35.490, shares:2000},
  {name:'同花顺', code:'300033', cost:511.220, shares:600},
  {name:'神农种业', code:'300189', cost:17.099, shares:5000},
  {name:'亿能电力', code:'920046', cost:35.936, shares:12731},
  {name:'普适导航', code:'831330', cost:20.415, shares:6370},
  {name:'圣博润', code:'430046', cost:0.478, shares:10334},
];

async function getPrice(code) {
  try {
    const res = await fetch('http://hq.sinajs.cn/list=' + code);
    const text = await res.text();
    const m = text.match(/"([^"]+)"/);
    if (!m) return null;
    const parts = m[1].split(',');
    return parseFloat(parts[3]) || 0;
  } catch(e) { return null; }
}

async function main() {
  const prices = [];
  for (const s of stocks) {
    const price = await getPrice(s.code);
    prices.push({...s, price: price || s.cost});
    await new Promise(r => setTimeout(r, 300));
  }

  let totalCost = 0, totalValue = 0, totalPnL = 0;
  let lines = [];

  for (const s of prices) {
    const costAmt = s.cost * s.shares;
    const value = s.price * s.shares;
    const pnl = value - costAmt;
    const pnlPct = (pnl / costAmt) * 100;
    totalCost += costAmt;
    totalValue += value;
    totalPnL += pnl;

    const sign = pnl >= 0 ? '+' : '';
    const arrow = pnl >= 0 ? '▲' : '▼';
    lines.push({
      name: s.name,
      price: s.price.toFixed(3),
      priceChange: pnlPct.toFixed(2),
      cost: s.cost.toFixed(3),
      pnl: pnl.toFixed(2),
      pnlPct: pnlPct.toFixed(2),
      arrow: arrow,
      sign: sign
    });
  }

  const totalPnLPct = (totalPnL / totalCost) * 100;

  // Generate markdown for Feishu
  let msg = `📊 **股票早报** | ${new Date().toLocaleDateString('zh-CN', {year:'numeric', month:'2-digit', day:'2-digit'})}\n\n`;

  for (const l of lines) {
    const sign = l.sign;
    const arrow = l.arrow;
    const pnlStr = `${sign}${l.pnl}元 (${sign}${l.pnlPct}%)`;
    msg += `**${l.name}**(${l.code})\n`;
    msg += `  现价 ${l.price}  ${arrow} ${l.priceChange}%\n`;
    msg += `  成本 ${l.cost}  |  盈亏 ${pnlStr}\n\n`;
  }

  const totalSign = totalPnL >= 0 ? '+' : '';
  const totalArrow = totalPnL >= 0 ? '▲' : '▼';
  msg += `──────────────────\n`;
  msg += `**合计**  总市值 ${totalValue.toFixed(2)}元  总成本 ${totalCost.toFixed(2)}元\n`;
  msg += `${totalArrow} 总盈亏 ${totalSign}${totalPnL.toFixed(2)}元 (${totalSign}${totalPnLPct.toFixed(2)}%)\n`;

  console.log(msg);

  // Also output JSON for programmatic use
  console.log('\n---JSON---');
  console.log(JSON.stringify({
    stocks: lines,
    totalCost: totalCost.toFixed(2),
    totalValue: totalValue.toFixed(2),
    totalPnL: totalPnL.toFixed(2),
    totalPnLPct: totalPnLPct.toFixed(2)
  }));
}

main();
