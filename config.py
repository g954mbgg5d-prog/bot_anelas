from pathlib import Path

# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

DATABASE_PATH = DATA_DIR / "tweets.db"

# ==================================================
# GOOGLE SHEETS
# ==================================================

SHEET_ID = "1Gad0WkvXNqMTcFnFlTzheTYSL42qNmZP"

GIDS = {
    "substantivos": "770008533",
    "adjetivos": "650797730",
    "verbos": "1308759085",
    "frases": "376019489",
    "chamada": "595278995",
    "templates": "1351279715",
    "lugares": "743943434",
    "coisas": "1073598073",
    "comidas": "340777854",
}

# ==================================================
# FILA
# ==================================================

MAX_QUEUE_SIZE = 5

# ==================================================
# SCHEDULER
# ==================================================

LOOP_INTERVAL_SECONDS = 60

# Atualizar planilha a cada 30 minutos
SHEETS_SYNC_INTERVAL_MINUTES = 30

# ==================================================
# LOGGING
# ==================================================

LOG_LEVEL = "INFO"

# ==================================================
# STATUS DOS TWEETS
# ==================================================

STATUS_PENDING = "pending"
STATUS_PUBLISHED = "published"
STATUS_DISCARDED = "discarded"
