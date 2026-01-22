package com.saciar.model;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Modelo de dados para Resgate
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class Resgate {
    private String id;
    @JsonProperty("cliente_id")
    private String clienteId;
    @JsonProperty("cliente_nome")
    private String clienteNome;
    @JsonProperty("telefone")
    @JsonAlias({"cliente_telefone"})
    private String telefone;
    private String premio;
    private Integer pontos;
    @JsonProperty("created_at")
    private String createdAt;
    @JsonProperty("updated_at")
    private String updatedAt;

    public Resgate(String telefone, Integer pontos) {
        this.telefone = telefone;
        this.pontos = pontos;
    }
}
