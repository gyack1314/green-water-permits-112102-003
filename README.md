# 排水混合区间与实验室复检协同入仓

流量段、样品交接、实验室分析项与排水许可资料。所有资料均为合成，可离线使用。

## 本地环境

使用 Python 3.11，依赖版本在 requirements.txt，可在隔离虚拟环境安装：

    python3 -m venv .venv
    . .venv/bin/activate
    python3 -m pip install -r requirements.txt

## 资料读取

字段含义见 docs/input-contract.md，文件目录与校验值见 data/catalog.json。原始数据不包含已算好的业务结果。

    python3 inspect_inputs.py
    python3 -m unittest discover -s tests -v

inspect_inputs.py 只检查原件哈希与格式，Parquet同时经PyArrow和DuckDB读取。测试核对原件完整性及明确引用，成功仅说明资料可读取，不证明业务入仓、核算、资格或发布已实现。业务处理命令尚未登记。
