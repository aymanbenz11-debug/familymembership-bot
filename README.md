# Familymembership Telegram Bot (نسخة نهائية جاهزة عبر Docker Compose)

وصف سريع
- بوت Telegram بسيط يسجّل المستخدمين ويقدّم 3 أزرار: تسجيل، فيديو تعرّف على الشركة، وفيديو 8 مصادر ربح.
- كل ضغطة زر تسجّل كنقرة في قاعدة بيانات. هناك خادم redirect اختياري لتتبُّع زيارات عبر روابط خارجية.

المتطلبات
- Docker و Docker Compose (أو Docker Engine مع دعم Compose).
- توكن بوت من BotFather (BOT_TOKEN).

الملفات المهمة
- bot.py: منطق البوت (polling).
- redirect_server.py: خادم إعادة توجيه لتتبُّع زيارات خارجية (اختياري).
- models.py: تعريف الجداول باستخدام SQLAlchemy.
- Dockerfile, docker-compose.yml: لتشغيل الحاويات.
- .env.example: مثال لمتغيرات البيئة.

خطوات التشغيل (محلي أو سيرفر)
1. انسخ المشروع إلى مجلد جديد، أو انسخ الملفات أعلاه.
2. أنشئ ملف .env في جذر المشروع بناءً على .env.example واملأ BOT_TOKEN:
   - مثال:
     BOT_TOKEN=123456:ABCDEF-xyz
     DB_URL=sqlite:////app/data/family_bot.db
     PORT=5000
3. أنشئ مجلد البيانات:
   mkdir -p data
4. شغّل Docker Compose:
   docker compose up -d --build
   (أو docker-compose up -d --build إذا تستخدم النسخة القديمة)
5. تحقق من السجلات:
   docker compose logs -f bot
   docker compose logs -f redirect
6. جرب البوت:
   - افتح Telegram، ابحث عن البوت الخاص بك، أرسل /start ثم اضغط الأزرار.
   - أرسل /stats لعرض عدد المستخدمين والنقرات.

استخدام روابط إعادة التوجيه خارجياً
- إذا أردت تضمين روابط في صفحات أو إعلانات مع تتبُّع، استخدم رابط الشكل:
  https://YOUR_HOST/r/<token>
- يمكنك استخراج التوكينات من قاعدة البيانات أو تعديل البوت لإرسال رابط خارجي بدل callback.

نقل إلى الإنتاج
- استبدل SQLite بـ PostgreSQL في DB_URL لثبات أعظم.
- استضف redirect_server خلف HTTPS (Cloud Run, Render, VPS + nginx + certbot).
- لا تشارك BOT_TOKEN; احتفظ به في متغيرات بيئة آمنة.

ملاحظات أمان وخصوصية
- نستخدم UUIDs كتوكنات؛ لا نضع tg_id مباشرة في روابط عامة.
- ضع قواعد rate-limiting إذا تعرض الخادم لزيارات كثيرة.

المساعدة الإضافية
- أريد أن أجهز لك ملف zip جاهز؟ أو أرفع المشروع إلى GitHub؟ أو أعدّل ليعمل مع PostgreSQL وبيئة إنتاج (systemd / Gunicorn)؟ أعلمني أي خيار تفضّل.
