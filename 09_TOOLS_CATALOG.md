# دليل الأدوات: ما استُعمل فعلًا ولماذا

كل أداة هنا استُعملت في مشروع سابق. الأدوات مفتوحة المصدر يجوز تنزيلها بلا استئذان، إلا إذا منع ذلك ملف الخيارات. احفظ نسخة مثبتة الإصدار من كل أداة حاسمة داخل `reference/` أو `work/deps/` مع رخصتها، فقد تتغير الأداة لاحقًا.

## 1. مكتبات بايثون

| المكتبة | الاستعمال | ملاحظة |
|---|---|---|
| `Pillow` | الصور والمعاينات وأوراق المقارنة وعينات الخطوط | `getextrema` لا `getbbox` لمقارنة RGBA |
| `fontTools` | قراءة cmap وإضافة الحروف وحذف `GSUB/GPOS` وتعديل الخطوط المتغيرة | حمّل `gvar/HVAR` قبل الإضافة |
| `arabic-reshaper` | التشكيل للصور والدراسات | يحذف الحركات افتراضيًا. عطّل ليغاتورة لفظ الجلالة |
| `python-bidi` | `get_display(s, base_dir='R')` | يختلف في `%` و`+` عن قرارات المشاريع |
| `uharfbuzz` + `freetype-py` | رسم عالي الجودة للعناوين والشعارات | قسّم المقاطع حسب الاتجاه |
| `numpy` | مسح الملفات الكبيرة عن أنماط صور، وأقنعة | مجاميع تراكمية لإيجاد بطاقات الأماكن (ACF) |
| `lz4`، `zstandard` | XNB وLZ4 (MonoGame)، وحالات DuckStation | |
| `texture2ddecoder`، `etcpak` | فك BC/DXT وضغطه (MI1 وMI2) | ارفض تغيير الحجم |
| `ispc_texcomp` | ترميز BC7/BC3 (RtMI) | ثبّته داخل المشروع |
| `pycdlib` | قراءة ISO9660 (PS2) | |
| `capstone` | تفكيك MIPS (R5900) مع `skipdata=True` | بعض تعليمات R5900 لا تُفك |
| `rubymarshal` | قراءة Ruby Marshal | **كاتبه يكسر الملفات ذات الكائنات المشتركة**، فاكتب بروبي الحقيقي (Impostor Factory وA Bird Story) |
| `mymcplus` / `mymc++` | بطاقات ذاكرة PS2: إنشاء واستيراد `.max/.cbs/.xps/.psu` | الحفظ مرتبط باسم الخانة |
| `CTranslate2` + OPUS-MT `opus-mt-tc-big-en-ar` | مسودات ترجمة محلية على المعالج | `HF_HUB_OFFLINE=1`، ومسودة فقط |

## 2. أدوات .NET وWindows

| الأداة | الاستعمال |
|---|---|
| `ilspycmd` | فك تجميعات .NET إلى C# (Yuppie: 1073 ملفًا) |
| Lib.Harmony | ترقيع دوال .NET في الذاكرة (Yuppie وBBQ) |
| Mono.Cecil | زرع نداءات داخل التجميعة. يحفظ MVID ورموز الأنواع. انتبه لبيانات RVA في `<PrivateImplementationDetails>` |
| `DOTNET_STARTUP_HOOKS` | حقن طبقة في تطبيق .NET مستقل ذاتيًا عبر مشغّل (Yuppie) |
| BepInEx 5 | إضافات Unity Mono. الكائن المدير قد لا يستقبل `Update`، فأنشئ GameObject خاصًا (BBQ) |
| `csc` المرفق بـWindows | ترجمة مثبت C# 5 دون تثبيت SDK (Tales) |
| `PrintWindow` | التقاط نافذة واحدة. أسود مع Vulkan، وأحيانًا مع نافذة مخفية |
| `dotnet` SDK 8/10 | بناء الطبقات والأدوات. `rollForward: Major` لتشغيل أدوات .NET Core 3 على 8 |
| ICU (`icu.dll`) | `ubidi_*` وقت التشغيل (Chrono Cross) |
| `d3dcompiler_47.dll` | ترجمة shaders وقت التشغيل (Chrono Cross) |

## 3. أدوات المحركات والصيغ

| المحرك/اللعبة | الأداة | ملاحظة |
|---|---|---|
| GameMaker | **UndertaleModTool / UndertaleModCli** + سكربتات `.csx` | كل استدعاء CLI يحتاج `< /dev/null` وإلا تعلّق |
| RPG Maker XP/VX/MV | Translator++، RPGMakerDecrypter-cli، RGSS Extractor، RPGXP | Translator++ لا يدعم العربية افتراضيًا. البديل خط أنابيب بايثون/روبي خاص |
| SCUMM (MI1/MI2 classic) | **ScummTR** 0.5.1 + **ScummRP**، والمرجع `scummvm/engines/scumm` | تحتاج تشغيلًا خارج العزل على Windows |
| MI SE | MISETranslator، monkeySERepaker | قراءة KAPL والتعليمات المعروفة |
| SCUMM V8 / GrimE | مصدر ScummVM الرسمي للوسم المطابق للنسخة المرفقة | `reference/scummvm-<tag>` |
| ScummVM GUI | `devtools/create_translations` و`translations.dat` | حزمة واجهة عربية خاصة بالمشروع (MI3) |
| Telltale | telltale-explorer، TTG-Tools | مراجع للصيغ |
| Dinky (RtMI) | Dinky-Explorer | مفاتيح XOR تُستخرج من exe ولا تُنشر |
| PS4 pkg | **LibOrbisPkg / PkgTool.Core** (مبنية على .NET 8)، OpenOrbis toolchain | أصلح `PFSCReader.cs` (قراءة Deflate في حلقة). لا تبنِ من استخراج PFS مضغوط فاسد |
| PS2 | PCSX2 + **PINE**، mymcplus | `DumpReplaceableTextures` |
| PS1 | DuckStation + GDB stub، وأدوات PackBits/LZSS خاصة | إعادة حساب EDC/ECC للقطاعات |
| shadPS4 | تشغيل مجلد لعبة `-g eboot.bin`، ونسخة محمولة | بعض الإصدارات لا تشغّل محاكي PS2 المدمج |
| Chrono Cross PC | CrossFix (مرجع)، DirectXTK SpriteFont (مرجع الصيغة) | |
| Android | apktool/zip، `zipalign -p 16`، `apksigner` (v1+v2+v3)، `adb logcat` | احتفظ بالمفتاح |

## 4. أدوات كتبتها المشاريع: أعد استعمال أفكارها

| الأداة | الفكرة | المشروع |
|---|---|---|
| `flowdir.py`، `subargs.py`، `anchor.py`، `direction.py` | تحليل تدفق المفتاح إلى دالة الرسم، ومعايرة على مرساة | DELTARUNE |
| `validate.py`، `metrics.py glyphs/check` | رموز التحكم، وتغطية الخط، وعرض السطر بمقاييس اللعبة | DELTARUNE |
| `gaps/mixed/crossfill/digits/revwords/revlines.py` | كواشف إحصائية | DELTARUNE |
| `fixtext.py` | تصحيح يتحقق من النص القديم حرفيًا قبل الكتابة | DELTARUNE |
| `batch.py take/put/expand`، `memory.py fill/refresh/self` | دفعات بالمشهد، وذاكرة ترجمة دقيقة | DELTARUNE |
| `drive.ps1` | سكربت قيادة اللعبة ولقطات | DELTARUNE |
| `ship_audit.py`، `uncovered.py`، `validate_lang.py`، `verify_install.py` | فحص ما يُشحن فعلًا، ولا حوار خارج نظام الترجمة، وفحص داخل الأرشيف، ومقارنة كل مدخل | Freebird |
| `test_reshape.rb`، `test_paragraph.rb` | المشكّل الحقيقي على كل سطر، مع اختبار إفساد متعمد | Freebird |
| `proof.py`، `preview.py`، `check_layout.py`، `render.py` | راسم مطابق للمحرك | HM، Chrono Trigger، Yuppie |
| `fitcheck.py`، `conflicts.py`، `evtrefresh.py`، `livetext.py`، `bisect4.py` | السعة، وتعارض الترجمات، وتحديث حالة قديمة، والحقن الحي، والتنصيف | WA |
| `texscan.py`، `texfind.py`، `gsmem.py` | تفريغ كل قوام من حالة، وتتبع مصدر صورة | WA |
| `mkpatch.py`، `mkrelease.py`، `reltest.py`، `check_installer.py` | رقع وإصدارات واختبار مثبت | WA |
| `image_assets.py`، `til_layout.py` | استيراد صور مؤلفة إلى مناطق مسجلة مع حماية | MI4 |
| `seed_runtime_qa.py`، `restore_runtime_checkpoint.py` | بذور اختبار لا تتسرب إلى البناء | RtMI |
| `memscan.py` | مقارنة ذاكرة العملية بين حالتين لإيجاد قيمة | Chrono Cross |

## 5. الأدوات المرفقة بهذا الدليل (`code/`)

| الملف | ما يفعله |
|---|---|
| `arabic_shaper.py` | تشكيل بلا تبعيات، مع حماية الرموز وشفافيتها، ولام ألف، وحذف الحركات، وحروف ڤ چ پ گ. مطابق لـ`arabic_reshaper` في العينات المختبرة |
| `rtl_layout.py` | ترتيب بصري للسطر (مقاطع لاتينية وأرقام وأقواس وبادئة @)، ولف منطقي متوازن بالقياس، وخط أنابيب كامل، وحشو محاذاة |
| `token_guard.py` | مقارنة رموز التحكم والأرقام والأسطر والبايتات بين الأصل والترجمة، بملفات تعريف لمحركات |
| `detectors.py` | المختلط، والكلمات المقلوبة، والأرقام المقلوبة، والإنجليزية المتبقية |
| `patch_tools.py` | بصمات، ورقعة بايتات محروسة، ورقعة نطاقات مع manifest، وتثبيت ذري |
| `image_guard.py` | لا تغيير خارج المناطق، وفئة الشفافية |
| `save_guard.py` | لقطة الحفظ ببصمات، والتحقق، والاستعادة، ورفض مسارات sandbox |
| `font_tools.py` | تغطية الحروف، والبديل الأساسي، وورقة مقارنة 1-بت، وتخصيص بنك أحادي البايت |

راجع `code/README.md` لطريقة التشغيل.

## 6. أدوات بيئة العمل ومزالقها

- **أداة Bash وheredoc** تحوّل `\\` إلى `\`، وقد تكتب `\0` و`\x00` بايتات NUL حقيقية داخل ملفات بايثون، وتكسر `\r` في المسارات. **اكتب الكود والترجمات بأداة الكتابة أو التحرير، لا بـheredoc.** ولبايت حرفي استعمل `chr(92)` أو `bytes([0])`.
- **`PYTHONIOENCODING=utf-8`** أو `python -X utf8` لكل أمر يطبع عربية، فهو لا يورَّث بين استدعاءات Bash المنفصلة.
- **`open()` في بايثون على Windows** يحتاج `encoding='utf-8'`.
- **مسار العمل الطويل جدًا** يمنع تشغيل برامج Windows الأصلية من Git Bash ("path longer than allowed"). اعمل في مسار قصير.
- **MSVC يقرأ المصدر بترميز النظام:** لا تكتب حروفًا عربية داخل `L"..."`، بل `\uXXXX` (Chrono Cross).
- **`sed` على ملفات الترجمة الكبيرة** يستهلك السياق بإشعارات التغيير، وعلى ملفات رسم الخط بالـASCII art يقص أنماطًا مشتركة (HM). اكتب ملف تصحيح صغيرًا وادمجه.
- **graphify:** بعد تعديل الكود شغّل `graphify update .`. إن تعطّل مشغله فشغّل `python -X utf8 -m graphify update .`. استبعد مكتبات الطرف الثالث بـ`.graphifyignore`، فتقرير MI1 تضخّم إلى 309 آلاف عقدة بسبب مكتبات الترجمة الآلية.
