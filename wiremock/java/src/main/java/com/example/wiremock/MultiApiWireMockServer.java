package com.example.wiremock;

import com.github.tomakehurst.wiremock.WireMockServer;
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;
import org.springframework.stereotype.Component;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Multi-API WireMock Server Manager
 * Auto-generated from OpenAPI specifications on 2025-09-11 11:39:36
 * 
 * Manages WireMock servers for: open_api, products, users
 * 
 * Usage:
 * 1. Include in your Spring Boot test context
 * 2. Access individual servers via getServer(apiName)
 * 3. Get base URLs via getServerUrls()
 */
@Component
public class MultiApiWireMockServer {
    
    private final Map<String, WireMockServer> servers = new HashMap<>();
    private static final int BASE_PORT = 8080;
    private static final AtomicInteger portCounter = new AtomicInteger(BASE_PORT);
    
    @PostConstruct
    public void startAllServers() {
        System.out.println("🚀 Starting WireMock servers for all APIs...");
        
        // Start OpenApi WireMock Server
        try {
            int open_apiPort = BASE_PORT + 0;
            WireMockServer open_apiServer = new WireMockServer(
                WireMockConfiguration.options()
                    .port(open_apiPort)
                    .usingFilesUnderClasspath("wiremock/open_api")
                    .verbose(true)
            );
            open_apiServer.start();
            servers.put("open_api", open_apiServer);
            System.out.println("✓ OpenApi API server started on port " + open_apiPort);
        } catch (Exception e) {
            System.err.println("❌ Failed to start OpenApi server: " + e.getMessage());
            throw new RuntimeException("Failed to start OpenApi WireMock server", e);
        }
        
        // Start Products WireMock Server
        try {
            int productsPort = BASE_PORT + 1;
            WireMockServer productsServer = new WireMockServer(
                WireMockConfiguration.options()
                    .port(productsPort)
                    .usingFilesUnderClasspath("wiremock/products")
                    .verbose(true)
            );
            productsServer.start();
            servers.put("products", productsServer);
            System.out.println("✓ Products API server started on port " + productsPort);
        } catch (Exception e) {
            System.err.println("❌ Failed to start Products server: " + e.getMessage());
            throw new RuntimeException("Failed to start Products WireMock server", e);
        }
        
        // Start Users WireMock Server
        try {
            int usersPort = BASE_PORT + 2;
            WireMockServer usersServer = new WireMockServer(
                WireMockConfiguration.options()
                    .port(usersPort)
                    .usingFilesUnderClasspath("wiremock/users")
                    .verbose(true)
            );
            usersServer.start();
            servers.put("users", usersServer);
            System.out.println("✓ Users API server started on port " + usersPort);
        } catch (Exception e) {
            System.err.println("❌ Failed to start Users server: " + e.getMessage());
            throw new RuntimeException("Failed to start Users WireMock server", e);
        }
        

        
        System.out.println("✅ All WireMock servers started successfully");
        getServerUrls().forEach((api, url) -> 
            System.out.println("  - " + api + ": " + url));
    }
    
    @PreDestroy
    public void stopAllServers() {
        System.out.println("🛑 Stopping all WireMock servers...");
        servers.values().forEach(server -> {
            if (server.isRunning()) {
                server.stop();
            }
        });
        servers.clear();
    }
    
    public WireMockServer getServer(String apiName) {
        return servers.get(apiName);
    }
    
    public Map<String, String> getServerUrls() {
        Map<String, String> urls = new HashMap<>();
        urls.put("open_api", "http://localhost:" + (BASE_PORT + 0));
        urls.put("products", "http://localhost:" + (BASE_PORT + 1));
        urls.put("users", "http://localhost:" + (BASE_PORT + 2));

        return urls;
    }
    
    public boolean isRunning(String apiName) {
        WireMockServer server = servers.get(apiName);
        return server != null && server.isRunning();
    }
    
    public void resetAll() {
        servers.values().forEach(WireMockServer::resetAll);
    }
}