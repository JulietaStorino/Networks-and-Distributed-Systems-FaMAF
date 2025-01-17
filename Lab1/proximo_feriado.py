import requests
from datetime import date

def get_url(year):
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"

months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
h_types = ['inamovible', 'trasladable', 'nolaborable', 'puente']

def day_of_week(day, month, year):
    return days[date(year, month, day).weekday()]

class NextHoliday:
    def __init__(self):
        self.loading = True
        self.year = date.today().year
        self.holiday = None
        self.type = None

    def set_next(self, holidays, h_type = None):
        self.type = h_types[0] if h_type not in h_types else h_type
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }

        if h_type not in h_types and h_type != None:
            self.loading = False
            self.holiday = holidays[0]
            raise ValueError("Tipo de feriado no válido")
        
        self.type = h_type
        holiday = next(
            (h for h in holidays if ((h['tipo'] == self.type) or self.type == None) and
                                    (h['mes'] == today['month'] and h['dia'] > today['day'] or h['mes'] > today['month'])),
            holidays[0]
        )

        self.loading = False
        self.holiday = holiday

    def fetch_holidays(self, h_type=None):
        response = requests.get(get_url(self.year))
        data = response.json()
        self.set_next(data, h_type)

    def render(self):
        if self.loading:
            print("Buscando...")
        else:
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            month = 12 if self.holiday['mes'] == 1 else self.holiday['mes'] - 1
            print(day_of_week(self.holiday['dia'], month, self.year))
            print(self.holiday['dia'])
            print(months[self.holiday['mes'] - 1])
            print("Tipo:")
            print(self.holiday['tipo'])

# Código de prueba
# next_holiday = NextHoliday()
# next_holiday.fetch_holidays('trasladable')
# next_holiday.render()