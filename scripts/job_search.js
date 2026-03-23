const https = require('https');
const url = 'https://www.lagou.com/jobs/list_%E8%B7%9F%E5%8D%95%E7%94%B5%E5%95%86?px=default&city=%E6%B5%99%E6%B1%9F&pn=1';
const options = {
    headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.lagou.com/'
    }
};
https.get(url, options, res => {
    let d = '';
    res.on('data', c => d += c);
    res.on('end', () => {
        // 提取总职位数
        const cnt = d.match(/totalCount["\s:]+(\d+)/);
        console.log('总职位数:', cnt ? cnt[1] : '未找到');
        // 提取薪资和职位名
        const re = /"positionName"\s*:\s*"([^"]+)"/g;
        const re2 = /"salary"\s*:\s*"([^"]+)"/g;
        let m;
        const names = [];
        const sals = [];
        while ((m = re.exec(d)) !== null) names.push(m[1]);
        while ((m = re2.exec(d)) !== null) sals.push(m[1]);
        console.log('--- 跨境电商相关职位 ---');
        names.slice(0,10).forEach((n,i) => {
            console.log((i+1) + '. ' + n + ' | 薪资: ' + (sals[i]||'待定'));
        });
    });
}).on('error', e => console.log(e.message));
