# ملف خيارات المعرّب — عدّله أنت، والنموذج يلتزم به

هذا الملف هو المكان الذي يقرر فيه **المعرّب (أنت)** ما يريده هو لا ما يفترضه النموذج. انسخه إلى مجلد كل مشروع جديد باسم `LOCALIZER_PROFILE.md`، وغيّر القيم داخل الكتلة أدناه فقط.

**للنموذج:**
- اقرأ هذه الكتلة قبل أي عمل.
- كل قيمة فيها تتقدّم على افتراضات الدليل، إلا قواعد السلامة في `00` (القسم 3).
- القيمة `ask` تعني: اعرض الخيارات على المستخدم مع توصيتك وأرقامك، ثم انتظر قراره.
- إن غاب حقل فخذ الافتراضي المذكور بجانبه.
- إن غيّر المستخدم رأيه في المحادثة فحدّث هذا الملف وسجّل التاريخ.

```yaml
# ===================== المشروع =====================
project:
  game: "اسم اللعبة"
  platform: pc            # pc | ps1 | ps2 | ps4 | android | other
  store_or_build: "GOG / Steam / رقم البناء / رمز القرص (SLUS-...)"
  original_path: "مسار اللعبة الأصلية (للقراءة فقط)"
  work_root: "مسار مجلد المشروع، مثل projects/<game>_ar"
  previous_projects_to_learn_from: []   # مسارات مشاريع سابقة قريبة

# ===================== اللغة والأسلوب =====================
language:
  register: msa_light          # msa_light (فصحى معاصرة خفيفة، الافتراضي) | msa_formal | dialect_light
  character_dialects: allowed  # allowed | forbidden: لهجة خفيفة لشخصية لها لهجة في الأصل (راعي بقر، عصابة...)
  imitate_broken_english: by_structure  # by_structure (حذف أدوات، ضمير غائب) | never | by_spelling
  digits: western              # western 0123 (الافتراضي، أسلم مع الخطوط) | eastern ٠١٢٣ | eastern_in_prose
  comma: arabic                # arabic ، (الافتراضي) | latin , (إن كان الخط يفتقد ، أو أراد المعرّب توحيدًا)
  question_mark: arabic        # arabic ؟ | latin ?
  quotes: guillemets           # guillemets «» | ascii ""
  tashkeel: disambiguation_only  # none | disambiguation_only | full (فقط إن كان الخط يحملها واختُبرت)
  tanween_fatha: write_in_source  # يُكتب في المصدر دائمًا، ويُحذف وقت البناء إن لم يحمله الخط
  kashida: never               # never | column_fill_only | decorative
  player_address: masculine_singular  # masculine_singular | feminine | neutral_rephrase | per_character
  proper_names: transliterate  # transliterate | keep_latin
  descriptive_names: translate # translate | transliterate
  keep_latin: [HP, MP, TP, LV, EXP, ATK, DEF, "أزرار التحكم", "أسماء فريق العمل", "حقوق النشر"]
  profanity: preserve_intensity  # preserve_intensity | soften | censor_like_original
  jokes: adapt                 # adapt (تكييف يحفظ الآلية) | literal_with_note (غير مستحسن)
  spoiler_safety: strict       # لا تكشف صياغةٌ معلومةً قبل أوانها (جنس شخصية متنكرة مثلًا)

# ===================== مصدر الترجمة =====================
translation:
  method: human_authored       # human_authored | mt_draft_then_full_review | prior_translation_port
  mt_engine_allowed: local_only  # none | local_only (OPUS-MT/CTranslate2) | online (يتطلب إذنًا صريحًا)
  critical_keys_manual: true   # الألغاز والأكواد وأسماء الأغراض المطلوبة: يدويًا دائمًا بلا مسودة آلية
  reuse_policy: exact_source_and_context  # إعادة الاستخدام عند تطابق الأصل حرفيًا فقط
  prior_fan_translation: ask   # ask | use_as_style_reference | port_as_base | ignore

# ===================== النطاق =====================
scope:
  dialogue: all
  ui_menus: all
  hints_journal_documents: all
  item_names_descriptions: all
  credits: roles_translated_names_latin   # all_latin | roles_translated_names_latin | all
  images_with_text: important   # none | important | all
  logo: follow_official_precedent  # translate | keep | follow_official_precedent (اقتدِ بلغات اللعبة الرسمية)
  videos_burned_text: ask      # none | subtitles_only | burned_text | ask
  classic_mode: ask            # للألعاب ذات النمطين (Monkey Island SE)
  keep_english_selectable: ask # replace_slot (العربية تحل محل لغة) | add_language (إن دعم المحرك) | ask

# ===================== الخط =====================
font:
  preferred: [Tajawal, "Noto Sans Arabic", "Noto Naskh Arabic", "Noto Kufi Arabic", Cairo, Almarai, Amiri]
  pixel_fonts: ["Arabixel (تحقق من الرخصة)", "PixelAE (تحقق من الرخصة)", "Plain Pixel CC-BY 4.0 (مضاعفات 15px)"]
  choose_by: measurement_sheet # measurement_sheet (عيّنة بالحجم الحقيقي) | user_choice
  min_readable_px: 12
  licenses_allowed: [OFL, CC-BY]   # لا تُشحن خطوط النظام المملوكة (Tahoma/Segoe) داخل الحزمة

# ===================== الاختبار =====================
testing:
  windowed: true
  mute_game_only: true
  monitor: any                 # any | primary | secondary
  steal_focus: false
  renderer: hardware           # في المحاكيات: اختبر بما يلعب به المستخدم فعلًا
  user_saves: read_only        # read_only | allow_backup_and_restore
  may_use_users_saves_for_test_copies: true
  ask_user_to_play_and_report: last_resort   # last_resort | co_play_sessions

# ===================== التسليم =====================
delivery:
  package: diff_patch_with_installer  # diff_patch_with_installer | mod_folder | overlay_zip
  installer: auto              # powershell_winforms | csharp_exe | html_browser_patcher | cmd_scripts | auto
  uninstall: required
  guide_html_with_screenshots: true
  folder_names_ascii: true     # أسماء مجلدات الحزمة إنجليزية بلا مسافات (USB/FTP/المحاكيات)
  version_scheme: "v1.0"
  credit_line: ""   # اكتب سطرك، مثل "تعريب: @اسمك". إن بقي فارغًا يسألك النموذج ولا يخترع اسمًا
  credit_placement: title_or_main_menu         # title_or_main_menu | credits_only | none
  release_post: true           # مقال تعريف بالتعريب للنشر (قالب في templates/)

# ===================== التواصل والصلاحيات =====================
communication:
  report_language: ar
  code_comments_language: en   # أسماء الملفات والتعليقات داخل الشيفرة
  ask_only_for_decisions: true
  send_screenshots: important_only
permissions:
  download_open_tools: true    # GitHub والأدوات مفتوحة المصدر وخطوط OFL
  install_python_packages: true
  modify_original_game: false
  modify_user_saves: false
  change_system_settings: false
```

---

## شرح الخيارات المهمة ولماذا وُجدت

| الخيار | لماذا يهم | مثال من مشروع سابق |
|---|---|---|
| `digits` | خطوط كثيرة تفتقد الأرقام الهندية، وبعض المحركات تطبع الأرقام بنفسها | WA4: «٤٣٪» غير موجودة في الخط فكُتبت «43%». Chrono Trigger أعاد توجيه cmap للأرقام اللاتينية إلى رسوم ٠-٩ |
| `comma` | بعض الخطوط أو المشاريع وحّدت الفاصلة اللاتينية | DELTARUNE وحّد «,» في الفصول الخمسة، وMonkey Island استعمل «،» |
| `tashkeel` | خلية الخط الصغيرة لا تفصل الحركة عن النقطة، والحركة المفقودة تظهر مربعًا | DELTARUNE: لا حركة سوى تنوين الفتح |
| `kashida` | تملأ عرض الأعمدة، وإن غابت عن بنك الخط أوقفت البناء | المعرّب الاحترافي للفصل الأول من DELTARUNE استعملها 2266 مرة، وفي Tales أوقفت البناء |
| `keep_english_selectable` | قد تكون إضافة لغة جديدة خطأً قاتلًا | DELTARUNE: اختيار `ar` يسلك المسار الياباني في الشيفرة كلها، فاستُبدلت الإنجليزية. Monkey Island: خانة الفرنسية |
| `logo` | الشعار هوية، لكن لغات رسمية عرّبته | Impostor Factory: كان مستثنى، ثم ظهر أن الأوكرانية الرسمية عرّبته فعُرّب |
| `credits` | الاعتمادات سجلّ بأسماء أصحابها | قاعدة كل المشاريع: تُترجم الأدوار، وتبقى الأسماء لاتينية |
| `testing.renderer` | محاكي الاختبار برسم برمجي أخفى عيبًا لم يره إلا المستخدم | WA5: الرسم بالعتاد يُسقط عمود بكسل عند حافة كل حرف |
| `spoiler_safety` | الصياغة العربية تكشف الجنس والعدد | Tales: منشور «صائد القراصنة» بالمذكر عمدًا حتى لا يُكشف أن مورغان امرأة |
| `prior_fan_translation` | تعريب قديم احترافي مرجعٌ ومجموعةُ اختبار | DELTARUNE: الفصل الأول الاحترافي صار المرساة لكل قواعد الاتجاه. Chrono Trigger: نُقل تعريب SNES إلى نسخة PC |

## سجل تغييرات القرارات

| التاريخ | القرار | من قرّر | السبب |
|---|---|---|---|
| YYYY-MM-DD | مثال: HP تبقى لاتينية في شريط القتال | المستخدم | الرسمة 16×11 لا تسع «حيوية» |
