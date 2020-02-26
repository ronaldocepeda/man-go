from wtforms import Form
from wtforms import StringField, TextField, PasswordField
from wtforms.fields.html5 import EmailField

from wtforms import validators, ValidationError


class LoginForm (Form):
    
# class CommentForm (Form):

    username = StringField('username',
    [
        validators.length(min=4, max=10, message='Igrese un nombre valido!'),
        validators.Required(message = 'El nombre es requerido')
    ]
    )
    apellido = StringField('apellido',
    [
        validators.length(min=4, max=10, message='Igrese un apellido valido!'),
        validators.Required(message = 'El apellido es requerido')
    ]
    )
    usuario = StringField('usuario',
    [
        validators.length(min=4, max=20, message='Igrese un usuario valido!'),
        validators.Required(message = 'El usuario es requerido'),

    ]
    )
    email = EmailField('email',
    [
       validators.Required(message = 'El email es requerido'),
       validators.Email(message='Ingrese un correo electronico valido')
    ]
    )
    password = PasswordField('password',
    [ validators.Required(message = 'Contraseña es requerido'),
       validators.length(min=4, max=255, message='Ingrese una contraseña valida')
    ]
    )

