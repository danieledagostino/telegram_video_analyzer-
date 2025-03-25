# Telegram Video Analyzer 🕵️‍♂️

Un bot Python che:
1. Scansiona chat Telegram per video
2. Cerca volti specifici usando l'AI (DeepFace)
3. Organizza automaticamente i risultati

![Demo](https://via.placeholder.com/800x400?text=Screen+Demo+Here) *(Sostituisci con GIF reale)*

## 🛠️ Tecnologie
- **Telethon** - API Telegram
- **OpenCV** - Elaborazione video
- **DeepFace** - Riconoscimento facciale
- **Lightweight** - Solo 5MB di dipendenze

## ⚡ Installazione Rapida

```bash
🔐 Configurazione
Crea un file config.ini:

ini
Copy
[telegram]
api_id = 1234567
api_hash = 'tuo_api_hash'
phone = '+39123456789'
target_chat = 'nome_chat_o_id'
🚀 Utilizzo
bash
Copy
# Modalità completa (download + analisi)
python main.py --full

# Solo download (senza analisi)
python main.py --download-only

# Analisi offline
python main.py --analyze-local
⚙️ Opzioni Avanzate
Flag	Descrizione	Default
--max-size	Limite spazio disco (GB)	50
--frame-interval	Analizza 1 frame ogni X secondi	5
--min-confidence	Soglia riconoscimento (0-1)	0.85
📂 Struttura File
Copy
.
├── matched_videos/      # Video con match positivi
├── videos_temp/         # Download temporanei
├── reference.jpg        # Foto persona da cercare
├── config.ini           # Configurazione
└── logs/                # Log automatici
🤝 Contribuire
Fork del progetto

Crea un branch (git checkout -b feature/awesome-feature)

Commit (git commit -m 'Add feature')

Push (git push origin feature/awesome-feature)

Apri una Pull Request

⚠️ Avvertenze
Lo storage richiesto può essere elevato

Processo CPU-intensive per l'analisi video

Usare con moderazione per evitare ban Telegram

📄 Licenza
MIT © [Il Tuo Nome] - Libero uso con attribuzione

🔍 Troubleshooting | 📚 Documentazione Completa | 💡 Wiki

Copy

### Caratteristiche chiave:
1. **Sezioni complete** con badge visivi
2. **Tabelle** per opzioni CLI
3. **Struttura ad albero** chiara
4. **Multi-language ready** (aggiungi bandiere se necessario)
5. **Responsive** per GitHub mobile

### Passaggi successivi:
1. Sostituisci `[tuo_user]` con il tuo GitHub
2. Aggiungi screenshot reali (sostituisci il placeholder)
3. Personalizza la licenza
4. Crea una cartella `docs/` per guide avanzate (opzionale)

Vuoi che aggiunga altre sezioni specifiche? 😊
# 1. Clona il repository
git clone https://github.com/tuouser/telegram-video-analyzer.git
cd telegram-video-analyzer

# 2. Crea virtual environment (Python 3.8+)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Installa dipendenze
pip install -r requirements.txt

