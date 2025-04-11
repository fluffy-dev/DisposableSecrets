"""Database helper module for managing SQLAlchemy sessions."""

import logging
from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncEngine,
)

# Use absolute imports
from src.core.config import settings

logger = logging.getLogger(__name__)

class DatabaseHelper:
    """
    Manages asynchronous database sessions using SQLAlchemy.

    Provides methods to get scoped sessions or sessions via an async context manager.
    """
    def __init__(self, url: str, echo: bool = False):
        """
        Initializes the DatabaseHelper.

        Args:
            url: The database connection URL.
            echo: If True, SQLAlchemy engine will log all statements.
        """
        logger.info("Initializing DatabaseHelper...")
        try:
            self.engine: AsyncEngine = create_async_engine(url=url, echo=echo)
            logger.debug(f"Async engine created for URL: {'***' if 'password' in url else url}") # Avoid logging full URL with password
        except Exception as e:
            logger.exception(f"Failed to create async engine: {e}")
            raise

        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession, # Ensure it uses AsyncSession
        )
        logger.debug("Async session factory configured.")

    def get_scoped_session(self) -> async_scoped_session[AsyncSession]:
        """
        Returns an async scoped session factory.

        The session scope is tied to the current asyncio task.

        Returns:
            An async_scoped_session instance.
        """
        logger.debug("Creating scoped session.")
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Provides an AsyncSession via an async context manager.

        Ensures the session is closed and rolls back on SQLAlchemy errors.
        This is suitable for manual session management within specific functions.

        Yields:
            An AsyncSession instance.

        Raises:
            SQLAlchemyError: If a database error occurs during the session.
        """
        session: AsyncSession = self.session_factory()
        logger.debug(f"Session {id(session)} created via context manager.")
        try:
            yield session
        except SQLAlchemyError as e:
            logger.exception(f"Session {id(session)} rollback because of SQLAlchemyError: {e}")
            await session.rollback()
            raise # Re-raise the original SQLAlchemyError
        except Exception as e:
            logger.exception(f"Session {id(session)} rollback because of generic exception: {e}")
            await session.rollback()
            raise # Re-raise other exceptions too
        finally:
            await session.close()
            logger.debug(f"Session {id(session)} closed.")

    # This generator is intended for use with FastAPI's Depends
    async def get_session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Provides an AsyncSession as a FastAPI dependency.

        Ensures the session is closed after the request.
        Rollback/commit logic should be handled elsewhere (e.g., middleware or endpoint).

        Yields:
            An AsyncSession instance.
        """
        session: AsyncSession = self.session_factory()
        logger.debug(f"Session {id(session)} created for dependency.")
        try:
            yield session
        finally:
            await session.close()
            logger.debug(f"Session {id(session)} closed by dependency.")


# --- Global Instance ---
# Initialize the helper using settings from the core config
# Ensure settings.DATABASE_URL is correctly formed (e.g., in core/config.py)
try:
    db_helper = DatabaseHelper(
        url=str(settings.DATABASE_URL), # Ensure it's a string
        echo=settings.DB_ECHO_LOG # Assuming DB_ECHO_LOG is defined in settings
    )
    logger.info("DatabaseHelper instance created successfully.")
except AttributeError:
    logger.error("DB_ECHO_LOG setting not found. Defaulting to False.")
    db_helper = DatabaseHelper(url=str(settings.DATABASE_URL), echo=False)
except Exception as e:
     logger.critical(f"Failed to initialize DatabaseHelper. Application might not work correctly. Error: {e}", exc_info=True)
     # Depending on the application, you might want to exit here or handle it differently
     db_helper = None # Or a dummy object