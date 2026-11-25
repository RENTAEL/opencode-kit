---
name: devops-ansible-playbook-creator
description: "AssistÃƒÆ’Ã‚Âªncia completa para criaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o e manutenÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de playbooks Ansible."
---
# Overview
AssistÃƒÆ’Ã‚Âªncia completa para criaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o e manutenÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de playbooks Ansible.

## Capacidades
1. **Gerar playbooks** a partir de descriÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes em linguagem natural
2. **Ajudar a escrever/expandir** trechos especÃƒÆ’Ã‚Â­ficos
3. **Fornecer snippets/templates** prontos para tarefas comuns
4. **Explicar playbooks** existentes

## Como Usar

### Para Criar Playbooks
Quando o usuÃƒÆ’Ã‚Â¡rio pedir para criar um playbook:
1. Analise os requisitos detalhadamente
2. Consulte a referÃƒÆ’Ã‚Âªncia em `reference/` para mÃƒÆ’Ã‚Â³dulos e sintaxe
3. ForneÃƒÆ’Ã‚Â§a YAML vÃƒÆ’Ã‚Â¡lido com explicaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes
4. Sugira melhorias e boas prÃƒÆ’Ã‚Â¡ticas

**Exemplo de prompt:**
```
Crie um playbook para instalar nginx, configurar virtual hosts e iniciar o serviÃƒÆ’Ã‚Â§o
```

**Resposta esperada:**
```yaml
- name: ConfiguraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o completa do Nginx
  hosts: webservers
  become: yes
  tasks:
    - name: Instalar Nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    
    - name: Criar diretÃƒÆ’Ã‚Â³rio de virtual hosts
      file:
        path: /etc/nginx/sites-available
        state: directory
        mode: '0755'
    
    # ... mais tarefas
```

### Para Ajudar a Escrever Trechos
Quando o usuÃƒÆ’Ã‚Â¡rio precisar de ajuda com partes especÃƒÆ’Ã‚Â­ficas:
1. ForneÃƒÆ’Ã‚Â§a o trecho solicitado com placeholders
2. Explique cada parte
3. OfereÃƒÆ’Ã‚Â§a alternativas quando aplicÃƒÆ’Ã‚Â¡vel

**Exemplo:**
```
Como faÃƒÆ’Ã‚Â§o para copiar vÃƒÆ’Ã‚Â¡rios arquivos usando loop?
```

**Resposta:**
```yaml
- name: Copiar mÃƒÆ’Ã‚Âºltiplos arquivos
  copy:
    src: "{{ item.src }}"
    dest: "{{ item.dest }}"
    owner: root
    group: root
    mode: '0644'
  loop:
    - { src: 'files/config.conf', dest: '/etc/app/config.conf' }
    - { src: 'files/service.service', dest: '/etc/systemd/system/app.service' }
```

### Para Explicar Playbooks
Quando o usuÃƒÆ’Ã‚Â¡rio precisar entender um playbook existente:
1. Analise a estrutura e fluxo
2. Explique cada seÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o e tarefa
3. Identifique padrÃƒÆ’Ã‚Âµes e possÃƒÆ’Ã‚Â­veis melhorias

## ReferÃƒÆ’Ã‚Âªncia

### Estrutura da Pasta
```
reference/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ README.md               # ÃƒÆ’Ã‚Ândice organizado
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ modules/                # DocumentaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de 73 mÃƒÆ’Ã‚Â³dulos
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ file.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ copy.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ...
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ docs/                   # DocumentaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o principal convertida
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ yaml_syntax.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ playbook_intro.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ...
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ topics/                 # Guias combinados por tÃƒÆ’Ã‚Â³pico
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ variables.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ conditionals_loops.md
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ...
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ ansible_builtin/        # Arquivos fonte Python (referÃƒÆ’Ã‚Âªncia tÃƒÆ’Ã‚Â©cnica)
```

### Como Consultar a ReferÃƒÆ’Ã‚Âªncia
1. **Para mÃƒÆ’Ã‚Â³dulos especÃƒÆ’Ã‚Â­ficos**: Use `reference/modules/<nome_modulo>.md`
2. **Para conceitos gerais**: Consulte `reference/topics/`
3. **Para detalhes completos**: Use `reference/docs/`

## Templates e Exemplos

### Templates DisponÃƒÆ’Ã‚Â­veis
- `templates/basic_playbook.yml.j2` - Playbook bÃƒÆ’Ã‚Â¡sico
- `templates/role_structure.yml.j2` - Estrutura de role

### Exemplos Prontos
- `examples/` - Playbooks de exemplo para diferentes cenÃƒÆ’Ã‚Â¡rios

## MÃƒÆ’Ã‚Â³dulos Mais Comuns

### GestÃƒÆ’Ã‚Â£o de Arquivos
- `file` - Gerenciamento de arquivos e diretÃƒÆ’Ã‚Â³rios
- `copy` - CÃƒÆ’Ã‚Â³pia de arquivos
- `template` - Templates Jinja2
- `assemble` - Montagem de arquivos

### GestÃƒÆ’Ã‚Â£o de ServiÃƒÆ’Ã‚Â§os
- `service` - ServiÃƒÆ’Ã‚Â§os SysVinit
- `systemd_service` - ServiÃƒÆ’Ã‚Â§os systemd

### GestÃƒÆ’Ã‚Â£o de Pacotes
- `apt` - Pacotes Debian/Ubuntu
- `yum` - Pacotes RHEL/CentOS
- `dnf` - Pacotes modernos RHEL
- `package` - Gerenciador genÃƒÆ’Ã‚Â©rico

### Comandos
- `command` - Comandos secos
- `shell` - Comandos com shell
- `script` - ExecuÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de scripts

### GestÃƒÆ’Ã‚Â£o de UsuÃƒÆ’Ã‚Â¡rios
- `user` - UsuÃƒÆ’Ã‚Â¡rios do sistema
- `group` - Grupos do sistema

## Sintaxe BÃƒÆ’Ã‚Â¡sica

### Estrutura de um Playbook
```yaml
---
- name: Nome do play
  hosts: grupo_de_hosts
  become: yes  # Usar sudo
  vars:
    variavel: valor
  tasks:
    - name: Nome da tarefa
      modulo:
        parametro: valor
      notify: handler_name  # Opcional
  handlers:
    - name: handler_name
      modulo:
        parametro: valor
```

### Patterns de InventÃƒÆ’Ã‚Â¡rio
```
webservers              # Grupo especÃƒÆ’Ã‚Â­fico
webservers[0]           # Primeiro host do grupo
webservers:!database    # Grupo webservers exceto database
webservers:&staging     # InterseÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de grupos
*.example.com           # Wildcard
192.168.1.*             # Range de IPs
```

### VariÃƒÆ’Ã‚Â¡veis Importantes
- `inventory_hostname` - Nome do host atual
- `group_names` - Grupos que o host pertence
- `ansible_facts` - Facts do sistema
- `hostvars` - VariÃƒÆ’Ã‚Â¡veis de outros hosts

## Casos de Uso Comuns

### 1. Provisionamento de Servidor
```yaml
- name: Provisionar servidor web
  hosts: webservers
  roles:
    - common
    - nginx
    - php
    - monitoring
```

### 2. Deploy de AplicaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o
```yaml
- name: Deploy da aplicaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o
  hosts: app_servers
  tasks:
    - name: Parar serviÃƒÆ’Ã‚Â§o
      service:
        name: myapp
        state: stopped
    
    - name: Atualizar cÃƒÆ’Ã‚Â³digo
      git:
        repo: https://github.com/meuapp/repo.git
        dest: /opt/myapp
        version: main
    
    - name: Instalar dependÃƒÆ’Ã‚Âªncias
      pip:
        requirements: /opt/myapp/requirements.txt
    
    - name: Iniciar serviÃƒÆ’Ã‚Â§o
      service:
        name: myapp
        state: started
```

### 3. ConfiguraÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de Banco de Dados
```yaml
- name: Configurar PostgreSQL
  hosts: databases
  become: yes
  vars:
    pg_version: 14
    pg_databases:
      - app_production
      - app_staging
  tasks:
    - name: Instalar PostgreSQL
      apt:
        name: postgresql-{{ pg_version }}
        state: present
    
    - name: Criar bancos de dados
      postgresql_db:
        name: "{{ item }}"
        state: present
      loop: "{{ pg_databases }}"
```

## Boas PrÃƒÆ’Ã‚Â¡ticas

1. **Use nomes descritivos** para tasks e plays
2. **Seja idempotente** - playbooks devem poder ser executados mÃƒÆ’Ã‚Âºltiplas vezes
3. **Use roles** para organizar cÃƒÆ’Ã‚Â³digo reutilizÃƒÆ’Ã‚Â¡vel
4. **Valide variÃƒÆ’Ã‚Â¡veis** com `assert` ou `fail`
5. **Use handlers** para serviÃƒÆ’Ã‚Â§os que precisam reiniciar
6. **Implemente tratamento de erros** com `block/rescue/always`
7. **Use tags** para execuÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o seletiva
8. **Documente** com comentÃƒÆ’Ã‚Â¡rios e nomes claros

## Comandos ÃƒÆ’Ã…Â¡teis

```bash
# Executar playbook
ansible-playbook playbook.yml

# Executar com inventÃƒÆ’Ã‚Â¡rio especÃƒÆ’Ã‚Â­fico
ansible-playbook -i inventory/hosts playbook.yml

# Executar apenas tasks com tag especÃƒÆ’Ã‚Â­fica
ansible-playbook --tags "config,deploy" playbook.yml

# Executar em modo dry-run (check)
ansible-playbook --check playbook.yml

# Listar hosts que seriam afetados
ansible-playbook --list-hosts playbook.yml

# Executar com limite de hosts
ansible-playbook --limit "webservers" playbook.yml
```

## SoluÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o de Problemas Comuns

### Erros de ConexÃƒÆ’Ã‚Â£o
- Verifique SSH e credenciais
- Teste com `ansible all -m ping`
- Verifique `ansible.cfg` e inventÃƒÆ’Ã‚Â¡rio

### Erros de Sintaxe YAML
- Use `ansible-playbook --syntax-check playbook.yml`
- Verifique indentaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Â£o (2 espaÃƒÆ’Ã‚Â§os)
- Evite tabs

### Tarefas NÃƒÆ’Ã‚Â£o Idempotentes
- Use mÃƒÆ’Ã‚Â³dulos apropriados
- Verifique `changed_when` e `creates`
- Use `check_mode` para teste

---
*Esta skill fornece assistÃƒÆ’Ã‚Âªncia completa para trabalhar com Ansible. Use a referÃƒÆ’Ã‚Âªncia em `reference/` para informaÃƒÆ’Ã‚Â§ÃƒÆ’Ã‚Âµes detalhadas.*