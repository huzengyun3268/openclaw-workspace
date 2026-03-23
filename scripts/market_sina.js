const https = require('https');
function req(url, headers) {
  return new Promise((resolve) => {
    const r = https.get(url, {headers: headers || {'User-Agent':'Mozilla/5.0'}}, res => {
      let d='';res.on('data',c=>d+=c);
      res.on('end',()=>{resolve(d);});
    });
    r.on('error',()=>resolve(null));
  });
}

async function main() {
  const headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer':'https://finance.sina.com.cn/'
  };
  
  // 大盘指数
  const r = await req('https://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006,s_sh000300,s_sz399688', headers);
  const lines = r.trim().split('\n');
  console.log('=== 大盘 ===');
  for (const line of lines) {
    const nameMatch = line.match(/hq_str_s_(\w+)="([^"]+)"/);
    if (!nameMatch) continue;
    const parts = nameMatch[2].split(',');
    const pct = parseFloat(parts[3]);
    const flag = pct > 0 ? '+' : '';
    console.log(parts[0] + ': ' + parts[1] + ' (' + flag + pct.toFixed(2) + '%)');
  }
  
  // 行业/概念 ETF
  const etfCodes = 'sh512760,sh512290,sh515050,sh512690,sh512660,sh512400,sz159992,sz159745,sh512480,sh512950,sh512980,sz159628';
  const r2 = await req('https://hq.sinajs.cn/list=' + etfCodes, headers);
  const lines2 = r2.trim().split('\n');
  console.log('\n=== ETF异动 ===');
  const results = [];
  for (const line of lines2) {
    const nameMatch = line.match(/hq_str_(\w+)="([^"]+)"/);
    if (!nameMatch) continue;
    const code = nameMatch[1];
    const parts = nameMatch[2].split(',');
    const pct = parseFloat(parts[3]);
    results.push({ code, name: parts[0], price: parts[1], pct });
  }
  results.sort((a,b) => b.pct - a.pct);
  for (const e of results) {
    const flag = e.pct > 1 ? '🟢+' : e.pct > 0 ? '🟢' : e.pct < -1 ? '🔴' : '🟡';
    console.log(flag + ' ' + e.name + ': ' + e.price + ' (' + (e.pct>0?'+':'') + e.pct.toFixed(2) + '%)');
  }
  
  // 龙头股
  console.log('\n=== 持仓相关 ===');
  const holdings = 'sh600352,sh600089,sz300033,sh603248,sz300189,sz920046,sh600114,sz301638';
  const r3 = await req('https://hq.sinajs.cn/list=' + holdings, headers);
  const lines3 = r3.trim().split('\n');
  for (const line of lines3) {
    const nameMatch = line.match(/hq_str_(\w+)="([^"]+)"/);
    if (!nameMatch) continue;
    const code = nameMatch[1];
    const parts = nameMatch[2].split(',');
    if (!parts[3]) continue;
    const pct = parseFloat(parts[3]);
    const price = parseFloat(parts[1]);
    const prevClose = parseFloat(parts[2]);
    const change = pct > 0 ? '+' : '';
    console.log(parts[0] + '(' + code + '): ' + price.toFixed(2) + ' (' + change + pct.toFixed(2) + '%)');
  }
}
main().catch(console.error);
