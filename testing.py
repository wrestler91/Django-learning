import jinja2 as j
from jinja2.filters import escape
dg = [1,2,3,4,5]
cars = [
    {'model': 'Audi', 'price': 10000, 'weight': 12},
    {'model': 'Volvo', 'price': 23000, 'weight': 13}, 
    {'model': 'Nissan', 'price': 7000, 'weight': 15}
    ]

# html = '''
# {% macro list_cars(list_of_cars) -%}
# <ul>
# {% for c in list_of_cars -%}
#     <li>{{c.model}} {{caller(c)}}
# {% endfor -%}
# </ul>
# {%- endmacro -%}

# {%- call(car) list_cars(cars) %}
#  <ul>
#  <li>price: {{car.price}}
#  <li>weight: {{car.weight}}
#  </u>
#  {%- endcall -%}
# '''
page = '''
{% macro dialog_1(title, msg = '') %}
<div class ='dialog'>
<p class='title>{{title}}</p> 
<p class='message>{{msg}}</p> 
</div>
{% endmacro %}
'''

main = '''
{% import 'page.htm' as dlg %}
{{dlg.dialog_1('Заголовок', 'Некое сообщение') }}
'''
# передается объект функции (без его вызова)
file_loader = j.FileSystemLoader('templates') 
env = j.Environment(loader=file_loader)
# формирует объект Template на основе содиржимого передаваемого файла. в скобках указывается имя файла
tm = env.get_template('base.htm') 
msg = tm.render()



# <ul>
# <li>Audi
#  <ul>
#  <li>price: 10000
#  <li>weight: 12
#  </u>
# <li>Volvo
#  <ul>
#  <li>price: 23000
#  <li>weight: 13
#  </u>
# <li>Nissan
#  <ul>
#  <li>price: 7000
#  <li>weight: 15
#  </u>
# </ul>
print(msg)