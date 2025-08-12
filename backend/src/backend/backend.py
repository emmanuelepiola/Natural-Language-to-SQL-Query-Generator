from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
import mariadb
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re
import requests
import json

OLLAMA_URL = "http://ollama:11434/api/generate"
OLLAMA_MODEL = "gemma3:1b-it-qat"

DB_HOST = "database"
DB_USER = "root"
DB_PASSWORD = "rootpassword"
DB_NAME = "database"
DB_PORT = 3306

app = FastAPI(title="Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class Property(BaseModel):
    property_name: str
    property_value: str

class Item(BaseModel):
    item_type: str
    properties: List[Property]

class SchemaItem(BaseModel):
    table_name: str
    table_column: str

class SqlQueryRequest(BaseModel):
    sql_query: str

class SearchRequest(BaseModel):
    question: str
    model: str

class SqlSearchResponse(BaseModel):
    sql: str
    sql_validation: Literal["valid", "invalid", "unsafe"]
    results: Optional[List[Item]] = None

class AddMovieRequest(BaseModel):
    data_line: str

# Database functions (connection and query)
def get_db_connection():
    try:
        connection = mariadb.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return connection
    except mariadb.Error as e:
        print(f"Database connection error: {e}")
        raise

def execute_query(query: str, params: tuple = ()):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        if query.strip().upper().startswith('SELECT') or query.strip().upper().startswith('SHOW') or query.strip().upper().startswith('DESCRIBE'):
            response = cursor.fetchall()
            return response
        else:
            connection.commit()
            return []
    except mariadb.Error as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()

# SQL Validation (check if the query is safe)
def validate_sql_query(query: str) -> str:
    query_upper = query.upper().strip()
    
    # Check for unsafe operators that modify the database
    unsafe_patterns = [
        r'\bDROP\b', r'\bDELETE\b', r'\bUPDATE\b', r'\bINSERT\b', 
        r'\bCREATE\b', r'\bALTER\b', r'\bTRUNCATE\b', r'\bGRANT\b', 
        r'\bREVOKE\b', r'\bEXEC\b', r'\bEXECUTE\b'
    ]
    
    for pattern in unsafe_patterns:
        if re.search(pattern, query_upper):
            return "unsafe"
    
    # Check if is a SELECT query
    if not query_upper.startswith('SELECT'):
        return "invalid"
    
    # Check if it contains FROM 
    if 'FROM' not in query_upper:
        return "invalid"
    
    # Check for unsafe patterns that can cause SQL injection
    dangerous_patterns = [r';', r'--', r'/\*', r'\*/', r'\bUNION\b.*\bSELECT\b']
    for pattern in dangerous_patterns:
        if re.search(pattern, query_upper):
            return "unsafe"
    
    # Check if the table exist
    try:
        table_match = re.search(r'FROM\s+([a-zA-Z_][a-zA-Z0-9_]*)', query_upper)
        if table_match:
            table_name = table_match.group(1).lower()
            tables = execute_query("SHOW TABLES;")
            existing_tables = [table[0].lower() for table in tables]
            if table_name not in existing_tables:
                return "invalid"
    except Exception as e:
        print(f"Error checking table existence: {e}")
        return "invalid"
    
    return "valid"

# Execute the query if it is safe
def execute_safe_sql(query: str) -> Optional[List[Item]]:
    validation = validate_sql_query(query)
    
    if validation != "valid":
        return None
    
    try:
        results = execute_query(query)
        return format_sql_results(results, query)
    except Exception as e:
        print(f"SQL execution error: {e}")
        return None

# Format the results of the query
def format_sql_results(results: List[tuple], query: str) -> List[Item]:
    formatted_results = []
    
    match = re.search(r"SELECT\s+(.*?)\s+FROM", query, re.IGNORECASE)
    if match:
        selected_fields = match.group(1).strip()
        if 'titolo' in selected_fields.lower():
            item_type = "film"
        elif 'regista' in selected_fields.lower():
            item_type = "regista"
        else:
            item_type = "film"
    else:
        item_type = "film"
    
    for result_tuple in results:
        if result_tuple and len(result_tuple) > 0:
            name_value = str(result_tuple[0]) if result_tuple[0] is not None else ""
            
            item = Item(
                item_type=item_type,
                properties=[
                    Property(property_name="name", property_value=name_value)
                ]
            )
            formatted_results.append(item)
    
    return formatted_results

# Get the database schema
def get_database_schema() -> str:
    """
    Dynamically retrieve database schema using information_schema.
    Returns a formatted string describing all tables and their columns.
    """
    try:
        # Get all tables in the current database
        tables_query = """
        SELECT TABLE_NAME 
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """
        tables = execute_query(tables_query)
        
        if not tables:
            return "No tables found in the database."
        
        schema_info = []
        
        for (table_name,) in tables:
            # Get column information for each table
            columns_query = """
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION
            """
            columns = execute_query(columns_query, (table_name,))
            
            if columns:
                table_info = f"\nTabella '{table_name}':"
                for column_name, data_type, is_nullable, column_default, column_comment in columns:
                    nullable_str = "NULL" if is_nullable == "YES" else "NOT NULL"
                    default_str = f", DEFAULT: {column_default}" if column_default else ""
                    comment_str = f" ({column_comment})" if column_comment else ""
                    table_info += f"\n  - {column_name} ({data_type.upper()}, {nullable_str}{default_str}){comment_str}"
                
                schema_info.append(table_info)
        
        return "\n".join(schema_info)
        
    except Exception as e:
        print(f"Error retrieving database schema: {e}")
        return "Errore nel recupero dello schema del database."

# LLM functions (convert natural language to SQL)
def ollama_query(query: str) -> str:
    response = requests.post(OLLAMA_URL, json={"model": OLLAMA_MODEL, "prompt": query, "stream": False})
    
    print("OLLAMA STATUS CODE:", response.status_code)
    print("OLLAMA RAW RESPONSE:", response.text)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Ollama error: {response.text}")
    
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        lines = response.text.strip().split('\n')
        full_response = ""
        for line in lines:
            if line.strip():
                try:
                    line_data = json.loads(line)
                    if "response" in line_data:
                        full_response += line_data["response"]
                except:
                    continue
        if full_response:
            return full_response
        else:
            raise HTTPException(status_code=500, detail=f"Failed to parse Ollama response: {response.text}")
    
    if "response" not in data:
        raise HTTPException(status_code=500, detail="Ollama did not return 'response' key.")
    
    return data["response"]

def convert_natural_language_to_sql(question: str, model: str) -> str:
    # Get dynamic schema information
    schema_info = get_database_schema()
    
    prompt = f"""
    Converti la seguente domanda in italiano in una query SQL valida utilizzando lo schema del database fornito.

    SCHEMA DEL DATABASE:
    {schema_info}

    Domanda: {question}

    Rispondi SOLO con la query SQL, senza spiegazioni aggiuntive.
    
    Esempi di query basate sullo schema:
    - "Elenca tutti i film" -> "SELECT titolo FROM movies"
    - "Elenca i film del 2010" -> "SELECT titolo FROM movies WHERE anno = 2010"
    - "Quali registi hanno fatto più di un film?" -> "SELECT regista FROM movies GROUP BY regista HAVING COUNT(*) > 1"
    - "Mostra la struttura del database" o "Che tabelle ci sono?" -> "SELECT * FROM movies LIMIT 1"
    - "Chi ha diretto Inception?" -> "SELECT regista FROM movies WHERE titolo = 'Inception'"
    - "Quali film sono disponibili su Netflix?" -> "SELECT titolo FROM movies WHERE piattaforma_1 = 'Netflix' OR piattaforma_2 = 'Netflix'"
    
    REGOLE IMPORTANTI:
    1. Usa SOLO i nomi delle tabelle e colonne presenti nello schema sopra riportato
    2. Usa SOLO query SELECT - non usare INSERT, UPDATE, DELETE, DROP o altre query che modificano il database
    3. Rispetta esattamente i nomi delle colonne come mostrati nello schema
    4. Se la domanda non può essere convertita in una query SQL valida con lo schema disponibile, rispondi con "SELECT 1 WHERE FALSE"
    """
    
    print(f"[LLM] Processing question: '{question}' with model: '{model}'")
    print(f"[LLM] Using dynamic schema: {schema_info}")
    
    try:
        global OLLAMA_MODEL
        original_model = OLLAMA_MODEL
        OLLAMA_MODEL = model
        
        print(f"[LLM] Sending request to Ollama...")
        sql_response = ollama_query(prompt)
        print(f"[LLM] Raw response from Ollama: '{sql_response}'")
        
        OLLAMA_MODEL = original_model
        
        sql_query = sql_response.strip()
        print(f"[LLM] Step 1 - Initial strip: '{sql_query}'")
        
        if sql_query.startswith('```sql'):
            sql_query = sql_query[6:]
            print(f"[LLM] Step 2a - Removed ```sql: '{sql_query}'")
        if sql_query.startswith('```'):
            sql_query = sql_query[3:]
            print(f"[LLM] Step 2b - Removed ```: '{sql_query}'")
        if sql_query.endswith('```'):
            sql_query = sql_query[:-3]
            print(f"[LLM] Step 2c - Removed ending ```: '{sql_query}'")
        
        sql_query = sql_query.strip()
        print(f"[LLM] Step 3 - After strip: '{sql_query}'")
                
        sql_query = ' '.join(line.strip() for line in sql_query.split('\n') if line.strip())
        print(f"[LLM] Step 4 - After joining lines: '{sql_query}'")
        
        if sql_query.endswith(';'):
            sql_query = sql_query[:-1]
            print(f"[LLM] Step 5 - Removed semicolon: '{sql_query}'")
        
        print(f"[LLM] Final processed SQL query: '{sql_query}'")
        
        if not sql_query or sql_query.lower() in ['', 'none', 'null']:
            print(f"[LLM] ERROR: Empty or invalid response from LLM")
            raise Exception("Empty response from LLM")
        
        return sql_query
        
    except Exception as e:
        print(f"[LLM] ERROR: Failed to convert natural language to SQL: {e}")
        raise Exception(f"LLM failed to process natural language query: {str(e)}")

# Get the database schema (esonero)
@app.get("/schema_summary", response_model=List[SchemaItem])
async def schema_summary():
    results = []
    tables = execute_query("SHOW TABLES;")
    for (table_name,) in tables:
        columns = execute_query(f"DESCRIBE `{table_name}`;")
        for column in columns:
            results.append(SchemaItem(table_name=table_name, table_column=column[0]))
    return results

# Execute the SQL query
@app.post("/sql_search", response_model=SqlSearchResponse)
async def sql_search(request: SqlQueryRequest):
    sql_query = request.sql_query
    validation_status = validate_sql_query(sql_query)
    
    if validation_status == "valid":
        results = execute_safe_sql(sql_query)
    else:
        results = None
    
    return SqlSearchResponse(
        sql=sql_query,
        sql_validation=validation_status,
        results=results
    )

# Execute the SQL query (natural language)
@app.post("/search", response_model=SqlSearchResponse)
async def search(request: SearchRequest):
    try:
        # Convert natural language to SQL
        sql_query = convert_natural_language_to_sql(request.question, request.model)
        
        # Validate and execute the SQL
        validation_status = validate_sql_query(sql_query)
        
        if validation_status == "valid":
            results = execute_safe_sql(sql_query)
        else:
            results = None
        
        return SqlSearchResponse(
            sql=sql_query,
            sql_validation=validation_status,
            results=results
        )
    except Exception as e:
        error_msg = f"LLM_ERROR: {str(e)}"
        return SqlSearchResponse(
            sql=error_msg,
            sql_validation="llm_error",
            results=None
        )

# Add a movie to the database (esonero)
@app.post("/add")
async def add_data(request: AddMovieRequest):
    data_line = request.data_line
    
    if not data_line:
        raise HTTPException(status_code=422, detail="Missing data_line")
    
    fields = data_line.split(",")
    
    if len(fields) != 7:
        raise HTTPException(status_code=422, detail="Wrong number of fields")
    
    titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2 = fields
    
    if not titolo.strip() or not regista.strip():
        raise HTTPException(status_code=422, detail="Missing required fields")
    
    try:
        eta_autore = int(eta_autore)
        anno = int(anno)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid number format in eta_autore or anno")
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT 1 FROM movies WHERE regista = ? LIMIT 1", (regista,))
        if cursor.fetchone():
            cursor.execute("UPDATE movies SET eta_autore = ? WHERE regista = ?", (eta_autore, regista))
        
        cursor.execute("SELECT * FROM movies WHERE titolo = ?", (titolo,))
        existing_movie = cursor.fetchone()
        
        if existing_movie:
            cursor.execute("DELETE FROM movies WHERE titolo = ?", (titolo,))
        
        cursor.execute("""
            INSERT INTO movies (titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (titolo, regista, eta_autore, anno, genere, piattaforma_1, piattaforma_2))
        
        connection.commit()
        return JSONResponse(content={"status": "ok"})
        
    except mariadb.Error as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        cursor.close()
        connection.close()
