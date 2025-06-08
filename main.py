#!/usr/bin/env python3
"""
Hybrid ECC-AES Cloud Workload Encryption Demo
NOVELTY: Demonstrates ECC-based hybrid encryption for cloud workloads
"""

import json
import time
from src.crypto.hybrid_encryption import HybridECCAES
from src.cloud.aws_handler import AWSCloudHandler
from src.benchmarks.performance_tests import PerformanceBenchmark

def demo_basic_encryption():
    """Demonstrate basic hybrid ECC-AES encryption."""
    print("🔐 Hybrid ECC-AES Cloud Workload Encryption Demo")
    print("=" * 50)
    
    # Initialize hybrid system
    hybrid_system = HybridECCAES(ecc_curve="secp256r1", aes_key_size=256)
    
    # Sample cloud workload data
    workload_data = {
        "vm_config": {
            "instance_type": "m5.large",
            "cpu_cores": 2,
            "memory_gb": 8,
            "storage_gb": 100
        },
        "application": {
            "name": "web-server",
            "version": "2.1.0",
            "environment": "production"
        },
        "sensitive_data": {
            "api_keys": ["key1", "key2"],
            "database_credentials": "encrypted_separately"
        }
    }
    
    workload_json = json.dumps(workload_data, indent=2)
    print(f"Original workload data ({len(workload_json)} bytes):")
    print(workload_json[:200] + "..." if len(workload_json) > 200 else workload_json)
    
    # Encrypt workload
    print("\n🔒 Encrypting workload...")
    encrypted_package = hybrid_system.encrypt_workload(
        workload_json,
        cloud_region="us-west-2",
        workload_type="web-application"
    )
    
    print(f"✅ Encryption completed in {encrypted_package['encryption_time']:.3f}s")
    print(f"Encrypted package size: {len(json.dumps(encrypted_package))} bytes")
    
    # Decrypt workload
    print("\n🔓 Decrypting workload...")
    decrypted_result = hybrid_system.decrypt_workload(encrypted_package)
    
    print(f"✅ Decryption completed in {decrypted_result['metadata']['decryption_time']:.3f}s")
    print("Decrypted data matches original:", decrypted_result['data'] == workload_json)
    
    return encrypted_package, decrypted_result

def demo_cloud_integration():
    """Demonstrate cloud storage integration."""
    print("\n☁️  Cloud Integration Demo")
    print("=" * 30)
    
    # Note: This requires AWS credentials and S3 bucket
    # For demo purposes, we'll simulate the process
    
    hybrid_system = HybridECCAES()
    
    # Encrypt a workload
    workload_data = "Sensitive cloud workload data that needs protection"
    encrypted_package = hybrid_system.encrypt_workload(
        workload_data,
        cloud_region="eu-west-1",
        workload_type="data-processing"
    )
    
    print("✅ Workload encrypted and ready for cloud storage")
    print(f"Cloud region: {encrypted_package['cloud_region']}")
    print(f"Workload type: {encrypted_package['workload_type']}")
    
    # Simulate cloud upload (uncomment for real AWS integration)
    # aws_handler = AWSCloudHandler(region_name='eu-west-1')
    # s3_url = aws_handler.upload_encrypted_workload(
    #     bucket_name='your-secure-bucket',
    #     workload_package=encrypted_package,
    #     object_key='workloads/encrypted_workload_001.json'
    # )
    # print(f"📤 Uploaded to: {s3_url}")

def demo_performance_benchmark():
    """Demonstrate performance benchmarking."""
    print("\n📊 Performance Benchmark Demo")
    print("=" * 35)
    
    benchmark = PerformanceBenchmark()
    
    # Benchmark different data sizes
    print("Testing encryption performance across different data sizes...")
    results = benchmark.benchmark_encryption_sizes([1024, 10240, 102400])
    
    # Benchmark different ECC curves
    print("\nTesting different ECC curves...")
    curve_results = benchmark.benchmark_curve_comparison()
    
    # Plot results
    benchmark.plot_performance_results()
    
    return results, curve_results

if __name__ == "__main__":
    # Run demos
    try:
        # Basic encryption demo
        encrypted_package, decrypted_result = demo_basic_encryption()
        
        # Cloud integration demo
        demo_cloud_integration()
        
        # Performance benchmark demo
        results, curve_results = demo_performance_benchmark()
        
        print("\n🎉 All demos completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
