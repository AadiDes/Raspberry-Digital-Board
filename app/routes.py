from flask import Blueprint, render_template
from app.db_utils import get_db_connection
from flask import request, redirect, url_for, flash

main = Blueprint('main', __name__)

@main.route("/")
def display():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM DisplayState WHERE id = 1")
    row = cur.fetchone()
    conn.close()

    return render_template("display.html", data=row)

@main.route("/admin", methods=["GET", "POST"])
def admin():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        form = request.form

        # Read form fields
        production = form.get("production")
        num_heats = form.get("num_heats")
        month_prod = form.get("month_prod")
        slogan = form.get("slogan")
        manpower = form.get("manpower")
        employee_name = form.get("employee_name")

        cur.execute("""
            UPDATE DisplayState SET
                production = ?, num_heats = ?, month_prod = ?, slogan = ?,
                manpower = ?, employee_name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """, (production, num_heats, month_prod, slogan, manpower, employee_name))

        conn.commit()
        conn.close()
        flash("Display values updated!", "success")
        return redirect(url_for("main.admin"))

    # GET request: load current data
    cur.execute("SELECT * FROM DisplayState WHERE id = 1")
    data = cur.fetchone()
    conn.close()
    return render_template("admin.html", data=data)