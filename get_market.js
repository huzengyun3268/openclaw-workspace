const https = require('https');

function fetch(url) {
    return new Promise((resolve, reject) => {
        https.get(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Referer': 'https://www.eastmoney.com'
            }
        }, (res) => {
            let data = '';
            res.on('data', d => data += d);
            res.on('end', () => resolve(data));
        }).on('error', reject);
    });
}

async function main() {
    // 行业板块
    const url1 = 'https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=30&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f2,f3,f12,f14,f9,f62';
    // 概念板块
    const url2 = 'https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=30&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f2,f3,f12,f14,f9,f62';
    // 科创板强势
    const url3 = 'https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:1+t:23&fields=f2,f3,f12,f14,f9,f62';
    // 主板强势
    const url5 = 'https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=80&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:1+t:2,m:1+t:23&fields=f2,f3,f12,f14,f9,f62';

    const [d1, d2, d3, d5] = await Promise.all([
        fetch(url1).catch(e => '{}'),
        fetch(url2).catch(e => '{}'),
        fetch(url3).catch(e => '{}'),
        fetch(url5).catch(e => '{}')
    ]);

    try {
        const j1 = JSON.parse(d1);
        console.log('=== 今日行业板块涨幅Top20 ===');
        (j1.data?.diff || []).slice(0, 20).forEach(item => {
            const chg = (item.f3 / 100).toFixed(2);
            const flow = item.f62 ? (item.f62 / 10000).toFixed(0) : 'N/A';
            const turnover = item.f9 ? (item.f9 / 100).toFixed(2) : 'N/A';
            console.log('  ' + item.f14 + ' | 涨幅:' + chg + '% | 换手:' + turnover + '% | 主力净流入:' + flow + '万');
        });
    } catch(e) { console.log('j1 error:', d1.substring(0, 200)); }

    try {
        const j2 = JSON.parse(d2);
        console.log('\n=== 今日概念板块涨幅Top20 ===');
        (j2.data?.diff || []).slice(0, 20).forEach(item => {
            const chg = (item.f3 / 100).toFixed(2);
            console.log('  ' + item.f14 + ' | 涨幅:' + chg + '%');
        });
    } catch(e) { console.log('j2 error'); }

    try {
        const j3 = JSON.parse(d3);
        console.log('\n=== 科创板强势Top20 ===');
        (j3.data?.diff || []).slice(0, 20).forEach(item => {
            const chg = (item.f3 / 100).toFixed(2);
            const price = item.f2 ? (item.f2 / 100).toFixed(2) : 'N/A';
            const flow = item.f62 ? (item.f62 / 10000).toFixed(0) : 'N/A';
            console.log('  ' + item.f14 + '(' + item.f12 + ') | ' + price + '元 | +' + chg + '% | 主力:' + flow + '万');
        });
    } catch(e) { console.log('j3 error'); }

    try {
        const j5 = JSON.parse(d5);
        console.log('\n=== 主板/中小板强势Top30 ===');
        (j5.data?.diff || []).slice(0, 30).forEach(item => {
            const chg = (item.f3 / 100).toFixed(2);
            const price = item.f2 ? (item.f2 / 100).toFixed(2) : 'N/A';
            const flow = item.f62 ? (item.f62 / 10000).toFixed(0) : 'N/A';
            console.log('  ' + item.f14 + '(' + item.f12 + ') | ' + price + '元 | +' + chg + '% | 主力:' + flow + '万');
        });
    } catch(e) { console.log('j5 error:', e.message); }
}

main().catch(console.error);
