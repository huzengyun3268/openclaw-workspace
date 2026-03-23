const { execSync } = require('child_process');
try {
  const r = execSync('openclaw --version', { shell: true, encoding: 'utf8' });
  console.log('openclaw found:', r.trim());
} catch(e) {
  console.log('not found via shell=true');
}
try {
  const r = execSync('openclaw --version', { encoding: 'utf8' });
  console.log('openclaw found (no shell):', r.trim());
} catch(e) {
  console.log('not found via no shell:', e.message);
}
try {
  const r = execSync('cmd /c openclaw --version', { encoding: 'utf8' });
  console.log('openclaw found (cmd):', r.trim());
} catch(e) {
  console.log('not found via cmd:', e.message);
}
try {
  const r = execSync('"C:\\Users\\Administrator\\AppData\\Roaming\\npm\\openclaw.cmd" --version', { encoding: 'utf8' });
  console.log('openclaw.cmd found:', r.trim());
} catch(e) {
  console.log('not found openclaw.cmd:', e.message);
}
