package com.saciar.controller;

import com.saciar.model.Premio;
import com.saciar.model.Resgate;
import com.saciar.service.ResgateService;
import javafx.application.Platform;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.scene.control.*;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Optional;

/**
 * Controller para a view de Resgates
 */
public class ResgateController {
    private static final Logger logger = LoggerFactory.getLogger(ResgateController.class);
    
    @FXML private TextField searchField;
    @FXML private TableView<Resgate> resgateTable;
    @FXML private TableColumn<Resgate, String> clienteColumn;
    @FXML private TableColumn<Resgate, String> telefoneColumn;
    @FXML private TableColumn<Resgate, String> premioColumn;
    @FXML private TableColumn<Resgate, Integer> pontosColumn;
    @FXML private TableColumn<Resgate, String> dataColumn;
    @FXML private Button btnRegistrar;
    @FXML private Button btnRemover;
    @FXML private Button btnExportar;
    @FXML private Button btnGerenciarPremios;
    
    private final ResgateService resgateService;
    private final ObservableList<Resgate> resgateList;
    private List<Premio> premiosDisponiveis;
    
    public ResgateController() {
        this.resgateService = new ResgateService();
        this.resgateList = FXCollections.observableArrayList();
    }
    
    @FXML
    public void initialize() {
        // Configura colunas da tabela
        clienteColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getClienteNome() != null ? 
                cellData.getValue().getClienteNome() : "Não identificado"));
        telefoneColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getTelefone() != null ? 
                cellData.getValue().getTelefone() : "Sem telefone"));
        premioColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getPremio() != null ? 
                cellData.getValue().getPremio() : "Sem prêmio"));
        pontosColumn.setCellValueFactory(cellData -> 
            new SimpleIntegerProperty(cellData.getValue().getPontos() != null ? 
                cellData.getValue().getPontos() : 0).asObject());
        dataColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getCreatedAt() != null ? 
                cellData.getValue().getCreatedAt() : "Sem data"));
        
        resgateTable.setItems(resgateList);
        
        // Carrega dados iniciais
        loadResgates();
        loadPremios();
        
        // Configura busca
        searchField.setOnAction(e -> handleSearch());
    }
    
    /**
     * Carrega todos os resgates
     */
    private void loadResgates() {
        new Thread(() -> {
            try {
                List<Resgate> resgates = resgateService.getResgates();
                Platform.runLater(() -> {
                    resgateList.clear();
                    resgateList.addAll(resgates);
                });
            } catch (Exception e) {
                logger.error("Erro ao carregar resgates", e);
                showError("Erro ao carregar resgates: " + e.getMessage());
            }
        }).start();
    }
    
    /**
     * Realiza busca de resgates
     */
    @FXML
    private void handleSearch() {
        String query = searchField.getText();
        if (query == null || query.trim().isEmpty()) {
            loadResgates();
            return;
        }
        
        new Thread(() -> {
            try {
                List<Resgate> resgates = resgateService.searchResgates(query.trim());
                Platform.runLater(() -> {
                    resgateList.clear();
                    resgateList.addAll(resgates);
                });
                logger.info("Encontrados {} resgates para busca: {}", resgates.size(), query);
            } catch (Exception e) {
                logger.error("Erro ao buscar resgates", e);
                Platform.runLater(() -> showError("Erro na busca: " + e.getMessage()));
            }
        }).start();
    }
    
    /**
     * Limpa filtro e recarrega todos os resgates
     */
    @FXML
    private void handleClearFilter() {
        searchField.clear();
        loadResgates();
    }
    
    /**
     * Exporta resgates para CSV
     */
    @FXML
    private void handleExportar() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Exportar Resgates");
        fileChooser.setInitialFileName("resgates.csv");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("CSV Files", "*.csv")
        );
        
        File file = fileChooser.showSaveDialog(btnExportar.getScene().getWindow());
        if (file != null) {
            new Thread(() -> {
                try (FileWriter writer = new FileWriter(file)) {
                    // Cabeçalho
                    writer.write("Cliente;Telefone;Prêmio;Pontos;Data\n");
                    
                    // Dados
                    for (Resgate resgate : resgateList) {
                        writer.write(String.format("%s;%s;%s;%d;%s\n",
                            resgate.getClienteNome() != null ? resgate.getClienteNome() : "N/A",
                            resgate.getTelefone(),
                            resgate.getPremio() != null ? resgate.getPremio() : "N/A",
                            resgate.getPontos(),
                            resgate.getCreatedAt() != null ? resgate.getCreatedAt() : "N/A"
                        ));
                    }
                    
                    Platform.runLater(() -> showInfo("Dados exportados com sucesso!"));
                    logger.info("Resgates exportados para: {}", file.getAbsolutePath());
                } catch (IOException e) {
                    logger.error("Erro ao exportar resgates", e);
                    Platform.runLater(() -> showError("Erro ao exportar: " + e.getMessage()));
                }
            }).start();
        }
    }
    
    /**
     * Carrega prêmios disponíveis
     */
    private void loadPremios() {
        new Thread(() -> {
            try {
                premiosDisponiveis = resgateService.getPremios();
                logger.info("{} prêmios carregados", premiosDisponiveis.size());
            } catch (Exception e) {
                logger.error("Erro ao carregar prêmios", e);
            }
        }).start();
    }
    
    /**
     * Registrar novo resgate
     */
    @FXML
    private void handleRegistrar() {
        if (premiosDisponiveis == null || premiosDisponiveis.isEmpty()) {
            showWarning("Carregando prêmios disponíveis...");
            loadPremios();
            return;
        }
        
        ResgateDialog dialog = new ResgateDialog(premiosDisponiveis);
        Optional<Resgate> result = dialog.showAndWait();
        
        result.ifPresent(resgate -> {
            new Thread(() -> {
                try {
                    var response = resgateService.createResgate(resgate);
                    Platform.runLater(() -> {
                        if (response.isSuccess()) {
                            showInfo("Resgate registrado com sucesso!");
                            loadResgates();
                        } else {
                            // Prioriza a mensagem da API se disponível
                            String errorMessage = response.getError();
                            if (errorMessage == null || errorMessage.isEmpty()) {
                                // Fallback para mensagens baseadas em status code
                                if (response.getStatusCode() != null && response.getStatusCode() == 404) {
                                    errorMessage = "Cliente não encontrado!";
                                } else if (response.getStatusCode() != null && response.getStatusCode() == 400) {
                                    errorMessage = "Pontos insuficientes ou dados inválidos!";
                                } else {
                                    errorMessage = "Erro ao registrar resgate!";
                                }
                            }
                            showError(errorMessage);
                        }
                    });
                } catch (Exception e) {
                    logger.error("Erro ao registrar resgate", e);
                    Platform.runLater(() -> showError("Erro ao registrar resgate: " + e.getMessage()));
                }
            }).start();
        });
    }
    
    /**
     * Remover resgate selecionado
     */
    @FXML
    private void handleRemover() {
        Resgate selected = resgateTable.getSelectionModel().getSelectedItem();
        
        if (selected == null) {
            showWarning("Selecione um resgate para remover!");
            return;
        }
        
        Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
        alert.setTitle("Confirmar Remoção");
        alert.setHeaderText("Remover resgate?");
        alert.setContentText("Deseja remover este resgate?");
        
        Optional<ButtonType> result = alert.showAndWait();
        
        if (result.isPresent() && result.get() == ButtonType.OK) {
            new Thread(() -> {
                try {
                    var response = resgateService.deleteResgate(selected.getId());
                    Platform.runLater(() -> {
                        if (response.isSuccess()) {
                            showInfo("Resgate removido com sucesso!");
                            loadResgates();
                        } else {
                            showError("Erro ao remover resgate!");
                        }
                    });
                } catch (Exception e) {
                    logger.error("Erro ao remover resgate", e);
                    Platform.runLater(() -> showError("Erro ao remover resgate: " + e.getMessage()));
                }
            }).start();
        }
    }
    
    /**
     * Gerenciar prêmios
     */
    @FXML
    private void handleGerenciarPremios() {
        PremiosDialog dialog = new PremiosDialog(resgateService, premiosDisponiveis);
        dialog.showAndWait();
        // Recarrega prêmios após fechar o dialog
        loadPremios();
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
 * Dialog para registro de resgate
 */
class ResgateDialog extends Dialog<Resgate> {
    private final TextField telefoneField = new TextField();
    private final ComboBox<Premio> premioCombo = new ComboBox<>();
    
    public ResgateDialog(List<Premio> premios) {
        setTitle("Registrar Resgate");
        setHeaderText(null);
        
        // Layout
        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.setPadding(new Insets(20));
        
        telefoneField.setPromptText("Telefone do cliente");
        premioCombo.setItems(FXCollections.observableArrayList(premios));
        premioCombo.setPromptText("Selecione o prêmio");
        premioCombo.setPrefWidth(250);
        
        grid.add(new Label("Telefone:"), 0, 0);
        grid.add(telefoneField, 1, 0);
        grid.add(new Label("Prêmio:"), 0, 1);
        grid.add(premioCombo, 1, 1);
        
        getDialogPane().setContent(grid);
        
        // Botões
        ButtonType saveButton = new ButtonType("Registrar", ButtonBar.ButtonData.OK_DONE);
        getDialogPane().getButtonTypes().addAll(saveButton, ButtonType.CANCEL);
        
        // Converte resultado
        setResultConverter(dialogButton -> {
            if (dialogButton == saveButton) {
                Premio premioSelecionado = premioCombo.getValue();
                if (premioSelecionado != null && !telefoneField.getText().isEmpty()) {
                    Resgate r = new Resgate();
                    r.setTelefone(telefoneField.getText());
                    r.setPontos(premioSelecionado.getPontos());
                    return r;
                }
            }
            return null;
        });
    }
}

/**
 * Dialog para gerenciar prêmios
 */
class PremiosDialog extends Dialog<Void> {
    private final ResgateService resgateService;
    private final TableView<Premio> premioTable = new TableView<>();
    private final ObservableList<Premio> premioList = FXCollections.observableArrayList();
    
    public PremiosDialog(ResgateService service, List<Premio> premios) {
        this.resgateService = service;
        
        setTitle("Gerenciar Prêmios");
        setHeaderText("Adicionar, editar ou remover prêmios");
        setResizable(true);
        
        // Layout
        VBox vbox = new VBox(15);
        vbox.setPadding(new Insets(20));
        
        // Tabela de prêmios
        TableColumn<Premio, String> premioCol = new TableColumn<>("PRÊMIO");
        premioCol.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getPremio()));
        
        TableColumn<Premio, Integer> pontosCol = new TableColumn<>("PONTOS");
        pontosCol.setCellValueFactory(cellData -> 
            new SimpleIntegerProperty(cellData.getValue().getPontos()).asObject());
        
        premioTable.getColumns().addAll(premioCol, pontosCol);
        premioTable.setItems(premioList);
        premioTable.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);
        VBox.setVgrow(premioTable, javafx.scene.layout.Priority.ALWAYS);
        
        if (premios != null) {
            premioList.addAll(premios);
        }
        
        // Botões
        HBox buttonBox = new HBox(10);
        Button btnAdicionar = new Button("➕ Adicionar Prêmio");
        btnAdicionar.setStyle("-fx-background-color: #27AE60; -fx-text-fill: white; -fx-font-weight: bold; -fx-min-width: 180px; -fx-min-height: 40px; -fx-font-size: 14px;");
        btnAdicionar.setOnAction(e -> handleAdicionarPremio());
        
        Button btnRemover = new Button("🗑️ Remover Prêmio");
        btnRemover.setStyle("-fx-background-color: #E74C3C; -fx-text-fill: white; -fx-font-weight: bold; -fx-min-width: 180px; -fx-min-height: 40px; -fx-font-size: 14px;");
        btnRemover.setOnAction(e -> handleRemoverPremio());
        
        buttonBox.getChildren().addAll(btnAdicionar, btnRemover);
        
        vbox.getChildren().addAll(premioTable, buttonBox);
        getDialogPane().setContent(vbox);
        
        // Botão fechar
        ButtonType closeButton = new ButtonType("Fechar", ButtonBar.ButtonData.OK_DONE);
        getDialogPane().getButtonTypes().add(closeButton);
        
        // Maximizar janela
        Platform.runLater(() -> {
            getDialogPane().getScene().getWindow().setWidth(
                javafx.stage.Screen.getPrimary().getVisualBounds().getWidth()
            );
            getDialogPane().getScene().getWindow().setHeight(
                javafx.stage.Screen.getPrimary().getVisualBounds().getHeight()
            );
        });
    }
    
    private void handleAdicionarPremio() {
        Dialog<Premio> dialog = new Dialog<>();
        dialog.setTitle("Adicionar Prêmio");
        dialog.setHeaderText(null);
        
        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.setPadding(new Insets(20));
        
        TextField premioField = new TextField();
        premioField.setPromptText("Nome do prêmio");
        premioField.setPrefWidth(300);
        
        TextField pontosField = new TextField();
        pontosField.setPromptText("Pontos necessários");
        
        grid.add(new Label("Prêmio:"), 0, 0);
        grid.add(premioField, 1, 0);
        grid.add(new Label("Pontos:"), 0, 1);
        grid.add(pontosField, 1, 1);
        
        dialog.getDialogPane().setContent(grid);
        
        ButtonType saveButton = new ButtonType("Adicionar", ButtonBar.ButtonData.OK_DONE);
        dialog.getDialogPane().getButtonTypes().addAll(saveButton, ButtonType.CANCEL);
        
        dialog.setResultConverter(dialogButton -> {
            if (dialogButton == saveButton) {
                try {
                    String premio = premioField.getText();
                    int pontos = Integer.parseInt(pontosField.getText());
                    if (!premio.isEmpty() && pontos > 0) {
                        Premio p = new Premio();
                        p.setPremio(premio);
                        p.setPontos(pontos);
                        return p;
                    }
                } catch (NumberFormatException e) {
                    showError("Pontos deve ser um número válido!");
                }
            }
            return null;
        });
        
        Optional<Premio> result = dialog.showAndWait();
        result.ifPresent(premio -> {
            new Thread(() -> {
                try {
                    // Adiciona novo prêmio à lista atual
                    List<Premio> premiosAtualizados = new java.util.ArrayList<>(premioList);
                    premiosAtualizados.add(premio);
                    
                    var response = resgateService.updatePremios(premiosAtualizados);
                    Platform.runLater(() -> {
                        if (response.isSuccess()) {
                            premioList.add(premio);
                            showInfo("Prêmio adicionado com sucesso!");
                        } else {
                            showError("Erro ao adicionar prêmio!");
                        }
                    });
                } catch (Exception e) {
                    Platform.runLater(() -> showError("Erro: " + e.getMessage()));
                }
            }).start();
        });
    }
    
    private void handleRemoverPremio() {
        Premio selected = premioTable.getSelectionModel().getSelectedItem();
        if (selected == null) {
            showWarning("Selecione um prêmio para remover!");
            return;
        }
        
        Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
        alert.setTitle("Confirmar Remoção");
        alert.setHeaderText("Remover prêmio?");
        alert.setContentText("Deseja remover: " + selected.getPremio() + "?");
        
        Optional<ButtonType> result = alert.showAndWait();
        if (result.isPresent() && result.get() == ButtonType.OK) {
            new Thread(() -> {
                try {
                    // Remove prêmio da lista e envia lista atualizada
                    List<Premio> premiosAtualizados = new java.util.ArrayList<>(premioList);
                    premiosAtualizados.remove(selected);
                    
                    var response = resgateService.updatePremios(premiosAtualizados);
                    Platform.runLater(() -> {
                        if (response.isSuccess()) {
                            premioList.remove(selected);
                            showInfo("Prêmio removido com sucesso!");
                        } else {
                            showError("Erro ao remover prêmio!");
                        }
                    });
                } catch (Exception e) {
                    Platform.runLater(() -> showError("Erro: " + e.getMessage()));
                }
            }).start();
        }
    }
    
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
