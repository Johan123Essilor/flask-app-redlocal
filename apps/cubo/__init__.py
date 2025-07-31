from flask import Blueprint, render_template

cubo_bp = Blueprint(
    "cubo", __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/cubo_static"
)

@cubo_bp.route("/")
def cubo():
    return render_template("cubo.html")
