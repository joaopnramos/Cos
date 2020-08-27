from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):
    """ Gera o token necessario á ativação do email """
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))

""" Objeto criado para gerar tokens """
tokengenerator = AppTokenGenerator()
