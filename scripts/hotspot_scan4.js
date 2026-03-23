const https = require('https');
const http = require('http');

function fetch(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': '',
        ...headers
      }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data }));
    }).on('error', reject);
  });
}

async function main() {
  // 百度热搜 - PC端
  try {
    const r = await fetch('https://top.baidu.com/');
    if (r.data.startsWith('<!DOCTYPE')) {
      // 试试 mobile 版
      const r2 = await fetch('https://top.baidu.com/mobile/v1/html/hotList.html');
      console.log('百度mobile:', r2.data.slice(0, 500));
    } else {
      console.log('百度:', r.data.slice(0, 500));
    }
  } catch(e) { console.log('百度: ' + e.message); }

  // 知乎热榜
  try {
    const r = await fetch('https://www.zhihu.com/api/v4/search/top_search?fields=query');
    const json = JSON.parse(r.data);
    console.log('知乎热搜:', JSON.stringify(json).slice(0, 500));
  } catch(e) { console.log('知乎: ' + e.message); }

  // 知乎热榜 v2
  try {
    const r = await fetch('https://www.zhihu.com/best-of-all/hot-list');
    const r2 = await fetch('https://www.zhihu.com/hot?list_id=0');
    console.log('知乎hot:', r2.data.slice(0, 500));
  } catch(e) { console.log('知乎v2: ' + e.message); }
}

main().catch(console.error);
