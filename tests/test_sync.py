import io, json, sys, unittest, tempfile
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
    def test_responses_text(self):
        self.assertEqual(t.response_text({'output_text':'# Output'}),'# Output')
        data={'output':[{'content':[{'type':'output_text','text':'# First '},{'type':'output_text','text':'part'}]}]}
        self.assertEqual(t.response_text(data),'# First part')

    def test_responses_request(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self): return b'{"output_text":"# translated"}'
        with patch.dict(t.os.environ, {'LLM_API_URL':'https://example.test/v1/responses','LLM_API_KEY':'test-key','LLM_MODEL':'gpt-test','LLM_WIRE_API':'responses'}), patch.object(t.urllib.request,'urlopen',return_value=Response()) as open_url:
            self.assertEqual(t.llm('# Source','zh','en','# Previous'),'# translated\n')
        request=open_url.call_args.args[0]
        payload=json.loads(request.data.decode())
        self.assertEqual(request.full_url,'https://example.test/v1/responses')
        self.assertEqual(payload['model'],'gpt-test')
        self.assertFalse(payload['store'])
        self.assertIn('source_markdown',payload['input'])

    def test_http_error_includes_server_detail(self):
        error=t.urllib.error.HTTPError(
            'https://example.test/v1/responses',400,'Bad Request',{},
            io.BytesIO(b'{"error":{"message":"unsupported model"}}'))
        with patch.dict(t.os.environ, {'LLM_API_URL':'https://example.test/v1/responses','LLM_API_KEY':'test-key','LLM_MODEL':'gpt-test','LLM_WIRE_API':'responses'}), patch.object(t.urllib.request,'urlopen',side_effect=error):
            with self.assertRaisesRegex(RuntimeError,'HTTP 400.*unsupported model'):
                t.llm('# Source','zh','en','# Previous')
    def test_429_honors_retry_after(self):
        class Response:
            def __enter__(self): return self
            def __exit__(self,*args): return False
            def read(self): return b'{"output_text":"# translated"}'
        error=t.urllib.error.HTTPError(
            'https://example.test/v1/responses',429,'Too Many Requests',
            {'Retry-After':'0'},io.BytesIO(b'{"error":{"message":"busy"}}'))
        with patch.dict(t.os.environ, {'LLM_API_URL':'https://example.test/v1/responses','LLM_API_KEY':'test-key','LLM_MODEL':'gpt-test','LLM_WIRE_API':'responses'}), patch.object(t.urllib.request,'urlopen',side_effect=[error,Response()]) as open_url, patch.object(t.time,'sleep') as sleep:
            self.assertEqual(t.llm('# Source','zh','en','# Previous'),'# translated\n')
        self.assertEqual(open_url.call_count,2)
        sleep.assert_called_once_with(0.0)

    def test_429_stops_after_two_retries(self):
        def make_error():
            return t.urllib.error.HTTPError(
                'https://example.test/v1/responses',429,'Too Many Requests',
                {},io.BytesIO(b'{"error":{"message":"busy"}}'))
        with patch.dict(t.os.environ, {'LLM_API_URL':'https://example.test/v1/responses','LLM_API_KEY':'test-key','LLM_MODEL':'gpt-test','LLM_WIRE_API':'responses'}), patch.object(t.urllib.request,'urlopen',side_effect=[make_error(),make_error(),make_error()]) as open_url, patch.object(t.time,'sleep') as sleep:
            with self.assertRaisesRegex(RuntimeError,'HTTP 429.*busy'):
                t.llm('# Source','zh','en','# Previous')
        self.assertEqual(open_url.call_count,3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list],[1,2])

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
