const https = require('https');

function fetch(url, headers = {}) {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://weibo.com/',
        ...headers
      }
    }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

async function main() {
  const results = {};

  // 微博热搜 - 移动端API
  try {
    const r = await fetch('https://weibo.com/ajax/side/hotSearch');
    const json = JSON.parse(r);
    const list = json.data?.realtime || json.data?.hotgov || json.data?.band_list || [];
    results.weibo = list.slice(0, 10).map((v, i) => `${i+1}. ${v.word || v.topic_name || v.note || JSON.stringify(v)}`);
    if (results.weibo.length === 0) results.weibo = ['无数据: ' + JSON.stringify(json.data).slice(0,100)];
  } catch(e) { results.weibo = ['微博获取失败: ' + e.message]; }

  // 百度热搜
  try {
    const r = await fetch('https://top.baidu.com/api?get=home');
    const json = JSON.parse(r);
    const list = json.result?.hots || [];
    results.baidu = list.slice(0, 10).map((v, i) => `${i+1}. ${v.word || v.query || JSON.stringify(v)}`);
    if (results.baidu.length === 0) results.baidu = ['无数据: ' + JSON.stringify(json).slice(0,200)];
  } catch(e) { results.baidu = ['百度获取失败: ' + e.message]; }

  // 抖音热点
  try {
    const r = await fetch('https://www.iesdouyin.com/share/bucket/", misc2');
    // 直接抓包失败，尝试备用
    results.douyin = ['(抖音热点需浏览器环境)'];
  } catch(e) { results.douyin = ['抖音: ' + e.message]; }

  // 知乎
  try {
    const r = await fetch('https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10');
    const json = JSON.parse(r);
    const list = json.data || [];
    results.zhihu = list.slice(0, 10).map((v, i) => `${i+1}. ${v.target?.title || v.title || JSON.stringify(v)}`);
    if (results.zhihu.length === 0) results.zhihu = ['无数据: ' + JSON.stringify(json).slice(0,200)];
  } catch(e) { results.zhihu = ['知乎: ' + e.message]; }

  console.log(JSON.stringify(results, null, 2));
}

main().catch(console.error);
