from telethon.sync import TelegramClient
import cv2
import os
from deepface import DeepFace
import math

# Configurazione
api_id = '' 
api_hash = ''
phone_number = ''
chat_name = ''
reference_image_path = "reference.jpg"

# Cartelle organizzate
download_folder = "videos_temp"
output_folder = "matched_videos"
os.makedirs(download_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Limiti configurabili
MAX_TOTAL_SIZE = 50  # GB
VIDEO_LIMIT = None  # Numero massimo video (None=illimitato)

client = TelegramClient('session_name', api_id, api_hash)

def convert_size(size_bytes):
    """Converti bytes in GB/MB"""
    if size_bytes == 0:
        return "0B"
    units = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    return f"{round(size_bytes / (1024 ** i), 2)}{units[i]}"

async def download_all_videos():
    """FASE 1: Scarica TUTTI i video"""
    await client.start(phone_number)
    total_size = 0
    
    async for message in client.iter_messages(chat_name, limit=VIDEO_LIMIT):
        if message.video:
            video_size = message.video.size
            
            if MAX_TOTAL_SIZE and (total_size + video_size) > MAX_TOTAL_SIZE * 1024**3:
                print(f"⚠️ Raggiunto limite di {MAX_TOTAL_SIZE}GB. Interruzione.")
                break
                
            video_path = os.path.join(download_folder, f"{message.id}.mp4")
            
            if not os.path.exists(video_path):
                await message.download_media(file=video_path)
                total_size += video_size
                print(f"📥 Scaricato: {os.path.basename(video_path)} - {convert_size(video_size)} (Totale: {convert_size(total_size)})")
    
    await client.disconnect()
    return total_size

def analyze_videos():
    """FASE 2: Analisi offline"""
    matched_count = 0
    
    for video_file in os.listdir(download_folder):
        video_path = os.path.join(download_folder, video_file)
        
        try:
            if analyze_single_video(video_path):
                matched_count += 1
                # Sposta il video positivo
                os.rename(video_path, os.path.join(output_folder, video_file))
            else:
                os.remove(video_path)  # Cancella i negativi
        except Exception as e:
            print(f"⚠️ Errore con {video_file}: {str(e)}")
    
    print(f"✅ Analisi completata. Video corrispondenti: {matched_count}")

def analyze_single_video(video_path):
    """Analizza un singolo video"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % int(fps * 5) == 0:  # Analizza 1 frame ogni 5 secondi
            temp_frame = "temp_frame.jpg"
            cv2.imwrite(temp_frame, frame)
            
            try:
                result = DeepFace.verify(
                    img1_path=temp_frame,
                    img2_path=reference_image_path,
                    enforce_detection=False
                )
                if result["verified"]:
                    return True
            finally:
                if os.path.exists(temp_frame):
                    os.remove(temp_frame)
                    
        frame_count += 1
        
    cap.release()
    return False

# Esecuzione
print("=== FASE 1: Download ===")
with client:
    total_downloaded = client.loop.run_until_complete(download_all_videos())

print(f"\n=== FASE 2: Analisi ({convert_size(total_downloaded)} da processare) ===")
analyze_videos()
