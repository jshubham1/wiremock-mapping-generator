package com.example.wiremock.test;

import com.example.wiremock.config.ProductsWireMockConfig;
import com.github.tomakehurst.wiremock.WireMockServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;

/**
 * Base test class for Products API integration tests
 * Auto-generated from OpenAPI specification: products-api.yaml
 * Generated on: 2025-09-11 11:39:36
 * 
 * Extend this class in your integration tests:
 * 
 * class ProductsIntegrationTest extends ProductsWireMockTest {
 *     @Test
 *     void shouldCallApi() {
 *         // Your test here using productsApiBaseUrl
 *         String response = restTemplate.getForObject(productsApiBaseUrl + "/endpoint", String.class);
 *         assertThat(response).isNotNull();
 *     }
 * }
 */
@ExtendWith(SpringExtension.class)
@SpringBootTest
@ContextConfiguration(classes = ProductsWireMockConfig.class)
public abstract class ProductsWireMockTest {

    @Autowired
    protected String productsApiBaseUrl;
    
    @Autowired
    protected WireMockServer productsWireMockServer;
    
    @BeforeEach
    void setUp() {
        // Reset to clean state before each test
        if (productsWireMockServer.isRunning()) {
            productsWireMockServer.resetAll();
        }
    }
    
    @AfterEach
    void tearDown() {
        // Clean up after each test
        if (productsWireMockServer.isRunning()) {
            productsWireMockServer.resetAll();
        }
    }
    
    protected String getApiBaseUrl() {
        return productsApiBaseUrl;
    }
    
    protected WireMockServer getWireMockServer() {
        return productsWireMockServer;
    }
}