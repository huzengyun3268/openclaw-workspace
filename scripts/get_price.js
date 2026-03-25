// 获取持仓股票实时行情 - 使用腾讯财经API
const http = require('http');

const stocks = {
    'sh600487': '亨通光电',
    'sh601168': '西部矿业',
    'sh600893': '航发动力',
    'sh600352': '浙江龙盛',
    'sh600089': '特变电工',
    'sz300033': '同花顺',
    'sh688295': '中复神鹰',
    'sz300499': '高澜股份',
    'sh600114': '东睦股份',
    'sz301638': '南网数字'
};

const url = 'http://qt.gtimg.cn/q=' + Object.keys(stocks).join(',');

const req = http.get(url, {
    headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'http://gu.qq.com' }
}, (res) => {
    const chunks = [];
    res.on('data', c => chunks.push(c));
    res.on('end', () => {
        const text = Buffer.concat(chunks).toString('utf8');
        const lines = text.split('\n');
        lines.forEach(line => {
            const m = line.match(/"([^"]+)"/);
            if (m) {
                const fields = m[1].split('~');
                if (fields.length > 35) {
                    const code = fields[2];
                    const name = fields[1];
                    const price = fields[3];
                    const pct = parseFloat(fields[32] || 0).toFixed(2);
                    const open = fields[5];
                    const high = fields[33];
                    const low = fields[34];
                    const sign = parseFloat(pct) > 0 ? '+' : '';
                    console.log(`${code} ${name}: 现价=${price} 涨幅=${sign}${pct}% 开盘=${open} 最高=${high} 最低=${low}`);
                }
            }
        });
    });
});

req.on('error', e => console.log('Error:', e.message));
req.setTimeout(10000, () => { console.log('Timeout'); req.destroy(); });
