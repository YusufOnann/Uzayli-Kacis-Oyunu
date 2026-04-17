import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
from datetime import datetime
import pygame

pygame.mixer.init()

# --- Ses oynatma fonksiyonu ---
def ses_cal(dosya_yolu):
    try:
        pygame.mixer.Sound(dosya_yolu).play()
    except Exception as e:
        print("Ses çalınamadı:", e)

# --- Zorluk seviyelerine göre kelimeleri ayır ---
def kelime_sec(zorluk):
    with open("kelimeler.txt", "r", encoding="utf-8") as f:
        satirlar = f.readlines()

    secenekler = []
    aktif = None
    for satir in satirlar:
        satir = satir.strip()
        if satir.startswith("#"):
            aktif = satir[2:].strip()
        elif aktif == zorluk:
            secenekler.append(satir)
    return random.choice(secenekler) if secenekler else None

# --- Başlangıç değerleri ---
TUZAK_HARFLER = {'x', 'z', 'j', 'q'}
MAKS_ADIM = 12
TAHMIN_SURESI = 20

# --- Ana oyun sınıfı ---
class UzayliOyunu:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Uzaylıdan Kaçış - Şifreli Mesaj")
        self.pencere.geometry("700x500")
        self.pencere.resizable(False, False)
        self.zorluk_penceresi()

    def zorluk_penceresi(self):
        for widget in self.pencere.winfo_children():
            widget.destroy()
        baslik = tk.Label(self.pencere, text="Zorluk Seçin", font=('Arial', 20))
        baslik.pack(pady=20)

        for zorluk in ['easy', 'medium', 'hard']:
            tk.Button(self.pencere, text=zorluk.capitalize(), font=('Arial', 16),
                      command=lambda z=zorluk: self.oyunu_baslat(z)).pack(pady=5)

    def oyunu_baslat(self, zorluk):
        self.secili_kelime = kelime_sec(zorluk)
        self.gorunen_kelime = ['_' if ch != ' ' else ' ' for ch in self.secili_kelime]
        self.tahmin_edilenler = set()
        self.kalan_adim = MAKS_ADIM
        self.toplam_sure = 0
        self.baslangic_suresi = time.time()
        self.sayac_aktif = False
        self.sure = TAHMIN_SURESI
        self.ipucu_kullanildi = False
        self.oyun_bitti = False

        for widget in self.pencere.winfo_children():
            widget.destroy()

        self.etiket_kelime = tk.Label(self.pencere, text=' '.join(self.gorunen_kelime), font=('Courier', 24))
        self.etiket_kelime.pack(pady=10)

        self.etiket_sayac = tk.Label(self.pencere, text=f"Kalan Süre: {self.sure}", font=('Arial', 14))
        self.etiket_sayac.pack()

        self.etiket_uzayli = tk.Label(self.pencere, text="", font=('Courier', 20))
        self.etiket_uzayli.pack(pady=10)

        self.etiket_kalan_adim = tk.Label(self.pencere, text="", font=('Arial', 12))
        self.etiket_kalan_adim.pack()

        self.guncelle_ascii()

        tk.Label(self.pencere, text="Harf Tahmini (1 karakter):").pack()
        self.harf_girdi = tk.Entry(self.pencere, font=('Courier', 14), width=5, justify='center')
        self.harf_girdi.pack()

        tk.Button(self.pencere, text="Harf Tahmin Et", command=self.harf_tahmin_et).pack(pady=5)

        tk.Label(self.pencere, text="Kelime(ler) Tahmini:").pack()
        self.kelime_girdi = tk.Entry(self.pencere, font=('Courier', 14), width=30, justify='center')
        self.kelime_girdi.pack()

        tk.Button(self.pencere, text="Kelime(ler) Tahmin Et", command=self.kelime_tahmin_et).pack(pady=5)

        tk.Button(self.pencere, text="İpucu Al (1 kez)", command=self.ipucu_ver).pack(pady=5)

        self.yeni_sayac()

    def sayaci_baslat(self):
        while self.sure > 0 and not self.oyun_bitti:
            time.sleep(1)
            self.sure -= 1
            self.etiket_sayac.config(text=f"Kalan Süre: {self.sure}")
        if self.sure == 0 and not self.oyun_bitti:
            self.sayac_aktif = False
            self.zaman_doldu()
        self.sayac_aktif = False

    def zaman_doldu(self):
        self.kalan_adim -= 2
        self.guncelle_ascii()
        self.kontrol_oyun_bitti()
        self.yeni_sayac()

    def guncelle_ascii(self):
        self.etiket_uzayli.config(text="🚀" + "-" * max(self.kalan_adim, 0) + "👽")
        self.etiket_kalan_adim.config(text=f"Kalan Adım: {max(self.kalan_adim, 0)}")

    def harf_tahmin_et(self):
        if self.oyun_bitti:
            return
        harf = self.harf_girdi.get().lower()
        self.harf_girdi.delete(0, tk.END)
        if len(harf) != 1 or not harf.isalpha() or harf in self.tahmin_edilenler:
            return

        self.tahmin_edilenler.add(harf)

        bulundu = False
        for i, ch in enumerate(self.secili_kelime):
            if ch.lower() == harf:
                self.gorunen_kelime[i] = ch
                bulundu = True

        if bulundu:
            ses_cal("alarm/correct.wav")
        else:
            ses_cal("alarm/wrong.wav")
            self.kalan_adim -= 2 if harf in TUZAK_HARFLER else 1

        self.etiket_kelime.config(text=' '.join(self.gorunen_kelime))
        self.guncelle_ascii()
        self.kontrol_oyun_bitti()
        self.yeni_sayac()

    def kelime_tahmin_et(self):
        if self.oyun_bitti:
            return
        tahmin = self.kelime_girdi.get().lower().strip()
        self.kelime_girdi.delete(0, tk.END)

        hedef = self.secili_kelime.lower()
        parcalar = hedef.split()

        if tahmin == hedef or tahmin in parcalar:
            ses_cal("alarm/correct.wav")
            index_baslangici = self.secili_kelime.lower().find(tahmin)
            for i in range(index_baslangici, index_baslangici + len(tahmin)):
                self.gorunen_kelime[i] = self.secili_kelime[i]
        else:
            ses_cal("alarm/wrong.wav")
            self.kalan_adim -= 1

        self.etiket_kelime.config(text=' '.join(self.gorunen_kelime))
        self.guncelle_ascii()
        self.kontrol_oyun_bitti()
        self.yeni_sayac()

    def ipucu_ver(self):
        if self.ipucu_kullanildi or self.oyun_bitti:
            return
        for i, ch in enumerate(self.secili_kelime):
            if ch != ' ':
                self.gorunen_kelime[i] = ch
                break
        self.kalan_adim -= 2
        self.ipucu_kullanildi = True
        self.etiket_kelime.config(text=' '.join(self.gorunen_kelime))
        self.guncelle_ascii()
        self.kontrol_oyun_bitti()

    def yeni_sayac(self):
        if not self.sayac_aktif:   # İş parçacıklarının üst üste binmelerini önlemek adına kontrol.
            self.sure = TAHMIN_SURESI
            self.sayac_aktif = True
            threading.Thread(target=self.sayaci_baslat).start()
        else:
            self.sure = TAHMIN_SURESI

    def kontrol_oyun_bitti(self):
        if '_' not in self.gorunen_kelime:
            self.oyun_bitti = True
            ses_cal("alarm/win.wav")
            self.oyun_sonu("KAZANDI")
        elif self.kalan_adim <= 0:
            self.oyun_bitti = True
            ses_cal("alarm/lose.wav")
            self.oyun_sonu("KAYBETTİ")

    def oyun_sonu(self, sonuc):
        self.toplam_sure = round(time.time() - self.baslangic_suresi)
        zaman = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("scores.txt", "a", encoding="utf-8") as f:
            f.write(f"{zaman} | {sonuc} | {self.secili_kelime} | {self.toplam_sure} saniye\n")
        messagebox.showinfo("Oyun Bitti", f"{sonuc}!\nKelime: {self.secili_kelime}\nSüre: {self.toplam_sure} saniye")
        self.zorluk_penceresi()


# --- Ana pencereyi başlat ---
pencere = tk.Tk()
app = UzayliOyunu(pencere)
pencere.mainloop()