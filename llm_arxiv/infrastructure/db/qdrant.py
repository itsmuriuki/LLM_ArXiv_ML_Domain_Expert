from loguru import logger
from qdrant_client import QdrantClient

from llm_arxiv.settings import settings


class QdrantConnector:
    _instance: QdrantClient | None = None

    def __new__(cls, *args, **kwargs) -> QdrantClient:
        if cls._instance is None:
            try:
                if settings.USE_QDRANT_CLOUD and settings.QDRANT_CLOUD_URL:
                    cls._instance = QdrantClient(url=settings.QDRANT_CLOUD_URL, api_key=settings.QDRANT_APIKEY)
                    logger.info("Initialized Qdrant cloud client")
                else:
                    cls._instance = QdrantClient(host=settings.QDRANT_DATABASE_HOST, port=settings.QDRANT_DATABASE_PORT)
                    logger.info(
                        f"Initialized Qdrant local client at {settings.QDRANT_DATABASE_HOST}:{settings.QDRANT_DATABASE_PORT}"
                    )

                # Probe connection
                cls._instance.get_collections()
                logger.info("Connection to Qdrant successful")
            except Exception as e:
                logger.error(f"Couldn't connect to Qdrant: {e!s}")
                raise

        return cls._instance


connection = QdrantConnector()