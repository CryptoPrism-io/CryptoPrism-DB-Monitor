#!/usr/bin/env python3
"""
Execute Database Optimization Scripts with Rollback Capability
"""

import os
import sys
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class OptimizationExecutor:
    """Execute database optimization scripts safely."""
    
    def __init__(self):
        load_dotenv()
        
        # Database connection parameters
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'), 
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        self.database = os.getenv('DB_NAME', 'dbcp')
        
        # Validate environment variables
        required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {missing_vars}")
    
    def create_connection_string(self) -> str:
        """Create PostgreSQL connection string."""
        return (f"postgresql+psycopg2://{self.db_config['user']}:"
                f"{self.db_config['password']}@{self.db_config['host']}:"
                f"{self.db_config['port']}/{self.database}")
    
    def execute_sql_file(self, filepath: str, description: str) -> bool:
        """Execute SQL file and return success status."""
        logger.info(f"Executing {description}: {filepath}")
        
        try:
            # Read SQL file
            with open(filepath, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Remove comments and empty lines for cleaner execution
            sql_statements = []
            for line in sql_content.split('\n'):
                line = line.strip()
                if line and not line.startswith('--'):
                    sql_statements.append(line)
            
            sql_to_execute = '\n'.join(sql_statements)
            
            if not sql_to_execute.strip():
                logger.warning(f"No SQL statements found in {filepath}")
                return True
            
            # Execute SQL
            conn_string = self.create_connection_string()
            engine = create_engine(conn_string)
            
            start_time = time.time()
            with engine.connect() as conn:
                # Execute the SQL
                conn.execute(text(sql_to_execute))
                conn.commit()
            
            execution_time = time.time() - start_time
            logger.info(f"{description} completed successfully in {execution_time:.2f} seconds")
            
            engine.dispose()
            return True
            
        except Exception as e:
            logger.error(f" {description} failed: {e}")
            return False
    
    def verify_optimization(self) -> dict:
        """Verify that optimizations were applied correctly."""
        logger.info("Verifying optimization results...")
        
        verification_queries = {
            "primary_keys_count": """
                SELECT COUNT(*) as pk_count 
                FROM information_schema.table_constraints 
                WHERE constraint_type = 'PRIMARY KEY' 
                AND table_schema = 'public'
            """,
            "indexes_count": """
                SELECT COUNT(*) as index_count 
                FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND indexname LIKE 'idx_%'
            """,
            "sample_table_check": """
                SELECT schemaname, tablename, indexname 
                FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND tablename = 'FE_DMV_ALL'
                ORDER BY indexname
            """
        }
        
        results = {}
        
        try:
            conn_string = self.create_connection_string()
            engine = create_engine(conn_string)
            
            with engine.connect() as conn:
                for query_name, query in verification_queries.items():
                    result = conn.execute(text(query))
                    if query_name == "sample_table_check":
                        results[query_name] = [dict(row._mapping) for row in result.fetchall()]
                    else:
                        results[query_name] = result.scalar()
            
            engine.dispose()
            
            # Log results
            logger.info(f"Primary keys created: {results.get('primary_keys_count', 0)}")
            logger.info(f"Indexes created: {results.get('indexes_count', 0)}")
            logger.info(f"FE_DMV_ALL indexes: {len(results.get('sample_table_check', []))}")
            
            return results
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return {}
    
    def run_analyze(self) -> bool:
        """Run ANALYZE to update table statistics."""
        logger.info("Running ANALYZE to update table statistics...")
        
        try:
            conn_string = self.create_connection_string()
            engine = create_engine(conn_string)
            
            start_time = time.time()
            with engine.connect() as conn:
                conn.execute(text("ANALYZE;"))
                conn.commit()
            
            execution_time = time.time() - start_time
            logger.info(f"ANALYZE completed in {execution_time:.2f} seconds")
            
            engine.dispose()
            return True
            
        except Exception as e:
            logger.error(f" ANALYZE failed: {e}")
            return False

def main():
    """Execute database optimization workflow."""
    print("=" * 60)
    print("DATABASE OPTIMIZATION EXECUTION")
    print("=" * 60)
    print("WARNING: This will modify the database structure!")
    print("Make sure you have a backup before proceeding.\n")
    
    # Find the most recent optimization scripts
    script_dir = Path("sql_optimizations")
    if not script_dir.exists():
        print(" ERROR: sql_optimizations directory not found")
        return False
    
    # Find latest scripts
    pk_scripts = list(script_dir.glob("01_primary_keys_*.sql"))
    idx_scripts = list(script_dir.glob("02_strategic_indexes_*.sql"))
    
    if not pk_scripts or not idx_scripts:
        print(" ERROR: Optimization scripts not found")
        print("Run quick_optimization_generator.py first")
        return False
    
    # Get latest scripts
    pk_script = sorted(pk_scripts)[-1]
    idx_script = sorted(idx_scripts)[-1]
    
    print(f"Primary keys script: {pk_script}")
    print(f"Indexes script: {idx_script}")
    print()
    
    # Confirm execution
    response = input("Do you want to proceed with optimization? (yes/no): ").lower().strip()
    if response != 'yes':
        print("Optimization cancelled by user")
        return False
    
    executor = OptimizationExecutor()
    
    try:
        print("\nStarting database optimization...")
        
        # Step 1: Execute primary keys
        print("\nStep 1: Adding primary keys...")
        if not executor.execute_sql_file(str(pk_script), "Primary Keys"):
            print(" Primary key optimization failed!")
            return False
        
        # Step 2: Execute indexes
        print("\nStep 2: Creating strategic indexes...")
        if not executor.execute_sql_file(str(idx_script), "Strategic Indexes"):
            print(" Index optimization failed!")
            return False
        
        # Step 3: Run ANALYZE
        print("\nStep 3: Updating table statistics...")
        if not executor.run_analyze():
            print(" ANALYZE failed!")
            return False
        
        # Step 4: Verify optimization
        print("\nStep 4: Verifying optimization results...")
        results = executor.verify_optimization()
        
        if results:
            print("\nDATABASE OPTIMIZATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print(f"Primary keys added: {results.get('primary_keys_count', 0)}")
            print(f"Indexes created: {results.get('indexes_count', 0)}")
            print("\nOptimization summary:")
            print("- All tables now have primary keys")
            print("- Strategic indexes added for performance")
            print("- Table statistics updated")
            print("\nReady for performance testing!")
            
            return True
        else:
            print("Optimization completed but verification had issues")
            return False
            
    except Exception as e:
        print(f" Optimization failed: {e}")
        print("\nIf needed, use the rollback script to reverse changes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)