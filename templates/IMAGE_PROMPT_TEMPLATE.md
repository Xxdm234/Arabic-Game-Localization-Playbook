# قالب طلب توليد صورة نصية (لأداة توليد الصور)

احفظ كل طلب في `trans/images/prompts/<اسم>.md`، وكل ناتج (المقبول والمرفوض) في `trans/images/`، مع سبب الرفض في `manifest.json`.

## القالب

```text
Use case: text-localization.
Replace the original <ENGLISH TEXT> lettering with EXACT Arabic "<النص العربي حرفيًا>"
arranged as <عدد> centered lines: "<السطر 1>" / "<السطر 2>" / ...
Style: <الأسلوب المأخوذ من الأصل: لون، وريشة، وخشونة، وظل، وحد، وتدرج>, matching the original's stroke weight and character.
Keep <العناصر الزخرفية الأصلية التي يجب أن تبقى> exactly, avoid overlapping them.
Same <W:H> composition, <transparent background / same background>, no extra board, no paper, NO English letters.
Correct connected Arabic letters and ALL dots. <إن كانت الخامة تُعرض معكوسة: Mirror the letters horizontally as a whole word (reads correctly in a mirror).>
```

## مثال حقيقي (RtMI — اسم المتحف)

```text
Use case: text-localization. Replace original MUSEUM OF Pirate Lore lettering with EXACT Arabic
"متحف تراث القراصنة" arranged three centered lines: "متحف" / "تراث" / "القراصنة".
Dark deep green rough hand-painted pirate museum logo, playful angular tall strokes matching original.
Keep the small original horizontal BONE decoration at the very bottom below all words, avoid text overlap.
Same 203:186 composition, transparent background, no sign board, no paper, no English.
Correct connected Arabic and all dots.
```

## قائمة مراجعة الناتج قبل الاستيراد

- [ ] النص العربي **حرفيًا** كما طُلب، والنقاط كلها في مكانها (ب، ت، ث، ن، ي، ج، خ، ش، ض، ظ، غ، ف، ق، ة)
- [ ] الحروف متصلة صحيحة، ولا انقلاب في الباء، ولا حرف لاتيني متسلل
- [ ] الأسلوب يطابق الأصل (الوزن، واللون، والحد، والظل)
- [ ] الأبعاد والنسبة تطابق منطقة الكتابة، ولا قص للعناصر المحمية
- [ ] الاسم يطابق المسرد والحوار والتلميح
- [ ] لا يكشف معلومة مبكرة (جنس، أو حل لغز)
- [ ] بعد الاستيراد: `code/image_guard.py` = صفر تغيير خارج المناطق، وفئة الشفافية محفوظة
- [ ] لقطة داخل اللعبة ببصمة الحزمة
