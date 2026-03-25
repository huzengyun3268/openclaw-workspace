const https = require('https');

const codes = ['600487', '601168', '600893', '600352', '600089', '300033', '688295', '300499', '600114', '301638'];
const secids = codes.map(c => {
    if (c.startsWith('6')) return '1.' + c;
    if (c.startsWith('0') || c.startsWith('3')) return '0.' + c;
    return c;
}).join(',');

const url = `https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f14,f3,f2,f4,f5,f6&secids=${secids}`;

const req = https.get(url, {
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://quote.eastmoney.com/',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
}, (res) => {
    const chunks = [];
    res.on('data', c => chunks.push(c));
    res.on('end', () => {
        try {
            const data = JSON.parse(Buffer.concat(chunks).toString());
            if (data.data && data.data.diff) {
                data.data.diff.forEach(item => {
                    const pct = item.f3;
                    const sign = pct > 0 ? '+' : '';
                    console.log(`${item.f12} ${item.f14}: 现价=${item.f2} 涨幅=${sign}${pct}% 开盘=${item.f5} 最高=${item.f6}`);
                });
            } else {
                console.log('No data:', JSON.stringify(data).substring(0, 200));
            }
        } catch (e) {
            console.log('Parse error:', e.message);
        }
    });
});

req.on('error', e => console.log('Request error:', e.message));
req.setTimeout(10000, () => { console.log('Timeout'); req.destroy(); });
