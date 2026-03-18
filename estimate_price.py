# -*- coding: utf-8 -*-
import pandas as pd

# 2024年浙江土建定额参考单价（元）
# 来源：浙江省建设工程造价信息网参考价
DINGE_PRICES = {
    # 混凝土 (C30商品混凝土)
    '混凝土': 580,
    
    # 钢筋
    '钢筋': 4800,
    '螺纹钢': 5100,
    
    # 砌块
    '砌块': 280,
    '加气混凝土砌块': 320,
    '页岩多孔砖': 380,
    
    # 水泥
    '水泥': 480,
    
    # 砂石
    '砂': 120,
    '石子': 95,
    
    # 模板
    '模板': 45,
    '木模板': 38,
    
    # 脚手架
    '脚手架': 28,
    
    # 人工费（综合工日）
    '人工': 135,
}

# 常见项目单价估算（综合单价，包含人工+材料+机械+管理费+利润）
ESTIMATED_PRICES = {
    # 混凝土工程
    '基础': 680,  # C30混凝土基础
    '柱': 720,    # C30混凝土柱
    '梁': 695,    # C30混凝土梁
    '板': 665,    # C30混凝土板
    '墙': 750,    # 剪力墙
    '楼梯': 680,
    '构造柱': 650,
    
    # 钢筋工程
    '钢筋': 5800,  # 含绑扎
    
    # 砌体工程
    '砌筑': 380,   # 砌体墙
    '砌块': 320,
    
    # 模板工程
    '模板': 58,    # 模板接触面积
    
    # 脚手架
    '脚手架': 35,  # 建筑面积
    
    # 装修
    '抹灰': 28,
    '墙面': 45,
    '地面': 35,
    '天棚': 32,
    '涂料': 18,
    '防水': 32,
    
    # 默认
    'default': 350,
}

def estimate_price(item_name):
    """根据项目名称估算综合单价"""
    name = item_name.lower() if isinstance(item_name, str) else ''
    
    # 混凝土相关
    if '混凝土' in name or any(x in name for x in ['柱', '梁', '板', '墙', '基础']):
        if '基础' in name:
            return ESTIMATED_PRICES['基础']
        elif '柱' in name:
            return ESTIMATED_PRICES['柱']
        elif '梁' in name:
            return ESTIMATED_PRICES['梁']
        elif '板' in name:
            return ESTIMATED_PRICES['板']
        elif '墙' in name:
            return ESTIMATED_PRICES['墙']
    
    # 钢筋
    if '钢筋' in name:
        return ESTIMATED_PRICES['钢筋']
    
    # 砌体
    if '砌' in name:
        return ESTIMATED_PRICES['砌筑']
    
    # 模板
    if '模板' in name or '模扳' in name:
        return ESTIMATED_PRICES['模板']
    
    # 脚手架
    if '脚手架' in name or '脚手扳' in name:
        return ESTIMATED_PRICES['脚手架']
    
    # 抹灰
    if '抹灰' in name or '粉刷' in name:
        return ESTIMATED_PRICES['抹灰']
    
    # 墙面
    if '墙面' in name or '墙饰面' in name:
        return ESTIMATED_PRICES['墙面']
    
    # 地面
    if '地面' in name or '楼地面' in name:
        return ESTIMATED_PRICES['地面']
    
    # 天棚
    if '天棚' in name or '吊顶' in name:
        return ESTIMATED_PRICES['天棚']
    
    # 防水
    if '防水' in name or '防潮' in name:
        return ESTIMATED_PRICES['防水']
    
    # 涂料
    if '涂料' in name or '油漆' in name or '乳胶漆' in name:
        return ESTIMATED_PRICES['涂料']
    
    return ESTIMATED_PRICES['default']

# Read Excel
df = pd.read_excel('5.xlsx', sheet_name=0, header=None)

# Extract items
items = []
for i in range(len(df)):
    row = df.iloc[i]
    col0 = str(row[0]).strip() if pd.notna(row[0]) else ''
    if col0.isdigit():
        try:
            code = str(row[1]) if pd.notna(row[1]) else ''
            name = str(row[2]) if pd.notna(row[2]) else ''
            unit = str(row[4]) if pd.notna(row[4]) else ''
            
            try:
                qty = float(row[5]) if pd.notna(row[5]) else 0
            except:
                qty = 0
            
            if name and qty > 0:
                # 估算单价
                unit_price = estimate_price(name)
                total = qty * unit_price
                
                items.append({
                    '序号': int(col0),
                    '项目编码': code,
                    '项目名称': name[:50],
                    '单位': unit,
                    '工程量': qty,
                    '估算单价': unit_price,
                    '估算合价': total
                })
        except:
            pass

df_items = pd.DataFrame(items)

# Calculate totals
total_qty = df_items['工程量'].sum()
total_price = df_items['估算合价'].sum()

print("=" * 70)
print("台州府城集散中心 - 土建工程清单 (定额估算)")
print("=" * 70)
print(f"总清单项目数: {len(df_items)}")
print(f"\n工程量总计: {total_qty:,.2f}")
print(f"估算总价: {total_price:,.2f} 元")
print(f"大写: {int(total_price)}元")

# 按类别汇总
def get_category(name):
    if '柱' in name: return '混凝土柱'
    elif '梁' in name: return '混凝土梁'
    elif '板' in name: return '混凝土板'
    elif '墙' in name: return '混凝土墙'
    elif '基础' in name: return '混凝土基础'
    elif '钢筋' in name: return '钢筋工程'
    elif '砌' in name: return '砌体工程'
    elif '模板' in name: return '模板工程'
    elif '脚手架' in name: return '脚手架'
    elif any(x in name for x in ['抹灰', '粉刷', '墙面', '涂料']): return '装饰工程'
    else: return '其他'

df_items['类别'] = df_items['项目名称'].apply(get_category)

print("\n" + "=" * 70)
print("按类别汇总")
print("=" * 70)
cat_sum = df_items.groupby('类别').agg({
    '工程量': 'sum',
    '估算合价': 'sum',
    '序号': 'count'
}).rename(columns={'序号': '项数'})
cat_sum = cat_sum.sort_values('估算合价', ascending=False)
print(cat_sum.to_string())

# Top 30 items
print("\n" + "=" * 70)
print("前30项清单")
print("=" * 70)
top = df_items.nlargest(30, '估算合价')
for _, r in top.iterrows():
    print(f"{r['序号']:3d}. {r['项目名称'][:25]:25s} {r['单位']:4s} {r['工程量']:10,.2f} {r['估算单价']:8,.0f} {r['估算合价']:12,.0f}")

# Save to Excel
output_file = '台州府城_清单_定额估算.xlsx'
df_items.to_excel(output_file, index=False)

print(f"\n已保存: {output_file}")
