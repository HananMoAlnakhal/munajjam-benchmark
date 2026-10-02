# munajjam-benchmark

معيار مفتوح لقياس دقة أداة [منجّم](https://github.com/Itqan-community/Munajjam) (مجتمع إتقان) في مزامنة التلاوة مع الآيات.

An open benchmark for measuring the accuracy of [Munajjam](https://github.com/Itqan-community/Munajjam) (Itqan Community) in aligning Quran recitations with ayah boundaries.

## الفكرة | Idea

نصل ملفات تلاوة مقسّمة آية آية، فنعرف حدود كل آية بدقة من مدد الملفات، ثم نقارن بها ما يخرجه منجّم.

We concatenate verse-by-verse recitation files, so the exact ayah boundaries are known from the file durations, then compare Munajjam's output against them.

## محايد تجاه الأدوات | Tool-agnostic

المعيار يقيس أي أداة تُخرج حدود الآيات (بداية ونهاية لكل آية)، ومنجّم إتقان أولها. ومن الأدوات المرشحة لاحقًا: [منجّم سطح المكتب](https://community.itqan.dev/d/812).

The benchmark measures any tool that outputs ayah boundaries (start/end per ayah); Itqan's Munajjam is the first. Candidates for later: [Munajjam Desktop](https://community.itqan.dev/d/812).

## تعريف الحد | Boundary definition

الحد المرجعي هو موضع الوصل بين ملفي الآيتين في الملف المدمج. وبعض الأدوات تترك عمدًا هامشًا آمنًا قبل بدء الصوت، فيُقاس الخطأ بطريقتين: الخطأ الخام، والخطأ بعد سماح بهامش صمت مُعلَن. ولا يُعدّ خطأً ما وقع داخل الصمت الفاصل بين آيتين.

The reference boundary is the join point between two ayah files in the concatenated audio. Some tools deliberately leave a safety margin before sound onset, so error is reported two ways: raw error, and error with a declared silence tolerance. A boundary placed inside the silence between two ayahs is not counted as an error.

## الترميز | Encoding

التوقيت مرتبط بنسخة الملف الصوتي بعينها، فيُوثَّق لكل ملف: الصيغة، ونوع الترميز (CBR أو VBR)، ومعدل البت، ومعدل العينة، وبصمة sha256.

Timings are tied to the exact audio file, so each file's format, encoding mode (CBR/VBR), bitrate, sample rate and sha256 are recorded.

## البنية | Layout

| المسار | المحتوى |
|---|---|
| `tasks/` | مهام كل أسبوع / weekly tasks |
| `scripts/` | نصوص بناء المجموعة والقياس / dataset & evaluation scripts |
| `data/` | ملفات CSV للحدود والنتائج فقط، لا صوت / boundary & result CSVs only, no audio |
| `logbook.md` | السجل اليومي للتدريب / daily training log |

## قواعد | Rules

- لا تُرفع أي ملفات صوتية إلى المستودع. تُحفظ روابط المصدر والبصمات فقط.
- No audio files are committed. Only source URLs and hashes are kept.
- يُوثَّق مصدر كل بيانات ورخصتها. / Every data source and its license is documented.

## الإشراف | Supervision

تدريب ميداني بإشراف GainInsight، بالتعاون مع الكلية الجامعية للعلوم التطبيقية – غزة.

Field training supervised by GainInsight, in cooperation with the University College of Applied Sciences – Gaza.

## الرخصة | License

MIT
