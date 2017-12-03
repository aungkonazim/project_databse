from flask import Flask, request, render_template, send_from_directory
import os
import psycopg2
__author__ = 'aungkon'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

connect_str = "dbname='Final' user='postgres' host='localhost' " + \
              "password='azim'"
# use our connection values to establish a connection
conn = psycopg2.connect(connect_str)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def query():
    cursor = conn.cursor()
    cursor.execute("""select restaurant.name as restaurant_name,restaurant.address,coupon.discount::int,coupon.valid from person inner join owns_coupon on owns_coupon.person_id = person.id 
	inner join coupon on coupon.id = owns_coupon.coupon_id inner join restaurant on coupon.restaurant_id=restaurant.id where person.name= 'A' and coupon.valid > now() order by coupon.discount desc""")
    result1 = cursor.fetchall()
    cursor.execute("""select cuisine.name as name_of_cuisine,restaurant.name as restaurant_name,restaurant.address from like_cuisines inner join person on person.id=like_cuisines.person_id inner join 
	cuisine on cuisine.id=like_cuisines.cuisine_id inner join has_cuisines on has_cuisines.cuisine_id = cuisine.id inner join restaurant on
	has_cuisines.restaurant_id = restaurant.id where person.name='A'""")
    result2 = cursor.fetchall()
    cursor.execute("""select restaurant.name,restaurant.address,(avg(review.ambiance_score)+avg(review.price_score)+avg(review.foodquality_score)+avg(review.service_score)+avg(review.experience_score))/5 as avg_score from 
	restaurant inner join review on review.restaurant_id = restaurant.id group by restaurant.id order by avg_score desc""")
    result3 = cursor.fetchall()
    cursor.execute("""select restaurant.name,restaurant.address,avg(review.price_score)::int as price_rating from restaurant inner join review on review.restaurant_id = restaurant.id 
    group by restaurant.id order by price_rating desc limit 1""")
    result4 = cursor.fetchall()
    return render_template("results.html",rows=result1,rows1 = result2,rows2=result3,rows3 = result4)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
