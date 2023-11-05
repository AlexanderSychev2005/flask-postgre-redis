from flask import Flask, render_template
import psycopg2
import redis

app = Flask(__name__)

pg = psycopg2.connect("""
    host=localhost
    dbname=postgres
    user=postgres
    password=admin
    port=5433   
""")


r = redis.Redis(host='localhost', port=6379, decode_responses=True)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/cities')
def read_count():
    pair = 'cities:count'
    redisCount = r.get(pair)
    if redisCount:
        result = redisCount + " из кеша"
        return render_template('cities.html', value=result)
    
    
    
    cursor = pg.cursor()
    cursor.execute("SELECT COUNT(*) FROM city WHERE countrycode = 'BRA';")
    pgCount = cursor.fetchone()[0]
    
    result = str(pgCount) + " (из постгри)"
    r.set(pair, pgCount)
    return render_template('cities.html', value=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)