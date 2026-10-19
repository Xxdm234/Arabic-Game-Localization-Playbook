# دليل تعريب الألعاب الاحترافي

هذا المجلد خلاصة مكتوبة لكل ما تعلّمناه من نحو عشرين مشروع تعريب ألعاب. شملت المشاريع ألعابًا على محركات PC مختلفة، وألعابًا تعمل بالمحاكاة (PS1 وPS2 وPS4 وأندرويد). مكتوب ليقرأه **نموذج ذكاء اصطناعي** فيتبع الخطوات الصحيحة من أول يوم، وليقرأه **المعرّب** فيعرف ما يطلب وكيف يراجع.

## كيف تستعمله؟

**أنت المعرّب:**

1. انسخ [`01_LOCALIZER_PROFILE.md`](01_LOCALIZER_PROFILE.md) إلى مجلد مشروعك باسم `LOCALIZER_PROFILE.md`، وغيّر الخيارات: اللهجة، والأرقام، والتشكيل، ونطاق الصور، وسطر التعريب، وطريقة الاختبار…
2. افتح جلسة مع أي نموذج والصق نص [`templates/SESSION_START_PROMPT.md`](templates/SESSION_START_PROMPT.md) بعد ملئه، أو قل له ببساطة: «اقرأ `<مسار الدليل>/Arabic-Game-Localization-Playbook/00_START_HERE_FOR_AI.md` ثم `LOCALIZER_PROFILE.md` وابدأ تعريب اللعبة في …».
3. القرارات التي تخصك (توحيد مصطلح، وتعريب الشعار، والخط النهائي) سيعرضها عليك النموذج بأرقام. سجّل قرارك في ملف الخيارات.

> **قبل الاستعمال أو النشر:** اقرأ [`DISCLAIMER.md`](DISCLAIMER.md). الدليل لنسختك النظامية فقط، وما يُنشر من التعريب ملف فروقات لا ملفات اللعبة.

**أنت النموذج:** ابدأ بـ[`00_START_HERE_FOR_AI.md`](00_START_HERE_FOR_AI.md)، ولا تتخطاه.

## المحتويات

| الملف | ما فيه |
|---|---|
| [`00_START_HERE_FOR_AI.md`](00_START_HERE_FOR_AI.md) | عقد العمل: المهمة، وترتيب القراءة، والقواعد التي لا تُكسر، ومفردات الحالة، وصيغة التقرير |
| [`01_LOCALIZER_PROFILE.md`](01_LOCALIZER_PROFILE.md) | **خيارات المعرّب** القابلة للتعديل، وشرح كل خيار |
| [`02_WORKFLOW.md`](02_WORKFLOW.md) | المراحل 0–13 وبوابة كل مرحلة |
| [`03_ARABIC_TEXT_ENGINEERING.md`](03_ARABIC_TEXT_ENGINEERING.md) | التشكيل، والاتجاه، والالتفاف، والمحاذاة، واتجاه التخزين، والقوالب، والرموز، والكتابة حرفًا حرفًا |
| [`04_FONTS.md`](04_FONTS.md) | الاختيار بالقياس، والرخص، وبنوك الخانات، والوصلات، والارتفاع، والطبقات |
| [`05_TRANSLATION_AND_EDITING.md`](05_TRANSLATION_AND_EDITING.md) | المستوى اللغوي، والأصوات، والنكات والألغاز، والجنس والعدد، والمسرد، والدفعات، والتدقيق |
| [`06_IMAGES_TEXTURES_VIDEO.md`](06_IMAGES_TEXTURES_VIDEO.md) | اكتشاف الكتابة في الصور، وطرق التعريب والحماية، والحاويات، والفيديو، وسطر المعرّب |
| [`07_TESTING_AND_EVIDENCE.md`](07_TESTING_AND_EVIDENCE.md) | العزل، وحماية الحفظ، والقيادة الآلية، والتجارب التشخيصية، وقائمة المعاينة، والأدلة |
| [`08_BUILD_PATCH_RELEASE.md`](08_BUILD_PATCH_RELEASE.md) | مبادئ البناء، واستراتيجيات الحقن، ورقع exe، وصيغ التوزيع، والمثبّت، والرخص |
| [`09_TOOLS_CATALOG.md`](09_TOOLS_CATALOG.md) | كل أداة ومكتبة استُعملت، ومزالق بيئة العمل |
| [`10_LESSONS_LEARNED.md`](10_LESSONS_LEARNED.md) | جداول «العرَض ← السبب ← القاعدة» من المشاريع كلها |
| [`11_DOCUMENTATION_AND_HANDOFF.md`](11_DOCUMENTATION_AND_HANDOFF.md) | نظام التوثيق، وملف البدء، والتسليم بين النماذج |
| [`engines/`](engines/README.md) | دليل لكل محرك ومنصة: RPG Maker، وGameMaker، وUnity، وMonoGame/.NET، وSCUMM/ScummVM، وGrimE، وTelltale، وDinky، ومحركات PC الخاصة، وPS1، وPS2، وPS4، وأندرويد |
| [`templates/`](templates/) | قوالب: AGENTS، وبدء الجلسة، وSKILLS، وPROGRESS، وSTYLE، والمسرد، والنكات، والتسليم، وتقرير الفحص، ومقال النشر، وطلب توليد الصور |
| [`DISCLAIMER.md`](DISCLAIMER.md) | إخلاء المسؤولية: عمل غير رسمي، ونسختك النظامية فقط، ونشر الفروقات فقط، وحدود قسم الحزم المزيفة |
| [`LICENSE.md`](LICENSE.md) | الرخصة: CC BY 4.0 للوثائق، وMIT للأكواد |
| [`code/`](code/README.md) | أدوات بايثون مجرّبة: التشكيل، والاتجاه والالتفاف، وحارس الرموز، والكواشف، والرقع والتثبيت، وحارس الصور، وحارس الحفظ، والخطوط، مع `selftest.py` (43 فحصًا) |

## المشاريع التي استُخلص منها الدليل

| المشروع | المحرك/المنصة |
|---|---|
| Yuppie Psycho (+Catechesis، +أندرويد) | MonoGame/.NET 8 |
| To the Moon، Impostor Factory، Beach Episode، A Bird Story | RPG Maker XP / mkxp |
| OMORI | RPG Maker MV (+APK) |
| DELTARUNE (5 فصول + أندرويد) | GameMaker |
| ENA: Dream BBQ | Unity + BepInEx |
| Chrono Trigger PC | محرك خاص (ARC1، TTF) |
| Chrono Cross PC (+Radical Dreamers) | DirectXTK/D3D11 |
| Monkey Island 1 SE، و2 SE، و3 Curse، و4 Escape، و5 Tales، و6 Return | SCUMM SE/classic، وScummVM V8، وGrimE، وTelltale، وDinky |
| Harvest Moon: Back to Nature | PS1 (+PS4 classic) |
| Wild Arms 2، 3، 4، 5، Alter Code F | PS1/PS2 + حزم PS4 |

## مبدأ واحد إن لم تقرأ غيره

> **المصدر العربي منطقي ونظيف. التفّ عليه بالقياس، ثم شكّل كل سطر واقلبه وقت البناء. احمِ الأصل وحفظ اللاعب. ولا تقل «أُصلح» قبل أن تراه داخل اللعبة ببصمة البناء نفسه.**

## الرخصة والمساهمة

- **الوثائق والقوالب:** [CC BY 4.0](LICENSE.md). انسخ وعدّل وانشر، واذكر المصدر: «دليل تعريب الألعاب الاحترافي — MXIAUDIO والمساهمون».
- **الأكواد في `code/`:** [MIT](code/LICENSE).
- **للمساهمة:** أضف دليل محرك جديدًا في `engines/` على نمط الملفات الموجودة، أو درسًا في `10_LESSONS_LEARNED.md` بصيغة «العرَض ← السبب ← القاعدة» مع اسم اللعبة. حدّث جدول المحتويات، وشغّل `python -X utf8 code/selftest.py` إن عدّلت الأكواد.

---

**English:** A practical Arabic game-localization playbook written for both AI agents and human localizers, distilled from ~20 real projects across PC engines (RPG Maker, GameMaker, Unity, MonoGame, SCUMM, GrimE, Telltale, Dinky, proprietary) and emulated platforms (PS1, PS2, PS4, Android). Agents start at [`AGENTS.md`](AGENTS.md). Unofficial; see [`DISCLAIMER.md`](DISCLAIMER.md). Docs CC BY 4.0, code MIT.
