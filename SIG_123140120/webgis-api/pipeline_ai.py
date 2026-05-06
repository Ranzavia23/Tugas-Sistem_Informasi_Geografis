import cv2
import rasterio
import json
from ultralytics import YOLO

def detect_large_image(image_path, model, tile_size=640):
    """Memotong citra (tiling) dan mendeteksi objek dengan YOLOv8"""
    print("Memulai deteksi objek pada citra...")
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    all_detections = []
    
    # Looping untuk memotong gambar menjadi tile kecil[cite: 2]
    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            tile = img[y:y+tile_size, x:x+tile_size]
            
            # Lewati jika potongan terlalu kecil di ujung gambar
            if tile.shape[0] < 100 or tile.shape[1] < 100:
                continue
                
            # Jalankan model YOLOv8 pada tile[cite: 2]
            results = model(tile, verbose=False)
            
            # Kembalikan koordinat kotak deteksi ke ukuran citra asli[cite: 2]
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                all_detections.append({
                    'bbox': [x1+x, y1+y, x2+x, y2+y],
                    'class': cls,
                    'confidence': conf
                })
    return all_detections

def pixel_to_geo(image_path, detections):
    """Mengubah koordinat Piksel ke Geografis (Lat/Lon) menggunakan Rasterio"""
    print("Mengonversi koordinat piksel ke geografis...")
    with rasterio.open(image_path) as src:
        transform = src.transform
        
        geo_detections = []
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            
            # Ambil titik tengah objek[cite: 2]
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            
            # Terapkan affine transform dari metadata GeoTIFF[cite: 2]
            lon, lat = transform * (cx, cy)
            
            geo_detections.append({
                'geometry': {
                    'type': 'Point',
                    'coordinates': [lon, lat]
                },
                'properties': {
                    'class': det['class'],
                    'confidence': det['confidence']
                }
            })
        return geo_detections

def export_to_geojson(geo_detections, output_path):
    """Menyimpan hasil ke format GeoJSON"""
    print("Mengekspor hasil ke GeoJSON...")
    geojson = {
        'type': 'FeatureCollection',
        'features': []
    }
    
    # Nama kelas default dari model YOLO COCO[cite: 2]
    class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat'] 
    
    for det in geo_detections:
        # Batasi hanya mendeteksi mobil/kendaraan (class 2) untuk simulasi
        if det['properties']['class'] <= 8: 
            feature = {
                'type': 'Feature',
                'geometry': det['geometry'],
                'properties': {
                    'class_id': det['properties']['class'],
                    'class_name': class_names[det['properties']['class']] if det['properties']['class'] < len(class_names) else "object",
                    'confidence': round(det['properties']['confidence'], 3)
                }
            }
            geojson['features'].append(feature)
            
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    print(f"Selesai! {len(geojson['features'])} objek berhasil diekspor ke {output_path}")

# ================= EKSEKUSI PIPELINE =================
if __name__ == "__main__":
    # 1. Siapkan model pretrained YOLOv8 Nano (paling cepat)[cite: 2]
    model_yolo = YOLO('yolov8n.pt') 
    
    # 2. Ganti ini dengan nama file citra GeoTIFF kamu
    FILE_CITRA = 'sample_aerial.tif' 
    FILE_OUTPUT = 'hasil_deteksi.geojson'
    
    try:
        # Jalankan 3 tahap utama
        deteksi_piksel = detect_large_image(FILE_CITRA, model_yolo)
        deteksi_geo = pixel_to_geo(FILE_CITRA, deteksi_piksel)
        export_to_geojson(deteksi_geo, FILE_OUTPUT)
    except FileNotFoundError:
        print(f"ERROR: File citra '{FILE_CITRA}' tidak ditemukan di folder ini.")