package com.saciar.controller;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.StackPane;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;

/**
 * Controller principal da aplicação
 * Gerencia navegação entre as views
 */
public class MainController {
    private static final Logger logger = LoggerFactory.getLogger(MainController.class);
    
    @FXML private BorderPane mainPane;
    @FXML private Button btnClientes;
    @FXML private Button btnCompras;
    @FXML private Button btnResgates;
    @FXML private StackPane contentPane;
    
    private Button activeButton;
    
    @FXML
    public void initialize() {
        // Carrega view de clientes por padrão
        loadClientesView();
        activeButton = btnClientes;
        updateButtonStyles();
    }
    
    @FXML
    private void handleClientesClick() {
        loadClientesView();
        activeButton = btnClientes;
        updateButtonStyles();
    }
    
    @FXML
    private void handleComprasClick() {
        loadComprasView();
        activeButton = btnCompras;
        updateButtonStyles();
    }
    
    @FXML
    private void handleResgatesClick() {
        loadResgatesView();
        activeButton = btnResgates;
        updateButtonStyles();
    }
    
    @FXML
    private void handleSairClick() {
        System.exit(0);
    }
    
    private void loadClientesView() {
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/ClienteView.fxml"));
            Parent view = loader.load();
            contentPane.getChildren().setAll(view);
            logger.info("View de clientes carregada");
        } catch (IOException e) {
            logger.error("Erro ao carregar view de clientes", e);
        }
    }
    
    private void loadComprasView() {
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/CompraView.fxml"));
            Parent view = loader.load();
            contentPane.getChildren().setAll(view);
            logger.info("View de compras carregada");
        } catch (IOException e) {
            logger.error("Erro ao carregar view de compras", e);
        }
    }
    
    private void loadResgatesView() {
        try {
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/ResgateView.fxml"));
            Parent view = loader.load();
            contentPane.getChildren().setAll(view);
            logger.info("View de resgates carregada");
        } catch (IOException e) {
            logger.error("Erro ao carregar view de resgates", e);
        }
    }
    
    private void updateButtonStyles() {
        btnClientes.getStyleClass().remove("active-button");
        btnCompras.getStyleClass().remove("active-button");
        btnResgates.getStyleClass().remove("active-button");
        
        if (activeButton != null) {
            activeButton.getStyleClass().add("active-button");
        }
    }
}
