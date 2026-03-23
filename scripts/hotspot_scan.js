const https = require('https');
const http = require('http');

function fetch(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function extractItems(json, count = 10) {
  try {
    const list = json.data || json.list || json.result || [];
    return list.slice(0, count).map((v, i) => {
      const text = v.title || v.name || v.word || v.topic || JSON.stringify(v);
      return `${i + 1}. ${text}`;
    });
  } catch(e) {
    return ['解析失败'];
  }
}

async function main() {
  const results = {};

  // 微博
  try {
    const r = await fetch('https://tophub.today/api/hotword/m/wb');
    results.weibo = extractItems(JSON.parse(r));
  } catch(e) { results.weibo = ['获取失败: ' + e.message]; }

  // 抖音
  try {
    const r = await fetch('https://tophub.today/api/hotword/m/dy');
    results.douyin = extractItems(JSON.parse(r));
  } catch(e) { results.douyin = ['获取失败: ' + e.message]; }

  // 百度
  try {
    const r = await fetch('https://tophub.today/api/hotword/m/bd');
    results.baidu = extractItems(JSON.parse(r));
  } catch(e) { results.baidu = ['获取失败: ' + e.message]; }

  // 小红书
  try {
    const r = await fetch('https://tophub.today/api/hotword/m/xhs');
    results.xiaohongshu = extractItems(JSON.parse(r));
  } catch(e) { results.xiaohongshu = ['获取失败: ' + e.message]; }

  console.log(JSON.stringify(results, null, 2));
}

main().catch(console.error);
