
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Django User model
User = settings.AUTH_USER_MODEL


# 🧑‍🏫 O‘qituvchi modeli
class Oqtuvchi(models.Model):
    """
    O‘qituvchi haqida ma’lumot:
    - name: foydalanuvchi bilan bog‘langan (User modeli)
    - yonalish: o‘qituvchi yo‘nalishi (backend, frontend, english, design)
    - rasm: o‘qituvchi rasmi
    - bio: qisqacha ma’lumot (ixtiyoriy)
    """



    name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='oqtuvchi')
    yonalish = models.CharField(max_length=20,)
    rasm = models.ImageField(upload_to="oqituvchi/")
    bio = models.TextField(blank=True, null=True)

    def str(self):
        return str(self.name)


# 📅 Kuni modeli
class Kuni(models.Model):
    """
    Haftaning kunlarini ifodalaydi (Dushanba, Seshanba, Chorshanba va hokazo)
    """
    kun = models.CharField(max_length=15, unique=True)

    def str(self):
        return self.kun


# 👥 Group modeli
class Group(models.Model):
    """
    O‘quv guruhi haqida ma’lumot:
    - name: guruh nomi
    - yonalish: qaysi yo‘nalishdagi kurs
    - oqtuvchi: o‘qituvchi bilan bog‘langan
    - start_date: kurs boshlanish sanasi
    - vaqt: darslar o‘tkaziladigan vaqt
    - dars_kunlari: haftaning qaysi kunlari dars bo‘ladi (ManyToMany)
    """
    YONALISHLAR = (
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('english', 'English'),
        ('design', 'Design'),
    )

    name = models.CharField(max_length=126)
    yonalish = models.CharField(max_length=20, choices=YONALISHLAR)
    oqtuvchi = models.ForeignKey(
        Oqtuvchi, on_delete=models.SET_NULL, null=True, blank=True, related_name='gruplar'
    )
    start_date = models.DateField()
    vaqt = models.CharField(max_length=50)
    dars_kunlari = models.ManyToManyField(Kuni, blank=True, related_name='gruplar')

    def str(self):
        return f"{self.name} ({self.yonalish})"


# 👨‍🎓 O‘quvchi modeli
class Oquvchi(models.Model):
    """
    O‘quvchi (talaba) haqida ma’lumot:
    - user: foydalanuvchi bilan bog‘langan (User modeli)
    - grup: o‘quvchi qaysi guruhda o‘qiyotgani
    - date_joined: tizimga qo‘shilgan sana
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='oquvchi')
    grup = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='oquvchilar'
    )
    date_joined = models.DateField(auto_now_add=True)

    def str(self):
        return str(self.user)


# 🗓 Dars jadvali (Schedule)
class Schedule(models.Model):
    """
    Guruhning dars jadvali (har bir dars sanasi):
    - grup: dars o‘tkaziladigan guruh
    - sana: dars kuni
    - mavzu: dars mavzusi (ixtiyoriy)
    """

    grup = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='jadval')
    sana = models.DateField()
    mavzu = models.CharField(max_length=200, blank=True, null=True)

    def str(self):
        return f"{self.grup.name} - {self.sana}"

    class Meta:
        ordering = ['-sana']
        unique_together = ('grup', 'sana')


# ✅ Davomat (yo‘qlama)
class Attendance(models.Model):
    """
    Har bir dars uchun o‘quvchilarning qatnashgan/qatnashmagan holatini saqlaydi:
    - oquvchi: kim qatnashgan
    - jadval: qaysi dars kuni
    - keldi: qatnashganmi yoki yo‘qmi
    """

    oquvchi = models.ForeignKey(Oquvchi, on_delete=models.CASCADE, related_name='yoqlama')
    jadval = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='yoqlamalar')
    keldi = models.BooleanField(default=False)

    def str(self):
        status = "✅ Keldi" if self.keldi else "❌ Kelmagan"
        return f"{self.oquvchi.user} - {self.jadval.sana} ({status})"

    class Meta:
        unique_together = ('oquvchi', 'jadval')


# 🏅 Baholar (Grade)
class Grade(models.Model):
    """
    O‘quvchilarning har bir darsdagi bahosi:
    - oquvchi: kimning bahosi
    - jadval: qaysi dars kuni
    - ball: olingan ball (0 dan 100 gacha)
    """

    oquvchi = models.ForeignKey(Oquvchi, on_delete=models.CASCADE, related_name='baholar')
    jadval = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='baholar')
    ball = models.PositiveSmallIntegerField(default=0)

    def str(self):
        return f"{self.oquvchi.user} - {self.ball} ball ({self.jadval.sana})"

    class Meta:
        unique_together = ('oquvchi', 'jadval')


# ⚙️ Signal — yangi Schedule qo‘shilganda avtomatik yo‘qlama yaratish
@receiver(post_save, sender=Schedule)
def create_attendance_for_group(sender, instance, created, **kwargs):
    """
    Har safar yangi dars (Schedule) yaratilganda:
    - Guruhdagi barcha o‘quvchilar uchun Attendance yozuvi avtomatik yaratiladi.
    - Agar yozuv mavjud bo‘lsa, qayta yaratilmaydi.
    """
    if created:
        group = instance.grup
        oquvchilar = group.oquvchilar.all()
        for oquvchi in oquvchilar:
            Attendance.objects.get_or_create(
                oquvchi=oquvchi,
                jadval=instance,
                defaults={'keldi': False}
            )