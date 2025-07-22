import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
from config import Config
import logging
import time

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.config = Config.DB_CONFIG
        self.conn = None

    def connect(self):
        """Establish PostgreSQL connection with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.conn = psycopg2.connect(
                    host=self.config["host"],
                    database=self.config["database"],
                    user=self.config["user"],
                    password=self.config["password"],
                    port=self.config["port"],
                    connect_timeout=5
                )
                self.conn.autocommit = False
                return True
            except psycopg2.OperationalError as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)
        return False

    def create_tables(self):
        """Create tables with proper schema and constraints"""
        commands = (
            """
            CREATE TABLE IF NOT EXISTS properties (
                id SERIAL PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                price TEXT,
                location TEXT,
                bedrooms TEXT,
                bathrooms TEXT,
                area TEXT,
                property_type TEXT,
                purpose TEXT,
                added_date TEXT,
                description TEXT,
                image_urls TEXT[],
                is_fake BOOLEAN DEFAULT FALSE,
                fake_probability FLOAT DEFAULT 0.0,
                fake_reasons TEXT[] DEFAULT ARRAY[]::TEXT[],
                scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT url_unique UNIQUE (url)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id SERIAL PRIMARY KEY,
                property_id INTEGER REFERENCES properties(id) ON DELETE CASCADE,
                analysis_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                result BOOLEAN,
                confidence FLOAT,
                notes TEXT,
                model_used TEXT
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_properties_url ON properties(url)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_properties_fake ON properties(is_fake)
            """
        )
        
        try:
            if not self.connect():
                raise Exception("Failed to connect to PostgreSQL")
            
            cursor = self.conn.cursor()
            for command in commands:
                cursor.execute(command)
            
            self.conn.commit()
            logger.info("PostgreSQL tables created/verified successfully")
            return True
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"Database error: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        finally:
            if self.conn:
                self.conn.close()

    def save_property(self, property_data):
        """Upsert property data with transaction handling"""
        if not property_data.get('url'):
            logger.error("No URL provided in property data")
            return None

        try:
            if not self.connect():
                raise Exception("Database connection failed")

            cursor = self.conn.cursor()

            # Upsert property data
            insert_query = sql.SQL("""
            INSERT INTO properties (
                url, title, price, location, bedrooms, bathrooms, 
                area, property_type, purpose, added_date, description, image_urls
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET
                title = EXCLUDED.title,
                price = EXCLUDED.price,
                description = EXCLUDED.description,
                image_urls = EXCLUDED.image_urls,
                scraped_at = CURRENT_TIMESTAMP
            RETURNING id
            """)
            
            cursor.execute(insert_query, (
                property_data['url'],
                property_data.get('title', ''),
                property_data.get('price', ''),
                property_data.get('location', ''),
                property_data.get('bedrooms', ''),
                property_data.get('bathrooms', ''),
                property_data.get('area', ''),
                property_data.get('type', ''),
                property_data.get('purpose', ''),
                property_data.get('added', ''),
                property_data.get('description', ''),
                property_data.get('image_urls', [])
            ))
            
            property_id = cursor.fetchone()[0]

            # Save analysis results if available
            if 'analysis' in property_data:
                analysis = property_data['analysis']
                
                update_query = sql.SQL("""
                UPDATE properties 
                SET is_fake = %s, 
                    fake_probability = %s, 
                    fake_reasons = %s 
                WHERE id = %s
                """)
                
                cursor.execute(update_query, (
                    analysis.get('is_suspicious', False),
                    analysis.get('confidence', 0.0),
                    analysis.get('reasons', []),
                    property_id
                ))
                
                history_query = sql.SQL("""
                INSERT INTO analysis_history (
                    property_id, result, confidence, notes, model_used
                ) VALUES (%s, %s, %s, %s, %s)
                """)
                
                cursor.execute(history_query, (
                    property_id,
                    analysis.get('is_suspicious', False),
                    analysis.get('confidence', 0.0),
                    "\n".join(analysis.get('reasons', [])),
                    "HuggingFace" if hasattr(Config, 'HF_API_TOKEN') and Config.HF_API_TOKEN else "Basic"
                ))

            self.conn.commit()
            return property_id
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"Save error: {e}")
            if self.conn:
                self.conn.rollback()
            return None
        finally:
            if self.conn:
                self.conn.close()

    def get_history(self):
        """Get analysis history with property details"""
        try:
            if not self.connect():
                raise Exception("Database connection failed")

            cursor = self.conn.cursor()
            cursor.execute("""
            SELECT h.analysis_time, p.url, p.title, h.result, h.confidence
            FROM analysis_history h
            JOIN properties p ON h.property_id = p.id
            ORDER BY h.analysis_time DESC
            LIMIT 50
            """)
            
            history_data = []
            for row in cursor.fetchall():
                history_data.append({
                    'analysis_time': row[0],
                    'url': row[1],
                    'title': row[2],
                    'result': row[3],
                    'confidence': row[4]
                })
                
            return history_data
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"Failed to fetch history: {e}")
            return []
        finally:
            if self.conn:
                self.conn.close()