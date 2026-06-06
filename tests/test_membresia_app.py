import unittest
from datetime import datetime
from unittest.mock import patch

from app import app


class MembresiaAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def autenticar(self):
        with self.client.session_transaction() as sess:
            sess["usuario_logado"] = "teste@igreja.org"
            sess["usuario_nome"] = "Usuario Teste"
            sess["usuario_perfil"] = "Administrador"
            sess["usuario_id"] = 1

    def test_rotas_publicas_renderizam(self):
        for rota in [
            "/",
            "/login",
            "/cadastro",
            "/sobre-equipe",
            "/app",
            "/app/eventos",
            "/app/cultos",
            "/app/feed",
            "/app/devocional",
            "/app/oracao",
            "/app/doacoes",
            "/app/cadastro",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 200)

    def test_app_usuario_home_exibe_conteudo_alimentado_pelo_admin(self):
        evento = {
            "id": 10,
            "nome": "Culto Jovem",
            "data_inicio": datetime(2026, 6, 12, 20, 0),
            "local": "Templo principal",
            "banner_path": None,
        }
        aviso = {
            "titulo": "Aviso Admin",
            "categoria": "Comunicado",
            "conteudo": "Conteúdo publicado pelo painel administrativo.",
        }
        devocional = {
            "titulo": "Devocional Admin",
            "categoria": "Devocional",
            "conteudo": "Reflexão publicada pela equipe.",
        }

        def config(chave, padrao=""):
            valores = {
                "programacao.domingo": "Domingo às 18h",
                "programacao.quarta": "Quarta às 20h",
                "programacao.celulas": "Durante a semana",
                "doacao.mensagem": "Mensagem de contribuição configurada no painel.",
            }
            return valores.get(chave, padrao)

        with patch("app.obter_igreja", return_value={"nome": "Igreja Teste", "endereco": "Rua Central"}), \
             patch("app.listar_eventos_publicos", return_value=[evento]), \
             patch("app.listar_mural_publico", side_effect=[[aviso], [devocional]]), \
             patch("app.gerar_metricas_app", return_value={"eventos": 1, "avisos": 1, "devocionais": 1, "testemunhos": 0, "visitantes": 3}), \
             patch("app.gerar_metricas", return_value={}), \
             patch("app.obter_config", side_effect=config):
            resposta = self.client.get("/app")

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Culto Jovem".encode(), resposta.data)
        self.assertIn("Aviso Admin".encode(), resposta.data)
        self.assertIn("Devocional Admin".encode(), resposta.data)
        self.assertIn("Domingo".encode(), resposta.data)

    def test_app_usuario_evento_inexistente_redireciona_para_agenda(self):
        resposta = self.client.get("/app/eventos/999999", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app/eventos", resposta.headers["Location"])

    def test_app_usuario_oracao_valida_campos_obrigatorios(self):
        resposta = self.client.post(
            "/app/oracao",
            data={"solicitante_nome": "", "pedido": ""},
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe seu nome e o pedido de oração".encode(), resposta.data)

    def test_rotas_privadas_exigem_login(self):
        resposta = self.client.get("/membros/listar", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])

    def test_listagens_privadas_renderizam_com_login(self):
        self.autenticar()

        for rota in [
            "/pessoas/painel",
            "/pessoas/aniversarios",
            "/membros/listar",
            "/financeiro/painel",
            "/financeiro/receitas",
            "/financeiro/despesas",
            "/financeiro/cadastros",
            "/financeiro/categorias",
            "/financeiro/centros-custo",
            "/financeiro/contas",
            "/financeiro/formas-recebimento",
            "/financeiro/formas-pagamento",
            "/ministerios/listar",
            "/ministerios/painel",
            "/usuarios/listar",
            "/celulas/listar",
            "/celulas/painel",
            "/eventos/listar",
            "/financeiro/listar",
            "/comunicacao/painel",
            "/comunicacao/listar",
            "/relatorios/listar",
            "/configuracoes/listar",
            "/configuracoes/igreja",
            "/configuracoes/historia",
            "/configuracoes/informacoes",
            "/configuracoes/programacao",
            "/configuracoes/permissoes",
            "/configuracoes/app",
            "/configuracoes/modulos",
            "/familias/listar",
            "/fornecedores/listar",
            "/doacoes/listar",
            "/mural/listar",
            "/intercessao/painel",
            "/intercessao/listar",
            "/intercessao/testemunhos",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 200)

    def test_cadastro_publico_exige_contato_para_visitante(self):
        resposta = self.client.post(
            "/cadastro",
            data={
                "nome": "Pessoa Teste",
            },
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe seu nome e pelo menos um contato".encode(), resposta.data)

    def test_cadastro_publico_registra_visitante_no_app(self):
        with patch("app.email_membro_em_uso", return_value=False), patch("app.db_write") as db_write:
            resposta = self.client.post(
                "/app/cadastro",
                data={
                    "nome": "Visitante Teste",
                    "email": "visitante@exemplo.com",
                    "telefone": "(14) 99999-9999",
                    "whatsapp": "(14) 99999-9999",
                    "interesse": "Quero conhecer a igreja",
                    "mensagem": "Participei do culto pelo app.",
                },
                follow_redirects=False,
            )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/app", resposta.headers["Location"])
        sql, params = db_write.call_args.args
        self.assertIn("INSERT INTO membros", sql)
        self.assertIn("'Visitante'", sql)
        self.assertEqual(params[0], "Visitante Teste")
        self.assertEqual(params[3], "visitante@exemplo.com")
        self.assertIn("Cadastro realizado pelo app do usuário", params[5])

    def test_inserir_membro_valida_telefone(self):
        self.autenticar()

        resposta = self.client.post(
            "/membros/inserir",
            data={"nome": "Novo Membro", "telefone": "123", "ministerio": "Louvor"},
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Informe um telefone v".encode(), resposta.data)

    def test_login_redireciona_para_listagem_de_usuarios(self):
        resposta = self.client.post(
            "/login",
            data={"email": "admin@igreja.org", "senha": "admin123"},
            follow_redirects=False,
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/usuarios/listar", resposta.headers["Location"])

    def test_exclusao_logica_nao_aceita_get(self):
        self.autenticar()

        for rota in [
            "/membros/excluir/101",
            "/membros/inativar/101",
            "/ministerios/excluir/201",
            "/usuarios/excluir/1",
            "/familias/excluir/1",
            "/fornecedores/excluir/1",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 405)

    def test_acoes_operacionais_nao_aceitam_get(self):
        self.autenticar()

        for rota in [
            "/mural/publicar/1",
            "/mural/arquivar/1",
            "/intercessao/orar/1",
            "/intercessao/responder/1",
            "/intercessao/arquivar/1",
            "/doacoes/receber/1",
            "/doacoes/cancelar/1",
        ]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 405)

    def test_inativar_membro_usa_post_com_redirect(self):
        self.autenticar()

        resposta = self.client.post("/membros/inativar/103", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/membros/listar", resposta.headers["Location"])


if __name__ == "__main__":
    unittest.main()
