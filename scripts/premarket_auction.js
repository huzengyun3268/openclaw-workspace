// premarket_auction.js - 集合竞价异动监控
// 9:15/9:20/9:25 检查持仓股竞价异动
// 2026-03-24: 改用新浪行情API，解决东财API超时问题

const https = require('https');
const iconv = require('iconv-lite');

const holdings = [
  // 主账户
  { code: 'sh600352', name: '浙江龙盛',   cost: 15.912, qty: 141700, stopLoss: 12.0 },
  { code: 'sh600089', name: '特变电工',   cost: 24.765, qty: 52300,  stopLoss: 25.0 },
  { code: 'sz300033', name: '同花顺',     cost: 511.22, qty: 600,    stopLoss: 280.0 },
  { code: 'bj920046', name: '亿能电力',   cost: 35.936, qty: 12731,  stopLoss: 27.0 },
  // 老婆账户
  { code: 'sh600114', name: '东睦股份',   cost: 32.428, qty: 9200,   stopLoss: 28.0 },
  { code: 'sz301638', name: '南网数字',   cost: 32.635, qty: 1700,   stopLoss: 28.0 },
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
      high: parseFloat(parts[5]) || 0,
      low: parseFloat(parts[6]) || 0,
      vol: parseFloat(parts[7]) || 0,
      amount: parseFloat(parts[8]) || 0,
    };
  }
  return map;
}

async function main() {
  const now = new Date();
  const alerts = [];
  const lines = [];

  const codes = holdings.map(h => h.code).join(',');
  const raw = await fetchSina(codes);
  const data = parseSina(raw || '');

  for (const h of holdings) {
    if (!h.qty || h.qty === 0) continue;
    const d = data[h.code];
    if (!d || !d.price) {
      lines.push(`${h.name} [数据获取失败]`);
      continue;
    }

    const { price, prevClose, open } = d;
    const pct = prevClose > 0 ? (price - prevClose) / prevClose * 100 : 0;
    const costDistort = (price - h.cost) / h.cost * 100;

    let tag = '';
    // 🚨 止损警报
    if (h.stopLoss > 0 && price <= h.stopLoss) {
      tag = '🚨止损';
      alerts.push(`🚨【止损警报】${h.name} 现价${price.toFixed(2)}元，跌至止损位 ${h.stopLoss}元！`);
    }
    // ⚠️ 大幅低开（竞价跌幅 > 3%）
    else if (pct <= -3.0) {
      tag = '⚠️大幅低开';
      alerts.push(`⚠️【大幅低开】${h.name} 竞价${pct.toFixed(2)}%，现价${price.toFixed(2)}元（昨收${prevClose.toFixed(2)}）`);
    }
    // 🚀 大幅高开（竞价涨幅 > 5%）
    else if (pct >= 5.0) {
      tag = '🚀大幅高开';
      alerts.push(`🚀【大幅高开】${h.name} 竞价${pct.toFixed(2)}%，现价${price.toFixed(2)}元`);
    }
    // 成本偏离 > 15%
    else if (costDistort <= -15) {
      tag = '⚠️成本偏离';
      alerts.push(`⚠️【成本偏离】${h.name} 现价${price.toFixed(2)}元，相对成本${h.cost.toFixed(2)}元已跌${costDistort.toFixed(1)}%`);
    }
    // 接近涨停（涨幅>9.8%且高于成本）
    else if (pct >= 9.8 && price > h.cost) {
      alerts.push(`🚀【接近涨停】${h.name} 涨幅${pct.toFixed(2)}%，注意获利了结机会`);
    }

    const tagStr = tag ? ` [${tag}]` : '';
    lines.push(`${h.name} 昨收${prevClose.toFixed(2)} → 当前${price.toFixed(2)} (${pct >= 0 ? '+' : ''}${pct.toFixed(2)}%) 开盘${open.toFixed(2)}${tagStr}`);
  }

  if (alerts.length > 0) {
    const header = `📊 集合竞价异动提醒 ${now.getHours()}:${String(now.getMinutes()).padStart(2,'0')}\n`;
    const body = alerts.join('\n');
    const detail = '\n\n📋 全量持仓状态：\n' + lines.join('\n');
    console.log('ALERT:' + header + body + detail);
  } else {
    const detail = '\n\n📋 全量持仓状态：\n' + lines.join('\n');
    console.log('OK: 暂无异动警报' + detail);
  }
}

main().catch(e => console.error('ERROR:' + e.message));
