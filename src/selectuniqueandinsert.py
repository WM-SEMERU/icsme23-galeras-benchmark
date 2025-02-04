import pymysql

# Establish database connection
con = pymysql.connect(
    host='192.168.0.1', 
    port=6603, 
    user='galeras', 
    passwd='galeras234', 
    db='galeras'
)
cursor = con.cursor()

# Corrected SQL Query
sql_query = """
INSERT INTO distinct_repo_code_dataset (
    id, commit_id, repo, path, file_name, fun_name, commit_message, code, url, language,
    ast_errors, n_ast_errors, ast_levels, n_whitespaces, n_words, vocab_size, complexity,
    nloc, token_counts, n_ast_nodes, n_identifiers
)
SELECT 
    r.id, r.commit_id, r.repo, r.path, r.file_name, r.fun_name, r.commit_message, r.code, r.url, r.language,
    r.ast_errors, r.n_ast_errors, r.ast_levels, r.n_whitespaces, r.n_words, r.vocab_size, r.complexity,
    r.nloc, r.token_counts, r.n_ast_nodes, r.n_identifiers
FROM repo_code_dataset r
WHERE NOT EXISTS (
    SELECT 1 FROM distinct_repo_code_dataset d WHERE d.code = r.code
);
"""

try:
    cursor.execute(sql_query)  # Execute the query
    con.commit()  # Commit changes
    print("Data inserted successfully.")
except pymysql.MySQLError as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    con.close()
