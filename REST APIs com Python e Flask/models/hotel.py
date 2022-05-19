from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'
    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    stars = banco.Column(banco.Float(precision = 2))
    diaria = banco.Column(banco.Float(precision = 2))
    cidade = banco.Column(banco.String(40))

    def __init__(self, hotel_id, nome, stars, diaria, cidade ):
        self.hotel_id = hotel_id
        self.nome = nome
        self.stars = stars
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            'hotel_id':self.hotel_id,
            'nome': self.nome,
            'stars':self.stars,
            'diaria':self.diaria,
            'cidade':self.cidade
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id = hotel_id).first() # select * from hoteis where hotel_id = $hotel_id limit 1
        if hotel:
            return hotel
        return None      

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, stars, diaria, cidade):
        self.nome = nome
        self.stars = stars
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()