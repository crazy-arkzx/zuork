import os
import requests
import json
from colorama import init, Fore, Style
import urllib.parse
import re

init(autoreset=True)

class DiscordWebhookCreator:
    def __init__(self):
        self.webhooks = self.load_webhooks()

    def load_webhooks(self):
        try:
            with open('webhooks.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_webhooks(self):
        with open('webhooks.json', 'w') as f:
            json.dump(self.webhooks, f, indent=4)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def banner(self):
        self.clear_screen()
        print(Fore.CYAN + r"""
 ██╗███╗   ███╗     ███████╗██╗   ██╗ ██████╗ ██████╗ ██╗  ██╗
 ██║████╗ ████║     ╚══███╔╝██║   ██║██╔═══██╗██╔══██╗██║ ██╔╝
 ██║██╔████╔██║       ███╔╝ ██║   ██║██║   ██║██████╔╝█████╔╝ 
 ██║██║╚██╔╝██║      ███╔╝  ██║   ██║██║   ██║██╔══██╗██╔═██╗ 
 ██║██║ ╚═╝ ██║     ███████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██╗
 ╚═╝╚═╝     ╚═╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

    ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄
   ████████████  ████████████  ████████████
   █░░░░░░░░░░█  █░░░░░░░░░░█  █░░░░░░░░░░█
   █░░░ZUORK░░█  █░WEBHOOK░░█  █░CREATOR░░█
   █░░░░░░░░░░█  █░░░░░░░░░░█  █░░░░░░░░░░█
    ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀

    ╔═══════════════════════════════╗
        ZUORK  |  WEBHOOK CREATOR       
    ╚═══════════════════════════════╝         
                                                                       
""" + Style.RESET_ALL)
        print(Fore.YELLOW + "===== Webhook Creator =====" + Style.RESET_ALL)

    def validar_url(self, url):
        url_regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_regex.match(url) is not None

    def menu_principal(self):
        while True:
            self.banner()
            print(Fore.GREEN + "1. " + Fore.WHITE + "Criar Novo Webhook")
            print(Fore.GREEN + "2. " + Fore.WHITE + "Listar Webhooks")
            print(Fore.GREEN + "3. " + Fore.WHITE + "Enviar Mensagem")
            print(Fore.GREEN + "4. " + Fore.WHITE + "Enviar Embed")
            print(Fore.GREEN + "5. " + Fore.WHITE + "Excluir Webhook")
            print(Fore.YELLOW + "6. " + Fore.WHITE + "Config Webhook")
            print(Fore.RED + "0. " + Fore.WHITE + "Sair")
            
            escolha = input(Fore.YELLOW + "\nEscolha uma Opção: " + Style.RESET_ALL)

            if escolha == '1':
                self.criar_webhook()
            elif escolha == '2':
                self.listar_webhooks()
            elif escolha == '3':
                self.enviar_mensagem_simples()
            elif escolha == '4':
                self.enviar_mensagem_embed()
            elif escolha == '5':
                self.excluir_webhook()
            elif escolha == '6':
                self.configuracoes_webhook()
            elif escolha == '0':
                print(Fore.GREEN + "\nObrigado por Usar o Zuork! Até Logo." + Style.RESET_ALL)
                break
            else:
                input(Fore.RED + "Opção Inválida. Pressione Enter Para Continuar..." + Style.RESET_ALL)

    def configuracoes_webhook(self):
        while True:
            self.clear_screen()
            print(Fore.CYAN + "===== CONFIGURAÇÕES WEBHOOK =====" + Style.RESET_ALL)
            print(Fore.GREEN + "1. " + Fore.WHITE + "Editar Webhook")
            print(Fore.GREEN + "2. " + Fore.WHITE + "Exportar Webhooks")
            print(Fore.GREEN + "3. " + Fore.WHITE + "Importar Webhooks")
            print(Fore.RED + "0. " + Fore.WHITE + "Voltar")
            
            escolha = input(Fore.YELLOW + "\nEscolha uma Opção: " + Style.RESET_ALL)
            
            if escolha == '1':
                self.editar_webhook()
            elif escolha == '2':
                self.exportar_webhooks()
            elif escolha == '3':
                self.importar_webhooks()
            elif escolha == '0':
                break
            else:
                input(Fore.RED + "Opção Inválida. Pressione Enter Para Continuar..." + Style.RESET_ALL)

    def editar_webhook(self):
        if not self.webhooks:
            input(Fore.RED + "Nenhum Webhook Salvo. Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        print(Fore.YELLOW + "Webhooks Salvas:" + Style.RESET_ALL)
        for i, nome in enumerate(self.webhooks.keys(), 1):
            print(f"{Fore.GREEN}{i}. {Fore.WHITE}{nome}")
        
        try:
            escolha = int(input(Fore.YELLOW + "\nEscolha um Webhook Para Editar (número): " + Style.RESET_ALL))
            nome_webhook = list(self.webhooks.keys())[escolha - 1]
        except (ValueError, IndexError):
            input(Fore.RED + "Escolha Inválida. Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        novo_nome = input(Fore.YELLOW + f"Novo Nome Para o Webhook '{nome_webhook}' (Deixe em Branco Para Manter): " + Style.RESET_ALL)
        nova_url = input(Fore.YELLOW + "Nova URL do Webhook (Deixe em Branco Para Manter): " + Style.RESET_ALL)
        
        if novo_nome and novo_nome != nome_webhook:
            self.webhooks[novo_nome] = self.webhooks.pop(nome_webhook)
            nome_webhook = novo_nome
        
        if nova_url:
            if not nova_url.startswith('https://discord.com/api/webhooks/'):
                input(Fore.RED + "URL Inválida! Pressione Enter Para Continuar." + Style.RESET_ALL)
                return
            
            self.webhooks[nome_webhook] = nova_url
        
        self.save_webhooks()
        input(Fore.GREEN + f"Webhook '{nome_webhook}' Atualizado com Sucesso! Pressione Enter Para Continuar." + Style.RESET_ALL)

    def exportar_webhooks(self):
        nome_arquivo = input(Fore.YELLOW + "Digite o Nome do Arquivo Para Exportar (sem extensão): " + Style.RESET_ALL)
        caminho_arquivo = f"{nome_arquivo}.json"
        
        with open(caminho_arquivo, 'w') as f:
            json.dump(self.webhooks, f, indent=4)
        
        input(Fore.GREEN + f"Webhooks Exportados Para {caminho_arquivo}! Pressione Enter Para Continuar." + Style.RESET_ALL)

    def importar_webhooks(self):
        nome_arquivo = input(Fore.YELLOW + "Digite o Nome do Arquivo Para Importar (sem extensão): " + Style.RESET_ALL)
        caminho_arquivo = f"{nome_arquivo}.json"
        
        try:
            with open(caminho_arquivo, 'r') as f:
                novos_webhooks = json.load(f)
                
            self.webhooks.update(novos_webhooks)
            self.save_webhooks()
            
            input(Fore.GREEN + f"Webhooks Importados de {caminho_arquivo}! Pressione Enter Para Continuar." + Style.RESET_ALL)
        except FileNotFoundError:
            input(Fore.RED + f"Arquivo {caminho_arquivo} não Encontrado. Pressione Enter Para Continuar." + Style.RESET_ALL)
        except json.JSONDecodeError:
            input(Fore.RED + "Arquivo Inválido ou Corrompido. Pressione Enter Para Continuar." + Style.RESET_ALL)

    def criar_webhook(self):
        self.clear_screen()
        print(Fore.CYAN + "===== CRIAR NOVO WEBHOOK =====" + Style.RESET_ALL)
        
        nome = input(Fore.YELLOW + "Digite um Nome Para o Webhook: " + Style.RESET_ALL)
        url = input(Fore.YELLOW + "Cole a URL do Webhook do Discord: " + Style.RESET_ALL)
        
        if not url.startswith('https://discord.com/api/webhooks/'):
            input(Fore.RED + "URL de Webhook Inválida! Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        if nome in self.webhooks:
            confirmar = input(Fore.RED + "Um Webhook com Este Nome já Existe. Deseja Substituir? (s/n): " + Style.RESET_ALL)
            if confirmar.lower() != 's':
                return
        
        self.webhooks[nome] = url
        self.save_webhooks()
        input(Fore.GREEN + f"Webhook '{nome}' Criado com Sucesso! Pressione Enter Para Continuar." + Style.RESET_ALL)

    def enviar_mensagem_simples(self):
        self.clear_screen()
        print(Fore.CYAN + "===== ENVIAR MENSAGEM SIMPLES =====" + Style.RESET_ALL)
        
        if not self.webhooks:
            input(Fore.RED + "Nenhum Webhook Salvo. Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        print(Fore.YELLOW + "Webhooks Salvos:" + Style.RESET_ALL)
        for i, nome in enumerate(self.webhooks.keys(), 1):
            print(f"{Fore.GREEN}{i}. {Fore.WHITE}{nome}")
        
        try:
            escolha = int(input(Fore.YELLOW + "\nEscolha o Webhook (número): " + Style.RESET_ALL))
            nome_webhook = list(self.webhooks.keys())[escolha - 1]
            url_webhook = self.webhooks[nome_webhook]
        except (ValueError, IndexError):
            input(Fore.RED + "Escolha Inválida. Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        username = input(Fore.YELLOW + "Nome de Usuário (opcional): " + Style.RESET_ALL) or None
        avatar_url = input(Fore.YELLOW + "URL do Avatar (opcional): " + Style.RESET_ALL) or None
        conteudo = input(Fore.YELLOW + "Mensagem a ser Enviada: " + Style.RESET_ALL)
        
        # Payload
        payload = {
            "content": conteudo
        }
        
        if username:
            payload["username"] = username
        if avatar_url:
            payload["avatar_url"] = avatar_url
        
        try:
            response = requests.post(url_webhook, json=payload)
            if response.status_code == 204:
                input(Fore.GREEN + "Mensagem Enviada com Sucesso! Pressione Enter Para Continuar." + Style.RESET_ALL)
            else:
                input(Fore.RED + f"Erro ao Enviar Mensagem. Código de Status: {response.status_code}. Pressione Enter Para Continuar." + Style.RESET_ALL)
        except Exception as e:
            input(Fore.RED + f"Erro: {e}. Pressione Enter Para Continuar." + Style.RESET_ALL)

    def enviar_mensagem_embed(self):
        self.clear_screen()
        print(Fore.CYAN + "===== ENVIAR MENSAGEM EMBED =====" + Style.RESET_ALL)
        
        if not self.webhooks:
            input(Fore.RED + "Nenhum Webhook Salvo. Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        print(Fore.YELLOW + "Webhooks Salvos:" + Style.RESET_ALL)
        for i, nome in enumerate(self.webhooks.keys(), 1):
            print(f"{Fore.GREEN}{i}. {Fore.WHITE}{nome}")
        
        try:
            escolha = int(input(Fore.YELLOW + "\nEscolha o Webhook (número): " + Style.RESET_ALL))
            nome_webhook = list(self.webhooks.keys())[escolha - 1]
            url_webhook = self.webhooks[nome_webhook]
        except (ValueError, IndexError):
            input(Fore.RED + "Opção Inválida. Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        username = input(Fore.YELLOW + "Nome de Usuário (opcional): " + Style.RESET_ALL) or None
        avatar_url = input(Fore.YELLOW + "URL do Avatar (opcional): " + Style.RESET_ALL) or None
        
        embed = {}
        embed['title'] = input(Fore.YELLOW + "Título do Embed (opcional): " + Style.RESET_ALL) or None
        embed['description'] = input(Fore.YELLOW + "Descrição do Embed (opcional): " + Style.RESET_ALL) or None
        
        cor = input(Fore.YELLOW + "Cor do Embed (ex: #FF0000): " + Style.RESET_ALL) or None
        if cor:
            try:
                embed['color'] = int(cor.replace('#', ''), 16)
            except ValueError:
                input(Fore.RED + "Cor Inválida! Usando cor Padrão..." + Style.RESET_ALL)
        
        thumbnail_url = input(Fore.YELLOW + "URL da Thumbnail (opcional): " + Style.RESET_ALL) or None
        if thumbnail_url and self.validar_url(thumbnail_url):
            embed['thumbnail'] = {"url": thumbnail_url}
        
        imagem_url = input(Fore.YELLOW + "URL da Imagem (opcional): " + Style.RESET_ALL) or None
        if imagem_url and self.validar_url(imagem_url):
            embed['image'] = {"url": imagem_url}
        
        footer_texto = input(Fore.YELLOW + "Texto do Footer (opcional): " + Style.RESET_ALL) or None
        footer_icone = input(Fore.YELLOW + "URL do Ícone do Footer (opcional): " + Style.RESET_ALL) or None
        if footer_texto:
            embed['footer'] = {"text": footer_texto}
            if footer_icone and self.validar_url(footer_icone):
                embed['footer']['icon_url'] = footer_icone
        
        campos = []
        while True:
            adicionar_campo = input(Fore.YELLOW + "Deseja Adicionar Field ao Embed? (s/n): " + Style.RESET_ALL).lower()
            if adicionar_campo != 's':
                break
            
            nome_campo = input(Fore.YELLOW + "Nome da Field: " + Style.RESET_ALL)
            valor_campo = input(Fore.YELLOW + "Descrição da Field: " + Style.RESET_ALL)
            inline = input(Fore.YELLOW + "A Field é Inline? (s/n): " + Style.RESET_ALL).lower() == 's'
            
            campos.append({
                "name": nome_campo,
                "value": valor_campo,
                "inline": inline
            })
        
        # Payload
        payload = {}
        
        if username:
            payload["username"] = username
        if avatar_url:
            payload["avatar_url"] = avatar_url
        
        # payload + embed
        payload['embeds'] = [embed]
        
        if campos:
            payload['embeds'][0]['fields'] = campos
        
        try:
            response = requests.post(url_webhook, json=payload)
            if response.status_code == 204:
                input(Fore.GREEN + "Embed Enviada com Sucesso! Pressione Enter Para Continuar." + Style.RESET_ALL)
            else:
                input(Fore.RED + f"Erro ao Enviar Embed. Código de Status: {response.status_code}. Pressione Enter Para Continuar." + Style.RESET_ALL)
        except Exception as e:
            input(Fore.RED + f"Erro: {e}. Pressione Enter Para Continuar." + Style.RESET_ALL)

    def listar_webhooks(self):
        self.clear_screen()
        print(Fore.CYAN + "===== WEBHOOKS SALVOS =====" + Style.RESET_ALL)
        
        if not self.webhooks:
            print(Fore.YELLOW + "Nenhum Webhook Encontrado." + Style.RESET_ALL)
        else:
            for nome, url in self.webhooks.items():
                print(f"{Fore.GREEN}{nome}: {Fore.WHITE}{self.ocultar_url(url)}")
        
        input(Fore.YELLOW + "\nPressione Enter Para Continuar..." + Style.RESET_ALL)

    def ocultar_url(self, url):
        partes = url.split('/')
        return f"{'*' * 20}/{partes[-2]}/{partes[-1][:10]}..."

    def excluir_webhook(self):
        self.clear_screen()
        print(Fore.CYAN + "===== EXCLUIR WEBHOOK =====" + Style.RESET_ALL)
        
        if not self.webhooks:
            input(Fore.RED + "Nenhum Webhook Salvo. Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        print(Fore.YELLOW + "Webhooks Disponíveis:" + Style.RESET_ALL)
        for i, nome in enumerate(self.webhooks.keys(), 1):
            print(f"{Fore.GREEN}{i}. {Fore.WHITE}{nome}")
        
        try:
            escolha = int(input(Fore.YELLOW + "\nEscolha o Webhook Para Excluir (número): " + Style.RESET_ALL))
            nome_webhook = list(self.webhooks.keys())[escolha - 1]
        except (ValueError, IndexError):
            input(Fore.RED + "Opção Inválida. Pressione Enter Para Continuar." + Style.RESET_ALL)
            return
        
        confirmar = input(Fore.RED + f"Tem Certeza que Deseja Excluir o Webhook '{nome_webhook}'? (s/n): " + Style.RESET_ALL)
        if confirmar.lower() == 's':
            del self.webhooks[nome_webhook]
            self.save_webhooks()
            input(Fore.GREEN + f"Webhook '{nome_webhook}' Excluído com Sucesso! Pressione Enter Para Continuar." + Style.RESET_ALL)

def main():
    try:
        webhook_creator = DiscordWebhookCreator()
        webhook_creator.menu_principal()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nOperação Cancelada Pelo Usuário." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Erro Inesperado: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()