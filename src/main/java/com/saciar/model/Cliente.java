package com.saciar.model;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
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
@JsonIgnoreProperties(ignoreUnknown = true)
public class Cliente {
    @JsonAlias({"_id", "id"})
    @JsonProperty("_id")
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
        return String.format("id: %s, nome: %s, telefone: %s, pontos: %d, qtdGasta: %.2f, troco: %.2f", 
            id, nome, telefone, pontos, qtdGasta, troco);
    }
}
