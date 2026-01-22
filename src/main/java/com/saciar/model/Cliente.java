package com.saciar.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Modelo de dados para Cliente
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Cliente {
    private String id;
    private String nome;
    private String telefone;
    private Integer pontos;
    @JsonProperty("qtd_gasta")
    private Double qtdGasta;
    private Double troco;
    @JsonProperty("created_at")
    private String createdAt;
    @JsonProperty("updated_at")
    private String updatedAt;

    public Cliente(String nome, String telefone, Integer pontos, Double qtdGasta, Double troco) {
        this.nome = nome;
        this.telefone = telefone;
        this.pontos = pontos != null ? pontos : 0;
        this.qtdGasta = qtdGasta != null ? qtdGasta : 0.0;
        this.troco = troco != null ? troco : 0.0;
    }

    @Override
    public String toString() {
        return String.format("%s - %s (Pontos: %d)", nome, telefone, pontos);
    }
}
