const https = require('https');

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

// Build secids: A shares use 1., BJT/New OTC use 0.
function secid(code) {
    if (code.match(/^(00|60|68|30)/)) return '1.' + code;
    if (code.match(/^(920|430)/)) return '0.' + code;
    return '1.' + code;
}

const secids = stocks.map(s => secid(s.code)).join(',');
const url = `https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f14,f3,f2&secids=${secids}`;

function httpGet(url) {
    return new Promise((resolve, reject) => {
        https.get(url, {headers: {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://eastmoney.com'}}, (res) => {
            let data = '';
            res.on('data', d => data += d);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
}

async function main() {
    let priceMap = {};
    try {
        const body = await httpGet(url);
        const json = JSON.parse(body);
        if (json.data && json.data.diff) {
            for (const item of json.data.diff) {
                priceMap[item.f12] = {price: item.f2, change: item.f3, name: item.f14};
            }
        }
    } catch(e) {
        console.error('Failed to fetch prices:', e.message);
    }

    let totalCost = 0, totalValue = 0;
    const lines = [];

    for (const s of stocks) {
        const p = priceMap[s.code];
        const price = p ? p.price : s.cost;
        const change = p ? p.change : 0;
        const costAmt = s.cost * s.shares;
        const value = price * s.shares;
        const pnl = value - costAmt;
        const pnlPct = costAmt !== 0 ? (pnl / costAmt) * 100 : 0;
        totalCost += costAmt;
        totalValue += value;
        lines.push({...s, price, change, pnl, pnlPct});
    }

    const totalPnL = totalValue - totalCost;
    const totalPnLPct = totalCost !== 0 ? (totalPnL / totalCost) * 100 : 0;

    // Build Feishu message
    let msg = '📊 **股票早报** | 2026/03/20\n\n';
    for (const l of lines) {
        const sign = l.pnl >= 0 ? '+' : '';
        const arrow = l.pnl >= 0 ? '▲' : '▼';
        const csign = l.change >= 0 ? '+' : '';
        const carrow = l.change >= 0 ? '▲' : '▼';
        const code = l.code;
        msg += `**${l.name}** (${code})\n`;
        msg += `  现价 ${l.price.toFixed(3)}  ${carrow} ${csign}${l.change.toFixed(2)}%\n`;
        msg += `  成本 ${l.cost.toFixed(3)}  |  盈亏 ${sign}${l.pnl.toFixed(2)}元 (${sign}${l.pnlPct.toFixed(2)}%)\n\n`;
    }

    const ts = totalPnL >= 0 ? '+' : '';
    const ta = totalPnL >= 0 ? '▲' : '▼';
    msg += '──────────────────\n';
    msg += `**合计**  总市值 ${totalValue.toFixed(2)}元  总成本 ${totalCost.toFixed(2)}元\n`;
    msg += `${ta} 总盈亏 ${ts}${totalPnL.toFixed(2)}元 (${ts}${totalPnLPct.toFixed(2)}%)\n`;
    msg += '\n⚠️ 行情数据仅供参考，实际以交易软件为准';

    console.log(msg);
}

main();
