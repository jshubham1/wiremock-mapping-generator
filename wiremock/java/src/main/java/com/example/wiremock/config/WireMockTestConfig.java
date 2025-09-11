package com.example.wiremock.config;

import com.example.wiremock.config.OpenApiWireMockConfig;
import com.example.wiremock.config.ProductsWireMockConfig;
import com.example.wiremock.config.UsersWireMockConfig;
import com.example.wiremock.MultiApiWireMockServer;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;
import org.springframework.context.annotation.Primary;

/**
 * Main WireMock Test Configuration
 * Auto-generated configuration for all APIs
 * Generated on: 2025-09-11 11:39:36
 * 
 * Use this configuration to import all WireMock servers in your tests:
 * 
 * @SpringBootTest
 * @Import(WireMockTestConfig.class)
 * class IntegrationTest {
 *     @Autowired
 *     private MultiApiWireMockServer multiApiServer;
 * }
 */
@TestConfiguration
@Import({
        OpenApiWireMockConfig.class,
        ProductsWireMockConfig.class,
        UsersWireMockConfig.class,
})
public class WireMockTestConfig {
    
    @Bean
    @Primary
    public MultiApiWireMockServer multiApiWireMockServer() {
        return new MultiApiWireMockServer();
    }
}