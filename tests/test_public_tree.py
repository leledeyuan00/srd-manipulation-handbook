import sys, tempfile, unittest, shutil
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import common

class PublicTreeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ('content','assets','vendor','web'):
            shutil.copytree(common.ROOT/name, self.root/name)
        for key,value in [('ROOT',self.root),('CONTENT',self.root/'content')]:
            p=patch.object(common,key,value); p.start(); self.addCleanup(p.stop)

    def test_chapter_agent_not_published(self):
        pages=common.scan()
        self.assertIn('05_handbook_maintenance/index',pages)
        self.assertIn('04_lessons_learned/index',pages)
        self.assertNotIn('02_imitation_learning',pages)
        self.assertEqual(set(pages),set(common.load_state()))

    def test_removed_project_path_rejected(self):
        p=self.root/'content/04_daihen_project/index/en.md'
        p.parent.mkdir(parents=True); p.write_text('# Placeholder\n')
        with self.assertRaises(ValueError): common.scan()

    def test_unexpected_asset_rejected(self):
        (self.root/'assets/private-example.zip').write_bytes(b'dummy')
        with self.assertRaises(ValueError): common.scan()

    def test_symlink_rejected(self):
        target=self.root/'outside.png'; target.write_bytes(b'dummy')
        try: (self.root/'assets/example.png').symlink_to(target)
        except (OSError, NotImplementedError): self.skipTest('Symlink unavailable')
        with self.assertRaises(ValueError): common.scan()

    def test_unexpected_web_file_rejected(self):
        (self.root/'web/draft.txt').write_text('dummy')
        with self.assertRaises(ValueError): common.scan()

if __name__=='__main__': unittest.main()
