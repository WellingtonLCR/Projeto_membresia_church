import unittest

from app import app


class MembresiaAppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def autenticar(self):
        with self.client.session_transaction() as sess:
            sess["usuario_logado"] = "teste@igreja.org"

    def test_rotas_publicas_renderizam(self):
        for rota in ["/", "/login", "/cadastro", "/sobre-equipe"]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 200)

    def test_rotas_privadas_exigem_login(self):
        resposta = self.client.get("/membros/listar", follow_redirects=False)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.headers["Location"])

    def test_listagens_privadas_renderizam_com_login(self):
        self.autenticar()

        for rota in ["/membros/listar", "/ministerios/listar", "/usuarios/listar"]:
            with self.subTest(rota=rota):
                resposta = self.client.get(rota)
                self.assertEqual(resposta.status_code, 200)

    def test_cadastro_valida_senha_minima(self):
        resposta = self.client.post(
            "/cadastro",
            data={
                "nome": "Pessoa Teste",
                "email": "pessoa@igreja.org",
                "senha": "123",
                "confirma_senha": "123",
            },
            follow_redirects=True,
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("A senha deve ter pelo menos 8 caracteres".encode(), resposta.data)

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

        for rota in ["/membros/excluir/101", "/membros/inativar/101", "/ministerios/excluir/201", "/usuarios/excluir/1"]:
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
