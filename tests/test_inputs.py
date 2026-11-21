"""核对合成原件及显式跨文件引用。"""
import json,unittest
from inspect_inputs import ROOT,rows,inspect

class InputContractTests(unittest.TestCase):
    def test_original_files(self):
        self.assertGreater(len(inspect()),0)

    def test_declared_references(self):
        definitions=json.loads((ROOT/'docs/references.json').read_text(encoding='utf-8'))
        for relation in definitions:
            target={str(row[relation['target_key']]) for row in rows(ROOT/relation['target'])}
            for row in rows(ROOT/relation['source']):
                values=row.get(relation['source_key'])
                if values is None:
                    continue
                values=values if isinstance(values,list) else [values]
                for value in values:
                    with self.subTest(source=relation['source'],key=relation['source_key'],value=value):
                        self.assertIn(str(value),target)

if __name__=='__main__':
    unittest.main()
