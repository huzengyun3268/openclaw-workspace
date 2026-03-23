const https = require('https');
const iconv = require('iconv-lite');
const r = https.get('https://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006,s_sh000300,s_sz399688', {headers:{'User-Agent':'Mozilla/5.0','Referer':'https://finance.sina.com.cn/'}}, res => {
  const c=[];res.on('data',d=>c.push(d));res.on('end',()=>{
    const s=iconv.decode(Buffer.concat(c),'gbk');
    const lines=s.trim().split('\n');
    for(const line of lines){
      const code=line.match(/hq_str_s_(\w+)=/);
      const data=line.match(/"([^"]+)"/);
      if(!code||!data)continue;
      const p=data[1].split(',');
      const price=parseFloat(p[3]);
      const prev=parseFloat(p[2]);
      const pct=((price-prev)/prev*100);
      const flag=pct<-3?'CRASH':pct<-2?'BAD':pct<-1?'DOWN':'DN';
      console.log(flag+'|'+p[0]+': '+price.toFixed(2)+' ('+(pct>0?'+':'')+pct.toFixed(2)+'%)');
    }
  });
});
r.on('error',()=>{});
