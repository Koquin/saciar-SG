package com.saciar.controller;

import com.saciar.model.Compra;
import com.saciar.service.CompraService;
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
 * Controller para a view de Compras
 */
public class CompraController {
    private static final Logger logger = LoggerFactory.getLogger(CompraController.class);
    
    @FXML private TextField searchField;
    @FXML private TableView<Compra> compraTable;
    @FXML private TableColumn<Compra, String> clienteColumn;
    @FXML private TableColumn<Compra, String> telefoneColumn;
    @FXML private TableColumn<Compra, Double> valorColumn;
    @FXML private TableColumn<Compra, Integer> pontosColumn;
    @FXML private TableColumn<Compra, String> dataColumn;
    @FXML private Button btnRegistrar;
    @FXML private Button btnRemover;
    @FXML private Button btnExportar;
    
    private final CompraService compraService;
    private final ObservableList<Compra> compraList;
    
    public CompraController() {
        this.compraService = new CompraService();
        this.compraList = FXCollections.observableArrayList();
    }
    
    @FXML
    public void initialize() {
        // Configura colunas da tabela
        clienteColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getCliente() != null ? 
                cellData.getValue().getCliente() : "Não identificado"));
        telefoneColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getTelefone() != null ? 
                cellData.getValue().getTelefone() : "Sem telefone"));
        valorColumn.setCellValueFactory(cellData -> 
            new SimpleDoubleProperty(cellData.getValue().getValor() != null ? 
                cellData.getValue().getValor() : 0.0).asObject());
        pontosColumn.setCellValueFactory(cellData -> 
            new SimpleIntegerProperty(cellData.getValue().getPontosGanhos() != null ? 
                cellData.getValue().getPontosGanhos() : 0).asObject());
        dataColumn.setCellValueFactory(cellData -> 
            new SimpleStringProperty(cellData.getValue().getData() != null ? 
                cellData.getValue().getData() : "Sem data"));
        
        compraTable.setItems(compraList);
        
        // Carrega dados iniciais
        loadCompras();
        
        // Configura busca
        searchField.setOnAction(e -> handleSearch());
    }
    
    /**
     * Carrega todas as compras
     */
    private void loadCompras() {
        new Thread(() -> {
            try {
                List<Compra> compras = compraService.getCompras();
                Platform.runLater(() -> {
                    compraList.clear();
                    compraList.addAll(compras);
                });
            } catch (Exception e) {
                logger.error("Erro ao carregar compras", e);
                showError("Erro ao carregar compras: " + e.getMessage());
            }
        }).start();
    }
    
    /**
     * Busca compras
     */
    @FXML
    private void handleSearch() {
        String query = searchField.getText().trim();
        
        new Thread(() -> {
            try {
                List<Compra> compras = compraService.searchCompras(query);
                Platform.runLater(() -> {
                    compraList.clear();
                    compraList.addAll(compras);
                });
            } catch (Exception e) {
                logger.error("Erro ao buscar compras", e);
                showError("Erro ao buscar compras: " + e.getMessage());
            }
        }).start();
    }
    
    /**
     * Limpa filtro
     */
    @FXML
    private void handleClearFilter() {
        searchField.clear();
        loadCompras();
    }
    
    /**
     * Registrar nova compra
     */
    @FXML
    private void handleRegistrar() {
        CompraDialog dialog = new CompraDialog();
        Optional<Compra> result = dialog.showAndWait();
        
        result.ifPresent(compra -> {
            new Thread(() -> {
                try {
                    var response = compraService.createCompra(compra);
                    Platform.runLater(() -> {
                        if (response.isSuccess() && response.getData() != null) {
                            if (response.getStatusCode() != null && response.getStatusCode() == 201) {
                                showInfo("Compra registrada com sucesso!");
                            } else {
                                showInfo("Operação realizada com sucesso!");
                            }
                            loadCompras();
                        } else {
                            if (response.getStatusCode() != null && response.getStatusCode() == 404) {
                                showError("Cliente não encontrado!");
                            } else if (response.getStatusCode() != null && response.getStatusCode() == 400) {
                                showError("Dados inválidos. Verifique os campos!");
                            } else {
                                showError("Erro ao registrar compra: " + response.getError());
                            }
                        }
                    });
                } catch (Exception e) {
                    logger.error("Erro ao registrar compra", e);
                    Platform.runLater(() -> showError("Erro ao registrar compra: " + e.getMessage()));
                }
            }).start();
        });
    }
    
    /**
     * Remover compra selecionada
     */
    @FXML
    private void handleRemover() {
        Compra selected = compraTable.getSelectionModel().getSelectedItem();
        
        if (selected == null) {
            showWarning("Selecione uma compra para remover!");
            return;
        }
        
        Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
        alert.setTitle("Confirmar Remoção");
        alert.setHeaderText("Remover compra?");
        alert.setContentText("Deseja remover esta compra?");
        
        Optional<ButtonType> result = alert.showAndWait();
        
        if (result.isPresent() && result.get() == ButtonType.OK) {
            new Thread(() -> {
                try {
                    var response = compraService.deleteCompra(selected.getId());
                    Platform.runLater(() -> {
                        if (response.isSuccess()) {
                            showInfo("Compra removida com sucesso!");
                            loadCompras();
                        } else {
                            showError("Erro ao remover compra!");
                        }
                    });
                } catch (Exception e) {
                    logger.error("Erro ao remover compra", e);
                    Platform.runLater(() -> showError("Erro ao remover compra: " + e.getMessage()));
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
        fileChooser.setTitle("Salvar Lista de Compras");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("CSV Files", "*.csv"));
        
        File file = fileChooser.showSaveDialog(compraTable.getScene().getWindow());
        
        if (file != null) {
            try (FileWriter writer = new FileWriter(file)) {
                writer.write("Cliente;Telefone;Valor;Pontos;Data\n");
                
                for (Compra compra : compraList) {
                    writer.write(String.format("%s;%s;%.2f;%d;%s\n",
                        compra.getCliente() != null ? compra.getCliente() : "N/A",
                        compra.getTelefone(),
                        compra.getValor(),
                        compra.getPontosGanhos() != null ? compra.getPontosGanhos() : 0,
                        compra.getData() != null ? compra.getData() : "N/A"));
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
 * Dialog para registro de compra
 */
class CompraDialog extends Dialog<Compra> {
    private final TextField telefoneField = new TextField();
    private final TextField valorField = new TextField();
    private final CheckBox deliveryCheck = new CheckBox();
    
    public CompraDialog() {
        setTitle("Registrar Compra");
        setHeaderText(null);
        
        // Layout
        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.setPadding(new Insets(20));
        
        telefoneField.setPromptText("Telefone do cliente");
        valorField.setPromptText("0.00");
        deliveryCheck.setSelected(false);
        
        grid.add(new Label("Telefone:"), 0, 0);
        grid.add(telefoneField, 1, 0);
        grid.add(new Label("Valor:"), 0, 1);
        grid.add(valorField, 1, 1);
        grid.add(new Label("Delivery:"), 0, 2);
        grid.add(deliveryCheck, 1, 2);
        
        getDialogPane().setContent(grid);
        
        // Botões
        ButtonType saveButton = new ButtonType("Registrar", ButtonBar.ButtonData.OK_DONE);
        getDialogPane().getButtonTypes().addAll(saveButton, ButtonType.CANCEL);
        
        // Converte resultado
        setResultConverter(dialogButton -> {
            if (dialogButton == saveButton) {
                try {
                    Compra c = new Compra();
                    c.setTelefone(telefoneField.getText());
                    c.setValor(Double.parseDouble(valorField.getText()));
                    c.setIsDelivery(deliveryCheck.isSelected());
                    return c;
                } catch (NumberFormatException e) {
                    return null;
                }
            }
            return null;
        });
    }
}
