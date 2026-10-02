# munajjam-benchmark

معيار مفتوح لقياس دقة أداة [منجّم](https://github.com/Itqan-community/Munajjam) (مجتمع إتقان) في مزامنة التلاوة مع الآيات.

An open benchmark for measuring the accuracy of [Munajjam](https://github.com/Itqan-community/Munajjam) (Itqan Community) in aligning Quran recitations with ayah boundaries.

## الفكرة | Idea

نصل ملفات تلاوة مقسّمة آية آية، فنعرف حدود كل آية بدقة من مدد الملفات، ثم نقارن بها ما يخرجه منجّم.

We concatenate verse-by-verse recitation files, so the exact ayah boundaries are known from the file durations, then compare Munajjam's output against them.

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
