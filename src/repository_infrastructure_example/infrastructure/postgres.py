import subprocess
from collections.abc import Generator
from contextlib import contextmanager
from typing import Final

from loguru import logger
from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlmodel import Session, create_engine

# Database Configuration
_DATABASE_ECHO: Final[bool] = False
_DATABASE_POOL_PRE_PING: Final[bool] = True
_DATABASE_POOL_RECYCLE: Final[int] = -1
_DATABASE_POOL_TIMEOUT: Final[int] = 30
_DATABASE_EXPIRE_ON_COMMIT: Final[bool] = False


class PostgresConnectionError(ConnectionError):
    """Raised when there is an error in establishing a connection to Postgres."""


class PostgresClient:
    _engine: Engine
    _session_factory: scoped_session[Session]

    _instances: dict[str, PostgresClient] = {}
    _initialized: bool = False

    def __new__(cls, connection_string: str) -> "PostgresClient":
        if connection_string not in cls._instances:
            cls._instances[connection_string] = super().__new__(cls)
        return cls._instances[connection_string]

    def __init__(self, connection_string: str) -> None:
        if self._initialized:
            return

        self._engine = create_engine(
            connection_string,
            echo=_DATABASE_ECHO,
            pool_pre_ping=_DATABASE_POOL_PRE_PING,
            pool_recycle=_DATABASE_POOL_RECYCLE,
            pool_timeout=_DATABASE_POOL_TIMEOUT,
        )

        self._session_factory = scoped_session(
            sessionmaker(
                expire_on_commit=_DATABASE_EXPIRE_ON_COMMIT,
                bind=self._engine,
                class_=Session,
            ),
        )

        self.check_health()
        self._initialized = True

    def check_health(self) -> None:
        """
        Check if the database connection is healthy.

        :return: None
        :raises DatabaseConnectionError: If the connection cannot be established.
        """
        try:
            self._engine.connect()
        except SQLAlchemyError as e:
            raise PostgresConnectionError(
                f"Cannot connect to database: {str(e.__cause__)}"
            )

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope around a series of operations.
        Automatically commits or rollbacks the session.

        :yield: SQLAlchemy Session object.
        :raises: Rolls back the session in case of an exception.
        """
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as error:
            logger.critical(f"Session rollback because of exception: {error}")
            session.rollback()
            raise
        else:
            session.commit()
        finally:
            session.close()

    @staticmethod
    def run_migrations(disable_logging: bool = False) -> None:
        """
        Run database migrations using Alembic.

        Note: This method runs Alembic in a subprocess to avoid interfering with
        existing loggers in the current process.

        :param disable_logging: Whether to disable logging during migration.
            Defaults to False.
        :return: None
        :raises RuntimeError: If the migration process fails.
        """
        if not disable_logging:
            logger.info("Running database migrations...")

        try:
            result = subprocess.run(
                ["alembic", "upgrade", "head"],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as error:
            stdout = error.stdout.strip() if error.stdout else "No output"
            stderr = error.stderr.strip() if error.stderr else "No error output"

            if not disable_logging:
                logger.critical(
                    f"Alembic migration failed (exit code {error.returncode})\n"
                    f"stdout:\n{stdout}\n"
                    f"stderr:\n{stderr}"
                )

            raise RuntimeError("Database migration failed") from error

        if not disable_logging:
            logger.info(f"Alembic Output:\n{result.stderr.strip()}")
            logger.success("Database migrations completed successfully.")
