const https=require('https');
const iconv=require('iconv-lite');
https.get('https://hq.sinajs.cn/list=sh600352,sh600089,sz300033,bj920046,sh600114,sz301638,sh688295',{headers:{'User-Agent':'Mozilla/5.0','Referer':'https://finance.sina.com.cn/'}},res=>{
  const c=[];res.on('data',d=>c.push(d));res.on('end',()=>{
    const s=iconv.decode(Buffer.concat(c),'gbk');
    s.trim().split('\n').forEach(line=>{
      const m=line.match(/"([^"]+)"/);
      if(!m)return;
      const p=m[1].split(',');
      if(p.length<4)return;
      const price=parseFloat(p[3]);
      const prev=parseFloat(p[2]);
      const pct=((price-prev)/prev*100);
      console.log(p[0]+'|'+price.toFixed(3)+'|'+pct.toFixed(2));
    });
  });
});
