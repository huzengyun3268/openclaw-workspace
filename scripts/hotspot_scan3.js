const https = require('https');

function fetch(url, headers = {}) {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
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
  // 知乎移动端
  try {
    const r = await fetch('https://api.zhihu.com/热搜', {'Accept-Language': 'zh-CN'});
    const json = JSON.parse(r);
    console.log('知乎raw:', JSON.stringify(json).slice(0, 500));
  } catch(e) { console.log('知乎: ' + e.message); }

  // 百度移动端
  try {
    const r = await fetch('https://top.baidu.com/mobile/v1/hot/list?topic=new&type=topic&pn=0&rn=10');
    const json = JSON.parse(r);
    const list = json.result?.hots || [];
    const baidu = list.map((v, i) => `${i+1}. ${v.word || v.query}`);
    console.log('百度:', baidu.join('\n'));
  } catch(e) { console.log('百度: ' + e.message); }

  // 抖音
  try {
    const r = await fetch('https://www.douyin.com/aweme/v1/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1');
    const json = JSON.parse(r);
    const list = json.data?.word_list || [];
    console.log('抖音:', list.slice(0,10).map((v,i) => `${i+1}. ${v.word}`).join('\n'));
  } catch(e) { console.log('抖音: ' + e.message); }
}

main().catch(console.error);
