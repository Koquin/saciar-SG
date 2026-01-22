package com.saciar.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import okhttp3.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.time.Duration;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

/**
 * Cliente HTTP centralizado com cache e tratamento de erros
 */
public class HttpClient {
    private static final Logger logger = LoggerFactory.getLogger(HttpClient.class);
    private static final String BASE_URL = "http://192.168.0.110:8000";
    private static final int CACHE_DURATION_SECONDS = 30;
    
    private final OkHttpClient client;
    private final ObjectMapper objectMapper;
    private final Map<String, CachedResponse> cache;
    
    private static HttpClient instance;
    
    private HttpClient() {
        this.client = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .readTimeout(10, TimeUnit.SECONDS)
                .writeTimeout(10, TimeUnit.SECONDS)
                .build();
        
        this.objectMapper = new ObjectMapper();
        this.objectMapper.registerModule(new JavaTimeModule());
        this.objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        
        this.cache = new ConcurrentHashMap<>();
    }
    
    public static synchronized HttpClient getInstance() {
        if (instance == null) {
            instance = new HttpClient();
        }
        return instance;
    }
    
    /**
     * Realiza requisição GET
     */
    public <T> ApiResponse<T> get(String endpoint, Class<T> responseType) {
        return get(endpoint, responseType, true);
    }
    
    /**
     * Realiza requisição GET com opção de cache
     */
    public <T> ApiResponse<T> get(String endpoint, Class<T> responseType, boolean useCache) {
        String cacheKey = "GET:" + endpoint;
        
        // Verifica cache
        if (useCache) {
            CachedResponse cached = cache.get(cacheKey);
            if (cached != null && !cached.isExpired()) {
                logger.info("Cache hit: {}", endpoint);
                @SuppressWarnings("unchecked")
                T cachedData = (T) cached.getData();
                return new ApiResponse<>(true, cachedData, null);
            }
        }
        
        try {
            String url = BASE_URL + endpoint;
            Request request = new Request.Builder()
                    .url(url)
                    .get()
                    .build();
            
            logger.info("GET {}", url);
            
            try (Response response = client.newCall(request).execute()) {
                String body = response.body() != null ? response.body().string() : null;
                int statusCode = response.code();
                
                if (response.isSuccessful() && body != null) {
                    T data = objectMapper.readValue(body, responseType);
                    
                    // Armazena no cache
                    if (useCache) {
                        cache.put(cacheKey, new CachedResponse(data));
                    }
                    
                    return new ApiResponse<>(true, data, null, statusCode);
                } else {
                    logger.error("Erro HTTP {}: {}", statusCode, body);
                    return new ApiResponse<>(false, null, "Erro: " + statusCode, statusCode);
                }
            }
        } catch (IOException e) {
            logger.error("Erro na requisição GET {}: {}", endpoint, e.getMessage());
            return new ApiResponse<>(false, null, "Erro de conexão: " + e.getMessage());
        }
    }
    
    /**
     * Realiza requisição POST
     */
    public <T, R> ApiResponse<R> post(String endpoint, T data, Class<R> responseType) {
        try {
            String url = BASE_URL + endpoint;
            String json = objectMapper.writeValueAsString(data);
            
            RequestBody body = RequestBody.create(json, MediaType.get("application/json; charset=utf-8"));
            Request request = new Request.Builder()
                    .url(url)
                    .post(body)
                    .build();
            
            logger.info("POST {}", url);
            
            try (Response response = client.newCall(request).execute()) {
                String responseBody = response.body() != null ? response.body().string() : null;
                int statusCode = response.code();
                
                if (response.isSuccessful()) {
                    invalidateCache(endpoint);
                    
                    if (responseBody != null && !responseBody.isEmpty()) {
                        R responseData = objectMapper.readValue(responseBody, responseType);
                        return new ApiResponse<>(true, responseData, null, statusCode);
                    }
                    return new ApiResponse<>(true, null, null, statusCode);
                } else {
                    logger.error("Erro HTTP {}: {}", statusCode, responseBody);
                    return new ApiResponse<>(false, null, "Erro: " + statusCode, statusCode);
                }
            }
        } catch (IOException e) {
            logger.error("Erro na requisição POST {}: {}", endpoint, e.getMessage());
            return new ApiResponse<>(false, null, "Erro de conexão: " + e.getMessage());
        }
    }
    
    /**
     * Realiza requisição PUT
     */
    public <T, R> ApiResponse<R> put(String endpoint, T data, Class<R> responseType) {
        try {
            String url = BASE_URL + endpoint;
            String json = objectMapper.writeValueAsString(data);
            
            RequestBody body = RequestBody.create(json, MediaType.get("application/json; charset=utf-8"));
            Request request = new Request.Builder()
                    .url(url)
                    .put(body)
                    .build();
            
            logger.info("PUT {}", url);
            
            try (Response response = client.newCall(request).execute()) {
                String responseBody = response.body() != null ? response.body().string() : null;
                int statusCode = response.code();
                
                if (response.isSuccessful()) {
                    invalidateCache(endpoint);
                    
                    if (responseBody != null && !responseBody.isEmpty()) {
                        R responseData = objectMapper.readValue(responseBody, responseType);
                        return new ApiResponse<>(true, responseData, null, statusCode);
                    }
                    return new ApiResponse<>(true, null, null, statusCode);
                } else {
                    logger.error("Erro HTTP {}: {}", statusCode, responseBody);
                    return new ApiResponse<>(false, null, "Erro: " + statusCode, statusCode);
                }
            }
        } catch (IOException e) {
            logger.error("Erro na requisição PUT {}: {}", endpoint, e.getMessage());
            return new ApiResponse<>(false, null, "Erro de conexão: " + e.getMessage());
        }
    }
    
    /**
     * Realiza requisição DELETE
     */
    public ApiResponse<Void> delete(String endpoint) {
        try {
            String url = BASE_URL + endpoint;
            Request request = new Request.Builder()
                    .url(url)
                    .delete()
                    .build();
            
            logger.info("DELETE {}", url);
            
            try (Response response = client.newCall(request).execute()) {
                int statusCode = response.code();
                
                if (response.isSuccessful()) {
                    invalidateCache(endpoint);
                    return new ApiResponse<>(true, null, null, statusCode);
                } else {
                    String body = response.body() != null ? response.body().string() : null;
                    logger.error("Erro HTTP {}: {}", statusCode, body);
                    return new ApiResponse<>(false, null, "Erro: " + statusCode, statusCode);
                }
            }
        } catch (IOException e) {
            logger.error("Erro na requisição DELETE {}: {}", endpoint, e.getMessage());
            return new ApiResponse<>(false, null, "Erro de conexão: " + e.getMessage());
        }
    }
    
    /**
     * Invalida cache relacionado ao endpoint
     */
    private void invalidateCache(String endpoint) {
        String baseEndpoint = endpoint.split("/")[1];
        cache.keySet().removeIf(key -> key.contains(baseEndpoint));
        logger.info("Cache invalidado para: {}", baseEndpoint);
    }
    
    /**
     * Limpa todo o cache
     */
    public void clearCache() {
        cache.clear();
        logger.info("Cache completamente limpo");
    }
    
    /**
     * Classe interna para resposta cacheada
     */
    private static class CachedResponse {
        private final Object data;
        private final long timestamp;
        
        public CachedResponse(Object data) {
            this.data = data;
            this.timestamp = System.currentTimeMillis();
        }
        
        public Object getData() {
            return data;
        }
        
        public boolean isExpired() {
            return (System.currentTimeMillis() - timestamp) > (CACHE_DURATION_SECONDS * 1000L);
        }
    }
    
    /**
     * Classe para resposta da API
     */
    public static class ApiResponse<T> {
        private final boolean success;
        private final T data;
        private final String error;
        private final Integer statusCode;
        
        public ApiResponse(boolean success, T data, String error) {
            this(success, data, error, null);
        }
        
        public ApiResponse(boolean success, T data, String error, Integer statusCode) {
            this.success = success;
            this.data = data;
            this.error = error;
            this.statusCode = statusCode;
        }
        
        public boolean isSuccess() {
            return success;
        }
        
        public T getData() {
            return data;
        }
        
        public String getError() {
            return error;
        }
        
        public Integer getStatusCode() {
            return statusCode;
        }
    }
}
