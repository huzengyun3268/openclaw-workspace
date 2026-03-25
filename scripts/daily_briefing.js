// 每日综合早报脚本 v2
const https = require('https');
const http = require('http');

function fetchUrl(url, encoding = 'utf8') {
    return new Promise((resolve, reject) => {
        const client = url.startsWith('https') ? https : http;
        const req = client.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml',
                'Accept-Language': 'zh-CN,zh;q=0.9'
            }
        }, (res) => {
            const chunks = [];
            res.on('data', chunk => chunks.push(chunk));
            res.on('end', () => {
                const raw = Buffer.concat(chunks);
                // Try detect encoding
                let text;
                if (encoding === 'gbk') {
                    text = raw.toString('binary');
                } else {
                    text = raw.toString('utf8');
                }
                resolve(text);
            });
        });
        req.on('error', reject);
        req.setTimeout(15000, () => { req.destroy(); reject(new Error('Timeout')); });
    });
}

function gbkToUtf8(binaryStr) {
    try {
        return Buffer.from(binaryStr, 'binary').toString('utf8');
    } catch (e) {
        return binaryStr;
    }
}

function extractText(html) {
    // Remove scripts and styles
    let text = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
    text = text.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
    text = text.replace(/<[^>]+>/g, ' ');
    text = text.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
    text = text.replace(/\s+/g, ' ').trim();
    return text;
}

async function getBaiduNews(keyword) {
    try {
        const url = `https://www.baidu.com/s?wd=${encodeURIComponent(keyword + ' 最新')}&rn=10&tn=news`;
        const html = await fetchUrl(url);
        const text = extractText(html);

        // Extract news titles - look for patterns like "新闻标题" near source names
        const lines = text.split(/[.。;；\n]/);
        const results = [];
        for (const line of lines) {
            const clean = line.replace(/<[^>]+>/g, '').trim();
            if (clean.length > 10 && clean.length < 80 &&
                !clean.includes('百度') && !clean.includes('搜索') &&
                !clean.includes('为您推荐') && !clean.includes('展开全部') &&
                (clean.includes('：') || clean.includes(':') || clean.match(/[\u4e00-\u9fa5]{6,}/))) {
                results.push(clean.substring(0, 60));
            }
            if (results.length >= 5) break;
        }
        return results.length > 0 ? results : ['（暂无结果，请查看百度热搜）'];
    } catch (e) {
        return ['（获取失败）'];
    }
}

async function getMarketBrief() {
    return new Promise((resolve) => {
        const req = https.request({
            hostname: 'hq.sinajs.cn',
            path: '/list=sh000001,sz399001,sz399006',
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0',
                'Referer': 'https://finance.sina.com.cn'
            }
        }, (res) => {
            const chunks = [];
            res.on('data', c => chunks.push(c));
            res.on('end', () => {
                const body = Buffer.concat(chunks).toString('utf8');
                const results = [];
                const regex = /"([^"]+)"/g;
                let match;
                while ((match = regex.exec(body)) !== null && results.length < 3) {
                    const fields = match[1].split(',');
                    if (fields.length > 4) {
                        const name = fields[0];
                        const prev = parseFloat(fields[2]);
                        const price = parseFloat(fields[3]);
                        const pct = ((price / prev - 1) * 100).toFixed(2);
                        const sign = pct > 0 ? '+' : '';
                        results.push(`${name} ${price.toFixed(2)} ${sign}${pct}%`);
                    }
                }
                resolve(results.join(' | ') || '（获取失败）');
            });
        });
        req.on('error', () => resolve('（网络错误）'));
        req.setTimeout(10000, () => resolve('（超时）'));
        req.end();
    });
}

async function getGold() {
    return new Promise((resolve) => {
        const req = https.request({
            hostname: 'hq.sinajs.cn',
            path: '/list=hf_GC,hf_SI',
            method: 'GET',
            headers: { 'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.sina.com.cn' }
        }, (res) => {
            const chunks = [];
            res.on('data', c => chunks.push(c));
            res.on('end', () => {
                const body = Buffer.concat(chunks).toString('utf8');
                const match = body.match(/"([^"]+)"/g);
                if (match && match.length >= 1) {
                    try {
                        const gold = parseFloat(match[0].replace(/"/g, '').split(',')[0]).toFixed(2);
                        resolve(`黄金(Comex): $${gold}/盎司`);
                    } catch (e) { resolve(''); }
                } else { resolve(''); }
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
    console.log(`\n📰 综合早报 — ${dateStr}`);
    console.log('═'.repeat(42));

    const [domestic, international, market, gold] = await Promise.all([
        getBaiduNews('国内时政'),
        getBaiduNews('国际大事'),
        getMarketBrief(),
        getGold()
    ]);

    console.log('\n🌏 国内要闻');
    domestic.forEach((item, i) => console.log(`  ${i+1}. ${item}`));

    console.log('\n🌍 国际动态');
    international.forEach((item, i) => console.log(`  ${i+1}. ${item}`));

    console.log('\n💹 财经参考');
    console.log(`  大盘: ${market}`);
    if (gold) console.log(`  ${gold}`);

    console.log('\n' + '═'.repeat(42));
}

main().catch(console.error);
