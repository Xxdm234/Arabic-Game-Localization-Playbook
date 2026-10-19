"""Regression tests for the playbook tools. Run: python -X utf8 selftest.py
Needs: pillow fonttools arabic-reshaper python-bidi (the last two only as references)."""
import sys, os, re, tempfile, shutil
from pathlib import Path
CODE = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE))
ok = True
def t(name, cond):
    global ok
    print(('PASS ' if cond else 'FAIL ') + name)
    ok &= bool(cond)

from arabic_shaper import shape, glyphs_used
import arabic_reshaper
cfg = arabic_reshaper.ArabicReshaper(configuration={'delete_harakat': False,'support_ligatures': False})
for s in ['سلام عليكم يا صديقي','الآن','شيء جميل','مستشفى','إلى أين؟','لؤلؤ','مُعلِّم','ڤيديو چاي']:
    t('shape==reshaper '+s, shape(s, lam_alef=False) == cfg.reshape(s))
t('lam-alef', shape('لا') == '\uFEFB' and shape('ملا') == '\uFEE3\uFEFC')
t('harakat strip', '\u064B' not in shape('مرحباً', strip_harakat=True))
TOK = re.compile(r'\{[^}]*\}|\^\d')
s = shape('اسم^5ك', token_re=TOK, tokens_transparent=True)
t('transparent token keeps joining', s == '\uFE8D\uFEB3\uFEE4^5\uFEDA')
s2 = shape('اسم^5ك', token_re=TOK, tokens_transparent=False)
t('opaque token breaks joining', s2.endswith('^5\uFED9'))
t('tokens untouched', '{name}' in shape('هيا {name}!', token_re=TOK))

from rtl_layout import visual_line, layout, wrap_logical, pad_right_align, has_arabic
from bidi.algorithm import get_display
cfg2 = arabic_reshaper.ArabicReshaper(configuration={'delete_harakat': False,'support_ligatures': True,'ARABIC LIGATURE ALLAH':False,'ARABIC LIGATURE ALLAH ISOLATED FORM':False})
for s in ['مرحبا بك في اللعبة','الوقت 3:26 الآن','اضغط CTRL-F للبحث','لديك 20,000 ريال','قال (بهدوء): نعم','بطاقة MEMORY CARD 1 جاهزة']:
    t('visual==python-bidi '+s, visual_line(shape(s)) == get_display(cfg2.reshape(s), base_dir='R'))
t('percent sticks', '50%' in visual_line(shape('حصلت على 50% من الذهب')))
t('@ attaches', '@Name' in visual_line(shape('تعريب: @Name'), attach_prefix='@'))
m = lambda x: len(x) * 8
lines = wrap_logical('هذه جملة طويلة جدا يجب أن تلتف على أكثر من سطر واحد داخل صندوق الحوار الصغير', 160, lambda x: m(shape(x)))
t('wrap fits', all(m(shape(l)) <= 160 for l in lines) and len(lines) == 4)
t('wrap keeps words', ' '.join(lines).split() == 'هذه جملة طويلة جدا يجب أن تلتف على أكثر من سطر واحد داخل صندوق الحوار الصغير'.split())
out = layout('جملة طويلة تحتاج إلى أكثر من سطر واحد {name}', 120, m, token_re=TOK, line_sep='\xFF\x01')
t('layout tokens + sep', '{name}' in out and '\xFF\x01' in out)
# visual lines are reversed, so the sentence's first word sits reversed at the right end
t('first visual line = start of sentence', out.split('\xFF\x01')[0].endswith(shape('جملة')[::-1]))
p = pad_right_align(['ab', 'abcd'], lambda x: len(x), 6, '\uE000', 1)
t('pad', p == ['\uE000'*4 + 'ab', '\uE000'*2 + 'abcd'])
t('has_arabic letters only', has_arabic('نعم') and not has_arabic('What?؟'))

from token_guard import check, PROFILES, main as tg_main
pr = PROFILES['gamemaker'] + PROFILES['generic']
t('tg missing code', check('a', '* Hi/%', '* مرحبا/', pr))
t('tg clean', check('a', '* Hi ~1!/%', '* مرحبا ~1!/%', pr) == [])
t('tg digits', check('b', 'x60', 'x06', pr))
t('tg reserved', check('c', 'a', 'ب|', pr, forbidden='|'))
d = Path(tempfile.mkdtemp())
(d/'en.tsv').write_text('1\t* Hi^1!/%\n2\tYou got 60 coins./\n', encoding='utf-8')
(d/'ar.tsv').write_text('1\t* مرحبا^1!/%\n2\tحصلت على 06 قطعة./\n', encoding='utf-8')
t('tg cli exit 1 on problems', tg_main([str(d/'en.tsv'), str(d/'ar.tsv'), '--profile', 'gamemaker']) == 1)

from patch_tools import make_patch, apply_patch, patch_bytes, diff_ranges
a = b'A'*1000; b = bytearray(a); b[10:12] = b'BB'; b[50] = ord('C'); b += b'TAIL'
r = diff_ranges(a, bytes(b))
t('diff merge gap', r[0][0] == 10 and len(r) == 2)
(d/'o.bin').write_bytes(a); (d/'n.bin').write_bytes(bytes(b)); shutil.copy(d/'o.bin', d/'g.bin')
make_patch(d/'o.bin', d/'n.bin', d/'p.bin')
apply_patch(d/'p.bin', d/'g.bin')
t('patch roundtrip', (d/'g.bin').read_bytes() == bytes(b))
t('patch idempotent', apply_patch(d/'p.bin', d/'g.bin') == 'already-installed')
(d/'x.bin').write_bytes(b'Z'*1000)
try:
    apply_patch(d/'p.bin', d/'x.bin'); t('patch rejects unknown', False)
except RuntimeError:
    t('patch rejects unknown', (d/'x.bin').read_bytes() == b'Z'*1000)
(d/'e.bin').write_bytes(b'\x00\x01\x02\x03')
patch_bytes(d/'e.bin', 1, b'\x01\x02', b'\xAA\xBB')
t('patch_bytes', (d/'e.bin').read_bytes() == b'\x00\xAA\xBB\x03')
try:
    patch_bytes(d/'e.bin', 0, b'\x09', b'\x08'); t('patch_bytes guard', False)
except RuntimeError:
    t('patch_bytes guard', True)

from PIL import Image, ImageDraw
from image_guard import changed_outside, alpha_class
im = Image.new('RGBA', (40, 20), (5, 5, 5, 0)); im2 = im.copy()
im2.putpixel((30, 10), (6, 5, 5, 0))   # RGB change under alpha 0 outside region
t('image_guard sees RGB under alpha0', changed_outside(im, im2, [(0, 0, 20, 20)]) == 1)
t('alpha class', alpha_class(im) in ('opaque', 'binary', 'gradient'))

from save_guard import refuse_sandbox
try:
    refuse_sandbox(Path(r'C:\Users\x\AppData\Local\Packages\sandbox.abc\AC')); t('save_guard refuses sandbox', False)
except SystemExit:
    t('save_guard refuses sandbox', True)

from font_tools import coverage, assign_bank
FONT = os.environ.get('TEST_FONT', r'C:\Windows\Fonts\arial.ttf')   # any TTF with Arabic
if os.path.exists(FONT):
    t('font coverage runs', isinstance(coverage(FONT, set(shape('مرحبا لا'))), dict))
else:
    print('SKIP font coverage (set TEST_FONT)')
bank = assign_bank(['a', 'b', 'c'], used_bytes={0x80}, forbidden=(0xFE, 0xFF))
t('bank skips used', bank['a'] == 0x81)
shutil.rmtree(d)
print('ALL OK' if ok else 'SOME FAILED')
sys.exit(0 if ok else 1)
