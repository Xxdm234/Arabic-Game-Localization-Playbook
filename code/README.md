# الأكواد المرجعية

أدوات بايثون صغيرة مستقلة، مأخوذة من دروس المشاريع السابقة وجُرّبت على عينات. انسخها إلى `tools/` في مشروعك وعدّلها بحسب رموز محركك. **ليست بديلًا عن فهم المحرك.** هي قطع بناء تختصر أخطاء معروفة.

**المتطلبات:** Python 3.10+، و`Pillow` و`fontTools` (لـ`image_guard` و`font_tools` فقط). أما `arabic_shaper` و`rtl_layout` و`token_guard` و`detectors` و`patch_tools` و`save_guard` فلا تحتاج مكتبات خارجية.

```bash
pip install pillow fonttools arabic-reshaper python-bidi
```

اكتب `export PYTHONIOENCODING=utf-8` (أو `python -X utf8`) قبل أي أمر يطبع عربية.

## 1. التشكيل — `arabic_shaper.py`

```python
import re
from arabic_shaper import shape, glyphs_used

TOK = re.compile(r'\{[^}]*\}|\\[A-Za-z]+\[[^\]]*\]|\^\d')   # رموز محركك
s = shape('اسم^5ك ورأى {name}!', token_re=TOK,
          tokens_transparent=True,   # وقفة داخل كلمة لا تقطع الوصل
          lam_alef=True,             # عطّله إن لم يكن للام ألف خانة في البنك
          strip_harakat=True)        # إن لم يحمل الخط الحركات
needed = glyphs_used([s])            # ما يجب أن يحمله بنك الخط
```

- مطابق لـ`arabic_reshaper` بلا ليغاتورات (12/12) ومع لام ألف (3/3) في الاختبار.
- يحفظ الحركات التي بين اللام والألف بدل أن يبتلعها (عيب Impostor Factory).
- يدعم ڤ وچ وڇ وپ وگ.

## 2. الاتجاه والالتفاف — `rtl_layout.py`

```python
from rtl_layout import layout, visual_line, wrap_logical, pad_right_align, has_arabic
from arabic_shaper import shape

# قياس بمقاييس خط اللعبة الحقيقية: هنا مثال بجدول تقدم لكل حرف
ADV = {}   # char -> pixels, اقرأه من ملف خط اللعبة المبني
def width(shaped: str) -> float:
    return sum(ADV.get(c, 8) for c in shaped)

engine_text = layout('جملة طويلة تحتاج إلى أكثر من سطر واحد', max_width=370,
                     measure_shaped=width, token_re=TOK,
                     shape_kw={'strip_harakat': True},
                     attach_prefix='@',            # «تعريب: @Name»
                     line_sep='\xFF\x01')          # فاصل المحرك (FF01 في SCUMM مثلًا)
```

- **اللف منطقي ومتوازن، ثم كل سطر يُشكَّل ويُقلب وحده.** والفقرة بدءًا من اليمين دائمًا.
- **المقاطع اللاتينية والأرقام** تبقى بترتيبها عبر الفواصل الداخلية («MEMORY CARD 1» و«3:26» و«CTRL-F» و«20,000»).
- **`%` و`+` و`-`** تلتصق بالرقم («50%» و«+25»). هذا قرار مقصود يخالف python-bidi في هاتين الحالتين (9/11 تطابق والباقيتان مقصودتان). عدّل `NUMBER_AFFIXES` إن أردت UBA القياسي.
- **مرايا الأقواس** مع «» ‹›. أضف الأقواس الصينية واليابانية إلى `MIRROR` إن استعملها نصك.
- **`pad_right_align`:** للمحركات التي تحاذي يسارًا فقط. استعمل حرف حشو شفافًا خاصًا لا المسافة.

## 3. حارس الرموز — `token_guard.py`

```bash
python token_guard.py source.tsv translated.tsv --profile gamemaker --forbidden "|~#="
```

يرصد ما يلي في كل سجل:

- رموز التحكم الناقصة أو الزائدة (أو تغيّر ترتيبها مع `--keep-order`).
- تغيّر عدد الأسطر (`\n` الحرفية).
- الأرقام المختلفة أو المقلوبة (يتجاهل الأرقام داخل الرموز).
- الأحرف المحجوزة لبنك الخط.
- تجاوز سعة الخانة بالبايت (عبر `check(..., max_bytes, encode)`).

يقسم السطر عند **أول** TAB، ويرفض المعرّف المكرر أو المجهول. أضف ملف تعريف لمحركك في `PROFILES`.

## 4. الكواشف — `detectors.py`

```bash
python detectors.py translated.tsv source.tsv
```

- **MIXED:** سطر فيه عربية وكلمات إنجليزية (أخطر من الإنجليزي كاملًا).
- **REVERSED?:** كلمة نادرة مقلوبها شائع، أي اتجاه تخزين خاطئ.
- **ENGLISH:** إنجليزي مرئي بقي بلا عربية.
- **DIGITS:** «06» مكان «60».

## 5. الرقع والتثبيت — `patch_tools.py`

```python
from pathlib import Path
from patch_tools import sha256, patch_bytes, make_patch, apply_patch

patch_bytes('work/runtime/Game.exe', 0x41F8C8,
            expected=bytes.fromhex('8B4508'), new=bytes.fromhex('8B450C'))  # يرفض أي نسخة أخرى
make_patch(Path('orig/data.bin'), Path('out/data.bin'), Path('release/data.arpatch'))
print(apply_patch(Path('release/data.arpatch'), Path('GameCopy/data.bin')))
```

- `patch_bytes` متساوي الطول، ولا يُطبَّق مرتين، ويتحقق من البايتات المتوقعة.
- `make_patch` و`apply_patch`:
  - نطاقات بدمج الفجوات ≤ 64 بايتًا.
  - manifest فيه بصمات المصدر والنتيجة والحمولة.
  - التثبيت: تحقق ← نسخة مؤقتة ← تحقق من النتيجة ← تبديل ذري، مع `.ar_old` للاستعادة.
  - يتعرف على «مثبّت من قبل».

## 6. حارس الصور — `image_guard.py`

```bash
python image_guard.py original.png edited.png "10,20,200,60" "300,40,380,70"
```

- يخرج 0 فقط إن لم يتغير أي بكسل خارج المناطق، في كل القنوات بما فيها RGB تحت الألفا الصفرية.
- يخرج 0 أيضًا إن لم تتغير فئة الشفافية (opaque، أو binary، أو gradient).

## 7. حارس الحفظ — `save_guard.py`

```bash
python save_guard.py snapshot "%LOCALAPPDATA%\DELTARUNE" backup\saves_20261019
#   ... شغّل الاختبار ...
python save_guard.py verify   "%LOCALAPPDATA%\DELTARUNE" backup\saves_20261019
python save_guard.py restore  "%LOCALAPPDATA%\DELTARUNE" backup\saves_20261019   # بإذن المستخدم فقط
```

يرفض المسارات المعزولة (`Packages/sandbox`)، ولا يكتب فوق نسخة احتياطية قديمة.

## 8. الخطوط — `font_tools.py`

```bash
python font_tools.py coverage Tajawal-Bold.ttf all_shaped_text.txt   # الناقص وبديله الأساسي
python font_tools.py sheet 12 compare.png NotoSansArabic.ttf Tajawal-Bold.ttf  # 1-بت بالحجم الحقيقي
```

```python
from font_tools import assign_bank
bank = assign_bank(sorted(needed_glyphs), used_bytes=ORIGINAL_BYTES,
                   forbidden=(0xFE, 0xFF), extra_free=(0x7C, 0x7E))
# احفظ bank في ملف بذرة، ولا تعِد ترتيبه بين البناءات
```

## 9. الاختبار الذاتي — `selftest.py`

```bash
python -X utf8 selftest.py          # 43 فحصًا، ويخرج 1 إن فشل أي منها
TEST_FONT=path/to/font.ttf python -X utf8 selftest.py   # خارج ويندوز
```

يقارن التشكيل بـ`arabic_reshaper`، والاتجاه بـ`python-bidi`. ويجرّب الالتفاف، وحارس الرموز، والرقع (ذهابًا وإيابًا، وعدم التكرار، ورفض الملف المجهول)، وحارس الصور، وحارس الحفظ، وبنك الخط. **شغّله بعد أي تعديل على هذه الأدوات.**

## سلسلة نموذجية لمحرك أحادي البايت بلا RTL

```text
trans/*.tsv (منطقي)
  → token_guard.py (رموز/أرقام/أسطر)
  → layout() لكل سجل بقياس خط اللعبة وفاصل المحرك
  → glyphs_used() → font_tools.assign_bank() (بذرة ثابتة) → بناء الخط
  → ترميز البايتات بالبنك → token_guard (سعة البايت) → كتابة الموارد
  → إعادة استخراج ومقارنة → detectors.py → اختبار داخل اللعبة
```
