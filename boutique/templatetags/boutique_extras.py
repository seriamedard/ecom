from django import template
register = template.Library()

@register.filter
def replace(texte):
    """
    Prend une chaine de caractère et remplace
    chaque espace et point par tiret.
    """
    pass