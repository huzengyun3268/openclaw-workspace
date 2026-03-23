const https=require('https');
const iconv=require('iconv-lite');
const r=https.get('https://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006',{headers:{'User-Agent':'Mozilla/5.0','Referer':'https://finance.sina.com.cn/'}},res=>{
  const c=[];res.on('data',d=>c.push(d));res.on('end',()=>{
    const s=iconv.decode(Buffer.concat(c),'gbk');
    s.trim().split('\n').forEach(line=>{
      const m=line.match(/"([^"]+)"/);
      if(m){
        const p=m[1].split(',');
        const pct=parseFloat(p[3]);
        const flag=pct<-3?'CRASH':pct<-2?'BAD':pct<-1?'DOWN':'DN';
        console.log(flag+'|'+p[0]+': '+(pct>=0?'+':'')+pct.toFixed(2)+'%');
      }
    });
  });
});
r.on('error',()=>{});
