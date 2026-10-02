# الأسبوع 1: بناء مجموعة الاختبار | Week 1: Build the benchmark dataset

## الهدف | Goal
بناء مجموعة اختبار بحدود آيات معروفة بدقة، قبل قياس منجّم عليها.
Build a test set with exactly known ayah boundaries, before measuring Munajjam against it.

## المهام | Tasks

### 1. تشغيل منجّم على الفاتحة | Run Munajjam on Al-Fatiha
```bash
git clone https://github.com/Itqan-community/Munajjam.git
cd Munajjam/munajjam
pip install ".[faster-whisper]"
munajjam align 001.mp3 --surah 1 --format json -o fatiha.json
```
إن لم يتوفر GPU محليًا فاستعملي Kaggle أو Colab.
If no local GPU is available, use Kaggle or Colab.

### 2. العينة | Sample
- **3 قرّاء بالحفص** من EveryAyah، بسرعات أداء مختلفة (سريع / متوسط / بطيء).
  **3 Hafs reciters** from EveryAyah with different pace (fast / medium / slow).
- **10 سور | 10 surahs:** 1, 12, 36, 55, 56, 67, 78, 93, 103, 112
- تحققي من أسماء المجلدات على EveryAyah ووثّقيها.
  Verify the reciter folder names on EveryAyah and document them.

### 3. السكربت `scripts/build_dataset.py`
- يحمّل ملفات الآيات (آية آية).
  Downloads the verse-by-verse files.
- يدمجها بـ ffmpeg في ملف واحد لكل سورة.
  Concatenates them with ffmpeg into one file per surah.
- يحسب بداية كل آية ونهايتها من المدد التراكمية (ffprobe).
  Computes each ayah's start/end from cumulative durations (ffprobe).
- يُخرج CSV في `data/` بالأعمدة:
  Outputs a CSV in `data/` with the columns:

```
reciter,surah,ayah,start,end,source_url,sha256
```

### 4. البسملة | Basmala
افحصي كيف تعامل EveryAyah البسملة (ملف مستقل؟ مدمجة في الآية الأولى؟)، وكيف يتوقعها منجّم، ووثّقي القرار في README.
Investigate how EveryAyah handles the basmala (separate file? merged into ayah 1?) and how Munajjam expects it; document the decision in the README.

## معايير القبول | Acceptance criteria
- [ ] إعادة الإنتاج بأمر واحد. | Reproducible with one command.
- [ ] نهاية آخر آية = مدة الملف المدمج (±10 ms). | Last ayah end equals concatenated file duration (±10 ms).
- [ ] لا ملفات صوتية في المستودع. | No audio files committed.
- [ ] لا ملفات مولّدة أو مخرجات تشغيل في المستودع (سجلات، مخرجات منجّم الخام، ملفات مؤقتة)؛ يُرفع الكود المصدري وملفات CSV النهائية فقط. | No generated files or run outputs committed (logs, raw Munajjam outputs, temp files); only source code and final CSVs.
- [ ] README يوثّق التثبيت والمصدر والبسملة. | README documents setup, data source and basmala handling.

## التقرير الأسبوعي | Weekly report
آخر يوم في الأسبوع، في ملف `reports/week1.md`:
At the end of the week, in `reports/week1.md`:

- **ما أُنجز | Done**
- **العوائق | Blockers**
- **التالي | Next**
- **أسئلة | Questions**
- **لماذا؟ | Why?** اشرحي بكلامك أنتِ، في فقرة أو فقرتين، لماذا حسبتِ بداية الآيات ونهاياتها بهذه الطريقة، وما الذي قد يُفسد دقتها (مثل الصمت في أول الملفات وآخرها، أو البسملة، أو حشو المُرمِّز encoder padding). المطلوب الفهم لا وصف الخطوات.
  In your own words, in one or two paragraphs, explain *why* you computed ayah start/end times this way, and what could break their accuracy (e.g. leading/trailing silence, the basmala, encoder padding). Understanding, not a list of steps.

وتذكير: سطر في `logbook.md` عن كل يوم عمل، يُرفع في اليوم نفسه.
Reminder: one line in `logbook.md` per working day, committed the same day.
