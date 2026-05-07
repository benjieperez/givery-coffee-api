from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError
from decouple import config as env
from urllib.parse import quote_plus

class Database:
    def __init__(self):
        self.db_engine = env("DB_ENGINE")
        self.db_user = env("DB_USER")
        self.db_password = quote_plus(env("DB_PASSWORD"))
        self.db_name = env("DB_NAME")
        self.db_host = env('DB_HOST', default='localhost')  # with default fallback
        self.db_port = env("DB_PORT")

    def database_db_creds(self, username, password, database_name):
        """Generate the Database Credentials"""

        if self.db_engine == "postgres":
            tortoise_db_engine = "tortoise.backends.asyncpg"
        elif self.db_engine in ["mysql", "mariadb"]:
            tortoise_db_engine = "tortoise.backends.mysql"
        elif self.db_engine in ["sqlite"]:
            tortoise_db_engine = "tortoise.backends.aiosqlite"

        default_credentials = {
            "engine": tortoise_db_engine, #Use specific driver for specific DB_ENGINE
            "credentials": {
                "database": self.db_name,
                "host": self.db_host,
                "port": self.db_port,
                "user": self.db_user,
                "password": self.db_password
            }
        }

        return default_credentials

    async def init_db(self):
        """Initialize the database connection and generate the schemas."""
        default_db_creds = self.database_db_creds(
            username=self.db_user,
            password=self.db_password,
            database_name=self.db_name,
        )
        
        DATABASE_CONFIG = {
            "connections": {
                "default": default_db_creds
            },
            "apps": {
                "models": {
                    "models": ["app.models"],
                    "default_connection": "default",
                }
            }
        }

        # Initialize the database connection with models (make sure to add your models)
        await Tortoise.init(config=DATABASE_CONFIG)
        await Tortoise.generate_schemas()

    async def check_database_status(self):
        """Check Database status."""
        try:
            # Test the connection by executing a simple query
            await Tortoise.get_connection("default").execute_query("SELECT 1")

            print(f"{self.db_engine} is up and reachable!")
            status = True
        except DBConnectionError as e:
            print(f"Failed to connect to {self.db_engine}: {e}")
            status = False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            status = False
            
        return status