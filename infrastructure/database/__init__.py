"""
Database Infrastructure Layer
Connection pooling, repositories, and data access patterns
"""

from typing import Optional, Dict, Any, List, TypeVar, Generic
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Type variable for generic repository
T = TypeVar('T')


@dataclass
class DatabaseConfig:
    """Database connection configuration"""
    host: str
    port: int
    database: str
    user: str
    password: str
    min_connections: int = 1
    max_connections: int = 10
    ssl_mode: str = "require"
    
    @property
    def connection_string(self) -> str:
        """Generate PostgreSQL connection string"""
        return (
            f"postgresql://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
            f"?sslmode={self.ssl_mode}"
        )


class ConnectionPool:
    """
    Database connection pool manager
    Handles connection lifecycle and pooling
    """
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._pool = None
        self._initialized = False
        
    def initialize(self) -> bool:
        """Initialize the connection pool"""
        try:
            import psycopg2
            from psycopg2 import pool
            
            self._pool = pool.ThreadedConnectionPool(
                self.config.min_connections,
                self.config.max_connections,
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                sslmode=self.config.ssl_mode
            )
            self._initialized = True
            logger.info("Database connection pool initialized successfully")
            return True
            
        except ImportError:
            logger.warning("psycopg2 not available - database features disabled")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            return False
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for getting database connections
        Automatically returns connection to pool on exit
        """
        if not self._initialized or not self._pool:
            raise RuntimeError("Connection pool not initialized")
        
        conn = None
        try:
            conn = self._pool.getconn()
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                self._pool.putconn(conn)
    
    @contextmanager
    def get_cursor(self, commit: bool = True):
        """
        Context manager for getting database cursor
        Handles commit/rollback automatically
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                if commit:
                    conn.commit()
            except Exception as e:
                conn.rollback()
                raise
            finally:
                cursor.close()
    
    def execute(self, query: str, params: tuple = None) -> Optional[List[tuple]]:
        """Execute a query and return results"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:
                return cursor.fetchall()
            return None
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute a query with multiple parameter sets"""
        with self.get_cursor() as cursor:
            cursor.executemany(query, params_list)
            return cursor.rowcount
    
    def close(self):
        """Close all connections in the pool"""
        if self._pool:
            self._pool.closeall()
            self._initialized = False
            logger.info("Database connection pool closed")
    
    @property
    def is_available(self) -> bool:
        """Check if database is available"""
        return self._initialized and self._pool is not None


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository implementing common CRUD operations
    Follows Repository Pattern for data access abstraction
    """
    
    def __init__(self, pool: ConnectionPool, table_name: str):
        self.pool = pool
        self.table_name = table_name
    
    @abstractmethod
    def _row_to_entity(self, row: tuple) -> T:
        """Convert database row to domain entity"""
        pass
    
    @abstractmethod
    def _entity_to_params(self, entity: T) -> Dict[str, Any]:
        """Convert domain entity to database parameters"""
        pass
    
    def find_by_id(self, id: Any) -> Optional[T]:
        """Find entity by primary key"""
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        results = self.pool.execute(query, (id,))
        if results:
            return self._row_to_entity(results[0])
        return None
    
    def find_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """Find all entities with pagination"""
        query = f"SELECT * FROM {self.table_name} ORDER BY id LIMIT %s OFFSET %s"
        results = self.pool.execute(query, (limit, offset))
        return [self._row_to_entity(row) for row in (results or [])]
    
    def count(self) -> int:
        """Count all entities"""
        query = f"SELECT COUNT(*) FROM {self.table_name}"
        results = self.pool.execute(query)
        return results[0][0] if results else 0
    
    def exists(self, id: Any) -> bool:
        """Check if entity exists"""
        query = f"SELECT 1 FROM {self.table_name} WHERE id = %s LIMIT 1"
        results = self.pool.execute(query, (id,))
        return bool(results)
    
    def delete(self, id: Any) -> bool:
        """Delete entity by id"""
        query = f"DELETE FROM {self.table_name} WHERE id = %s"
        with self.pool.get_cursor() as cursor:
            cursor.execute(query, (id,))
            return cursor.rowcount > 0


class QueryBuilder:
    """
    Fluent query builder for complex queries
    Provides type-safe query construction
    """
    
    def __init__(self, table: str):
        self.table = table
        self._select = "*"
        self._where: List[str] = []
        self._params: List[Any] = []
        self._order_by: Optional[str] = None
        self._limit: Optional[int] = None
        self._offset: Optional[int] = None
        self._joins: List[str] = []
    
    def select(self, *columns: str) -> 'QueryBuilder':
        """Specify columns to select"""
        self._select = ", ".join(columns) if columns else "*"
        return self
    
    def where(self, condition: str, *params) -> 'QueryBuilder':
        """Add WHERE condition"""
        self._where.append(condition)
        self._params.extend(params)
        return self
    
    def where_equals(self, column: str, value: Any) -> 'QueryBuilder':
        """Add WHERE column = value condition"""
        return self.where(f"{column} = %s", value)
    
    def where_in(self, column: str, values: List[Any]) -> 'QueryBuilder':
        """Add WHERE column IN (...) condition"""
        placeholders = ", ".join(["%s"] * len(values))
        return self.where(f"{column} IN ({placeholders})", *values)
    
    def where_like(self, column: str, pattern: str) -> 'QueryBuilder':
        """Add WHERE column LIKE pattern condition"""
        return self.where(f"{column} LIKE %s", f"%{pattern}%")
    
    def where_between(self, column: str, start: Any, end: Any) -> 'QueryBuilder':
        """Add WHERE column BETWEEN start AND end condition"""
        return self.where(f"{column} BETWEEN %s AND %s", start, end)
    
    def join(self, table: str, on: str, join_type: str = "INNER") -> 'QueryBuilder':
        """Add JOIN clause"""
        self._joins.append(f"{join_type} JOIN {table} ON {on}")
        return self
    
    def order_by(self, column: str, direction: str = "ASC") -> 'QueryBuilder':
        """Set ORDER BY clause"""
        self._order_by = f"{column} {direction}"
        return self
    
    def limit(self, limit: int) -> 'QueryBuilder':
        """Set LIMIT"""
        self._limit = limit
        return self
    
    def offset(self, offset: int) -> 'QueryBuilder':
        """Set OFFSET"""
        self._offset = offset
        return self
    
    def build(self) -> tuple:
        """Build the final query and parameters"""
        query_parts = [f"SELECT {self._select} FROM {self.table}"]
        
        if self._joins:
            query_parts.extend(self._joins)
        
        if self._where:
            query_parts.append("WHERE " + " AND ".join(self._where))
        
        if self._order_by:
            query_parts.append(f"ORDER BY {self._order_by}")
        
        if self._limit is not None:
            query_parts.append(f"LIMIT {self._limit}")
        
        if self._offset is not None:
            query_parts.append(f"OFFSET {self._offset}")
        
        return " ".join(query_parts), tuple(self._params)


class MigrationManager:
    """
    Database migration manager
    Handles schema versioning and migrations
    """
    
    def __init__(self, pool: ConnectionPool):
        self.pool = pool
        self._ensure_migrations_table()
    
    def _ensure_migrations_table(self):
        """Create migrations tracking table if not exists"""
        query = """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                version VARCHAR(50) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        try:
            self.pool.execute(query)
        except Exception as e:
            logger.warning(f"Could not create migrations table: {e}")
    
    def get_applied_versions(self) -> List[str]:
        """Get list of applied migration versions"""
        query = "SELECT version FROM schema_migrations ORDER BY version"
        results = self.pool.execute(query)
        return [row[0] for row in (results or [])]
    
    def apply_migration(self, version: str, name: str, sql: str):
        """Apply a migration"""
        applied = self.get_applied_versions()
        if version in applied:
            logger.info(f"Migration {version} already applied")
            return
        
        with self.pool.get_cursor() as cursor:
            # Execute migration SQL
            cursor.execute(sql)
            
            # Record migration
            cursor.execute(
                "INSERT INTO schema_migrations (version, name) VALUES (%s, %s)",
                (version, name)
            )
        
        logger.info(f"Applied migration {version}: {name}")
    
    def rollback_migration(self, version: str, rollback_sql: str):
        """Rollback a migration"""
        with self.pool.get_cursor() as cursor:
            cursor.execute(rollback_sql)
            cursor.execute(
                "DELETE FROM schema_migrations WHERE version = %s",
                (version,)
            )
        
        logger.info(f"Rolled back migration {version}")


# AURIX-specific migrations
AURIX_MIGRATIONS = [
    {
        "version": "001",
        "name": "create_visitor_tables",
        "up": """
            CREATE TABLE IF NOT EXISTS visitor_sessions (
                id SERIAL PRIMARY KEY,
                visitor_id VARCHAR(255) NOT NULL,
                session_start TIMESTAMP NOT NULL,
                session_end TIMESTAMP,
                total_page_views INTEGER DEFAULT 0,
                theme VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS page_views (
                id SERIAL PRIMARY KEY,
                visitor_id VARCHAR(255) NOT NULL,
                page_name VARCHAR(100) NOT NULL,
                view_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_duration INTEGER DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS daily_stats (
                id SERIAL PRIMARY KEY,
                stat_date DATE NOT NULL UNIQUE,
                total_visits INTEGER DEFAULT 0,
                unique_visitors INTEGER DEFAULT 0,
                total_page_views INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_page_views_visitor ON page_views(visitor_id);
            CREATE INDEX IF NOT EXISTS idx_page_views_timestamp ON page_views(view_timestamp);
            CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats(stat_date);
        """,
        "down": """
            DROP TABLE IF EXISTS daily_stats;
            DROP TABLE IF EXISTS page_views;
            DROP TABLE IF EXISTS visitor_sessions;
        """
    },
    {
        "version": "002",
        "name": "create_audit_tables",
        "up": """
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                category VARCHAR(100),
                content_hash VARCHAR(64),
                file_size INTEGER,
                mime_type VARCHAR(100),
                metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS findings (
                id SERIAL PRIMARY KEY,
                finding_id VARCHAR(50) NOT NULL UNIQUE,
                title VARCHAR(255) NOT NULL,
                audit_area VARCHAR(100),
                risk_rating VARCHAR(20),
                category VARCHAR(100),
                description TEXT,
                root_cause TEXT,
                recommendation TEXT,
                management_response TEXT,
                owner VARCHAR(100),
                due_date DATE,
                status VARCHAR(50) DEFAULT 'Open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                closed_at TIMESTAMP,
                metadata JSONB DEFAULT '{}'
            );
            
            CREATE TABLE IF NOT EXISTS risk_assessments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                area VARCHAR(100),
                description TEXT,
                likelihood INTEGER,
                impact INTEGER,
                inherent_score DECIMAL(5,2),
                control_score DECIMAL(5,2),
                residual_score DECIMAL(5,2),
                risk_level VARCHAR(20),
                assessed_by VARCHAR(100),
                assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB DEFAULT '{}'
            );
            
            CREATE TABLE IF NOT EXISTS working_papers (
                id SERIAL PRIMARY KEY,
                reference VARCHAR(50) NOT NULL UNIQUE,
                template_type VARCHAR(100),
                audit_area VARCHAR(100),
                objective TEXT,
                preparer VARCHAR(100),
                reviewer VARCHAR(100),
                content JSONB DEFAULT '{}',
                status VARCHAR(50) DEFAULT 'Draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_findings_status ON findings(status);
            CREATE INDEX IF NOT EXISTS idx_findings_rating ON findings(risk_rating);
            CREATE INDEX IF NOT EXISTS idx_risk_assessments_level ON risk_assessments(risk_level);
        """,
        "down": """
            DROP TABLE IF EXISTS working_papers;
            DROP TABLE IF EXISTS risk_assessments;
            DROP TABLE IF EXISTS findings;
            DROP TABLE IF EXISTS documents;
        """
    },
    {
        "version": "003",
        "name": "create_continuous_audit_tables",
        "up": """
            CREATE TABLE IF NOT EXISTS continuous_audit_rules (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                category VARCHAR(100),
                rule_type VARCHAR(50),
                parameters JSONB DEFAULT '{}',
                threshold TEXT,
                is_active BOOLEAN DEFAULT FALSE,
                trigger_count INTEGER DEFAULT 0,
                last_triggered TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS audit_alerts (
                id SERIAL PRIMARY KEY,
                rule_id INTEGER REFERENCES continuous_audit_rules(id),
                alert_type VARCHAR(50),
                severity VARCHAR(20),
                message TEXT,
                data JSONB DEFAULT '{}',
                is_resolved BOOLEAN DEFAULT FALSE,
                resolved_at TIMESTAMP,
                resolved_by VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS kri_values (
                id SERIAL PRIMARY KEY,
                indicator_name VARCHAR(100) NOT NULL,
                category VARCHAR(100),
                value DECIMAL(15,4),
                threshold DECIMAL(15,4),
                unit VARCHAR(20),
                status VARCHAR(20),
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB DEFAULT '{}'
            );
            
            CREATE INDEX IF NOT EXISTS idx_ca_rules_active ON continuous_audit_rules(is_active);
            CREATE INDEX IF NOT EXISTS idx_alerts_unresolved ON audit_alerts(is_resolved) WHERE NOT is_resolved;
            CREATE INDEX IF NOT EXISTS idx_kri_category ON kri_values(category);
        """,
        "down": """
            DROP TABLE IF EXISTS kri_values;
            DROP TABLE IF EXISTS audit_alerts;
            DROP TABLE IF EXISTS continuous_audit_rules;
        """
    }
]


def run_migrations(pool: ConnectionPool):
    """Run all pending migrations"""
    manager = MigrationManager(pool)
    
    for migration in AURIX_MIGRATIONS:
        try:
            manager.apply_migration(
                migration["version"],
                migration["name"],
                migration["up"]
            )
        except Exception as e:
            logger.error(f"Migration {migration['version']} failed: {e}")
            raise


# Export public API
__all__ = [
    'DatabaseConfig',
    'ConnectionPool',
    'BaseRepository',
    'QueryBuilder',
    'MigrationManager',
    'run_migrations',
    'AURIX_MIGRATIONS'
]
