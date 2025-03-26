Ecco il file `README.md` aggiornato con le istruzioni per Ubuntu e il comando `caffeinate`:

```markdown
# Telegram Video Analyzer 🔍

Un sistema avanzato per scaricare e analizzare video da Telegram con riconoscimento facciale.

## 🛠️ Installazione su Ubuntu

```bash
# 1. Installa le dipendenze di sistema
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# 2. Clona il repository
git clone https://github.com/tuoutente/telegram-video-analyzer.git
cd telegram-video-analyzer

# 3. Crea e attiva l'ambiente virtuale
python3 -m venv venv
source venv/bin/activate

# 4. Installa le dipendenze Python
pip install -r requirements.txt

# 5. Installa caffeinate (per prevenire sospensioni)
sudo apt install -y caffeine
```

## 🚀 Avvio del Programma

**Modalità base:**
```bash
python3 main.py --mode new
```

**Con prevenzione sospensione (macOS):**
```bash
caffeinate -d -s -i $(python3 main.py --mode new)
```

**Su Ubuntu (usando caffeine):**
```bash
# Avvia caffeine in background
caffeine &

# Poi esegui lo script
python3 main.py --mode new

# Disattiva caffeine quando completato
pkill caffeine
```

## 🔧 Parametri di Esecuzione

| Parametro   | Descrizione                                  | Esempio                     |
|-------------|----------------------------------------------|-----------------------------|
| `--mode`    | Modalità operativa (new/resume/analyze)      | `--mode resume`             |
| `--notify`  | Notifiche desktop (richiede `libnotify-bin`) | `--mode new --notify`       |

## 🛑 Prevenzione Sospensione

Per sessioni lunghe:

**macOS:**
```bash
caffeinate -d -s -i $(python3 main.py --mode new)
```

**Ubuntu:**
```bash
# Metodo 1 - caffeine
sudo apt install caffeine
caffeine &

# Metodo 2 - systemd
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

**Disattivare dopo l'uso (Ubuntu):**
```bash
sudo systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

## 📌 Note Importanti

1. Per Ubuntu 22.04+ potrebbe essere necessario:
```bash
sudo apt install python3-tk
```

2. Se usi GNOME:
```bash
# Previene sospensione durante l'esecuzione
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout 0
```

3. Per monitorare lo stato:
```bash
watch -n 1 "du -sh videos_temp/; ls -1 videos_temp/ | wc -l"
```

## 🌟 Funzionalità Aggiuntive

- **Notifiche desktop** (Ubuntu):
```bash
sudo apt install libnotify-bin
python3 main.py --mode new --notify
```

- **Avvio in background**:
```bash
nohup python3 main.py --mode new > output.log 2>&1 &
```

Aggiornato con:
- Comandi specifici per Ubuntu
- Istruzioni complete per caffeinate/caffeine
- Soluzioni per prevenire sospensioni
- Comandi di monitoraggio
- Opzioni per notifiche desktop
```

### Novità principali:
1. **Sezione Ubuntu** completa con tutti i pacchetti necessari
2. **Istruzioni caffeine** per entrambi i sistemi operativi
3. **Comandi di monitoraggio** durante l'esecuzione
4. **Soluzioni GNOME** specifiche
5. **Opzioni avanzate** per esecuzione in background

### Per completare:
1. Sostituisci `tuoutente` con il tuo nome utente GitHub
2. Aggiungi eventuali note specifiche per il tuo caso d'uso
3. Personalizza le sezioni avanzate in base alle tue esigenze
