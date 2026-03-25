// 综合早报生成器 - 通过web_fetch获取新闻
const https = require('https');
const http = require('http');

function fetchSina(codes) {
    return new Promise((resolve) => {
        const req = http.request({
            hostname: 'hq.sinajs.cn',
            path: '/list=' + codes,
            method: 'GET',
            headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.sina.com.cn' }
        }, (res) => {
            const chunks = [];
            res.on('data', c => chunks.push(c));
            res.on('end', () => {
                const body = Buffer.concat(chunks).toString('utf8');
                const results = [];
                const regex = /"([^"]+)"/g;
                let match;
                while ((match = regex.exec(body)) !== null) {
                    const fields = match[1].split(',');
                    if (fields.length > 4) {
                        const name = fields[0];
                        const prev = parseFloat(fields[2]);
                        const price = parseFloat(fields[3]);
                        if (!isNaN(prev) && !isNaN(price) && prev > 0) {
                            const pct = ((price / prev - 1) * 100).toFixed(2);
                            const sign = parseFloat(pct) > 0 ? '+' : '';
                            results.push(`${name} ${price.toFixed(2)} ${sign}${pct}%`);
                        }
                    }
                }
                resolve(results.join(' | '));
            });
        });
        req.on('error', () => resolve(''));
        req.setTimeout(8000, () => resolve(''));
        req.end();
    });
}

function getGold() {
    return new Promise((resolve) => {
        const req = http.request({
            hostname: 'hq.sinajs.cn',
            path: '/list=hf_GC',
            method: 'GET',
            headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.sina.com.cn' }
        }, (res) => {
            const chunks = [];
            res.on('data', c => chunks.push(c));
            res.on('end', () => {
                try {
                    const body = Buffer.concat(chunks).toString('utf8');
                    const m = body.match(/"([^"]+)"/);
                    if (m) {
                        const price = parseFloat(m[1].split(',')[0]).toFixed(2);
                        resolve(`Comex黄金: $${price}/盎司`);
                    } else { resolve(''); }
                } catch (e) { resolve(''); }
            });
        });
        req.on('error', () => resolve(''));
        req.end();
    });
}

function getDateStr() {
    const now = new Date();
    const month = now.getMonth() + 1;
    const day = now.getDate();
    const wd = ['周日','周一','周二','周三','周四','周五','周六'][now.getDay()];
    return `${month}月${day}日 ${wd}`;
}

async function main() {
    const dateStr = getDateStr();
    const [market, gold] = await Promise.all([
        fetchSina('sh000001,sz399001,sz399006'),
        getGold()
    ]);

    // News content embedded (since fetch is unreliable) - will be replaced by parent agent
    const output = {
        date: dateStr,
        market: market || '（获取失败）',
        gold: gold,
        status: 'ready'
    };

    console.log(JSON.stringify(output));
}

main().catch(e => { console.log(JSON.stringify({status:'error', msg: e.message})); });
