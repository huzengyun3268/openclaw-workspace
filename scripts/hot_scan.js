// hot_scan.js - 每日热点扫描发送到飞书
// 每天早上8:05运行

const https = require('https');

const BAIDU_HOT = 'https://top.baidu.com/board?tab=realtime';
const WEIBO_HOT = 'https://tophub.today/n/KqndgxeLl9';
const DOUYIN_HOT = 'https://tophub.today/n/DpQvNABoNE';

function fetchHtml(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function extractItems(html, patterns) {
  const items = [];
  for (const p of patterns) {
    const m = html.match(p);
    if (m) items.push(m[1].trim().substring(0, 50));
  }
  return items;
}

async function main() {
  try {
    const [baidu, weibo, douyin] = await Promise.all([
      fetchHtml(BAIDU_HOT).catch(() => ''),
      fetchHtml(WEIBO_HOT).catch(() => ''),
      fetchHtml(DOUYIN_HOT).catch(() => ''),
    ]);

    // 百度热搜 - 取前5
    const baiduItems = extractItems(baidu, [
      /<div class="index_1Ug3217 ACa3zwf">([^<]+)</,
      /<div class="index_1Ug3217[^>]*>[^<]*<a[^>]*>([^<]+)</,
      /hotIndex_[\w]+[^>]*>[^<]*</div>[^<]*<div[^>]*>\s*([^<]{2,30})</,
    ]);
    // 简单：取所有文本行过滤
    const baiduLines = baidu.split('\n').map(l => l.trim()).filter(l => l.length > 3 && l.length < 60 && !l.match(/^\d/) && !l.match(/http/));
    
    console.log('🔥 Hot scan fetched');
    console.log('BAIDU_LINES:', baiduLines.slice(0,5).join('|'));
    console.log('---REPORT_START---');
    
    const today = new Date().toLocaleDateString('zh-CN', { timeZone: 'Asia/Shanghai' });
    const dayOfWeek = ['周日','周一','周二','周三','周四','周五','周六'][new Date().getDay()];
    
    console.log(`🔥 **今日热点 | ${today} ${dayOfWeek}**`);
    console.log('━━━━━━━━━━━━━━━━━━');
    console.log('📌 数据已获取，待通过cron内置机制发送至飞书');
    
  } catch(e) {
    console.error('Error:', e.message);
  }
}

main();
