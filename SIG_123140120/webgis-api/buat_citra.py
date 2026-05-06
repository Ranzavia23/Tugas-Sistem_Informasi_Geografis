import urllib.request
import cv2
import rasterio
from rasterio.transform import from_origin

print("1. Mengunduh gambar sampel...")
# Menggunakan gambar uji coba standar YOLO (ada mobil dan bus)
url = "https://raw.githubusercontent.com/ultralytics/yolov5/master/data/images/bus.jpg"
urllib.request.urlretrieve(url, "temp.jpg")

print("2. Membaca gambar...")
img = cv2.imread("temp.jpg")
# Rasterio butuh format warna RGB dan urutan (Channel, Height, Width)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_raster = img_rgb.transpose(2, 0, 1) 
c, h, w = img_raster.shape

print("3. Membuat file GeoTIFF buatan...")
# Menyuntikkan titik koordinat Rajabasa, Lampung (Lon: 105.24, Lat: -5.37)
transform = from_origin(105.24, -5.37, 0.0001, 0.0001) 

with rasterio.open(
    'sample_aerial.tif', 'w', driver='GTiff',
    height=h, width=w, count=c, dtype=img_raster.dtype,
    crs='+proj=latlong', transform=transform
) as dst:
    dst.write(img_raster)

print("✅ Selesai! File 'sample_aerial.tif' sudah siap digunakan.")