const https = require('https');

const stocks = [
    { code: '600352', name: '浙江龙盛', cost: 15.91, shares: 106700 },
    { code: '600089', name: '特变电工', cost: 24.765, shares: 52300 },
    { code: '301667', name: '纳百川', cost: 82.715, shares: 3000 },
    { code: '920046', name: '亿能电力', cost: 35.936, shares: 12731 },
    { code: '300033', name: '同花顺', cost: 511.22, shares: 600 },
    { code: '831330', name: '普适导航', cost: 20.415, shares: 6370 },
    { code: '300189', name: '神农种业', cost: 17.099, shares: 5000 },
    { code: '430046', name: '圣博润', cost: 0.478, shares: 10334 },
];

const wifeStocks = [
    { code: '600114', name: '东睦股份', cost: 32.428, shares: 9200 },
    { code: '301638', name: '南网数字', cost: 32.635, shares: 1700 },
];

async function fetchStock(code) {
    return new Promise((resolve) => {
        const market = code.startsWith('6') ? '1' : '0';
        const url = `https://push2.eastmoney.com/api/qt/stock/get?secid=${market}.${code}&fields=f43,f170`;
        https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    if (json.data) {
                        const price = json.data.f43 / 100;
                        const change = json.data.f170 / 100;
                        resolve({ price, change });
                    } else {
                        resolve(null);
                    }
                } catch (e) {
                    resolve(null);
                }
            });
        }).on('error', () => resolve(null));
    });
}

async function main() {
    console.log('=== 我的账户持仓监控 ===');
    let totalProfit = 0;
    for (const s of stocks) {
        const info = await fetchStock(s.code);
        if (info) {
            const value = info.price * s.shares;
            const cost = s.cost * s.shares;
            const profit = value - cost;
            const profitPct = ((info.price - s.cost) / s.cost * 100).toFixed(2);
            totalProfit += profit;
            const emoji = profit >= 0 ? '📈' : '📉';
            console.log(`${emoji} ${s.code} ${s.name}: 现价${info.price} | 涨跌${info.change.toFixed(2)}% | 成本${s.cost} | 持仓${s.shares}股 | 盈亏${profit.toFixed(0)}元 (${profitPct}%)`);
        } else {
            console.log(`⚠️ ${s.code} ${s.name}: 获取失败`);
        }
    }
    console.log(`\n账户总盈亏: ${totalProfit >= 0 ? '+' : ''}${totalProfit.toFixed(0)}元`);

    console.log('\n=== 老婆账户持仓监控 ===');
    let wifeTotalProfit = 0;
    for (const s of wifeStocks) {
        const info = await fetchStock(s.code);
        if (info) {
            const value = info.price * s.shares;
            const cost = s.cost * s.shares;
            const profit = value - cost;
            const profitPct = ((info.price - s.cost) / s.cost * 100).toFixed(2);
            wifeTotalProfit += profit;
            const emoji = profit >= 0 ? '📈' : '📉';
            console.log(`${emoji} ${s.code} ${s.name}: 现价${info.price} | 涨跌${info.change.toFixed(2)}% | 成本${s.cost} | 持仓${s.shares}股 | 盈亏${profit.toFixed(0)}元 (${profitPct}%)`);
        } else {
            console.log(`⚠️ ${s.code} ${s.name}: 获取失败`);
        }
    }
    console.log(`\n老婆账户总盈亏: ${wifeTotalProfit >= 0 ? '+' : ''}${wifeTotalProfit.toFixed(0)}元`);
    console.log(`\n两账户合计盈亏: ${(totalProfit + wifeTotalProfit) >= 0 ? '+' : ''}${(totalProfit + wifeTotalProfit).toFixed(0)}元`);
}

main();
