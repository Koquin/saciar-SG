package com.saciar.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.saciar.model.Compra;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Serviço para operações com compras
 */
public class CompraService {
    private static final Logger logger = LoggerFactory.getLogger(CompraService.class);
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public CompraService() {
        this.httpClient = HttpClient.getInstance();
        this.objectMapper = new ObjectMapper();
    }
    
    /**
     * Busca todas as compras
     */
    public List<Compra> getCompras() {
        logger.info("Buscando todas as compras");
        
        var response = httpClient.get("/purchase/", Object.class);
        
        if (response.isSuccess() && response.getData() != null) {
            try {
                List<Compra> compras = objectMapper.convertValue(
                    response.getData(), 
                    new TypeReference<List<Compra>>() {}
                );
                logger.info("{} compras encontradas", compras.size());
                return compras;
            } catch (Exception e) {
                logger.error("Erro ao converter compras: {}", e.getMessage());
            }
        }
        
        return Collections.emptyList();
    }
    
    /**
     * Busca compras por query
     */
    public List<Compra> searchCompras(String query) {
        logger.info("Buscando compras com query: {}", query);
        
        if (query == null || query.trim().isEmpty()) {
            return getCompras();
        }
        
        var response = httpClient.get("/purchase/search?q=" + query, Object.class, false);
        
        if (response.isSuccess() && response.getData() != null) {
            try {
                List<Compra> compras = objectMapper.convertValue(
                    response.getData(), 
                    new TypeReference<List<Compra>>() {}
                );
                logger.info("{} compras encontradas", compras.size());
                return compras;
            } catch (Exception e) {
                logger.error("Erro ao converter compras: {}", e.getMessage());
            }
        }
        
        return Collections.emptyList();
    }
    
    /**
     * Registra nova compra
     */
    public HttpClient.ApiResponse<Compra> createCompra(Compra compra) {
        logger.info("Criando compra de R$ {}", compra.getValor());
        
        Map<String, Object> data = new HashMap<>();
        data.put("telefone", compra.getTelefone() != null ? compra.getTelefone() : "AVULSO");
        data.put("valor", compra.getValor());
        data.put("is_delivery", compra.getIsDelivery());
        data.put("isFromClient", false);
        
        var response = httpClient.post("/purchase", data, Object.class);
        
        // Se retornou 201, a compra foi criada com sucesso
        if (response.getStatusCode() != null && response.getStatusCode() == 201) {
            if (response.getData() != null) {
                try {
                    Compra novaCompra = objectMapper.convertValue(response.getData(), Compra.class);
                    logger.info("Compra criada com sucesso");
                    return new HttpClient.ApiResponse<>(true, novaCompra, "Compra registrada com sucesso!", response.getStatusCode());
                } catch (Exception e) {
                    logger.error("Erro ao converter compra: {}", e.getMessage());
                    return new HttpClient.ApiResponse<>(false, null, "Erro ao processar resposta", response.getStatusCode());
                }
            }
        }
        
        // Qualquer outro status code é erro interno do servidor
        return new HttpClient.ApiResponse<>(false, null, "Erro interno do servidor", response.getStatusCode());
    }
    
    /**
     * Remove compra
     */
    public HttpClient.ApiResponse<Void> deleteCompra(String compraId) {
        logger.info("Removendo compra ID: {}", compraId);
        
        var response = httpClient.delete("/purchase/" + compraId);
        
        if (response.isSuccess()) {
            logger.info("Compra removida com sucesso");
        }
        
        return response;
    }
}
