const https = require('https');

function fetch(url, headers = {}) {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
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

function fetchHttp(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : require('http');
    mod.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
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

  // 微博热搜
  try {
    const r = await fetch('https://weibo.com/ajax/side/hotSearch');
    const json = JSON.parse(r);
    const list = json.data?.realtime || json.data?.band_list || [];
    results.weibo = list.slice(0, 10).map((v, i) => `${i+1}. ${v.word || v.topic_name || v.note}`);
    if (results.weibo.length === 0) throw new Error('empty');
  } catch(e) { results.weibo = ['获取失败']; }

  // 抖音热点
  try {
    const r = await fetch('https://www.douyin.com/aweme/v1/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1');
    const json = JSON.parse(r);
    const list = json.data?.word_list || [];
    results.douyin = list.slice(0, 10).map((v, i) => `${i+1}. ${v.word}`);
    if (results.douyin.length === 0) throw new Error('empty');
  } catch(e) { results.douyin = ['获取失败']; }

  // 百度热搜
  try {
    const r = await fetchHttp('http://top.baidu.com/mobile/v1/hot/list?topic=new&type=topic&pn=0&rn=10');
    const json = JSON.parse(r);
    const list = json.result?.hots || [];
    results.baidu = list.slice(0, 10).map((v, i) => `${i+1}. ${v.word}`);
    if (results.baidu.length === 0) throw new Error('empty');
  } catch(e) {
    // 备用：知乎热搜字段
    try {
      const r2 = await fetch('https://www.zhihu.com/api/v4/search/top_search?fields=query');
      const json2 = JSON.parse(r2);
      results.baidu = (json2.top_search?.words || []).slice(0, 10).map((v, i) => `${i+1}. ${v.display_query}`);
    } catch(e2) { results.baidu = ['获取失败']; }
  }

  console.log(JSON.stringify(results, null, 2));
}

main().catch(console.error);
