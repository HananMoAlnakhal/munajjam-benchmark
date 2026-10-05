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

> **تصحيح (3 أكتوبر) | Correction (Oct 3):** الأوامر أعلاه منقولة من README منجّم، وهي لا تعمل كما هي، وقد كشفت ذلك المتدربة في يومها الأول:
> The commands above are copied from Munajjam's README and do not work as-is; the trainee found this on day 1:
> 1. لا يوجد extra باسم `faster-whisper` في `pyproject.toml` (يظهر التحذير `does not provide the extra 'faster-whisper'`).
>    There is no `faster-whisper` extra in `pyproject.toml`.
> 2. الواجهة الافتراضية `--whisper-backend openai` (transformers)، بينما النموذج الافتراضي `OdyAsh/faster-whisper-base-ar-quran` بصيغة CTranslate2، فيفشل الأمر الافتراضي بـ `Unrecognized model ... model_type`. الحل: `--whisper-backend fasterwhisper` مع تثبيت `faster-whisper` يدويًا.
>    The default backend is `openai` (transformers) while the default model is a CTranslate2 faster-whisper model, so the default command fails. Fix: `--whisper-backend fasterwhisper` with `faster-whisper` installed manually.
>
> **المطلوب | Required:** وثّقي في README الأوامر التي نجحت فعلًا، حرفيًا، مع نسخ Python و`faster-whisper` و`av`. ثم صوغي المشكلتين في مسودتي issue لمستودع منجّم في `reports/upstream-issues.md` (لا تنشريهما قبل المراجعة).
> Document the exact commands that actually worked, with Python, `faster-whisper` and `av` versions. Then draft both problems as Munajjam issues in `reports/upstream-issues.md` (don't post before review).

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
reciter,surah,ayah,start,end,lead_silence,trail_silence,source_url,sha256
```

### 4. البسملة | Basmala
افحصي كيف تعامل EveryAyah البسملة (ملف مستقل؟ مدمجة في الآية الأولى؟)، وكيف يتوقعها منجّم، ووثّقي القرار في README.
Investigate how EveryAyah handles the basmala (separate file? merged into ayah 1?) and how Munajjam expects it; document the decision in the README.

### 5. الترميز وتعريف الحد | Encoding and boundary definition
- سجّلي لكل ملف، في `data/sources.csv`: الصيغة، ونوع الترميز (CBR أو VBR)، ومعدل البت، ومعدل العينة، وsha256. استعملي `ffprobe` ولا تعتمدي على اسم الملف.
  For each file, record in `data/sources.csv`: format, encoding mode (CBR/VBR), bitrate, sample rate, sha256. Use `ffprobe`; don't rely on the file name.
- قيسي مدة الصمت في أول كل ملف آية وآخره (مثلًا بمرشح `silencedetect` في ffmpeg)، واحفظيها في عمودين `lead_silence` و`trail_silence`. ستُستعمل لاحقًا في سماح الهامش الآمن.
  Measure leading/trailing silence in each ayah file (e.g. ffmpeg `silencedetect`) and store it as `lead_silence`, `trail_silence`. It will be used later for the safety-margin tolerance.
- اقرئي فقرة «تعريف الحد» في README، واكتبي في تقريرك هل توافقين عليها أم تقترحين غيرها، ولماذا.
  Read "Boundary definition" in the README; in your report, say whether you agree or propose otherwise, and why.

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
