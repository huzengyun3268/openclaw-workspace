/**
 * A股持仓综合技术分析报告 v3
 * 实时价格 + K线历史数据 + 多指标综合评分
 */
const http = require('http');
const { spawn } = require('child_process');

const PYTHON = 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python314\\python.exe';
const TA_SCRIPT = 'C:\\tools\\stock_analysis\\ta_analysis.py';

const stocks = [
  { code:'600352', name:'浙江龙盛', stoploss:12.0, cost:15.912 },
  { code:'600089', name:'特变电工', stoploss:25.0, cost:24.765 },
  { code:'300033', name:'同花顺', stoploss:280.0, cost:511.22 },
  { code:'920046', name:'亿能电力', stoploss:27.0, cost:35.936 },
  { code:'688295', name:'中复神鹰', stoploss:0, cost:49.193 },
  { code:'600487', name:'亨通光电', stoploss:0, cost:42.391 },
  { code:'600893', name:'航发动力', stoploss:0, cost:47.196 },
  { code:'601168', name:'西部矿业', stoploss:0, cost:24.863 },
  { code:'300499', name:'高澜股份', stoploss:0, cost:41.625 },
  { code:'600114', name:'东睦股份', stoploss:0, cost:26.44 },
  { code:'831330', name:'普适导航', stoploss:18.0, cost:20.415 },
  { code:'430046', name:'圣博润', stoploss:0.25, cost:0.478 },
];

function fetch(url) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const options = { hostname: u.hostname, path: u.pathname + u.search, headers: { 'Referer': 'http://quote.eastmoney.com', 'User-Agent': 'Mozilla/5.0' } };
    http.get(options, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function toSecid(code) {
  code = code + '';
  if (code.startsWith('6')) return '1.' + code;
  if (code.startsWith('0') || code.startsWith('3')) return '0.' + code;
  if (code.startsWith('4') || code.startsWith('8') || code.startsWith('9')) return '0.' + code;
  return '1.' + code;
}

async function getRealtimePrices() {
  const secids = stocks.map(s => toSecid(s.code)).join(',');
  const url = `http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f1,f2,f3,f12,f14&secids=${secids}&ut=fa5fd1943c7b386f172d6893dbfba10b`;
  const data = await fetch(url);
  try {
    const d = JSON.parse(data);
    const prices = {};
    if (d.data && d.data.diff) {
      d.data.diff.forEach(s => {
        if (s.f2 !== '-') {
          const code = String(s.f12).padStart(6, '0');
          prices[code] = { price: parseFloat(s.f2), change: parseFloat(s.f3) };
        }
      });
    }
    return prices;
  } catch(e) {
    console.error('价格获取失败:', e.message);
    return {};
  }
}

function runPython(script, code) {
  return new Promise((resolve) => {
    const py = spawn(PYTHON, [script, code]);
    let out = '';
    py.stdout.on('data', d => out += d.toString('utf8'));
    py.stderr.on('data', d => out += d.toString('utf8'));
    py.on('close', () => resolve(out));
    py.on('error', () => resolve(''));
  });
}

function parseScore(text) {
  const m = text.match(/综合评分: ([+-]?\d+\.\d+)分/);
  return m ? parseFloat(m[1]) : null;
}

function parseRec(text) {
  // 提取最后一行含"建议"的内容
  const lines = text.split('\n');
  const recLine = lines.reverse().find(l => l.includes('建议'));
  if (recLine) {
    const m = recLine.match(/建议[^\u0000-\u007f]*(.+)/);
    return m ? m[1].trim() : recLine.trim();
  }
  return '数据不足';
}

function em(code) {
  return '    ';
}

async function main() {
  console.log('正在获取实时行情...\n');
  const prices = await getRealtimePrices();

  console.log('正在获取技术分析（60日K线）...\n');
  const taResults = {};
  for (const s of stocks) {
    process.stdout.write(`  分析 ${s.name}...`);
    const ta = await runPython(TA_SCRIPT, s.code);
    taResults[s.code] = ta;
    console.log(' OK');
  }

  console.log('\n');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('  A股持仓技术分析报告');
  console.log('  ' + new Date().toLocaleString('zh-CN', {timeZone:'Asia/Shanghai'}));
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  for (const s of stocks) {
    const priceData = prices[s.code];
    const price = priceData ? priceData.price : null;
    const change = priceData ? priceData.change : null;
    const ta = taResults[s.code] || '';
    const score = parseScore(ta);
    const rec = parseRec(ta);

    // 涨跌符号
    const chgStr = change !== null ? (change >= 0 ? '+' : '') + change.toFixed(2) + '%' : 'N/A';
    const chgArrow = change !== null ? (change >= 0 ? '▲' : '▼') : '?';

    // 盈亏
    const pnl = price && s.cost ? (price - s.cost) / s.cost * 100 : null;
    const pnlStr = pnl !== null ? ((pnl >= 0 ? '盈利' : '亏损') + Math.abs(pnl).toFixed(1) + '%') : '';

    // 止损距
    const stopDist = price && s.stoploss ? ((s.stoploss - price) / price * 100).toFixed(1) + '%' : '';

    // 评分颜色
    const scoreColor = score === null ? '' : score >= 3 ? '[绿]' : score >= 1 ? '[黄]' : score >= -1 ? '[蓝]' : score >= -3 ? '[黄]' : '[红]';

    console.log(`【${s.name}(${s.code})】`);
    console.log(`  现价: ${price || 'N/A'} ${chgArrow}${chgStr}  |  ${pnlStr}  ${stopDist ? '|  距止损:' + stopDist : ''}`);
    console.log(`  技术评分: ${score !== null ? scoreColor + (score >= 0 ? '+' : '') + score.toFixed(1) + '分' : 'N/A'}`);
    console.log(`  建议: ${rec}`);
    console.log('  ' + '─'.repeat(44));
    console.log('');
  }

  console.log('⚠️ 分析仅供参考，不构成投资建议');
}

main().catch(console.error);
