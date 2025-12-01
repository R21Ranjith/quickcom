
from database import db
from models import Project, User

class SellerService:
    @staticmethod
    def create_project(user_id, title, description, price, category_id, tags, image=None):
        project = Project(
            user_id=user_id,
            title=title,
            description=description,
            price=price,
            category_id=category_id,
            tags=tags,
            image=image
        )
        db.session.add(project)
        db.session.commit()
        return project
    
    @staticmethod
    def get_seller_projects(user_id):
        return Project.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def update_project(project_id, **kwargs):
        project = Project.query.get(project_id)
        if project:
            for key, value in kwargs.items():
                setattr(project, key, value)
            db.session.commit()
        return project
    
    @staticmethod
    def delete_project(project_id):
        project = Project.query.get(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return True
        return False
