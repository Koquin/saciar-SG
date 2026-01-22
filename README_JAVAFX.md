# SACIAR - Sistema de Gerenciamento (JavaFX)

Sistema moderno de gerenciamento com interface JavaFX, refatorado do Python/CustomTkinter original.

## 🚀 Tecnologias

- **Java 17** - Linguagem principal
- **JavaFX 21** - Framework de interface gráfica
- **Maven** - Gerenciamento de dependências
- **OkHttp** - Cliente HTTP assíncrono
- **Jackson** - Serialização/deserialização JSON
- **Lombok** - Redução de boilerplate
- **SLF4J + Logback** - Sistema de logging
- **ControlsFX** - Componentes adicionais

## 📁 Estrutura do Projeto

```
src/
├── main/
│   ├── java/
│   │   └── com/saciar/
│   │       ├── controller/          # Controllers JavaFX
│   │       │   ├── ClienteController.java
│   │       │   └── MainController.java
│   │       ├── model/               # Modelos de dados
│   │       │   ├── Cliente.java
│   │       │   ├── Compra.java
│   │       │   ├── Premio.java
│   │       │   └── Resgate.java
│   │       ├── service/             # Camada de serviços
│   │       │   ├── HttpClient.java
│   │       │   ├── ClienteService.java
│   │       │   └── CompraService.java
│   │       └── SaciarApplication.java  # Classe principal
│   └── resources/
│       ├── css/
│       │   └── styles.css           # Estilos da aplicação
│       ├── fxml/
│       │   ├── MainView.fxml        # Layout principal
│       │   └── ClienteView.fxml     # View de clientes
│       └── logback.xml              # Configuração de logs
└── pom.xml                          # Configuração Maven
```

## ⚙️ Pré-requisitos

- **JDK 17** ou superior
- **Maven 3.8+**
- **API Backend** rodando em `http://localhost:8000`

## 🔧 Instalação e Execução

### 1. Clone o repositório

```bash
cd "Saciar - Sistema de Gerenciamento"
```

### 2. Compile o projeto

```bash
mvn clean compile
```

### 3. Execute a aplicação

```bash
mvn javafx:run
```

### 4. Ou crie um JAR executável

```bash
mvn clean package
java -jar target/saciar-sistema-2.0.0.jar
```

## 🎨 Funcionalidades

### ✅ Implementado

- **Gerenciamento de Clientes**
  - ✅ Listar todos os clientes
  - ✅ Buscar por nome ou telefone
  - ✅ Cadastrar novos clientes
  - ✅ Atualizar informações
  - ✅ Remover clientes
  - ✅ Exportar para CSV

- **Interface Moderna**
  - ✅ Design responsivo
  - ✅ Sidebar com navegação
  - ✅ Botões com ícones
  - ✅ Cores e estilos profissionais
  - ✅ Feedback visual (hover, seleção)

- **Infraestrutura**
  - ✅ Cliente HTTP otimizado
  - ✅ Sistema de logging
  - ✅ Tratamento de erros
  - ✅ Operações assíncronas

### 🔄 Próximas Implementações

- **Gerenciamento de Compras**
  - Registrar novas compras
  - Visualizar histórico
  - Filtros avançados
  - Estatísticas

- **Gerenciamento de Resgates**
  - Criar resgates de prêmios
  - Histórico de resgates
  - Validação de pontos

- **Melhorias**
  - Cache de dados
  - Modo offline
  - Relatórios em PDF
  - Dashboard com gráficos

## 🎯 Melhorias em relação à versão Python

1. **Performance**
   - Operações assíncronas nativas
   - Connection pooling otimizado
   - Renderização mais rápida

2. **Arquitetura**
   - Separação clara de responsabilidades
   - Services reutilizáveis
   - Código type-safe

3. **Manutenibilidade**
   - Logging estruturado
   - Tratamento robusto de erros
   - Código autodocumentado com Lombok

4. **UX/UI**
   - Animações suaves
   - Feedback visual aprimorado
   - Design mais profissional
   - Responsividade melhorada

## 📝 Configuração

### Alterar URL da API

Edite `src/main/java/com/saciar/service/HttpClient.java`:

```java
private static final String BASE_URL = "http://seu-servidor:porta";
```

### Personalizar Cores

Edite `src/main/resources/css/styles.css`:

```css
.root {
    -fx-primary-color: #SuaCor;
    /* ... */
}
```

## 🐛 Troubleshooting

### Erro: Module not found

Certifique-se de ter o JDK 17 e o JavaFX configurados:

```bash
java --version
mvn --version
```

### Erro de conexão com API

Verifique se o backend está rodando:

```bash
curl http://localhost:8000/clientes
```

### Logs

Os logs são salvos em `logs/saciar.log` para debug.

## 👥 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Add nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto é de uso interno.

## 🙏 Créditos

- Versão original em Python/CustomTkinter
- Refatoração completa para Java/JavaFX
- Icons: Unicode Emojis

---

**Desenvolvido com ☕ e JavaFX**
