import json
from datetime import datetime, timedelta
from random import randint

from django.db import models as django_models
from django.forms import Textarea
from model_utils import FieldTracker
from otree.api import (
    models,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer, widgets,
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    players_per_group = None
    name_in_url = 'experimiento_1'
    num_rounds = 1
    experiment_days = 15


class Subsession(BaseSubsession):
    tipo_de_juego = models.IntegerField(default=1)
    resultados_anteriores = models.StringField(blank=True)
    etapa_actual = models.IntegerField(default=1)

    def vars_for_admin_report(self):
        survey_keys = []
        survey_items = []
        cuestionario_items = []
        dataSession1_items = []
        dataSession2_items = []
        dataSession3_items = []
        for player in self.get_players():
            survey_data = json.loads(player.survey) if player.survey else {}
            cuestionario = json.loads(
                player.cuestionario) if player.cuestionario else {}
            dataSession1_variable = json.loads(
                player.dataSession1) if player.dataSession1 else {}
            dataSession2_variable = json.loads(
                player.dataSession2) if player.dataSession2 else {}
            dataSession3_variable = json.loads(
                player.dataSession3) if player.dataSession3 else {}
            dataSession1_items.append(dataSession1_variable)
            dataSession2_items.append(dataSession2_variable)
            dataSession3_items.append(dataSession3_variable)
            survey_items.append(survey_data)
            cuestionario_items.append(cuestionario)
        return dict(dataSession1=json.dumps(dataSession1_items), dataSession2=json.dumps(dataSession2_items), dataSession3=json.dumps(dataSession3_items), survey=json.dumps(survey_items), cuestionario=json.dumps(cuestionario_items), )


class Constants(BaseConstants):
    players_per_group = None
    name_in_url = 'experimiento_1'
    num_rounds = 1
    experiment_days = 15


class Group(BaseGroup):

    def players_info(self):
        query = Player.objects.filter(group_id=self.id)
        user_number = query.count()
        money_decisions_group = [
            query.filter(money_decision=0).count(),
            query.filter(money_decision=1).count(),
            query.filter(money_decision=2).count()
        ]

        return [int((value / user_number) * 100) for value in money_decisions_group]


CONTRACT_TYPE = [
    (0, 'Contrato informal (CI)'),
    (1, 'Contrato formal (CF)'),
]

MONEY_DECISION_CHOICES = [
    (0, 'Recibir los $4.000 al finalizar el día.'),
    (1, 'Guardar una parte de su pago y por cada $100 que decida guardar '
        'nosotros le daremos ${price_session} más. Podrá recibir en esta sesión una parte de su '
        'pago y el monto guardado será transferido en la última sesión, es decir, entre {fecha_inicial} y {fecha_final} días a partir de hoy.'),
    (2, 'Guardar la totalidad de su pago y recibirlo al finalizar la tercera sesión; '
        'es decir, entre {fecha_inicial} y {fecha_final} días a partir de hoy. '
        'Recuerde que por cada $100 nosotros le daremos ${price_session} más.'),
]


class Player(BasePlayer):

    # Variables
    decisionsesion1 = models.StringField()
    ahorrosesion1 = models.BooleanField(default=False)
    montoahorrosesion1 = models.IntegerField(default=0)
    pagoAhorroSession1 = models.IntegerField(default=0)

    decisionsesion2 = models.StringField()
    ahorrosesion2 = models.BooleanField(default=False)
    montoahorrosesion2 = models.IntegerField(default=0)
    pagoAhorroSession2 = models.IntegerField(default=0)

    montoTranscripcion1 = models.IntegerField(default=0)
    montoTranscripcion2 = models.IntegerField(default=0)
    montoTranscripcion3 = models.IntegerField(default=0)

    montoSesion1 = models.IntegerField(default=0)
    montoSesion2 = models.IntegerField(default=0)
    montoSesion3 = models.IntegerField(default=0)

    pagoMoneda = models.IntegerField(default=0)
    moneda = models.StringField()

    # def live_moneda(self, data):
    #     # if (data['resultado'] == 'azul'):
    #     #     self.pagoMoneda = 5000 - int(data['monto'])
    #     # elif (data['resultado'] == 'azul'):
    #     #     self.pagoMoneda = (5000-int(data['monto'])) + (int(data['monto'])*0.5) + int(data['monto'])

    #     print(self.pagoMoneda)

    def live_intermedio(self, data):

        if (data['type'] == 'sesion1'):
            if (data['decision'] == 0):
                self.decisionsesion1 = MONEY_DECISION_CHOICES[0][1]
            elif (data['decision'] == 1):
                self.decisionsesion1 = MONEY_DECISION_CHOICES[1][1]
                self.ahorrosesion1 = True
                self.montoahorrosesion1 = int((4000*data['porcentaje'])/100)
            elif (data['decision'] == 2):
                self.decisionsesion1 = MONEY_DECISION_CHOICES[2][1]
        elif (data['type'] == 'sesion2'):
            if (data['decision'] == 0):
                self.decisionsesion2 = MONEY_DECISION_CHOICES[0][1]
            elif (data['decision'] == 1):
                self.decisionsesion2 = MONEY_DECISION_CHOICES[1][1]
                self.ahorrosesion2 = True
                self.montoahorrosesion2 = int((4000*data['porcentaje'])/100)
            elif (data['decision'] == 2):
                self.decisionsesion2 = MONEY_DECISION_CHOICES[2][1]

        # print(self.decisionsesion1)
        # print(self.ahorrosesion1)
        # print(self.montoahorrosesion1)

        # print(self.decisionsesion2)
        # print(self.ahorrosesion2)
        # print(self.montoahorrosesion2)

    sesion = models.IntegerField(default=0)

    codigo = models.StringField()

    terminos_actividad = models.BooleanField(
        label='¿Acepta los términos de esta actividad?',
        choices=[
            [True, "Sí"],
            [False, "No"],
        ],
        widget=widgets.RadioSelectHorizontal
    )

    is_final = models.BooleanField(initial=False)

    num_temporal = models.IntegerField(
        label="Por favor, ingrese el número de identificación temporal que le llegó en el mensaje de invitación")
    accepts_data = models.BooleanField(
        label="¿Autoriza el uso de los datos recolectados para futuros estudios?",
        choices=[
            [True, "Sí"],
            [False, "No"],
        ],
        default=True
    )
    accepts_terms = models.BooleanField()

    coin_select = models.IntegerField(null=True,
                                      label="Cara obtenida",
                                      choices=[
                                          [0, "Cara"],
                                          [1, "Sello"],
                                      ]
                                      )

    money_decision = models.IntegerField(choices=MONEY_DECISION_CHOICES, blank=False,
                                         verbose_name="¿Cómo desea recibir el dinero de la sesión de hoy?",
                                         widget=widgets.RadioSelect)
    contract_type = models.IntegerField(choices=CONTRACT_TYPE)
    experiment_start_date = django_models.DateTimeField(auto_now=True)
    intermedio = models.IntegerField(default=0)
    percentage_saved = models.IntegerField(
        max=100, min=0, default=0, verbose_name="Porcentaje guardado")
    file_session_1 = models.LongStringField(default="", verbose_name="Ingrese el texto del documento",
                                            widget=Textarea(attrs={'rows': 40, 'cols': 40}))
    file_session_2 = models.LongStringField(default="", verbose_name="Ingrese el texto del documento",
                                            widget=Textarea(attrs={'rows': 40, 'cols': 40}))
    file_session_3 = models.LongStringField(default="", verbose_name="Ingrese el texto del documento",
                                            widget=Textarea(attrs={'rows': 40, 'cols': 40}))
    Monto = models.IntegerField(max=5000, min=0, default=0)
    updated_at = django_models.DateTimeField(auto_now=True)
    disbursement = models.CurrencyField(
        null=True, doc="Valor retirado", default=0)
    survey = models.LongStringField()
    cuestionario = models.LongStringField()
    tracker = FieldTracker()

    dataSession1 = models.LongStringField()
    dataSession2 = models.LongStringField()
    dataSession3 = models.LongStringField()

    def start(self):
        if not self.contract_type:
            self.experiment_start_date = datetime.now()

            if self.session.config['tipo'] == "linea_base_contrato_informal":
                self.contract_type = 0
                self.save()
            elif self.session.config['tipo'] == "linea_base_contrato_formal":
                self.contract_type = 1
                self.save()

            # self.contract_type = randint(0, 1)
            # self.save()

    @property
    def intermedio_actual(self):
        return self.intermedio + 1

    intermedio2 = models.IntegerField(default=0)

    @property
    def intermedio_actual2(self):
        print("en intermedio actual 2 ", self.intermedio2)
        return self.intermedio2 + 1

    @property
    def experiment_end_date(self):
        return self.experiment_start_date + timedelta(days=Constants.experiment_days)
