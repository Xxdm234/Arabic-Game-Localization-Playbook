# حزم PS4 (‏.pkg) وshadPS4 — للألعاب الكلاسيكية داخل محاكيات سوني

**مصدر الخبرة:** Harvest Moon: Back to Nature، وWild Arms 2 وAlter Code F و4 بنسخها على PS4.

> ⚠️ **اقرأ [`DISCLAIMER.md`](../DISCLAIMER.md) قبل هذا الملف.** ما فيه للنسخ التي تملكها نظاميًا وعلى جهازك أنت، ولا يُنشر فيه إلا ملف فروقات.

## الأدوات

- **LibOrbisPkg / PkgTool.Core:** بُنيت من المصدر على .NET 8.
  - **أصلح `PFSCReader.cs`:** ‏`DeflateStream.Read` لا يضمن قراءة الكتلة كاملة، فاقرأ في حلقة.
  - الأوامر:

```text
PkgTool.Core pkg_extract --passcode 0000…0 <pkg> <out>
PkgTool.Core pkg_extractentry <pkg> 11 sce_sys/param.sfo
PkgTool.Core pkg_makegp4 --passcode 0000…0 <pkg> pkgbuild/proj      (مرة واحدة)
PkgTool.Core pkg_build pkgbuild/proj/Project.gp4 pkgbuild/out
PkgTool.Core pkg_validate <pkg>
```

- **OpenOrbis toolchain:** فيه `PkgTool.Core.exe` لـWindows. أضف `"rollForward": "Major"` إلى runtimeconfig ليعمل على .NET 8.

## مصيدة: نظام الملفات الداخلي المضغوط

في حزمة Harvest Moon الأصلية كان الـPFS الداخلي مضغوطًا:

- `pkg_extract` سقط بـ`inode 0 is corrupt`.
- **`pkg_makegp4` لم يسقط بل كتب بيانات فاسدة بصمت:** 24 ملفًا من 126 بالحجم الصحيح ومحتوى خاطئ، منها القرص والبايوس.

كُشف ذلك بمقارنة البايوس ببصماته المعروفة ومطابقة ثلاث نسخ مستخرجة أخرى. **ابنِ من استخراج سليم، وتحقق بعد البناء:**

- `pkg_validate` (38 أو 39 فحصًا).
- فك الحزمة الناتجة ومقارنة كل ملف بمصدره، والمداخل التي ليست ملفات (`param.sfo` والأيقونات) بـ`pkg_extractentry`.

## محتوى الحزم الكلاسيكية

- **PS1 Classic:**
  - الأقراص في `uroot/data/*.bin`، أو `SIEA/data/*.BIN` المطابق للأصل.
  - الإعدادات في `config-title.txt` (مثل `--screenshot-dir` و`--show-game-ui=0`). **أعدها إلى أصلها قبل بناء الحزمة.**
- **PS2 Classic:**
  - `image/disc01.iso`، وسكربتات Lua في `scripts/*.lua` و`patches/*_config.lua`.
  - ومع PS2HD الأحدث: كود مترجم مسبقًا `aot/*.prx`.
  - **رقع exe** عبر `eeInsnReplace` في Lua، ولا تمس عناوين يخطّفها Lua الأصلي.
  - علّق `emuMediaPatch` إن لزم (WA3).
- **القرص داخل الحزمة قد يحمل ذيلًا** (`LIMG` بحجم 16 KB) يختلف به عن Redump. والمثبت يقبل الحجمين.

## الحزمة المزيفة (fake pkg)

> للجهاز الذي تملكه وعدّلته بنفسك وعلى مسؤوليتك. لا تُنشر الحزمة الكاملة لأنها تحمل ملفات اللعبة. انظر [`DISCLAIMER.md`](../DISCLAIMER.md) §4.

- **موقعة بمفتاح التصحيح،** فلا تعمل إلا على جهاز مكسور الحماية.
- **معرّف المحتوى والإصدار كما هما،** فتُركَّب فوق النسخة الإنجليزية.
- **فروق مقصودة توثَّق:**
  - الحجم أكبر، لأن LibOrbisPkg لا يضغط PFS.
  - `pkg_flags` مختلفة.
  - مداخل `PUBTOOLINFO` مختلفة.
  - رخصة مزيفة من معرّف المحتوى.
- **قل صراحة «لم تُختبر على جهاز فعلي»** إن لم تُختبر.
- **GoldHEN AFR** مسار بديل لم يُجرَّب.

## shadPS4

- **نسخة اختبار مستقلة** (`shad_test/shadPS4.exe` + مجلد `user` محمول)، فلا تمس إعدادات المستخدم في `%APPDATA%\shadPS4`.
- **التشغيل:** `shadPS4.exe -f false -g <folder>/eboot.bin`. والمجلد يجب أن يكون مفكوكًا بـ`pkg_makegp4`، فـ`uroot` بلا param.sfo يفشل بـ«Failed to get TITLE_ID».
- **النافذة خارج الشاشة** بـ`SetWindowPos` دون تفعيل. وPostMessage يصل.
- **`PrintWindow` يعطي أسود مع Vulkan.**
- **أول تشغيل:** نافذة «Save Migration»، تُضغط فيها «Do nothing» آليًا.
- **في محاكي PS1 من سوني:** START وSELECT نصفا لوحة اللمس، وOPTIONS تفتح قائمة المحاكي.
- **بعض الإصدارات لا تشغّل محاكي PS2 المدمج** (انهيار عند شعار PS2). لا تعتمد عليه، وأعد التجربة إذا حُدّث.
- **سجل المحاكي** `user/log/shad_log.txt` يظهر أسطر `e-Lua : eeInsnReplace(...)`، ومنه تتحقق من قبول Lua.
- **اختبار القرص الأصلي دون نسخه:** مجلد بروابط صلبة (`os.link` أو `cp -al`)، ثم احذف الروابط.

## مجلد الإصدار متعدد المنصات (Harvest Moon)

```text
README.html                دليل التثبيت بالعربية
PS4-pkg-for-console/       حزمة pkg
PS4-shadPS4/CUSAxxxxx/     مجلد اللعبة لمحاكي shadPS4
PS1-DuckStation/           صورة القرص المعرّبة .bin/.cue
controls/shadPS4/          default.ini و CUSAxxxxx.ini (المحاكي يقرأ أحدهما بحسب use_unified_input_config)
controls/DuckStation/      ملف تحكم مولّد من settings.ini الحي
```

أسماء المجلدات إنجليزية بلا مسافات.
