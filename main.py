import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Diretório para salvar os arquivos CSV
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

comando_sql = """
  SELECT codigo, nome, quantidade
  FROM PL01;
"""

@app.route('/')
def index():
    return render_template('index.html')

# Rota para buscar resultados
@app.route('/buscar_resultados/<codigo>')
def buscar_resultados(codigo):
    conexao = sqlite3.connect("estoque.db")
    cursor = conexao.cursor()
    cursor.execute(f"SELECT codigo, nome, quantidade FROM PL01 WHERE codigo = ?",
                 (codigo, ))
    dados = cursor.fetchall()
    return render_template("resultados.html", data=dados)

# Rota para fazer upload do arquivo CSV
@app.route('/base_de_dados', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # Se o usuário não selecionou nenhum arquivo, retorne para a página
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Salva o arquivo no diretório UPLOAD_FOLDER
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)