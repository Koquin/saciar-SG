package com.saciar.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.saciar.model.Cliente;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Serviço para operações com clientes
 */
public class ClienteService {
    private static final Logger logger = LoggerFactory.getLogger(ClienteService.class);
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public ClienteService() {
        this.httpClient = HttpClient.getInstance();
        this.objectMapper = new ObjectMapper();
    }
    
    /**
     * Busca todos os clientes
     */
    public List<Cliente> getClientes() {
        logger.info("Buscando todos os clientes");
        
        var response = httpClient.get("/clientes", Object.class);
        
        if (response.isSuccess() && response.getData() != null) {
            try {
                List<Cliente> clientes = objectMapper.convertValue(
                    response.getData(), 
                    new TypeReference<List<Cliente>>() {}
                );
                logger.info("{} clientes encontrados", clientes.size());
                return clientes;
            } catch (Exception e) {
                logger.error("Erro ao converter clientes: {}", e.getMessage());
            }
        }
        
        return Collections.emptyList();
    }
    
    /**
     * Busca clientes por query
     */
    public List<Cliente> searchClientes(String query) {
        logger.info("Buscando clientes com query: {}", query);
        
        if (query == null || query.trim().isEmpty()) {
            return getClientes();
        }
        
        var response = httpClient.get("/clientes/search?q=" + query, Object.class, false);
        
        if (response.isSuccess() && response.getData() != null) {
            try {
                List<Cliente> clientes = objectMapper.convertValue(
                    response.getData(), 
                    new TypeReference<List<Cliente>>() {}
                );
                logger.info("{} clientes encontrados", clientes.size());
                return clientes;
            } catch (Exception e) {
                logger.error("Erro ao converter clientes: {}", e.getMessage());
            }
        }
        
        return Collections.emptyList();
    }
    
    /**
     * Cadastra novo cliente
     */
    public HttpClient.ApiResponse<Cliente> createCliente(Cliente cliente) {
        logger.info("Cadastrando cliente: {}", cliente.getNome());
        
        Map<String, Object> data = new HashMap<>();
        data.put("nome", cliente.getNome());
        data.put("telefone", cliente.getTelefone());
        data.put("pontos", cliente.getPontos());
        
        var response = httpClient.post("/clientes", data, Object.class);
        
        // Se retornou 201, o cliente foi criado com sucesso
        if (response.getStatusCode() != null && response.getStatusCode() == 201) {
            if (response.getData() != null) {
                try {
                    Cliente novoCliente = objectMapper.convertValue(response.getData(), Cliente.class);
                    logger.info("Cliente cadastrado com sucesso: ID {}", novoCliente.getId());
                    return new HttpClient.ApiResponse<>(true, novoCliente, "Cliente cadastrado com sucesso!", response.getStatusCode());
                } catch (Exception e) {
                    logger.error("Erro ao converter cliente: {}", e.getMessage());
                    return new HttpClient.ApiResponse<>(false, null, "Erro ao processar resposta", response.getStatusCode());
                }
            }
        }
        
        // Qualquer outro status code é erro interno do servidor
        return new HttpClient.ApiResponse<>(false, null, "Erro interno do servidor", response.getStatusCode());
    }
    
    /**
     * Atualiza cliente existente
     */
    public Cliente updateCliente(Cliente cliente) {
        logger.info("Atualizando cliente: {}", cliente.getNome());
        
        if (cliente.getId() == null || cliente.getId().isEmpty()) {
            logger.error("ID é obrigatório para atualizar");
            return null;
        }
        
        Map<String, Object> data = new HashMap<>();
        data.put("nome", cliente.getNome());
        data.put("telefone", cliente.getTelefone());
        data.put("pontos", cliente.getPontos());
        data.put("troco", cliente.getTroco());
        
        var response = httpClient.put("/clientes/" + cliente.getId(), data, Object.class);
        
        if (response.isSuccess()) {
            logger.info("Cliente atualizado com sucesso");
            return cliente;
        }
        
        return null;
    }
    
    /**
     * Remove cliente
     */
    public boolean deleteCliente(String clienteId) {
        logger.info("Removendo cliente ID: {}", clienteId);
        
        var response = httpClient.delete("/clientes/" + clienteId);
        
        if (response.isSuccess()) {
            logger.info("Cliente removido com sucesso");
            return true;
        }
        
        return false;
    }
}
