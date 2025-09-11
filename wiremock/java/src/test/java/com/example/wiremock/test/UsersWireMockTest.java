package com.example.wiremock.test;

import com.example.wiremock.config.UsersWireMockConfig;
import com.github.tomakehurst.wiremock.WireMockServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit.jupiter.SpringExtension;

/**
 * Base test class for Users API integration tests
 * Auto-generated from OpenAPI specification: users-api.yaml
 * Generated on: 2025-09-11 11:39:36
 * 
 * Extend this class in your integration tests:
 * 
 * class UsersIntegrationTest extends UsersWireMockTest {
 *     @Test
 *     void shouldCallApi() {
 *         // Your test here using usersApiBaseUrl
 *         String response = restTemplate.getForObject(usersApiBaseUrl + "/endpoint", String.class);
 *         assertThat(response).isNotNull();
 *     }
 * }
 */
@ExtendWith(SpringExtension.class)
@SpringBootTest
@ContextConfiguration(classes = UsersWireMockConfig.class)
public abstract class UsersWireMockTest {

    @Autowired
    protected String usersApiBaseUrl;
    
    @Autowired
    protected WireMockServer usersWireMockServer;
    
    @BeforeEach
    void setUp() {
        // Reset to clean state before each test
        if (usersWireMockServer.isRunning()) {
            usersWireMockServer.resetAll();
        }
    }
    
    @AfterEach
    void tearDown() {
        // Clean up after each test
        if (usersWireMockServer.isRunning()) {
            usersWireMockServer.resetAll();
        }
    }
    
    protected String getApiBaseUrl() {
        return usersApiBaseUrl;
    }
    
    protected WireMockServer getWireMockServer() {
        return usersWireMockServer;
    }
}