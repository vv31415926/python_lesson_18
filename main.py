from flask import Flask
from flask import render_template, url_for, request
import flask
import datetime
from person import Person
from my_lib import get_week
#from parser import Parser
from parser_price import Parser_price
#import requests
from head_hunter_vacancies import HeadHunter_vacancies
from bd_apartment import Appartment_BD

pers = Person()

app = Flask( __name__ )

@app.route("/")
@app.route("/index/")
def main_win():   # Главная страница
    today = datetime.datetime.today()
    scw = get_week( int( today.strftime('%w') ) )
    return render_template( 'index.html',  curdate = today.strftime('%d-%m-%Y'), curweek = scw )

@app.route("/personal/")
def pers_win():  # Персональные данные -------------------------------------------------------
    dic={
    'photo' : pers.get_photo(),
    'fio' : pers.get_name() + ' ' + pers.get_otch() + ' ' + pers.get_fam(),
    'birthday' : pers.get_birthday(),
    'attach': pers.get_attach()
    }
    return render_template( 'personal.html', **dic )

@app.route("/parser/" )
def parser():   # начальная страница парсера квартир - выбор района ---------------------------
    return render_template( 'parser_form.html' )

@app.route("/price_apartments/", methods=['POST'] )
def price():  # результат работы парсера - цены
    region = request.form['region']   # получение параметра

    parser = Parser_price( region )   # создать объект парсинга
    dicMin = parser.cost_min(rej='dic')
    dicMax = parser.cost_max(rej='dic')

    # параметры для страницы
    dic={}
    dic['region'] = region
    dic['minprice'] = dicMin['price']
    dic['mincity'] = dicMin['city']
    dic['mincharact'] = dicMin['address']+'; '+dicMin['region']+'; '+dicMin['characteristic']
    dic['maxprice'] = dicMax['price']
    dic['maxcity'] = dicMax['city']
    dic['maxcharact'] = dicMax['address'] + '; ' + dicMax['region'] + '; ' + dicMax['characteristic']

    return render_template( 'price_apartments.html', **dic )

@app.route("/hh_main/" )
def hh_main():   # начальная страница выкансий  API  ---------------------------------------------
    return render_template('hh_city.html')


@app.route("/hh_vacancy/", methods=['POST'] )
def hh_vacancy():
    city = request.form['city']   # какой город был выбран
    vac = request.form['vac']

    hh = HeadHunter_vacancies()

    lst, num, sum = hh.view_vacancies( city, vac )
    dic={}
    s = ''
    for v in lst:
        if v:
            s += '* '+v+'\n'
    dic['skills'] = s
    dic['city'] = city
    dic['vac'] = vac
    if num == 0:
        dic['salary'] = 0.0
    else:
        dic['salary'] = round( sum/num, 2 )

    return render_template('hh_vacancy.html', **dic)


@app.route("/bd_apartment/" )
def bd_apartment():
    return render_template('bd_apartment.html')

@app.route("/bd_apartment_view/", methods=['POST'] )
def bd_apartment_view():
    region = request.form['region']  # получение параметра
    load  = request.form.get('load')  # получение параметра

    dic = {}
    bd = Appartment_BD( )

    dic['field'] = []
    if bd.is_connect == 'OK':
        lstField = bd.get_title_table()  # список кортежей(записей) с полями внутри
        dic['field']=lstField

    # данные БД
    # перезаписать
    if load:
        parser = Parser_price( )  # создать объект парсинга по району
        lst_data = parser.data_search( region )
        bd.save_data(  lst_data )

    lst_view_data, update = bd.get_data( region )
    dic['data'] = lst_view_data
    dic['region'] = region
    dic['update'] = update

    return render_template('bd_apartment_view.html', **dic)


# ********************************************************************
if __name__ == "__main__":
    #print( 'версия:', flask.__version__ )
    app.run( debug=True )