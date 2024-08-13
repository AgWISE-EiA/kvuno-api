import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(verbose=True)


class MyDb:
    db_engine = None
    db_url: str = os.getenv("DB_URL")
    debug_db = os.getenv('DEBUG_DB') == '1'

    def __new__(cls, *args, **kwargs):
        if cls.db_engine is None:
            cls.db_engine = create_engine(
                url=cls.db_url,
                echo=cls.debug_db,
                echo_pool=cls.debug_db,
                hide_parameters=not cls.debug_db,
            )

        return cls.db_engine
