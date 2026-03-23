// stock_alert.js - 持仓异动监控脚本
// 每15分钟执行一次（工作日9-15时），有异动立刻发飞书
// 2026-03-24: 改用新浪行情API，解决东财API超时问题；pct 自行计算

const https = require('https');
const iconv = require('iconv-lite');

const stocks = [
  // 主账户
  { code: 'sh600352', name: '浙江龙盛',   cost: 15.912, qty: 141700, stopLoss: 12.0,  alertPct: 3 },
  { code: 'sh600089', name: '特变电工',   cost: 24.765, qty: 52300,  stopLoss: 25.0,  alertPct: 3 },
  { code: 'sz300033', name: '同花顺',     cost: 511.22, qty: 600,    stopLoss: 280.0, alertPct: 3 },
  { code: 'bj920046', name: '亿能电力',   cost: 35.936, qty: 12731,  stopLoss: 27.0,  alertPct: 3 },
  // 普适导航(831330)为新三板，暂用手动更新
  // 圣博润(430046)为新三板，Sina暂无数据，暂时移除自动监控
  // 老婆账户
  { code: 'sh600114', name: '东睦股份',   cost: 32.428, qty: 9200,   stopLoss: 28.0,  alertPct: 3 },
  { code: 'sz301638', name: '南网数字',   cost: 32.635, qty: 1700,   stopLoss: 28.0,  alertPct: 3 },
];

function fetchSina(codes) {
  return new Promise((resolve) => {
    const url = `https://hq.sinajs.cn/list=${codes}`;
    const r = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Referer': 'https://finance.sina.com.cn/'
      }
    }, res => {
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        const buf = Buffer.concat(chunks);
        const str = iconv.decode(buf, 'gbk');
        resolve(str);
      });
    });
    r.on('error', () => resolve(null));
    r.setTimeout(8000, () => { r.destroy(); resolve(null); });
  });
}

function parseSina(raw) {
  const map = {};
  const lines = raw.trim().split('\n');
  for (const line of lines) {
    const m = line.match(/hq_str_(\w+)="([^"]+)"/);
    if (!m) continue;
    const code = m[1];
    const parts = m[2].split(',');
    if (parts.length < 4) continue;
    map[code] = {
      name: parts[0],
      price: parseFloat(parts[1]) || 0,
      prevClose: parseFloat(parts[2]) || 0,
      pct: parseFloat(parts[3]) || 0,
      open: parseFloat(parts[4]) || 0,
      vol: parseFloat(parts[5]) || 0,    // 成交量
      amount: parseFloat(parts[6]) || 0, // 成交额
    };
  }
  return map;
}

async function main() {
  const now = new Date();
  const alerts = [];
  const lines = [];

  const codes = stocks.map(s => s.code).join(',');
  const raw = await fetchSina(codes);
  const data = parseSina(raw || '');

  for (const s of stocks) {
    if (!s.qty || s.qty === 0) continue;
    const d = data[s.code];
    if (!d || !d.price) {
      lines.push(`${s.name} [数据获取失败]`);
      continue;
    }

    const { price, prevClose } = d;
    const pct = prevClose > 0 ? (price - prevClose) / prevClose * 100 : 0;
    const profit = (price - s.cost) * s.qty;

    let tag = '';
    // 🚨 止损警报
    if (s.stopLoss > 0 && price <= s.stopLoss) {
      tag = '🚨止损';
      alerts.push(`🚨【止损警报】${s.name} 现价${price.toFixed(2)}元，跌至止损位 ${s.stopLoss}元！`);
    }
    // ⚠️ 跌幅 > 3%
    else if (pct <= -s.alertPct) {
      tag = '⚠️跌幅';
      alerts.push(`⚠️【跌幅预警】${s.name} 下跌${pct.toFixed(2)}%，现价${price.toFixed(2)}元`);
    }
    // 🚀 涨幅 > 5%（大幅上涨提示）
    else if (pct >= 5.0) {
      tag = '🚀涨幅';
      alerts.push(`🚀【涨幅提示】${s.name} 上涨${pct.toFixed(2)}%，现价${price.toFixed(2)}元`);
    }

    const tagStr = tag ? ` [${tag}]` : '';
    lines.push(`${s.name} ${price.toFixed(2)}元 (${pct >= 0 ? '+' : ''}${pct.toFixed(2)}%) 盈亏${profit >= 0 ? '+' : ''}${(profit/10000).toFixed(1)}万${tagStr}`);
  }

  if (alerts.length > 0) {
    const header = `📊 持仓异动提醒 ${now.getHours()}:${String(now.getMinutes()).padStart(2,'0')}\n`;
    const body = alerts.join('\n');
    const detail = '\n\n📋 全量持仓状态：\n' + lines.join('\n');
    console.log('ALERT:' + header + body + detail);
  } else {
    console.log('OK:' + now.toLocaleTimeString('zh-CN', {timeZone:'Asia/Shanghai'}) + ' 无异动\n' + lines.join('\n'));
  }
}

main().catch(e => console.error('ERROR:' + e.message));
