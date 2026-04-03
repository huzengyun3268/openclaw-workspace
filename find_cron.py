with open(r'C:\Users\Administrator\.openclaw\agents\main\sessions\sessions.json', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

patterns = ['cron', 'schedule', 'heartbeat', '持仓', 'monitor', 'trigger']
for pattern in patterns:
    idx = content.find(pattern)
    if idx >= 0:
        print(f'Found "{pattern}" at {idx}:')
        print(content[max(0,idx-50):idx+300])
        print('---')
