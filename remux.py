import subprocess, os

src = r'C:\Users\Administrator\.openclaw\media\inbound\f5352c01-be92-4b17-a585-d704dcffa1c6.mp4'
dst = r'C:\Users\Administrator\Desktop\大浪坑泳纯净版.mp4'

result = subprocess.run([
    'ffmpeg', '-y', '-i', src,
    '-c:v', 'libx264', '-preset', 'fast', '-crf', '22',
    '-c:a', 'aac', '-b:a', '128k',
    '-movflags', '+faststart',
    dst
], capture_output=True)

print('Done')
print('Size:', os.path.getsize(dst) / 1024 / 1024, 'MB')
