# 原始资料约定

流量 m3，浓度 mg/L，负荷 kg=m3*mg/L/1000。时间 UTC，区间左闭右开。flow.parquet 是原始区间计量。
samples.jsonl：sample,point,start,end,mode,parent,custody；mode=grab/composite。grab 只证明采样时刻浓度，不自动代表区间。custody.csv 的 from/to/at/accepted 是连续实物交接。
assays.jsonl：assay,sample,analyte,method,unit,result_type,value,status,replace_assay,at。exact 是数值，below_limit 表示[0,value)，替代只作用于同污染物。mixing.csv 给出 in/out 区间与 attributed_m3，未覆盖部分不可外推。
permits.jsonl 的 window_hours 为连续滚动窗，浓度和负荷比较以可能范围判断；跨窗流量仅在有子区间观测时可拆。contracts.csv 指定每家工厂认可的取样点与方法。
mixing修订以相同进出范围整组替代旧归属，revision=2替代revision=1。并行未显式替代的有效分析项相异时是冲突，非平均取值。

所有名称与数值均为本地合成数据，不代表真实企业、监管结论或生态调查。data/catalog.json 保存文件哈希、原始行数与列；data/updates/ 为后到修订资料，可独立接收。JSON null 表示尚无该值，不与数值零等同；CSV保留原字符串，金额和数量应按十进制解释。来源身份相同且内容相同的重送不产生新业务事实，同身份版本不同内容需保留争议，除明确替代关系外不按到达顺序判定权威。
