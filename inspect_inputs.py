"""读取并校验项目原始资料，不生成业务判断。"""
from pathlib import Path
import csv,hashlib,json,zlib
import duckdb
import pyarrow.parquet as pq
ROOT=Path(__file__).resolve().parent

def rows(path):
    if path.suffix=='.csv':
        with path.open(encoding='utf-8',newline='') as f:
            return list(csv.DictReader(f))
    if path.suffix=='.jsonl':
        return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x]
    if path.suffix=='.parquet':
        return pq.read_table(path).to_pylist()
    value=json.loads(path.read_text(encoding='utf-8'))
    return value if isinstance(value,list) else [value]

def inspect():
    manifest=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
    result=[]
    for f in manifest['files']:
        path=ROOT/f['path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=f['sha256']:
            raise ValueError('文件校验不符：'+f['path'])
        parsed=rows(path)
        if len(parsed)!=f['rows']:
            raise ValueError('记录数量不符：'+f['path'])
        if path.suffix=='.parquet':
            with duckdb.connect() as db:
                amount=db.execute('select count(*) from read_parquet(?)',[str(path)]).fetchone()[0]
                if amount!=len(parsed):
                    raise ValueError('列存读取数量不符')
        result.append(dict(path=f['path'],rows=len(parsed),columns=f['columns']))
    binary=ROOT/'data/blocks.jsonl'
    if binary.exists():
        for row in rows(binary):
            data=(ROOT/'data'/row['file']).read_bytes()
            if hashlib.sha256(data).hexdigest()!=row['sha256'] or (zlib.crc32(data)&0xffffffff)!=row['crc32']:
                raise ValueError('二进制块校验不符：'+row['block'])
            if len(data)!=row['sample_count']*row['channel_count']*2:
                raise ValueError('二进制块尺寸不符：'+row['block'])
    return result

if __name__=='__main__':
    print(json.dumps(dict(raw_files=inspect(),scope='仅校验原件读取与完整性'),ensure_ascii=False,indent=2))
