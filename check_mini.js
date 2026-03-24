var http=require('http');
var ic=require('iconv-lite');
var o={hostname:'hq.sinajs.cn',path:'/list=sh600352,sh600089,sh688295',headers:{'Referer':'http://finance.sina.com.cn'}};
http.get(o,function(r){var d='';r.on('data',function(c){d+=c});r.on('end',function(){var s=ic.decode(Buffer.from(d),'GBK');var lines=s.trim().split('\n');lines.forEach(function(l){var i=l.indexOf('="');if(i>0){var f=l.substring(i+2,l.length-2).split(',');if(f[1]&&f[1]!='0.000')console.log(f[0]+':'+f[1]+'('+f[3]+'%)');}});});}).on('error',function(e){console.log(e.message);});
