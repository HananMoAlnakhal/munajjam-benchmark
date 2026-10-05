# السجل اليومي | Daily logbook

يُملأ كل يوم عمل، ويُرفع في اليوم نفسه. وعلى أساسه يُملأ كشف الحضور ويُوقَّع.

Filled in on every working day and committed the same day. The attendance sheet is filled and signed from it.

| # | التاريخ / Date | البدء / Start (غزة) | الانتهاء / End (غزة) | ما أُنجز / Done | عوائق / Blockers |
|---|---|---|---|---|---|
| 1 | 2/10/2026 |9:00 | 2:00| تشغيل منجم على البسملة وتصليح بعض المشاكل(موضح في التقرير)|  مشاكل في ال pyproject.toml حيث انه لا يوجدتوافق مع ال faster-whisper غير ان ال av غير متوافق |
| 2 | 3/10/2026 |10:00 |1:00| اختيار القراء والتحقق من everyayah -كل المهمة 2 | لا مشاكل |

!curl -L -o 001.mp3 "https://pub-9ee413c8af4041c6bd5223d08f5d0f0f.r2.dev/media/uploads/assets/11/recitations/001.mp3"
!munajjam align 001.mp3 --surah 1 --format json -o fatiha.json --whisper-backend fasterwhisper
