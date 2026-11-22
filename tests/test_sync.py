import sys,unittest,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import translate as t
from common import digest,signature,scan,load_state

class SyncTests(unittest.TestCase):
    def setUp(self):
        self.old={'en':'# Hello\n','ja':'# こんにちは\n','zh':'# 你好\n'}
        self.state={l:digest(s) for l,s in self.old.items()}
    def test_unchanged(self): self.assertIsNone(t.decision('home',self.old,self.state,lambda p:''))
    def test_source_any_language(self):
        for lang in self.old:
            self.assertEqual(t.decision('home',{**self.old,lang:'# Changed\n'},self.state,lambda p:'docs: change'),lang)
    def test_manual(self):
        self.assertEqual(t.decision('home',{**self.old,'ja':'# 修正\n'},self.state,lambda p:'【翻译错误】'),'manual')
    def test_new(self): self.assertEqual(t.decision('home',{'zh':'# 新页面\n'},{},lambda p:'new'),'zh')
    def test_conflict(self):
        with self.assertRaises(ValueError):t.decision('home',{**self.old,'en':'# A\n','zh':'# B\n'},self.state,lambda p:'normal')
    def test_protection(self):
        a='# Test\n\nUse `ros2` and [docs](https://example.org).\n\n```bash\nros2 topic list\n```\n'
        b=a.replace('Test','测试').replace('Use','使用')
        self.assertEqual(signature(a),signature(b))
        self.assertNotEqual(signature(a),signature(b.replace('ros2 topic list','ros2 topic echo')))
        self.assertNotEqual(signature(a),signature(b.replace('example.org','example.com')))
    def test_sync_mock_model(self):
        versions={**self.old,'zh':'# 新内容\n'}
        writes={}; calls=[]
        def fake_translator(text,src,dst,prev):
            calls.append((src,dst));return '# '+dst+' translated\n'
        with patch.object(t,'scan',return_value={'home':versions}),patch.object(t,'load_state',return_value={'home':self.state}),patch.object(t,'commit_message',return_value='change'),patch.object(t,'decision',side_effect=lambda ident,v,b:t.decision_original(ident,v,b,lambda p:'change')),patch.object(t,'write',side_effect=lambda p,s:writes.update({p.name:s})),patch.object(t,'dump'):
            t.synchronize(fake_translator)
        self.assertEqual(calls,[('zh','en'),('zh','ja')]);self.assertEqual(set(writes),{'en.md','ja.md'})
    def test_seed(self):
        self.assertIn('home',scan()); self.assertIsInstance(load_state(),dict)

# preserve unpatched function for integration test
t.decision_original=t.decision
if __name__=='__main__':unittest.main()
