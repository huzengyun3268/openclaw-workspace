const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require('docx');

const files = [
    { md: 'resume_京东_跨境电商运营.md', name: '京东_跨境电商运营' },
    { md: 'resume_字节_TikTok运营.md', name: '字节_TikTok运营' },
    { md: 'resume_网易_运营实习生.md', name: '网易_运营实习生' },
    { md: 'resume_亚马逊_卖家支持.md', name: '亚马逊_卖家支持' }
];

function parseMarkdownToDocxSections(mdContent) {
    const lines = mdContent.split('\n');
    const sections = [];
    let currentSection = { type: 'paragraph', content: [] };
    
    for (let line of lines) {
        line = line.trim();
        if (!line) continue;
        
        if (line.startsWith('# ')) {
            sections.push({ type: 'title', content: line.replace('# ', '') });
        } else if (line.startsWith('## ')) {
            sections.push({ type: 'heading1', content: line.replace('## ', '') });
        } else if (line.startsWith('### ')) {
            sections.push({ type: 'heading2', content: line.replace('### ', '') });
        } else if (line.startsWith('- ') || line.startsWith('● ')) {
            const text = line.replace(/^[●\-]\s*/, '').replace(/\*\*/g, '');
            sections.push({ type: 'bullet', content: text });
        } else if (line.startsWith('|')) {
            // 表格行 - 跳过
        } else {
            const text = line.replace(/\*\*/g, '');
            if (text) sections.push({ type: 'paragraph', content: text });
        }
    }
    return sections;
}

function createDocxFromSections(sections) {
    const children = [];
    
    for (const section of sections) {
        if (section.type === 'title') {
            children.push(
                new Paragraph({
                    children: [new TextRun({ text: section.content, bold: true, size: 44 })],
                    alignment: AlignmentType.CENTER,
                    spacing: { after: 200 }
                })
            );
        } else if (section.type === 'heading1') {
            children.push(
                new Paragraph({
                    text: section.content,
                    heading: HeadingLevel.HEADING_1,
                    spacing: { before: 400, after: 200 },
                    border: { bottom: { color: '333333', space: 10, value: 'single', size: 6 } }
                })
            );
        } else if (section.type === 'heading2') {
            children.push(
                new Paragraph({
                    text: section.content,
                    heading: HeadingLevel.HEADING_2,
                    spacing: { before: 200, after: 100 }
                })
            );
        } else if (section.type === 'bullet') {
            children.push(
                new Paragraph({
                    text: section.content,
                    bullet: { level: 0 },
                    spacing: { after: 50 }
                })
            );
        } else if (section.type === 'paragraph') {
            children.push(
                new Paragraph({
                    text: section.content,
                    spacing: { after: 100 }
                })
            );
        }
    }
    
    return new Document({
        sections: [{ children }]
    });
}

async function convert() {
    for (const file of files) {
        const mdPath = path.join(__dirname, file.md);
        let mdContent = fs.readFileSync(mdPath, 'utf8');
        
        // 去除AI痕迹
        mdContent = mdContent.replace(/✅/g, '●');
        mdContent = mdContent.replace(/📧/g, 'Email: ');
        mdContent = mdContent.replace(/📱/g, 'Tel: ');
        
        const sections = parseMarkdownToDocxSections(mdContent);
        const doc = createDocxFromSections(sections);
        
        // 保存docx
        const docxPath = path.join(__dirname, file.name + '.docx');
        await Packer.toBuffer(doc).then(buffer => {
            fs.writeFileSync(docxPath, buffer);
        });
        console.log('Created:', file.name + '.docx');
        
        // 保存HTML（可打印为PDF）
        let htmlContent = mdContent
            .replace(/^# (.*$)/gm, '<h1>$1</h1>')
            .replace(/^## (.*$)/gm, '<h2>$1</h2>')
            .replace(/^### (.*$)/gm, '<h3>$1</h3>')
            .replace(/^- (.*$)/gm, '<li>$1</li>')
            .replace(/^● (.*$)/gm, '<li>$1</li>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/---/g, '<hr>');
        
        const html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>${file.name}</title>
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 40px; font-size: 11pt; line-height: 1.6; max-width: 800px; }
        h1 { font-size: 20pt; text-align: center; margin-bottom: 10px; }
        h2 { font-size: 14pt; border-bottom: 1px solid #666; padding-bottom: 5px; margin-top: 25px; color: #333; }
        h3 { font-size: 12pt; color: #555; margin-top: 15px; }
        p { margin: 8px 0; }
        li { margin: 5px 0; margin-left: 20px; }
        hr { border: none; border-top: 1px solid #ccc; margin: 20px 0; }
        strong { color: #000; }
    </style>
</head>
<body>
${htmlContent}
</body>
</html>`;
        
        const htmlPath = path.join(__dirname, file.name + '.html');
        fs.writeFileSync(htmlPath, html);
        console.log('Created:', file.name + '.html');
    }
    console.log('\\n✅ 完成！');
    console.log('使用方法：');
    console.log('1. .docx 文件 - 直接用Word打开');
    console.log('2. .html 文件 - 用浏览器打开 -> 打印 -> 另存为PDF');
}

convert().catch(console.error);
