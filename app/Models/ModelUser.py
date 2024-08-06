from .entities.user import User

class ModuleUser():
    @classmethod
    def login(self, db, user):
        try:
            cur=db.cursor()
            sql="SELECT id_usuario, correo_usuario, password FROM usuarios WHERE visible_usuario=true and correo_usuario=%s"
            cur.execute(sql, (user.correo_usuario,))
            row=cur.fetchone()
            print(row)
            if row != None:
                user=User(row[0], None, None, row[1], user.check_password(row[2],user.password), None, None)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self, db, id_usuario):
        try:
            cur=db.cursor()
            sql="SELECT id_usuario, username, apellidos, correo_usuario, img_usuario, visible_usuario FROM usuarios WHERE visible_usuario='true' and id_usuario=%s"
            cur.execute(sql, (id_usuario,))
            row=cur.fetchone()
            print(row)
            if row != None:
                return User(row[0], row[1], row[2], row[3], None, row[4], row[5])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)