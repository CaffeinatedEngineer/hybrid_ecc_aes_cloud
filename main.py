#!/usr/bin/env python3
"""
Hybrid ECC-AES Cloud Workload Encryption Demo
NOVELTY: Demonstrates ECC-based hybrid encryption for cloud workloads
"""

import json
import time
import os
import sys

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from crypto.hybrid_encryption import HybridECCAES
from cloud.aws_handler import AWSCloudHandler
from benchmarks.performance_tests import PerformanceBenchmark

def demo_basic_encryption():
    """Demonstrate basic hybrid ECC-AES encryption."""
    print("🔐 Hybrid ECC-AES Cloud Workload Encryption Demo")
    print("=" * 50)
    
    # Initialize hybrid system (no keys needed - auto-generated)
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
    """Demonstrate cloud storage integration (simulation mode)."""
    print("\n☁️  Cloud Integration Demo (Simulation Mode)")
    print("=" * 45)
    
    # Use simulation mode (no AWS credentials needed)
    hybrid_system = HybridECCAES()
    aws_handler = AWSCloudHandler(region_name='eu-west-1', use_simulation=True)
    
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
    
    # Simulate cloud upload
    s3_url = aws_handler.upload_encrypted_workload(
        bucket_name='your-secure-bucket',
        workload_package=encrypted_package,
        object_key='workloads/encrypted_workload_001.json'
    )
    print(f"📤 Simulated upload to: {s3_url}")
    
    # Simulate download
    downloaded_package = aws_handler.download_encrypted_workload(
        bucket_name='your-secure-bucket',
        object_key='workloads/encrypted_workload_001.json'
    )
    print("📥 Simulated download completed")

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
    
    # Plot results (will save as image file)
    try:
        benchmark.plot_performance_results()
        print("📈 Performance charts saved as 'hybrid_ecc_aes_performance.png'")
    except Exception as e:
        print(f"⚠️  Could not generate plots: {e}")
    
    return results, curve_results

if __name__ == "__main__":
    # Run demos
    try:
        print("🚀 Starting Hybrid ECC-AES Cloud Encryption Demos...\n")
        
        # Basic encryption demo
        encrypted_package, decrypted_result = demo_basic_encryption()
        
        # Cloud integration demo (simulation)
        demo_cloud_integration()
        
        # Performance benchmark demo
        results, curve_results = demo_performance_benchmark()
        
        print("\n🎉 All demos completed successfully!")
        print("\n📋 Summary:")
        print(f"   - Encryption/Decryption: ✅ Working")
        print(f"   - Cloud Integration: ✅ Simulated")
        print(f"   - Performance Benchmarks: ✅ Completed")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()