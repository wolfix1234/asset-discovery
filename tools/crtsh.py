import psycopg2
import re
import time


def crtsh(domain, retries=3, delay=2):
    # Database connection parameters
    db_params = {
        "dbname": "certwatch",
        "user": "guest",
        "password": "",  # Add password if required
        "host": "crt.sh",
        "port": 5432,
    }

    # SQL query
    query = f"""
    SELECT
        ci.NAME_VALUE
    FROM
        certificate_and_identities ci
    WHERE
        plainto_tsquery('certwatch', %s) @@ identities(ci.CERTIFICATE)
    """

    for attempt in range(retries):
        try:
            # Establish connection and execute query
            connection = psycopg2.connect(**db_params)
            connection.autocommit = True

            cursor = connection.cursor()
            cursor.execute(query, (domain,))
            results = cursor.fetchall()

            # Process results
            processed_results = set()
            for row in results:
                name_value = row[0].strip()
                if (
                    re.search(r"\.\s*" + re.escape(domain), name_value, re.IGNORECASE)
                    and "*" not in name_value
                ):
                    processed_results.add(name_value.lower().replace(f".{domain}", ""))

            # Output results
            res = []
            for sub in list(processed_results):
                if sub != "*":
                    res.append(f"{sub}.{domain}")

            return res

        except psycopg2.Error as e:
            print(f"Database error on attempt {attempt + 1}: {e}")
            time.sleep(delay)  # Wait before retrying

        finally:
            if connection:
                cursor.close()
                connection.close()

    # If all retries fail
    print("All retry attempts failed.")
    return []
