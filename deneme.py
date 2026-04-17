def merdiven_ciz(yukseklik, genislik, basamak_sayisi):
    """
    Merdiven pattern'i çizer
    
    Args:
        yukseklik: Her basamağın yüksekliği (kaç satır)
        genislik: Her basamağın genişliği (kaç yıldız)
        basamak_sayisi: Toplam basamak sayısı
    """
    
    # Her basamak için
    for basamak in range(basamak_sayisi):
        # Her basamağın her satırı için
        for satir in range(yukseklik):
            # Boşlukları yazdır
            # Her basamakta (genislik - 1) kadar boşluk ekleniyor
            bosluk_sayisi = basamak * (genislik - 1)
            print(" " * bosluk_sayisi, end="")
            
            # Yıldızları yazdır
            # İlk basamakta genislik kadar, sonra her basamakta genislik kadar ekleniyor
            yildiz_sayisi = genislik + (basamak * genislik)
            print("*" * yildiz_sayisi)


# Örnek kullanımlar
print("Örnek 1: Yükseklik=3, Genişlik=2, Basamak=5")
merdiven_ciz(yukseklik=3, genislik=2, basamak_sayisi=5)

print("\n" + "="*40 + "\n")

print("Örnek 2: Yükseklik=4, Genişlik=3, Basamak=4")
merdiven_ciz(yukseklik=4, genislik=3, basamak_sayisi=4)

print("\n" + "="*40 + "\n")

print("Örnek 3: Yükseklik=2, Genişlik=4, Basamak=3")
merdiven_ciz(yukseklik=2, genislik=4, basamak_sayisi=3)
def merdiven_ciz(yukseklik, genislik, basamak_sayisi):
    """
    Merdiven pattern'i çizer
    
    Args:
        yukseklik: Her basamağın yüksekliği (kaç satır)
        genislik: Her basamağın genişliği (kaç yıldız)
        basamak_sayisi: Toplam basamak sayısı
    """
    
    # Her basamak için
    for basamak in range(basamak_sayisi):
        # Her basamağın her satırı için
        for satir in range(yukseklik):
            # Boşlukları yazdır
            # Her basamakta (genislik - 1) kadar boşluk ekleniyor
            bosluk_sayisi = basamak * (genislik - 1)
            print(" " * bosluk_sayisi, end="")
            
            # Yıldızları yazdır
            # İlk basamakta genislik kadar, sonra her basamakta genislik kadar ekleniyor
            yildiz_sayisi = genislik + (basamak * genislik)
            print("*" * yildiz_sayisi)


# Örnek kullanımlar
print("Örnek 1: Yükseklik=3, Genişlik=2, Basamak=5")
merdiven_ciz(yukseklik=3, genislik=2, basamak_sayisi=5)

print("\n" + "="*40 + "\n")

print("Örnek 2: Yükseklik=4, Genişlik=3, Basamak=4")
merdiven_ciz(yukseklik=4, genislik=3, basamak_sayisi=4)

print("\n" + "="*40 + "\n")

print("Örnek 3: Yükseklik=2, Genişlik=4, Basamak=3")
merdiven_ciz(yukseklik=2, genislik=4, basamak_sayisi=3)
