# Query-to-SQL Application

Un'applicazione web che converte domande in linguaggio naturale in query SQL utilizzando un modello di intelligenza artificiale locale (Ollama) e gestisce un database di film.

## 🎯 Descrizione

Questa applicazione permette agli utenti di interrogare un database di film attraverso domande in linguaggio naturale. Utilizza un modello AI locale (Gemma 3:1B) per convertire le domande in query SQL, garantendo sicurezza e validazione delle query prima dell'esecuzione.

## 🏗️ Architettura

L'applicazione è strutturata in microservizi containerizzati con Docker:

- **Frontend**: Interfaccia web in Python/FastAPI con template HTML
- **Backend**: API REST in Python/FastAPI per la logica di business
- **Database**: MariaDB per la persistenza dei dati
- **Ollama**: Servizio per l'esecuzione del modello AI locale

## 🚀 Funzionalità

### 🔍 Ricerca con AI
- Conversione di domande in linguaggio naturale in query SQL
- Utilizzo del modello Gemma 3:1B instruction-tuned
- Validazione automatica delle query SQL per sicurezza

### 🎬 Gestione Film
- Database pre-popolato con film di esempio
- Aggiunta di nuovi film
- Ricerca avanzata tramite query SQL dirette

### 🛡️ Sicurezza
- Validazione delle query SQL per prevenire operazioni pericolose
- Blocco di comandi DROP, DELETE, UPDATE, INSERT, CREATE, ALTER, TRUNCATE
- Controllo degli accessi al database

## 📊 Schema Database

La tabella `movies` contiene i seguenti campi:
- `titolo`: Titolo del film
- `regista`: Nome del regista
- `eta_autore`: Età del regista
- `anno`: Anno di uscita
- `genere`: Genere cinematografico
- `piattaforma_1`: Prima piattaforma di streaming
- `piattaforma_2`: Seconda piattaforma di streaming

## 🛠️ Tecnologie Utilizzate

- **Backend**: Python, FastAPI, MariaDB
- **Frontend**: HTML, CSS, JavaScript, Jinja2
- **AI**: Ollama, Gemma 3:1B instruction-tuned model
- **Containerizzazione**: Docker, Docker Compose
- **Database**: MariaDB 11.7.2

## 📋 Prerequisiti

- Docker e Docker Compose installati
- Almeno 4GB di RAM disponibili per il modello AI
- Connessione internet per il download iniziale del modello

## 🚀 Installazione e Avvio

### 1. Clona il repository
```bash
git clone <repository-url>
cd Query-to-SQL
```

### 2. Avvia i servizi
```bash
docker-compose up -d
```

### 3. Attendi l'inizializzazione
Il servizio Ollama impiegherà alcuni minuti per scaricare e inizializzare il modello AI.

### 4. Accedi all'applicazione
- Frontend: http://localhost:8000
- Backend API: http://localhost:8003
- Ollama API: http://localhost:11434

## 📱 Utilizzo

### Interfaccia Web
1. Apri http://localhost:8000 nel browser
2. Utilizza la sezione "Ricerca con AI" per porre domande in linguaggio naturale
3. Visualizza i risultati e la query SQL generata
4. Usa la sezione "Query SQL Diretta" per eseguire query personalizzate

### Esempi di Domande
- "Mostra tutti i film di Christopher Nolan"
- "Quali film sono disponibili su Netflix?"
- "Film di fantascienza usciti dopo il 2010"
- "Registi nati prima del 1960"

### API Endpoints

#### Frontend
- `GET /` - Interfaccia principale
- `POST /api/llm_search` - Ricerca con AI
- `POST /api/add_movie` - Aggiunta film
- `GET /api/schema` - Schema database
- `POST /api/sql_search` - Ricerca SQL diretta

#### Backend
- `POST /search` - Conversione domanda in SQL
- `POST /add` - Aggiunta film al database
- `GET /schema_summary` - Schema database
- `POST /sql_search` - Esecuzione query SQL

## 🔧 Configurazione

### Variabili d'Ambiente
Le configurazioni del database sono gestite tramite variabili d'ambiente nel `docker-compose.yaml`:

```yaml
environment:
  - DB_HOST=database
  - DB_PORT=3306
  - DB_NAME=database
  - DB_USER=user
  - DB_PASSWORD=password
```

### Modello AI
Il modello utilizzato è configurato in `backend/backend.py`:
```python
OLLAMA_MODEL = "gemma3:1b-it-qat"
```

## 📁 Struttura del Progetto

```
Query-to-SQL/
├── backend/                 # Servizio backend
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/backend/
│       └── backend.py
├── frontend/               # Servizio frontend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src/frontend/
│   │   └── frontend.py
│   └── templates/
│       └── index.html
├── mariadb_init/           # Script di inizializzazione DB
│   └── init.sql
├── text_to_sql/           # Servizio Ollama
│   ├── Dockerfile
│   └── init_model.sh
├── docker-compose.yaml     # Orchestrazione servizi
└── README.md
```

## 🧪 Testing

### Health Check
I servizi includono health check automatici:
- Frontend: http://localhost:8000
- Backend: http://localhost:8003
- Database: Controllo connessione MariaDB
- Ollama: http://localhost:11434/api/tags

### Logs
```bash
# Visualizza logs di tutti i servizi
docker-compose logs

# Logs di un servizio specifico
docker-compose logs frontend
docker-compose logs backend
docker-compose logs ollama
```

## 🚨 Troubleshooting

### Problemi Comuni

1. **Modello AI non disponibile**
   - Verifica che Ollama sia in esecuzione: `docker-compose ps ollama`
   - Controlla i logs: `docker-compose logs ollama`

2. **Database non raggiungibile**
   - Verifica la connessione: `docker-compose exec database mysql -u root -p`
   - Controlla i logs: `docker-compose logs database`

3. **Porte già in uso**
   - Modifica le porte nel `docker-compose.yaml`
   - Verifica processi in ascolto: `lsof -i :8000`

### Riavvio Servizi
```bash
# Riavvia tutti i servizi
docker-compose restart

# Riavvia un servizio specifico
docker-compose restart ollama
```

## 🔒 Sicurezza

- Le query SQL vengono validate prima dell'esecuzione
- Operazioni pericolose (DROP, DELETE, UPDATE, etc.) sono bloccate
- L'applicazione è configurata per uso locale/development

## 📈 Performance

- Il modello AI locale riduce la latenza di rete
- Query database ottimizzate con indici appropriati
- Health check automatici per monitoraggio servizi

## 🤝 Contributi

Per contribuire al progetto:
1. Fork del repository
2. Creazione di un branch per la feature
3. Commit delle modifiche
4. Push e creazione di una Pull Request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT.

## 📞 Supporto

Per supporto tecnico o domande:
- Apri una issue su GitHub
- Contatta il team di sviluppo

---

**Nota**: Questa applicazione è progettata per scopi educativi e di sviluppo. Per uso in produzione, considerare implementazioni di sicurezza aggiuntive. 