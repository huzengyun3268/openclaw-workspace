import subprocess, os, json

workspace = r'C:\Users\Administrator\.openclaw\workspace'
clawhub = r'C:\npm-global\clawhub.cmd'

skills = [
    'subtitle',
    'ai-video-summarizer',
    'youtube-watcher',
    'image-ocr',
    'audio-editor',
    'podcast-generator',
    'voice-tts',
    'bilibili-youtube-watcher',
    'moss-tts-voice',
]

results = {}
for skill in skills:
    print(f'Installing {skill}...')
    result = subprocess.run(
        [clawhub, 'install', skill, '--workdir', workspace, '--no-input'],
        capture_output=True, text=True, cwd=workspace
    )
    out = (result.stdout + result.stderr)
    if result.returncode == 0:
        print(f'  OK: {skill}')
        results[skill] = 'OK'
    else:
        print(f'  FAIL: {skill} - {out[-200:]}')
        results[skill] = 'FAIL'

print('\n=== Summary ===')
for s, r in results.items():
    print(f'{s}: {r}')
