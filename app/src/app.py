import os
import psycopg2
import redis
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = "postgres"
DB_NAME = "secureapp"
DB_USER = "secureuser"
DB_PASSWORD_FILE = "/run/secrets/db_password"

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_db_password():
    with open(DB_PASSWORD_FILE, "r") as f:
        return f.read().strip()


def check_postgres():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=get_db_password()
        )

        cur = conn.cursor()
        cur.execute(
            "SELECT service_name, status "
            "FROM lab_status ORDER BY id DESC LIMIT 1"
        )
        result = cur.fetchone()

        cur.close()
        conn.close()

        return {
            "status": "healthy",
            "data": {
                "service_name": result[0],
                "status": result[1]
            }
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


def check_redis():
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            decode_responses=True
        )

        client.ping()

        return {"status": "healthy"}

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.route("/")
def home():
    return jsonify({
        "service": "secure-devops-app",
        "status": "ok"
    })


@app.route("/health")
def health():
    postgres = check_postgres()
    redis_status = check_redis()

    overall = (
        "healthy"
        if postgres["status"] == "healthy"
        and redis_status["status"] == "healthy"
        else "degraded"
    )

    return jsonify({
        "application": overall,
        "postgres": postgres,
        "redis": redis_status
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)