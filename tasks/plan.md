# خطة التدريب | Training plan

المدة الرسمية: شهر واحد. يجوز إنهاء المهام قبل موعدها، لكن أيام الحضور تُسجَّل كما وقعت فعلًا في `logbook.md` (بنظام 24 ساعة، بتوقيت غزة)، ولا يُوقَّع إلا ما سُجِّل.
Official duration: one month. Tasks may be finished early, but attendance is recorded exactly as it happened in `logbook.md` (24-hour clock, Gaza time); only what is logged is signed.

> **تسريع التدريب | Acceleration:** إن اشترطت الكلية عددًا من الساعات لا من الأيام، أمكن إنهاء التدريب أسرع بزيادة ساعات العمل اليومية، بشرط أن تُسجَّل فعلًا. تأكدي من القسم: هل الشرط أيام أم ساعات؟
> If the college requires a number of hours rather than days, the training can end sooner by working longer days, provided they are actually logged. Confirm with the department: days or hours?

---

## الأسبوع 1 — بناء مجموعة الاختبار | Week 1 — Build the dataset
التفاصيل في [`week1.md`](week1.md). التسليم: Pull Request + `reports/week1.md`.
Details in `week1.md`. Deliverable: Pull Request + `reports/week1.md`.

## الأسبوع 2 — تشغيل منجّم والقياس | Week 2 — Run Munajjam and measure
1. **التشغيل | Run:** شغّلي منجّم (commit `419c699`) على الملفات المدمجة الثلاثين (3 قراء × 10 سور)، بالبسملة وبدونها. أدخلي ملف WAV المدمج نفسه، لا نسخة مُعاد ترميزها إلى MP3، حتى تبقى الحدود المرجعية دقيقة.
   Run Munajjam (commit `419c699`) on the 30 concatenated files, with and without basmala. Feed the exact concatenated WAV, not a re-encoded MP3, so the reference boundaries stay exact.
2. **`scripts/evaluate.py`:** يقارن مخرجات منجّم بـ `data/boundaries.csv` ويحسب لكل آية خطأ البداية وخطأ النهاية.
   Compares Munajjam output with `data/boundaries.csv`; per-ayah start and end error.
3. **المقاييس | Metrics:** متوسط الخطأ المطلق، والوسيط، والمئين 90، ونسبة الآيات ضمن ±100 و±250 و±500 ms؛ خامًا ومع سماح الهامش الآمن (انظري «تعريف الحد» في README).
   Mean absolute error, median, P90, % within ±100/250/500 ms; raw and with the silence tolerance.
4. **الاستراتيجيات | Strategies:** قارني `auto` و`greedy` و`dp` و`hybrid` على سورة قصيرة وسورة طويلة على الأقل.
   Compare the four strategies on at least one short and one long surah.

التسليم: `data/results_*.csv` + `reports/week2.md`.

## الأسبوع 3 — التحليل | Week 3 — Analysis
1. **أنماط الخطأ | Error patterns:** هل يزيد الخطأ مع طول الآية؟ مع سرعة القارئ؟ عند الآية الأولى (البسملة)؟ ولماذا يظهر فراغ ثابت (~0.3 ث) بين الآيات؟
   Does error grow with ayah length, reciter pace, at ayah 1 (basmala)? Why the constant ~0.3 s gap?
2. **المعايرة | Calibration:** إن أخرج منجّم درجة ثقة، فهل الآيات منخفضة الثقة هي التي يخطئ فيها؟
   If Munajjam outputs a confidence score, are low-confidence ayahs the wrong ones?
3. **الـ Issues:** إنهاء مسودات `reports/upstream-issues.md` (أربع مشكلات حتى الآن) ومراجعتها قبل النشر.
   Finalize the four upstream-issue drafts for review before posting.

التسليم: رسوم بيانية + `reports/week3.md`.

## الأسبوع 4 — النشر | Week 4 — Publish
1. **README:** قسم النتائج (جدول ورسم)، وطريقة إعادة الإنتاج بأمر واحد، وحدود المعيار.
   Results section, one-command reproduction, limitations.
2. **التقرير الختامي | Final report:** `reports/final.md`: ما قيس، وكيف، والنتائج، وما تعلّمتِه، وما بقي مفتوحًا.
   What was measured, how, results, what you learned, open questions.
3. **العرض | Presentation:** ملخص في 5 شرائح، يصلح لعرضه في الكلية وفي مجتمع إتقان.
   A 5-slide summary for the college and the Itqan community.

---

## قاعدة الأدوات | Tools rule
الاستعانة بأدوات الذكاء الاصطناعي مسموحة، بشرطين: أن يُذكر في التقرير أين استُعين بها، وأن تُشرح كل خطوة بكلامك. ما تفهمينه يُحسب لك، وما لا تفهمينه لا يُحسب ولو عمل.
AI tools are allowed on two conditions: state in the report where they were used, and explain every step in your own words. What you understand counts; what you don't, doesn't, even if it runs.
