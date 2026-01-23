package com.saciar;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Classe principal da aplicação SACIAR
 */
public class SaciarApplication extends Application {
    private static final Logger logger = LoggerFactory.getLogger(SaciarApplication.class);
    
    @Override
    public void start(Stage primaryStage) {
        try {
            logger.info("Iniciando aplicação SACIAR...");

            // Carrega tela de login
            FXMLLoader loginLoader = new FXMLLoader(getClass().getResource("/fxml/LoginView.fxml"));
            Parent loginRoot = loginLoader.load();
            Scene loginScene = new Scene(loginRoot, 400, 300);
            Stage loginStage = new Stage();
            loginStage.setTitle("Login - SACIAR");
            loginStage.setScene(loginScene);
            loginStage.setResizable(false);
            loginStage.show();

            // Quando login for bem-sucedido, abre MainView
            com.saciar.controller.LoginController loginController = loginLoader.getController();
            loginController.setOnLoginSuccess(() -> {
                Platform.runLater(() -> {
                    try {
                        FXMLLoader loader = new FXMLLoader(getClass().getResource("/fxml/MainView.fxml"));
                        Parent root = loader.load();
                        Scene scene = new Scene(root, 1200, 700);
                        scene.getStylesheets().add(getClass().getResource("/css/styles.css").toExternalForm());
                        primaryStage.setTitle("SACIAR - Sistema de Gerenciamento");
                        primaryStage.setScene(scene);
                        primaryStage.setMinWidth(1000);
                        primaryStage.setMinHeight(600);
                        try {
                            primaryStage.getIcons().add(new Image(getClass().getResourceAsStream("/assets/logoSaciar.jpeg")));
                        } catch (Exception e) {
                            logger.warn("Ícone não encontrado");
                        }
                        primaryStage.show();
                        logger.info("Aplicação iniciada com sucesso!");
                    } catch (Exception e) {
                        logger.error("Erro ao abrir MainView", e);
                        e.printStackTrace();
                    }
                });
            });

        } catch (Exception e) {
            logger.error("Erro ao iniciar aplicação", e);
            e.printStackTrace();
        }
    }
    
    @Override
    public void stop() {
        logger.info("Encerrando aplicação...");
    }
    
    public static void main(String[] args) {
        launch(args);
    }
}
