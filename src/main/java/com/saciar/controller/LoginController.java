package com.saciar.controller;

import com.saciar.service.HttpClient;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

import java.util.HashMap;
import java.util.Map;

public class LoginController {
    @FXML private TextField usernameField;
    @FXML private PasswordField passwordField;
    @FXML private Button btnLogin;

    private Runnable onLoginSuccess;

    public void setOnLoginSuccess(Runnable callback) {
        this.onLoginSuccess = callback;
    }

    @FXML
    private void handleLogin() {
        String username = usernameField.getText();
        String password = passwordField.getText();
        if (username == null || username.isEmpty() || password == null || password.isEmpty()) {
            showError("Preencha usuário e senha.");
            return;
        }
        btnLogin.setDisable(true);
        new Thread(() -> {
            try {
                Map<String, Object> data = new HashMap<>();
                data.put("username", username);
                data.put("password", password);
                var response = HttpClient.getInstance().post("/auth/login", data, Object.class);
                Platform.runLater(() -> {
                    btnLogin.setDisable(false);
                    if (response.isSuccess() && Boolean.TRUE.equals(response.getData())) {
                        if (onLoginSuccess != null) onLoginSuccess.run();
                        Stage stage = (Stage) btnLogin.getScene().getWindow();
                        stage.close();
                    } else {
                        String msg = "Erro ao fazer login.";
                        if (response.getStatusCode() != null) {
                            if (response.getStatusCode() == 404) {
                                msg = "Usuário não encontrado.";
                            } else if (response.getStatusCode() == 401) {
                                msg = "Credenciais inválidas.";
                            } else if (response.getError() != null) {
                                msg = response.getError();
                            }
                        }
                        showError(msg);
                    }
                });
            } catch (Exception e) {
                Platform.runLater(() -> {
                    btnLogin.setDisable(false);
                    showError("Erro: " + e.getMessage());
                });
            }
        }).start();
    }

    private void showError(String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle("Login");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
}
