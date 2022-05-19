from flask_restful import Resource, reqparse
from werkzeug.exceptions import RequestURITooLarge
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} #Select * from hoteis


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('nome', type = str, required = True, help="The field 'nome' cannot be left blank" )
    atributos.add_argument('stars', type = float, required = True, help="The field 'stars' cannot be left blank")
    atributos.add_argument('diaria',type = float, required = True, help="The field 'diaria' cannot be left blank")
    atributos.add_argument('cidade', type = str, required = True, help="The field 'cidade' cannot be left blank")

    def get(self, hotel_id):
        hotel_id = int(hotel_id)
        hotel = HotelModel.find_hotel(hotel_id = hotel_id)
        if hotel:
            return hotel.json(), 200
        return {'message':'Hotel not found.'}, 404 #não encontrado

    def post(self, hotel_id):
        hotel_id = int(hotel_id)

        if HotelModel.find_hotel(hotel_id):
            return {'message':'Hotel id {} alredy exists.'.format(hotel_id)}, 400

        dados = Hotel.atributos.parse_args()
        novo_hotel = HotelModel(hotel_id, **dados) #Utilizando o conceitos de **qwargs, ele já desempacota os dados nesta lista
        try:
            novo_hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'},500 # erro interno ao salva
        return novo_hotel.json()
        

    def put(self, hotel_id):
        hotel_id = int(hotel_id)
        dados = Hotel.atributos.parse_args()
        
        hotel = HotelModel.find_hotel(hotel_id = hotel_id)
        if hotel:
            hotel.update_hotel(**dados)
            hotel.save_hotel()
            return hotel.json(), 200

        novo_hotel = HotelModel(hotel_id, **dados) #Utilizando o conceitos de **qwargs, ele já desempacota os dados nesta lista
        try:
            novo_hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred trying to save hotel.'},500 # erro interno ao salva
        return novo_hotel.json(), 201  #Hotel criado

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id = hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred trying to delete hotel.'},500 # erro interno ao salva
            return {'message':'Hotel deleted','id':hotel_id}, 200
        return {'message':'Hotel not found.'}, 404