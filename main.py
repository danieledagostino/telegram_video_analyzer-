import json
import argparse
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeVideo, DocumentAttributeFilename
import cv2
import os
from deepface import DeepFace
import math
import time
from datetime import datetime

# Caricamento configurazione
with open('config.json') as f:
    config = json.load(f)

# Inizializzazione client Telegram
client = TelegramClient(
    'session_name',
    config['telegram']['api_id'],
    config['telegram']['api_hash']
)

def convert_size(size_bytes):
    """Converti bytes in GB/MB"""
    if size_bytes == 0:
        return "0B"
    units = ("B", "KB", "MB", "GB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    return f"{round(size_bytes / (1024 ** i), 2)}{units[i]}"

def load_download_status():
    """Carica lo stato dei download"""
    if not os.path.exists(config['storage']['log_file']):
        return {'downloaded': {}, 'last_message_id': None}
    
    with open(config['storage']['log_file'], 'r') as f:
        return json.load(f)

def save_download_status(status):
    """Salva lo stato dei download"""
    with open(config['storage']['log_file'], 'w') as f:
        json.dump(status, f, indent=2)

def is_video_message(message):
    """Controlla se il messaggio contiene un video"""
    if message.video:
        return True
    if message.document:
        for attr in message.document.attributes:
            if isinstance(attr, (DocumentAttributeVideo, DocumentAttributeFilename)):
                return True
    return False

async def download_videos(resume=False):
    """Scarica i video dalla chat"""
    await client.start(config['telegram']['phone_number'])
    status = load_download_status()
    total_size = sum(int(v['size']) for v in status['downloaded'].values())
    
    request_params = {
        'entity': config['telegram']['chat_name'],
        'limit': None
    }
    
    if resume and status['last_message_id']:
        request_params['offset_id'] = status['last_message_id']
    
    async for message in client.iter_messages(**request_params):
        try:
            if not is_video_message(message):
                continue
                
            # Ottieni la dimensione in modo sicuro
            media = message.video or message.document
            if not media:
                continue
                
            video_size = media.size
            video_date = message.date.strftime('%Y-%m-%d_%H-%M-%S')
            video_name = f"{video_date}_{message.id}.mp4"
            video_path = os.path.join(config['storage']['download_folder'], video_name)
            
            if str(message.id) in status['downloaded']:
                continue
                
            # Controllo spazio disco
            if (total_size + video_size) > config['storage']['max_size_gb'] * 1024**3:
                print(f"⚠️ Raggiunto limite di {config['storage']['max_size_gb']}GB")
                break
                
            await message.download_media(file=video_path)
            status['downloaded'][str(message.id)] = {
                'name': video_name,
                'size': video_size,
                'date': video_date,
                'analyzed': False
            }
            status['last_message_id'] = message.id
            total_size += video_size
            
            print(f"📥 [{video_date}] Scaricato: {video_name} - {convert_size(video_size)}")
            save_download_status(status)
            
        except Exception as e:
            print(f"⚠️ Errore durante il processing del messaggio {message.id}: {str(e)}")
            time.sleep(5)
    
    await client.disconnect()

def analyze_videos():
    """Analizza i video scaricati"""
    status = load_download_status()
    analyzed_count = 0
    
    for video_id, video_info in status['downloaded'].items():
        if not video_info['analyzed']:
            video_path = os.path.join(
                config['storage']['download_folder'],
                video_info['name']
            )
            
            try:
                print(f"🔍 Analisi {video_info['name']}...")
                if analyze_single_video(video_path):
                    os.rename(
                        video_path,
                        os.path.join(config['storage']['output_folder'], video_info['name'])
                    )
                    analyzed_count += 1
                    print(f"✅ Trovata corrispondenza in {video_info['name']}")
                else:
                    os.remove(video_path)
                
                video_info['analyzed'] = True
                save_download_status(status)
                
            except Exception as e:
                print(f"⚠️ Errore analisi {video_info['name']}: {str(e)}")
                time.sleep(2)
    
    print(f"✅ Analisi completata. Video corrispondenti: {analyzed_count}")

def analyze_single_video(video_path):
    """Analizza un singolo video"""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % int(fps * config['analysis']['frame_interval']) == 0:
            temp_frame = "temp_frame.jpg"
            cv2.imwrite(temp_frame, frame)
            
            try:
                result = DeepFace.verify(
                    img1_path=temp_frame,
                    img2_path=config['analysis']['reference_image'],
                    enforce_detection=False
                )
                if result["verified"] and result["distance"] < (1 - config['analysis']['min_confidence']):
                    return True
            finally:
                if os.path.exists(temp_frame):
                    os.remove(temp_frame)
                    
        frame_count += 1
        
    cap.release()
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['new', 'resume', 'analyze'], required=True,
                       help="Modalità esecuzione: new (scarica tutto), resume (continua download), analyze (solo analisi)")
    args = parser.parse_args()

    # Crea cartelle se mancanti
    os.makedirs(config['storage']['download_folder'], exist_ok=True)
    os.makedirs(config['storage']['output_folder'], exist_ok=True)

    if args.mode in ['new', 'resume']:
        print("=== FASE DOWNLOAD ===")
        with client:
            client.loop.run_until_complete(download_videos(resume=(args.mode == 'resume')))

    if args.mode in ['new', 'resume', 'analyze']:
        print("\n=== FASE ANALISI ===")
        analyze_videos()
