package com.example.wiremock.test;

import com.example.wiremock.config.WireMockTestConfig;
import com.example.wiremock.MultiApiWireMockServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;

/**
 * Base Integration Test Class
 * Auto-generated test base for all APIs
 * Generated on: 2025-09-11 11:39:36
 * 
 * Extend this class for comprehensive integration tests:
 * 
 * class MyIntegrationTest extends BaseWireMockIntegrationTest {
 *     @Test
 *     void shouldTestMultipleApis() {
 *         // Test interactions between multiple APIs
 *         // All APIs are available via getXxxBaseUrl() methods
 *     }
 * }
 */
@ExtendWith(SpringExtension.class)
@SpringBootTest
@ContextConfiguration(classes = WireMockTestConfig.class)
public abstract class BaseWireMockIntegrationTest {

    @Autowired
    protected MultiApiWireMockServer multiApiServer;
    
    @Autowired
    protected String open_apiApiBaseUrl;
    
    @Autowired
    protected String productsApiBaseUrl;
    
    @Autowired
    protected String usersApiBaseUrl;
    
    @BeforeEach
    void setUpAll() {
        // Ensure all servers are running
        if (multiApiServer != null) {
            // Reset all servers to clean state
            multiApiServer.resetAll();
        }
    }
    
    @AfterEach 
    void tearDownAll() {
        // Clean up after each test
        if (multiApiServer != null) {
            multiApiServer.resetAll();
        }
    }
    
    protected MultiApiWireMockServer getMultiApiServer() {
        return multiApiServer;
    }
    
    protected String getOpenApiBaseUrl() {
        return open_apiApiBaseUrl;
    }
    
    protected String getProductsBaseUrl() {
        return productsApiBaseUrl;
    }
    
    protected String getUsersBaseUrl() {
        return usersApiBaseUrl;
    }
}