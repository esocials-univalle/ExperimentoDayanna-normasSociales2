from datetime import datetime, timedelta

from otree.views.admin import AdminReport

from ._builtin import Page, WaitPage

from django.utils.crypto import get_random_string


class MyPage(Page):
    form_model = 'player'


class SessionBase(object):

    def post(self, *args, **kwargs):
        session_payoff = 4000
        percentage_saved = self.player.percentage_saved
        saved = 0

        print("payoff antes del proceso", self.player.payoff)

        # if self.player.intermedio_actual2 == 1:
        #     self.player.intermedio2 = self.player.intermedio2 + 1

        if self.player.money_decision == 0:
            disbursement = 4000
            print("desicion 0")
            if self.player.sesion == 1:
                self.player.montoahorrosesion1 = 0
                self.player.pagoAhorroSession1 = 0
                self.player.montoSesion1 = 4000
            elif self.player.sesion == 2:
                self.player.montoahorrosesion2 = 0
                self.player.pagoAhorroSession2 = 0
                self.player.montoSesion2 = 4000
        elif self.player.money_decision == 1:
            saved = (percentage_saved / 100) * session_payoff
            disbursement = session_payoff - saved
            print("desicion 1")
            if self.player.sesion == 1:
                self.player.montoahorrosesion1 = int(saved)
            elif self.player.sesion == 2:
                self.player.montoahorrosesion2 = int(saved)
        elif self.player.money_decision == 2:
            saved = session_payoff
            disbursement = 0
            print("desicion 2")
            if self.player.sesion == 1:
                self.player.montoahorrosesion1 = session_payoff
            elif self.player.sesion == 2:
                self.player.montoahorrosesion2 = session_payoff
        if saved:
            print("guarde dinero")
            print("dinero guardado", saved)
            # money = 50 if self.player.intermedio_actual2 == 1 else 25
            if self.player.sesion == 1:
                money = 50
                saved_parcial = saved
                print("money ", money)
                self.player.pagoAhorroSession1 = int((saved / 100) * money)
                saved += int((saved / 100) * money)
                self.player.montoSesion1 = int((session_payoff-saved_parcial) + saved)
            elif self.player.sesion == 2:
                money = 25
                saved_parcial = saved
                print("money ", money)
                self.player.pagoAhorroSession2 = int((saved / 100) * money)
                saved += int((saved / 100) * money)
                self.player.montoSesion2 = int((session_payoff-saved_parcial) + saved)

            # print("money ", money)
            # saved += int((saved / 100) * money)
        print("saved final ", saved)
        self.player.payoff = self.player.payoff + saved
        self.player.disbursement = self.player.disbursement + disbursement
        self.player.save()
        print("payoff ", self.player.payoff)
        print("disbursement", self.player.disbursement)
        return super(SessionBase, self).post(*args, **kwargs)


class EncuestaSocioEconomica(Page):
    template_name = 'experimiento_1/encuesta_economica.html'
    form_model = 'player'
    form_fields = [
        'survey'
    ]

    def js_vars(self):
        return dict(
            codigo=self.player.codigo,
        )


class Session1(SessionBase, Page):
    print("hola")
    
    form_model = 'player'
    form_fields = [
        'dataSession1'
    ]

    def js_vars(self):
        return dict(
            codigo=self.player.codigo,
        )
    # template_name = 'experimiento_1/session_1.html'
    # form_model = 'player'
    # form_fields = ['file_session_1']
    # document = 'experimento_1/session_1.pdf'
    title = 'Sesión 1'
    # text_info = "Las siguientes páginas hacen parte del libro: La Era del Desarrollo Sostenible (2014), y es necesario para nosotros transcribir la información contenida en el documento. El tiempo aproximado del siguiente trabajo es de 15 min, en caso de no terminar de digitar el documento en el tiempo estipulado puede enviar lo trabajado. Por favor, transcriba la información en el espacio disponible. "

    def get_context_data(self, *args, **kwargs):
        context = super(Session1, self).get_context_data(*args, **kwargs)
    #     context['text_info'] = self.text_info
    #     context['document_url'] = self.document
        self.player.montoTranscripcion1 = 4000-self.player.montoahorrosesion1
        self.player.sesion += 1
        return context


class Session2(SessionBase, Page):
    form_model = 'player'
    form_fields = [
        'dataSession2'
    ]

    def js_vars(self):
        return dict(
            codigo=self.player.codigo,
        )
    # template_name = 'experimiento_1/session_1.html'
    # form_model = 'player'
    # form_fields = ['file_session_2']
    # document = 'experimento_1/session_2.pdf'

    # text_info = "Las siguientes páginas hacen parte del libro: Decrecimiento. Vocabulario ara la nueva era (2015), y es necesario para nosotros transcribir la información contenida en el documento. El tiempo aproximado del siguiente trabajo es de 15 min, en caso de no terminar de digitar el documento en el tiempo estipulado puede enviar lo trabajado. Por favor, transcriba la información en el espacio disponible. "

    def get_context_data(self, *args, **kwargs):
        context = super(Session2, self).get_context_data(*args, **kwargs)
    #     context['text_info'] = self.text_info
    #     context['document_url'] = self.document
        self.player.montoTranscripcion2 = 4000-self.player.montoahorrosesion2
        self.player.sesion += 1
        return context


class Session3(Page):
    form_model = 'player'
    form_fields = [
        'dataSession3'
    ]

    def js_vars(self):
        return dict(
            codigo=self.player.codigo,
        )
    # template_name = 'experimiento_1/session_1.html'
    # form_model = 'player'
    # form_fields = ['file_session_3']
    # document = 'experimento_1/session_3.pdf'
    # text_info = "Las siguientes páginas hacen parte del libro: Prosperidad sin crecimiento (2011), y es necesario para nosotros transcribir la información contenida en el documento. El tiempo aproximado del siguiente trabajo es de 15 min, en caso de no terminar de digitar el documento en el tiempo estipulado puede enviar lo trabajado. Por favor, transcriba la información en el espacio disponible. "

    def get_context_data(self, *args, **kwargs):
        context = super(Session3, self).get_context_data(*args, **kwargs)
    #     context['text_info'] = self.text_info
    #     context['document_url'] = self.document
        self.player.montoTranscripcion3 = 4000
        self.player.montoSesion3 = 4000
        self.player.payoff += 4000
        self.player.sesion += 1
        return context


class Session4(Page):
    template_name = 'experimiento_1/session_2.html'
    form_model = 'player'
    form_fields = ['Monto', 'coin_select']
    # live_method ='live_moneda'

    def post(self, *args, **kwargs):
        monto = int(self.request.POST.get('Monto'))
        if self.request.POST.get('coin_select') == '0':
            self.player.pagoMoneda = int(
                (5000 - monto) + monto + (monto * 0.5))
            self.player.moneda = "rojo"
            self.player.payoff += (5000 - monto) + monto + (monto * 0.5)
        elif self.request.POST.get('coin_select') == '1':
            self.player.pagoMoneda = int(5000 - monto)
            self.player.moneda = "azul"
            self.player.payoff += (5000 - monto)
        self.player.save()
        return super(Session4, self).post(*args, **kwargs)


class resultados_sesiones(Page):
    def vars_for_template(self):

        mensaje = ""

        if self.player.money_decision == 0:
            mensaje = "Ha finalizado esta sesión. Por completarla usted ha ganado $4000 COP, los cuales se verán reflejados en su cuenta al finalizar el día. "
        if self.player.money_decision == 1:
            self.player.percentage_saved
            mensaje = "Ha finalizado esta sesión. Por completarla usted ha ganado $4000 COP y ha decidido guardar el " + str(self.player.percentage_saved) + "%, el cual será transferido al finalizar la tercera sesión. Mientras que el porcentaje restante será transferido al final del día."
        if self.player.money_decision == 2:
            mensaje = "Ha finalizado esta sesión. Por completarla usted ha ganado $4000 COP y ha decidido guardar la totalidad del pago, el cual será transferido al finalizar la tercera sesión. "

        return {
            "mensaje": mensaje,

        }


class Informacion(Page):

    def js_vars(self):
        return dict(
            intermedio_actual=self.player.intermedio_actual,
        )

    def vars_for_template(self):

        money = 50 if self.player.intermedio_actual == 1 else 25

        return {
            "price_session": money,
        }


class Informacion2(Page):

    def js_vars(self):
        return dict(
            intermedio_actual=self.player.intermedio_actual,
        )

    def vars_for_template(self):

        money = 50 if self.player.intermedio_actual == 1 else 25

        return {
            "price_session": money,
        }


class Informacion_moneda(Page):
    def vars_for_template(self):
        return {
            "1": 2,
        }


class IntermedioSession(Page):
    template_name = 'experimiento_1/intermedio.html'
    form_model = 'player'
    form_fields = ['money_decision', 'percentage_saved']

    def get_context_data(self, *args, **kwargs):
        context = super(IntermedioSession, self).get_context_data(
            *args, **kwargs)
        return context

    def get_form(self, *args, **kwargs):
        form = super(IntermedioSession, self).get_form(*args, **kwargs)
        new_decisions = []
        money = 50 if self.player.intermedio_actual == 1 else 25
        fecha_inicial_var= 15 if self.player.intermedio_actual == 1 else 8
        fecha_final_var=22 if self.player.intermedio_actual == 1 else 16

        for field in form.fields['money_decision'].choices:
            new_decisions.append(
                (field[0], field[1].format(price_session=money, fecha_inicial= fecha_inicial_var, fecha_final=fecha_final_var)))
        form.fields['money_decision'].choices = new_decisions
        return form

    def post(self, *args, **kwargs):
        money_decision = self.request.POST.get('money_decision')
        percentage_saved = self.request.POST.get('percentage_saved')

        self.player.intermedio = self.player.intermedio + 1
        self.player.save()
        return super(IntermedioSession, self).post(*args, **kwargs)

    def js_vars(self):
        return dict(
            sesion=1 if self.player.intermedio_actual == 1 else 2,
        )

    live_method = 'live_intermedio'


class SevenDaysWaitPage(Page):
    template_name = 'experimiento_1/wait_page.html'

    def get_context_data(self, *args, **kwargs):
        day_available = self.player.updated_at.replace(
            hour=0, tzinfo=None) + timedelta(days=1)
        today = datetime.now()
        context = super(SevenDaysWaitPage, self).get_context_data(
            *args, **kwargs)
        context['day_available'] = day_available
        context['can_access'] = today > day_available
        return context


class Consent(Page):
    def vars_for_template(self):
        self.player.codigo = get_random_string(8)
        print(self.player.codigo)

    form_model = 'player'  # Le dice que es un jugador
    form_fields = ['num_temporal','terminos_actividad']


class EndGame(Page):
    def is_displayed(self):
        if self.player.consentimiento == False:
            return True
        if self.player.terminos_actividad == False:
            return True
        if self.round_number == Constants.num_rounds:
            return True
        else:
            return False


class cuestionario(Page):
    template_name = 'experimiento_1/cuestionario.html'
    form_model = 'player'
    form_fields = [
        'cuestionario'
    ]

    def js_vars(self):
        return dict(
            codigo=self.player.codigo,
        )


class sesion_3(Page):
    template_name = 'experimiento_1/sesion_3.html'
    form_model = 'player'


class sesion_E(Page):
    template_name = 'experimiento_1/sesion_E.html'
    form_model = 'player'


class Results(Page):

    def vars_for_template(self):
        self.player.is_final = True
        return{
            "montoahorrosesion1": self.player.montoahorrosesion1,
            "pagoAhorroSession1": self.player.pagoAhorroSession1,
            "montoSesion1": self.player.montoSesion1,
            "ahorroSesión1": self.player.montoahorrosesion1 + self.player.pagoAhorroSession1,
            "montoahorrosesion2": self.player.montoahorrosesion2,
            "pagoAhorroSession2": self.player.pagoAhorroSession2,
            "montoSesion2": self.player.montoSesion2,
            "ahorroSesión2": self.player.montoahorrosesion2 + self.player.pagoAhorroSession2,
            "montoSesion3": self.player.montoSesion3,
            "pagoMoneda": self.player.pagoMoneda,
            "moneda": self.player.moneda,
        }


class Final(Page):
    template_name = 'experimiento_1/Final.html'
    form_model = 'player'
    def is_displayed(self):
        if self.player.terminos_actividad == False:
            return True
        if self.player.is_final == True:
            return True
           


class PaginaEspera(Page):
    timeout_seconds = 604800

    def vars_for_template(self):
        return{
            "": 2,
        }


page_sequence = [
    Consent,
    Final,
    MyPage,
    Informacion,
    IntermedioSession,
    cuestionario,
    Session1,
    EncuestaSocioEconomica,
    resultados_sesiones,
    PaginaEspera,
    # SevenDaysWaitPage,
    Informacion2,
    IntermedioSession,
    Session2,
    resultados_sesiones,
    PaginaEspera,
    # SevenDaysWaitPage,
    sesion_3,
    Session3,
    Informacion_moneda,
    Session4,
    Results,
    Final
]
