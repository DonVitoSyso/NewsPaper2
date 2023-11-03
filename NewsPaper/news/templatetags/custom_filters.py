from django import template


register = template.Library()

poor_words = {
   'are': 'a**',
   'Are': 'A**',
}
# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter() # or register.filter(name=’currency_rub’)
def censor(value): # {{ price|currency }}
   """
   value: значение, к которому нужно применить фильтр
   """
   # Возвращаемое функцией значение подставится в шаблон.
   value_split = value.split()

   for i in range(len(value_split)):
       for p in poor_words:
           if p == value_split[i]:
               value_split[i] = poor_words[p]
   value = ' '.join(value_split)
   return f'{value}'
