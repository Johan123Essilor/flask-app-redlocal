from flask import Blueprint, render_template

cubo_bp2 = Blueprint(
    "cubo2", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/cubo_static"
)

@cubo_bp2.route("/")
def cubo2():
    return render_template("cubo.html")
