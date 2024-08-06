from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    
    def get_id(self):
        return self.id_usuario

    def __init__(self, id_usuario, username, apellidos, correo_usuario, password, img_usuario, visible_usuario) -> None:
        self.id_usuario = id_usuario
        self.username = username
        self.apellidos = apellidos
        self.correo_usuario = correo_usuario
        self.password = password
        self.img_usuario = img_usuario
        self.visible_usuario = visible_usuario

    @classmethod
    def check_password(cls, hashed_password, password):
        print(cls)
        print(hashed_password)
        print(password)
        return check_password_hash(hashed_password, password)
