from collections import defaultdict
from datetime import datetime

from flask import Flask, render_template, request


app = Flask(__name__)


VENDAS = [
	{"id_venda": 1, "data": "2026-08-01", "produto": "Notebook", "categoria": "Tecnologia", "quantidade": 2, "valor": 6000, "cliente": "Ana Souza", "regiao": "Sudeste", "horario": "09:15"},
	{"id_venda": 2, "data": "2026-08-01", "produto": "Mouse", "categoria": "Acessórios", "quantidade": 10, "valor": 500, "cliente": "Bruno Lima", "regiao": "Sul", "horario": "10:30"},
	{"id_venda": 3, "data": "2026-08-02", "produto": "Teclado", "categoria": "Acessórios", "quantidade": 5, "valor": 750, "cliente": "Carla Mendes", "regiao": "Sudeste", "horario": "14:20"},
	{"id_venda": 4, "data": "2026-08-02", "produto": "Notebook", "categoria": "Tecnologia", "quantidade": 3, "valor": 9000, "cliente": "Diego Alves", "regiao": "Nordeste", "horario": "15:10"},
	{"id_venda": 5, "data": "2026-08-03", "produto": "Monitor", "categoria": "Tecnologia", "quantidade": 4, "valor": 4800, "cliente": "Ana Souza", "regiao": "Sudeste", "horario": "11:45"},
	{"id_venda": 6, "data": "2026-08-03", "produto": "Mouse", "categoria": "Acessórios", "quantidade": 15, "valor": 750, "cliente": "Eduardo Reis", "regiao": "Centro-Oeste", "horario": "16:00"},
	{"id_venda": 7, "data": "2026-08-04", "produto": "Notebook", "categoria": "Tecnologia", "quantidade": 1, "valor": 3000, "cliente": "Carla Mendes", "regiao": "Sudeste", "horario": "18:30"},
	{"id_venda": 8, "data": "2026-08-04", "produto": "Teclado", "categoria": "Acessórios", "quantidade": 8, "valor": 1200, "cliente": "Fernanda Costa", "regiao": "Sul", "horario": "19:10"},
	{"id_venda": 9, "data": "2026-08-05", "produto": "Monitor", "categoria": "Tecnologia", "quantidade": 3, "valor": 3600, "cliente": "Bruno Lima", "regiao": "Nordeste", "horario": "13:25"},
	{"id_venda": 10, "data": "2026-08-05", "produto": "Mouse", "categoria": "Acessórios", "quantidade": 20, "valor": 1000, "cliente": "Ana Souza", "regiao": "Sudeste", "horario": "10:05"},
]


def analisar_vendas(vendas):
	def agrupar(chave, valor):
		resultado = defaultdict(int)
		for venda in vendas:
			resultado[venda[chave]] += venda[valor]
		return sorted(resultado.items(), key=lambda item: item[1], reverse=True)

	produtos = agrupar("produto", "valor")
	regioes = agrupar("regiao", "valor")
	quantidades = agrupar("produto", "quantidade")
	clientes = agrupar("cliente", "valor")
	horarios = agrupar("horario", "quantidade")
	melhor_produto = produtos[0][0] if produtos else "Sem dados"
	melhor_regiao = regioes[0][0] if regioes else "Sem dados"
	melhor_horario = horarios[0][0] if horarios else "Sem dados"

	return {
		"faturamento": sum(venda["valor"] for venda in vendas),
		"quantidade_vendas": len(vendas),
		"itens_vendidos": sum(venda["quantidade"] for venda in vendas),
		"produto_destaque": melhor_produto,
		"regiao_destaque": melhor_regiao,
		"horario_destaque": melhor_horario,
		"produto_potencial": quantidades[0][0] if quantidades else "Sem dados",
		"produtos": produtos,
		"quantidades": quantidades,
		"regioes": regioes,
		"clientes": clientes,
		"horarios": horarios,
	}


@app.route("/")
def inicio():
	return render_template("index.html")


@app.route("/dashboard")
def dashboard():
	periodo = request.args.get("periodo", "todos")
	vendas = VENDAS
	if periodo in {"01-03", "04-05"}:
		inicio, fim = (1, 3) if periodo == "01-03" else (4, 5)
		vendas = [venda for venda in VENDAS if inicio <= datetime.strptime(venda["data"], "%Y-%m-%d").day <= fim]
	return render_template("dashboard.html", analise=analisar_vendas(vendas), vendas=vendas, periodo=periodo)


@app.route("/admin", methods=["GET", "POST"])
def admin():
	mensagem = None
	if request.method == "POST":
		quantidade = int(request.form["quantidade"])
		valor = float(request.form["valor"].replace(",", "."))
		VENDAS.append({
			"id_venda": len(VENDAS) + 1,
			"data": request.form["data"],
			"produto": request.form["produto"].strip(),
			"categoria": request.form["categoria"],
			"quantidade": quantidade,
			"valor": valor,
			"cliente": request.form["cliente"].strip() or "Cliente não informado",
			"regiao": request.form["regiao"],
			"horario": request.form["horario"],
		})
		mensagem = "Venda adicionada. Os indicadores já foram atualizados."

	return render_template("admin.html", mensagem=mensagem, analise=analisar_vendas(VENDAS))


@app.route("/vendas")
def vendas():
	return render_template("vendas.html", vendas=VENDAS)


if __name__ == "__main__":
	app.run(debug=True)