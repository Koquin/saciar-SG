package com.saciar.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.saciar.model.Premio;
import com.saciar.model.Resgate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Serviço para operações com resgates
 */
public class ResgateService {
    private static final Logger logger = LoggerFactory.getLogger(ResgateService.class);
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public ResgateService() {
        this.httpClient = HttpClient.getInstance();
        this.objectMapper = new ObjectMapper();
    }
    
    /**
     * Busca todos os resgates
     */
    public List<Resgate> getResgates() {
        logger.info("Buscando todos os resgates");
        
        var response = httpClient.get("/redeems/", Object.class);
        
        if (response.isSuccess() && response.getData() != null) {
            try {
                List<Resgate> resgates = objectMapper.convertValue(
                    response.getData(), 
                    new TypeReference<List<Resgate>>() {}
                );
                logger.info("{} resgates encontrados", resgates.size());
                return resgates;
            } catch (Exception e) {
                logger.error("Erro ao converter resgates: {}", e.getMessage());
            }
        }
        
        return Collections.emptyList();
    }
    
    /**
     * Busca resgates por query
     */
    public List<Resgate> searchResgates(String query) {
        logger.info("Buscando resgates com query: {}", query);
        
        if (query == null || query.trim().isEmpty()) {
            return getResgates();
        }
        
        var response = httpClient.get("/redeems/search?q=" + query, Object.class, false);
        
        if (response.isSuccess() && response.getData() != null) {
            try {
                List<Resgate> resgates = objectMapper.convertValue(
                    response.getData(), 
                    new TypeReference<List<Resgate>>() {}
                );
                logger.info("{} resgates encontrados", resgates.size());
                return resgates;
            } catch (Exception e) {
                logger.error("Erro ao converter resgates: {}", e.getMessage());
            }
        }
        
        return Collections.emptyList();
    }
    
    /**
     * Busca todos os prêmios disponíveis
     */
    public List<Premio> getPremios() {
        logger.info("Buscando prêmios disponíveis");
        
        var response = httpClient.get("/prizes", Object.class);
        
        if (response.isSuccess() && response.getData() != null) {
            try {
                List<Premio> premios = objectMapper.convertValue(
                    response.getData(), 
                    new TypeReference<List<Premio>>() {}
                );
                logger.info("{} prêmios encontrados", premios.size());
                return premios;
            } catch (Exception e) {
                logger.error("Erro ao converter prêmios: {}", e.getMessage());
            }
        }
        
        return Collections.emptyList();
    }
    
    /**
     * Registra novo resgate
     */
    public HttpClient.ApiResponse<Resgate> createResgate(Resgate resgate) {
        logger.info("Registrando resgate para: {}", resgate.getTelefone());
        
        Map<String, Object> data = new HashMap<>();
        data.put("telefone", resgate.getTelefone());
        data.put("pontos", resgate.getPontos());
        
        var response = httpClient.post("/redeems/", data, Object.class);
        
        // Se retornou 201, a chamada HTTP deu certo, mas pode não ter sido permitido o resgate
        if (response.getStatusCode() != null && response.getStatusCode() == 201) {
            if (response.getData() != null) {
                try {
                    // A API retorna: {'success': True/False, 'redeem': {...}, 'message': '...'}
                    Map<String, Object> responseData = objectMapper.convertValue(
                        response.getData(), 
                        new TypeReference<Map<String, Object>>() {}
                    );
                    
                    // Extrai o campo success
                    Boolean success = responseData.get("success") != null ? 
                        (Boolean) responseData.get("success") : false;
                    
                    // Extrai mensagem da resposta
                    String message = responseData.get("message") != null ? 
                        responseData.get("message").toString() : null;
                    
                    if (success) {
                        // Resgate permitido - extrai o campo 'redeem'
                        Object redeemData = responseData.get("redeem");
                        if (redeemData != null) {
                            Resgate novoResgate = objectMapper.convertValue(redeemData, Resgate.class);
                            logger.info("Resgate registrado com sucesso: ID {}", novoResgate.getId());
                            return new HttpClient.ApiResponse<>(true, novoResgate, message, response.getStatusCode());
                        } else {
                            logger.error("Campo 'redeem' não encontrado na resposta");
                            return new HttpClient.ApiResponse<>(false, null, message, response.getStatusCode());
                        }
                    } else {
                        // Resgate não permitido (ex: pontos insuficientes)
                        logger.warn("Resgate não permitido: {}", message);
                        return new HttpClient.ApiResponse<>(false, null, message, response.getStatusCode());
                    }
                } catch (Exception e) {
                    logger.error("Erro ao converter resgate: {}", e.getMessage());
                    return new HttpClient.ApiResponse<>(false, null, "Erro ao processar resposta", response.getStatusCode());
                }
            }
        }
        
        // Para outros status codes, erro interno do servidor
        return new HttpClient.ApiResponse<>(false, null, "Erro interno do servidor", response.getStatusCode());
    }
    
    /**
     * Remove resgate
     */
    public HttpClient.ApiResponse<Void> deleteResgate(String resgateId) {
        logger.info("Removendo resgate ID: {}", resgateId);
        
        var response = httpClient.delete("/redeems/" + resgateId);
        
        if (response.isSuccess()) {
            logger.info("Resgate removido com sucesso");
        }
        
        return response;
    }
    
    /**
     * Atualiza lista completa de prêmios (PUT substitui tudo)
     */
    public HttpClient.ApiResponse<Void> updatePremios(List<Premio> premios) {
        logger.info("Atualizando lista de prêmios: {} itens", premios.size());
        
        var response = httpClient.put("/prizes", premios, Object.class);
        
        if (response.isSuccess()) {
            logger.info("Lista de prêmios atualizada com sucesso");
            return new HttpClient.ApiResponse<>(true, null, null, response.getStatusCode());
        }
        
        return new HttpClient.ApiResponse<>(false, null, response.getError(), response.getStatusCode());
    }
}
