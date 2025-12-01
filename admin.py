from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from database import db
from models import Project

admin_bp = Blueprint("admin", __name__)

@admin_bp.before_request
def restrict_to_admins():
    if not current_user.is_authenticated or not current_user.is_admin:
        return "Access denied."

@admin_bp.route("/admin")
def dashboard():
    pending = Project.query.filter_by(approved=False).all()
    approved = Project.query.filter_by(approved=True).all()
    return render_template("admin_dashboard.html", pending=pending, approved=approved)


@admin_bp.route("/admin/approve/<int:project_id>")
def approve(project_id):
    project = Project.query.get_or_404(project_id)
    project.approved = True
    db.session.commit()
    flash("Project approved.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/admin/reject/<int:project_id>")
def reject(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash("Project rejected and deleted.", "warning")
    return redirect(url_for("admin.dashboard"))
