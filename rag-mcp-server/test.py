import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('supabase_test.log', mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_supabase_connection():
    # Load environment variables
    load_dotenv()
    
    # Get Supabase credentials
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    # Validate credentials
    if not supabase_url or not supabase_key:
        print('Error: SUPABASE_URL or SUPABASE_KEY is missing')
        return False
    
    try:
        # Create Supabase client
        print(f'Connecting to Supabase at: {supabase_url}')
        supabase = create_client(supabase_url, supabase_key)
        print('Supabase client created successfully')
        
        # Attempt to list documents or perform a simple query
        try:
            # Adjust the table name as per your Supabase setup
            result = supabase.table('documents_reranking').select('*', count='exact').limit(1).execute()
            
            print(f'Query successful. Total documents: {result.count}')
            print(f'Sample document: {result.data[:1]}')  # Print only first document
            return True
        
        except Exception as query_error:
            print(f'Error executing query: {query_error}')
            return False
    
    except Exception as conn_error:
        print(f'Supabase connection error: {conn_error}')
        return False

def main():
    connection_result = test_supabase_connection()
    print(f'Supabase Connection Test: {"PASSED" if connection_result else "FAILED"}')

if __name__ == '__main__':
    main()
