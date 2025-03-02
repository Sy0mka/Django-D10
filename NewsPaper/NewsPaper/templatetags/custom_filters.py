from django import template
from django.template.defaultfilters import stringfilter
import re

register = template.Library()

# Список запрещенных слов (дополните своими словами)
CENSORED_WORDS = ['редиска', 'плохой', 'негодяй']

@register.filter(name='censor')
@stringfilter  # Гарантирует, что фильтр применяется только к строкам
def censor(value):
    if not isinstance(value, str):
        raise TypeError("Фильтр 'censor' применяется только к строкам!")

    for word in CENSORED_WORDS:
        # Замена слова независимо от регистра первой буквы
        pattern = r'(?i)\b{}\b'.format(word)
        replacement = word[0] + '*' * (len(word) - 1)
        value = re.sub(pattern, replacement, value)
    return value