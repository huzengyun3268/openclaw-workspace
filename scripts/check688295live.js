const https = require('https');
const iconv = require('iconv-lite');
const r = https.get('https://hq.sinajs.cn/list=sh688295', {headers:{'User-Agent':'Mozilla/5.0','Referer':'https://finance.sina.com.cn/'}}, res => {
  const c=[];res.on('data',d=>c.push(d));res.on('end',()=>{
    const s=iconv.decode(Buffer.concat(c),'gbk');
    const m=s.match(/"([^"]+)"/);
    if(!m)return;
    const p=m[1].split(',');
    const price=parseFloat(p[3]);
    const prev=parseFloat(p[2]);
    const pct=((price-prev)/prev*100);
    const high=parseFloat(p[4]);
    const low=parseFloat(p[5]);
    console.log('price='+price.toFixed(2));
    console.log('pct='+pct.toFixed(2));
    console.log('prev='+prev);
    console.log('high='+high.toFixed(2));
    console.log('low='+low.toFixed(2));
    console.log('open='+p[1]);
  });
});
r.on('error',()=>console.log('err'));
