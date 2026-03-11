package com.saciar.controller;

import com.saciar.model.Cliente;
import com.saciar.service.ClienteService;
import javafx.application.Platform;
import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import javafx.stage.FileChooser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Optional;

/**
 * Controller para a view de Clientes
 */
public class ClienteController {
    private static final Logger logger = LoggerFactory.getLogger(ClienteController.class);
    
    @FXML private TextField searchField;
    @FXML private TableView<Cliente> clienteTable;
    @FXML private TableColumn<Cliente, String> nomeColumn;
    @FXML private TableColumn<Cliente, String> telefoneColumn;
    @FXML private TableColumn<Cliente, Integer> pontosColumn;
    @FXML private TableColumn<Cliente, Double> trocoColumn;
    @FXML private Button btnCadastrar;
    @FXML private Button btnAtualizar;
    @FXML private Button btnRemover;
    @FXML private Button btnExportar;
    
    private final ClienteService clienteService;
    private final ObservableList<Cliente> clienteList;
    
    public ClienteController() {
        this.clienteService = new ClienteService();
        this.clienteList = FXCollections.observableArrayList();
    }
    
    @FXML
    public void initialize() {
        // Configura colunas da tabela
        nomeColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getNome() != null ? 
                cellData.getValue().getNome() : "Não identificado"));
        telefoneColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getTelefone() != null ? 
                cellData.getValue().getTelefone() : "Sem telefone"));
        pontosColumn.setCellValueFactory(cellData -> 
            new SimpleIntegerProperty(cellData.getValue().getPontos() != null ? 
                cellData.getValue().getPontos() : 0).asObject());
        trocoColumn.setCellValueFactory(cellData -> 
            new SimpleDoubleProperty(cellData.getValue().getTroco() != null ? 
                cellData.getValue().getTroco() : 0.0).asObject());
        
        clienteTable.setItems(clienteList);
        
        // Carrega dados iniciais
        loadClientes();
        
        // Configura busca
        searchField.setOnAction(e -> handleSearch());
    }
    
    /**
     * Carrega todos os clientes
     */
    private void loadClientes() {
        new Thread(() -> {
            try {
                List<Cliente> clientes = clienteService.getClientes();
                Platform.runLater(() -> {
                    clienteList.clear();
                    clienteList.addAll(clientes);
                });
            } catch (Exception e) {
                logger.error("Erro ao carregar clientes", e);
                showError("Erro ao carregar clientes: " + e.getMessage());
            }
        }).start();
    }
    
    /**
     * Busca clientes
     */
    @FXML
    private void handleSearch() {
        String query = searchField.getText().trim();
        
        new Thread(() -> {
            try {
                List<Cliente> clientes = clienteService.searchClientes(query);
                Platform.runLater(() -> {
                    clienteList.clear();
                    clienteList.addAll(clientes);
                });
            } catch (Exception e) {
                logger.error("Erro ao buscar clientes", e);
                showError("Erro ao buscar clientes: " + e.getMessage());
            }
        }).start();
    }
    
    /**
     * Limpa filtro
     */
    @FXML
    private void handleClearFilter() {
        searchField.clear();
        loadClientes();
    }
    
    /**
     * Cadastrar novo cliente
     */
    @FXML
    private void handleCadastrar() {
        ClienteDialog dialog = new ClienteDialog();
        Optional<Cliente> result = dialog.showAndWait();
        
        result.ifPresent(cliente -> {
            new Thread(() -> {
                try {
                    var response = clienteService.createCliente(cliente);
                    Platform.runLater(() -> {
                        if (response.isSuccess() && response.getData() != null) {
                            if (response.getStatusCode() != null && response.getStatusCode() == 201) {
                                showInfo("Cliente cadastrado com sucesso!");
                            } else {
                                showInfo("Operação realizada com sucesso!");
                            }
                            loadClientes();
                        } else {
                            if (response.getStatusCode() != null && response.getStatusCode() == 403) {
                                showError("Cliente já existe no sistema!");
                            } else if (response.getStatusCode() != null && response.getStatusCode() == 400) {
                                showError("Dados inválidos. Verifique os campos!");
                            } else if (response.getStatusCode() != null && response.getStatusCode() == 500) {
                                showError("Erro no servidor. Tente novamente mais tarde!");
                            } else {
                                showError("Erro ao cadastrar cliente: " + response.getError());
                            }
                        }
                    });
                } catch (Exception e) {
                    logger.error("Erro ao cadastrar cliente", e);
                    Platform.runLater(() -> showError("Erro ao cadastrar cliente: " + e.getMessage()));
                }
            }).start();
        });
    }
    
    /**
     * Atualizar cliente selecionado
     */
    @FXML
    private void handleAtualizar() {
        Cliente selected = clienteTable.getSelectionModel().getSelectedItem();
        
        if (selected == null) {
            showWarning("Selecione um cliente para atualizar!");
            return;
        }
        
        ClienteDialog dialog = new ClienteDialog(selected);
        Optional<Cliente> result = dialog.showAndWait();
        
        result.ifPresent(cliente -> {
            new Thread(() -> {
                try {
                    Cliente updated = clienteService.updateCliente(cliente);
                    Platform.runLater(() -> {
                        if (updated != null) {
                            showInfo("Cliente atualizado com sucesso!");
                            loadClientes();
                        } else {
                            showError("Erro ao atualizar cliente!");
                        }
                    });
                } catch (Exception e) {
                    logger.error("Erro ao atualizar cliente", e);
                    Platform.runLater(() -> showError("Erro ao atualizar cliente: " + e.getMessage()));
                }
            }).start();
        });
    }
    
    /**
     * Remover cliente selecionado
     */
    @FXML
    private void handleRemover() {
        Cliente selected = clienteTable.getSelectionModel().getSelectedItem();
        
        if (selected == null) {
            showWarning("Selecione um cliente para remover!");
            return;
        }
        System.out.println("Removendo cliente: " + clienteTable.getSelectionModel().getSelectedItem().toString());
        Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
        alert.setTitle("Confirmar Remoção");
        alert.setHeaderText("Remover cliente?");
        alert.setContentText("Deseja remover " + selected.getNome() + "?");
        
        Optional<ButtonType> result = alert.showAndWait();
        
        if (result.isPresent() && result.get() == ButtonType.OK) {
            new Thread(() -> {
                try {
                    boolean deleted = clienteService.deleteCliente(selected.getId());
                    Platform.runLater(() -> {
                        if (deleted) {
                            showInfo("Cliente removido com sucesso!");
                            loadClientes();
                        } else {
                            showError("Erro ao remover cliente!");
                        }
                    });
                } catch (Exception e) {
                    logger.error("Erro ao remover cliente", e);
                    Platform.runLater(() -> showError("Erro ao remover cliente: " + e.getMessage()));
                }
            }).start();
        }
    }
    
    /**
     * Exportar para CSV
     */
    @FXML
    private void handleExportar() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Salvar Lista de Clientes");
        fileChooser.setInitialFileName("clientes.csv");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("CSV Files", "*.csv"));
        
        File file = fileChooser.showSaveDialog(clienteTable.getScene().getWindow());
        
        if (file != null) {
            if (!file.getName().toLowerCase().endsWith(".csv")) {
                file = new File(file.getParentFile(), file.getName() + ".csv");
            }
            try (FileWriter writer = new FileWriter(file)) {
                writer.write("Nome;Telefone;Pontos;Troco\n");
                
                for (Cliente cliente : clienteList) {
                    writer.write(String.format("%s;%s;%d;%.2f\n",
                        cliente.getNome(),
                        cliente.getTelefone(),
                        cliente.getPontos(),
                        cliente.getTroco()));
                }
                
                showInfo("Dados exportados com sucesso!");
            } catch (IOException e) {
                logger.error("Erro ao exportar", e);
                showError("Erro ao exportar: " + e.getMessage());
            }
        }
    }
    
    // Métodos utilitários para dialogs
    
    private void showError(String message) {
        Platform.runLater(() -> {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setTitle("Erro");
            alert.setHeaderText(null);
            alert.setContentText(message);
            alert.showAndWait();
        });
    }
    
    private void showWarning(String message) {
        Alert alert = new Alert(Alert.AlertType.WARNING);
        alert.setTitle("Atenção");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
    
    private void showInfo(String message) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Sucesso");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
}

/**
 * Dialog para cadastro/edição de cliente
 */
class ClienteDialog extends Dialog<Cliente> {
    private final TextField nomeField = new TextField();
    private final TextField telefoneField = new TextField();
    private final TextField pontosField = new TextField();
    private final TextField trocoField = new TextField();
    
    public ClienteDialog() {
        this(null);
    }
    
    public ClienteDialog(Cliente cliente) {
        setTitle(cliente == null ? "Cadastrar Cliente" : "Atualizar Cliente");
        setHeaderText(null);
        
        // Layout
        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.setPadding(new Insets(20));
        
        nomeField.setPromptText("Nome completo");
        telefoneField.setPromptText("(XX) XXXXX-XXXX");
        pontosField.setPromptText("0");
        trocoField.setPromptText("0.00");
        
        grid.add(new Label("Nome:"), 0, 0);
        grid.add(nomeField, 1, 0);
        grid.add(new Label("Telefone:"), 0, 1);
        grid.add(telefoneField, 1, 1);
        grid.add(new Label("Pontos:"), 0, 2);
        grid.add(pontosField, 1, 2);
        grid.add(new Label("Troco:"), 0, 3);
        grid.add(trocoField, 1, 3);
        
        // Preenche dados se for edição
        if (cliente != null) {
            nomeField.setText(cliente.getNome());
            telefoneField.setText(cliente.getTelefone());
            pontosField.setText(String.valueOf(cliente.getPontos()));
            trocoField.setText(String.valueOf(cliente.getTroco()));
        }
        
        getDialogPane().setContent(grid);
        
        // Botões
        ButtonType saveButton = new ButtonType("Salvar", ButtonBar.ButtonData.OK_DONE);
        getDialogPane().getButtonTypes().addAll(saveButton, ButtonType.CANCEL);
        
        // Converte resultado
        setResultConverter(dialogButton -> {
            if (dialogButton == saveButton) {
                try {
                    Cliente c = cliente != null ? cliente : new Cliente();
                    c.setNome(nomeField.getText());
                    c.setTelefone(telefoneField.getText());
                    c.setPontos(Integer.parseInt(pontosField.getText()));
                    c.setTroco(Double.parseDouble(trocoField.getText()));
                    return c;
                } catch (NumberFormatException e) {
                    return null;
                }
            }
            return null;
        });
        
        // Regras de telefone: só números, máximo 11 dígitos
        telefoneField.textProperty().addListener((obs, old, val) -> {
            String onlyDigits = val.replaceAll("\\D", "");
            if (onlyDigits.length() > 11) {
                telefoneField.setText("");
            } else {
                telefoneField.setText(onlyDigits);
            }
        });
        // Regras de pontos: só números, máximo 10
        pontosField.textProperty().addListener((obs, old, val) -> {
            String onlyDigits = val.replaceAll("\\D", "");
            if (onlyDigits.length() > 2 || (onlyDigits.length() == 2 && Integer.parseInt(onlyDigits) > 10)) {
                pontosField.setText("");
            } else {
                pontosField.setText(onlyDigits);
            }
        });
    }
}
