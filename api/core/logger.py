import logging
import sys

# Flag para garantir que o logging seja configurado apenas uma vez
_logging_configured = False


def setup_logging():
    """
    Configura o sistema de logging para enviar logs para stdout/stderr.
    Isso permite que os logs sejam capturados pelo Docker container.
    """
    global _logging_configured

    if _logging_configured:
        return

    # Configurar formato de log
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configurar logging básico
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout)  # Envia logs para stdout (capturado pelo Docker)
        ],
        force=True  # Força reconfiguração se já foi configurado antes
    )

    _logging_configured = True


# Criar instância do logger para SerpAPI
# O setup será feito quando o módulo for importado ou quando setup_logging() for chamado
setup_logging()
serpapi_logger = logging.getLogger("serpapi")
serpapi_logger.setLevel(logging.INFO)

