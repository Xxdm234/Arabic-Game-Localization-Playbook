# تحديد المحرك واختيار الملف المناسب

حدّد المحرك من **التواقيع والبنية** لا من اسم اللعبة أو الامتداد. ثم افتح ملفه. وإن لم يكن محركك هنا، فاقرأ الأقرب إليه واتبع `02_WORKFLOW.md` حرفيًا.

## 1. علامات التعرّف

| ما تراه في مجلد اللعبة | المحرك المرجّح | الملف |
|---|---|---|
| `Game.exe` + `Game.rgssad`/`.rgss3a` + `Data/*.rxdata` أو `Scripts.rxdata`، أو `mkxp.json` | RPG Maker XP/VX/VXA (RGSS) أو mkxp | [RPG_MAKER.md](RPG_MAKER.md) |
| `www/` + `js/rpg_*.js` + `data/*.json` (أو APK فيه `assets/www`) | RPG Maker MV/MZ | [RPG_MAKER.md](RPG_MAKER.md) (قسم MV/MZ) |
| `data.win` / `game.droid` / `options.ini` + `lang/*.json` | GameMaker | [GAMEMAKER.md](GAMEMAKER.md) |
| `*_Data/` + `UnityPlayer.dll` + `Managed/Assembly-CSharp.dll` | Unity | [UNITY.md](UNITY.md) |
| `*.dll` .NET + `Content/*.xnb` + MonoGame/FNA | MonoGame/XNA/.NET | [MONOGAME_DOTNET.md](MONOGAME_DOTNET.md) |
| `*.pak` بتوقيع KAPL + `audio/speech.info` + `localization/uiText.info` | LucasArts Special Edition (MI1/MI2 SE) | [SCUMM_SCUMMVM.md](SCUMM_SCUMMVM.md) |
| `*.000/*.001` (XOR 0x69) أو `*.LA0/LA1` + `RESOURCE/LANGUAGE.TAB` + `*.NUT` | SCUMM (classic / V8 عبر ScummVM) | [SCUMM_SCUMMVM.md](SCUMM_SCUMMVM.md) |
| `*.m4b`/`*.lab` بتوقيع LABN + `script.tab` + خطوط LAF | GrimE (EMI / Grim Fandango) | [GRIME_EMI.md](GRIME_EMI.md) |
| `Pack/*.ttarch` + `*.langdb` + `*.d3dtx` | Telltale Tool | [TELLTALE.md](TELLTALE.md) |
| `*.ggpack*` + `weird.dink` + `Text_en.tsv` | Dinky (Return to Monkey Island، Thimbleweed Park) | [DINKY.md](DINKY.md) |
| أرشيف خاص مشفّر (`resources.bin` ARC1)، أو ZIP بامتداد `.dat`، أو D3D11 + DirectXTK | محرك PC خاص (Square Enix ports) | [PROPRIETARY_PC.md](PROPRIETARY_PC.md) |
| صورة قرص `.bin/.cue` بنظام PS-X EXE (`SLUS_xxx.xx`) | PlayStation 1 | [PS1.md](PS1.md) |
| ISO بملف `SLUS_xxx.xx` ELF MIPS R5900 | PlayStation 2 | [PS2.md](PS2.md) |
| `.pkg` أو `CUSAxxxxx/` + `eboot.bin` + `sce_sys/` | حزمة PS4 (قد تحمل محاكي PS1/PS2 رسميًا) | [PS4_PACKAGES.md](PS4_PACKAGES.md) |
| `.apk` | أندرويد (.NET/MonoGame، GameMaker، RPG Maker WebView...) | [ANDROID.md](ANDROID.md) |

**أدوات التعرّف السريع:**

- التواقيع في أول البايتات: `RGSSAD` و`FORM` و`KAPL` و`LABN` و`ERTM` و`ANIM` و`DXTKfont` و`XNBd` و`KTX` و`DDS`.
- `strings` على الملف التنفيذي.
- قراءة ملف `*.json` للإعدادات.
- مقارنة نسخ اللغات الرسمية في مجلدات اللغة.

## 2. شجرة القرار العامة للاستراتيجية

```text
هل للمحرك نظام لغات أو mods رسمي يقبل لغة جديدة؟
├─ نعم → جرّب إضافة "ar"
│        ├─ هل تسلك "ar" مسارًا خاطئًا في الشيفرة (if lang=="en" else ياباني)؟ → استبدل لغة موجودة
│        └─ وإلا → أضف اللغة (Yuppie: properties، Freebird: Data/lang/ar)
└─ لا  → استبدل خانة لغة موجودة (الفرنسية غالبًا إن كانت الإنجليزية تتجاوز الترجمة)

هل يشكّل المحرك العربية ويرسم RTL؟
├─ نعم (نادر) → النص منطقي كما هو، واختبر الالتفاف والأرقام
└─ لا → هل تستطيع حقن كود وقت التشغيل (Harmony، BepInEx، DLL وكيل، سكربت روبي/Lua، كهف كود)؟
        ├─ نعم → الأفضل: نص منطقي في البيانات + تشكيل وقلب وقت التشغيل بعد الالتفاف
        │        (Yuppie، BBQ، Chrono Cross، Freebird draw_text)
        └─ لا  → شكّل واقلب وقت البناء، والتفّ أنت بالقياس، وأدخل فواصل الأسطر الصريحة للمحرك
                 (DELTARUNE، MI1–MI6، HM، WA، Chrono Trigger)

هل يحمل الخط العربية؟
├─ TTF يقرؤه المحرك → أضف الحروف إلى الخط أو سجّل خطًا احتياطيًا
└─ أطلس نقطي / بنك أحادي البايت → ابنِ الخانات (04_FONTS.md)
```

## 3. مقارنة سريعة بين المشاريع السابقة

| المشروع | المحرك | خانة اللغة | التشكيل والاتجاه | الخط | التوزيع |
|---|---|---|---|---|---|
| Yuppie Psycho | MonoGame/.NET 8 | `ar` جديدة (mod) | وقت التشغيل: Harmony على BitmapText | أطلس XNB موسّع | مشغّل + startup hook، وزرع Cecil للأندرويد |
| To the Moon / IF / Beach / ABS | RPG Maker XP (mkxp/RGSS1) | `Data/lang/ar` (Freebird)، أو استبدال | وقت التشغيل: `ArabicFont.rb` يعترض `draw_text` | Tahoma TTF | إعادة بناء Game.rgssad |
| DELTARUNE | GameMaker 2023 | استبدال الإنجليزية | البناء + ترقيع GML (`hspace` سالب) | أطلس من تعريب احترافي | data.win مرقّع، وAPK عبر منفذ قائم |
| ENA Dream BBQ | Unity 2021 + TMP + Yarn | جدول runtime لـYarn | البناء (reshape+bidi+reverse) + علم RTL | TMP fallback وقت التشغيل | إضافة BepInEx |
| Chrono Trigger PC | خاص (ARC1، TTF مشفر) | استبدال الإنجليزية | البناء + توائم PUA بتقارب سالب | TTF نقطي معدّل | `.ctar` + مثبت |
| Chrono Cross PC | خاص (DXTK، D3D11) | استبدال الإنجليزية | البناء (تشكيل) + ICU وقت التشغيل عبر DLL وكيل | SpriteFont موسّع | DLL + أرشيفات |
| MI1/MI2 SE | MISE/Monkey2.exe + SCUMM | الفرنسية | البناء + لف صريح | خطوط .font موسعة | ملفات سائبة + رقعة exe |
| MI3 | SCUMM V8 / ScummVM 2.0 | fr في LANGUAGE.TAB | البناء + FF01 + رقع سكربت | NUT | فروق بايتات + ملفات |
| MI4 | GrimE EMI / ScummVM daily | script.tab في datausr.m4b | البناء + رقعة التفاف في المشغل + Lua | LAF | مجلد بروابط + مشغّل معدّل |
| Tales | Telltale | english.langdb في نسخة الأرشيف | البناء + حشو محاذاة | DDS أطلس | فروق أمامية/عكسية + C# |
| RtMI | Dinky | عمود en | البناء + ⏎ ▫ + رقع ثوابت | TTF موسّعة | (لم يكتمل) |
| Harvest Moon | PS1 | استبدال | البناء | ورقة VRAM | صورة bin/cue + pkg |
| WA2 | PS1 classic على PS4 | استبدال | ترقيع R3000 للرسم | ورقة خط | مرقّع HTML + pkg |
| WA3/WA4/WA5/ACF | PS2 (PCSX2، PS2 classic على PS4) | استبدال | كهوف R5900 (محاذاة، وظهور من اليمين) + البناء | خانات كانا | فروق ISO + pkg + Lua |
