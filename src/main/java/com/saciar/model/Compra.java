package com.saciar.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Modelo de dados para Compra
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Compra {
    private String id;
    private String cliente;
    private String telefone;
    private Double valor;
    private boolean created;
    @JsonProperty("is_delivery")
    private Boolean isDelivery;
    @JsonProperty("pontos_ganhos")
    private Integer pontosGanhos;
    private String data;
    @JsonProperty("created_at")
    private String createdAt;

    public Compra(String telefone, Double valor, Boolean isDelivery) {
        this.telefone = telefone;
        this.valor = valor;
        this.isDelivery = isDelivery != null ? isDelivery : false;
    }
}
