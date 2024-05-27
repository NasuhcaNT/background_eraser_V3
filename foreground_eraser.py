from rembg import remove
import cv2
import numpy as np

def subtract_foreground_from_background(input_background_path, input_foreground_path, output_path):
    # Arka plan resmini yükle
    background = cv2.imread(input_background_path)
    
    # Ön plan resmini yükle (rembg kullanılarak oluşturulmuş olmalı)
    foreground = cv2.imread(input_foreground_path, cv2.IMREAD_UNCHANGED)
    
    # Alpha kanalını kontrol et. Eğer varsa, maske olarak kullan
    if foreground.shape[2] == 4:
        # Alpha kanalını maske olarak ayır
        alpha_channel = foreground[:, :, 3]
        # Maskeyi ters çevir (alfa kanalı 255 olan yerler şeffaf olacak)
        _, mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY_INV)
        
        # Maskeyi 3 kanallı hale getir
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        
        # Arka plan resmini maskele
        background_masked = cv2.bitwise_and(background, mask_3ch)

        # Beyaz arka plan oluştur
        white_background = np.ones_like(background, np.uint8) * 255
        # Beyaz arka planı maskeyle birleştir
        white_masked = cv2.bitwise_and(white_background, cv2.bitwise_not(mask_3ch))
        
        # Maskelenmiş arka plan ile beyaz arka planı birleştir
        result = cv2.add(background_masked, white_masked)
        
        # Sonuç olarak maskelenmiş arka planı kaydet
        cv2.imwrite(output_path, result)
    else:
        print("Görsel uygun alpha kanalına sahip değil.")

# Arka plan resminin yolu
input_background_path = r'C:\Users\examplename\Desktop\background.jpg'

# rembg kullanılarak arka planı kaldırılmış ön plan resminin yolu
input_foreground_path = r'C:\Users\examplename\Desktop\background_eraser_output.jpg'

# Sonuç olarak elde edilen resmin kaydedileceği yol
output_path = r'C:\Users\examplename\Desktop\result_image2.jpg'

# Fonksiyonu çağır
subtract_foreground_from_background(input_background_path, input_foreground_path, output_path)
