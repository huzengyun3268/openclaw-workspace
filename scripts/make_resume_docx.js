const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require('docx');
const fs = require('fs');

const doc = new Document({
  sections: [{
    properties: {},
    children: [
      // Title
      new Paragraph({
        children: [
          new TextRun({ text: "胡仲翰 个人简历（海康微影版）", bold: true, size: 36 }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
      }),
      
      // Contact
      new Paragraph({
        children: [
          new TextRun({ text: "📧 huzhonghan4@gmail.com  |  📱 13357639369  |  24岁", size: 22 }),
        ],
        alignment: AlignmentType.CENTER,
        spacing: { after: 300 },
      }),

      // Section: 求职意向
      new Paragraph({ children: [new TextRun({ text: "求职意向", bold: true, size: 28, color: "2563EB" })], spacing: { before: 200, after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "海康微影—海外营销推广专员 / 海外市场运营（应届硕士）", size: 24 })], spacing: { after: 300 } }),

      // Section: 核心优势
      new Paragraph({ children: [new TextRun({ text: "核心优势", bold: true, size: 28, color: "2563EB" })], spacing: { before: 200, after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "▶ 英语+海外业务能力（核心竞争力）", bold: true, size: 24 })], spacing: { before: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 雅思 7.0 | 六级 528 分，全英文授课环境，熟悉海外商务沟通规范", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 可无障碍完成英文商务邮件撰写、海外客户对接、KOL洽谈及英文汇报演示", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 海外独立站运营经验：Shopify全英文建站、SEO优化、Facebook英文社媒运营", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 硕士阶段系统掌握海外市场调研、跨境数字营销、品牌全球化专业知识", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "▶ 实战经验", bold: true, size: 24 })], spacing: { before: 150, after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 独立负责全英文独立站搭建，3个月海外自然流量提升3000+", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 对接15+海外KOL，独立完成英文合作洽谈，转化率20-30%", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 海外市场调研项目全程英文对接客户与导师，输出专业英文分析报告", size: 22 })], spacing: { after: 300 } }),

      // Section: 教育背景
      new Paragraph({ children: [new TextRun({ text: "教育背景", bold: true, size: 28, color: "2563EB" })], spacing: { before: 200, after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "布里斯托大学（QS55）| 市场营销硕士 | 2024.09 - 应届（可全职入职）", bold: true, size: 24 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 全英文授课，主修跨境数字营销、海外市场调研、品牌全球化运营", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 市场营销学士（浙江财经大学，GPA 4.0/5.0，专业前5%）", size: 22 })], spacing: { after: 300 } }),

      // Section: 工作经历
      new Paragraph({ children: [new TextRun({ text: "工作经历", bold: true, size: 28, color: "2563EB" })], spacing: { before: 200, after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "星盘启航 | 独立站运营助理 | 2023.09-2024.01", bold: true, size: 24 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 独立负责全英文独立站（Shopify）搭建与优化，以英文完成产品详情页、落地页撰写，3个月海外自然流量提升3000+", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 以英文对接15+海外垂直领域KOL，独立完成合作洽谈与效果跟进，转化率20-30%，带来精准海外流量", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 负责Facebook等海外社媒全英文运营，发布英文产品推广内容，搭建海外用户触达渠道，提升品牌海外曝光", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "国泰君安 | 销售助理 | 2022.06-2022.09", bold: true, size: 24 })], spacing: { before: 150, after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 协助完成30+客户开户对接与需求沟通，促成4位客户首次投资，锻炼商务沟通与客户维护能力", size: 22 })], spacing: { after: 300 } }),

      // Section: 项目经历
      new Paragraph({ children: [new TextRun({ text: "项目经历", bold: true, size: 28, color: "2563EB" })], spacing: { before: 200, after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "Equi-scotia 海外市场调研微实习 | 项目负责人", bold: true, size: 24 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 全程英文对接海外客户与导师，牵头完成海外市场需求调研，独立撰写专业英文分析报告", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "海外独立站创建与优化项目 | 独立负责人", bold: true, size: 24 })], spacing: { before: 150, after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 独立完成Shopify全英文独立站搭建，配置支付链路，开展SEO优化，提升海外搜索引擎排名", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "蓝创集市校园创业营销项目 | 团队负责人", bold: true, size: 24 })], spacing: { before: 150, after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 带领团队完成选品、定价、线上线下推广全流程，304家商铺中销售额第二名", size: 22 })], spacing: { after: 300 } }),

      // Section: 技能证书
      new Paragraph({ children: [new TextRun({ text: "技能证书", bold: true, size: 28, color: "2563EB" })], spacing: { before: 200, after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 英语：雅思 7.0 | 六级 528（可英文工作）", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 工具：Google Analytics、Shopify、SPSS、PS/LR、Office", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 专业：独立站运营、Facebook社媒营销、海外SEO优化、跨境营销策划", size: 22 })], spacing: { after: 300 } }),

      // Section: 投递备注
      new Paragraph({ children: [new TextRun({ text: "投递备注（给HR看）", bold: true, size: 28, color: "2563EB" })], spacing: { before: 200, after: 100 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 布里斯托大学QS55硕士，英语可作为工作语言，适合海外市场拓展岗位", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 有独立站全英文运营及海外KOL对接经验，对安防/物联网企业出海业务有强烈兴趣", size: 22 })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: "  • 雅思7.0，已毕业可立即全职入职", size: 22 })], spacing: { after: 200 } }),
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync('C:\\Users\\Administrator\\.openclaw\\workspace\\胡仲翰_简历_海康微影.docx', buffer);
  console.log('OK - 文件已生成');
}).catch(err => {
  console.error('Error:', err.message);
});
