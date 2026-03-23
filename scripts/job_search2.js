const https = require('https');
const url = 'https://sogou.com/web?query=%E6%B5%99%E6%B1%9F+%E8%B7%9F%E5%8D%95%E7%94%B5%E5%95%86+%E8%BF%90%E8%90%A5+%E6%8B%9B%E5%95%86&ie=utf8&num=10';
https.get(url, {headers:{'User-Agent':'Mozilla/5.0'}}, res => {
    let d=''; res.on('data',c=>d+=c);
    res.on('end',()=>{
        const titles = d.match(/class="vrTitle[^>]*>([^<]+)/g) || [];
        titles.slice(0,8).forEach(t=>console.log(t.replace(/<[^>]+>/g,'')));
    });
}).on('error',e=>console.log(e.message));
