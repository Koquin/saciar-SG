package com.saciar.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Modelo de dados para Prêmio
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Premio {
    private String id;
    private Integer pontos;
    private String premio;

    @Override
    public String toString() {
        return String.format("%d pontos - %s", pontos, premio);
    }
}
