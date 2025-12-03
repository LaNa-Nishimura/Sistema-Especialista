from flask import Flask, render_template, request
from experta import *

app = Flask(__name__)

# --------------------------
# Sistema Especialista
# --------------------------

class Sintoma(Fact):
    pass

class DiagnosticoVideiras(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.resultados = []

    def registrar(self, texto):
        self.resultados.append(texto)

    @Rule(Sintoma(manchas_amarelas=True), Sintoma(folhas_murchas=True))
    def mildio(self):
        self.registrar("Possível <b>Míldio</b> (manchas + murcha).")

    @Rule(Sintoma(poeira_branca=True))
    def oidio(self):
        self.registrar("Possível <b>Oídio</b> (pó branco).")

    @Rule(Sintoma(frutos_escurecidos=True))
    def podridao_negra(self):
        self.registrar("Possível <b>Podridão Negra</b> (frutos escurecidos).")

    @Rule(Sintoma(caule_lesoes=True))
    def cancro(self):
        self.registrar("Possível <b>Cancro</b> (lesões no caule).")

    @Rule(Sintoma(manchas_marrons=True), Sintoma(mofo_cinza=True))
    def botrytis(self):
        self.registrar("Possível <b>Botrytis (mofo cinzento)</b> (manchas marrons + mofo cinza).")

    @Rule(Sintoma(galhos_quebradicos=True), Sintoma(folhas_murchas=True))
    def estresse(self):
        self.registrar("Possível <b>Estresse hídrico</b> (galhos frágeis + folhas murchas).")

    @Rule(Sintoma(insetos=True), Sintoma(folhas_murchas=True))
    def acaros(self):
        self.registrar("Possível <b>Ataque de ácaros</b> (insetos + folhas murchas).")

    @Rule(Sintoma(solo_encharcado=True), Sintoma(folhas_murchas=True))
    def asfixia(self):
        self.registrar("Possível <b>Asfixia radicular</b> (solo encharcado + murcha).")

    @Rule(Sintoma(manchas_amarelas=True), Sintoma(poeira_branca=True))
    def combinada(self):
        self.registrar("Possível <b>Infecção combinada: Míldio + Oídio</b> (manchas + pó branco).")

    @Rule(Sintoma(manchas_marrons=True), Sintoma(frutos_escurecidos=True))
    def podridao_acida(self):
        self.registrar("Possível <b>Podridão ácida</b> (manchas marrons + frutos moles/escuros).")


# --------------------------
# ROTA WEB
# --------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        sintomas = {chave: True for chave in request.form.keys()}

        engine = DiagnosticoVideiras()
        engine.reset()
        engine.declare(Sintoma(**sintomas))
        engine.run()

        if not engine.resultados:
            return render_template("index.html", resultado="Nenhuma doença encontrada.")

        html_resultado = "<br>".join(engine.resultados)
        return render_template("index.html", resultado=html_resultado)

    return render_template("index.html", resultado=None)


if __name__ == "__main__":
    app.run(debug=True)